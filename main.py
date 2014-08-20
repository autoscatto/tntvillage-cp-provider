from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import simplifyString, tryUrlencode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentMagnetProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
import datetime
import traceback
import re
import requests
import time
log = CPLog(__name__)


class TNTVillage(TorrentMagnetProvider, MovieProvider):

    sess = None
    last_login_check = None
    payload = None


    urls = {
        'test': 'http://forum.tntvillage.scambioetico.org/index.php',
        # TODO: understand how the fuck the super does login
        #'login': 'http://forum.tntvillage.scambioetico.org/index.php',  
        'base_url': 'http://forum.tntvillage.scambioetico.org/index.php',
    }

    http_time_between_calls = 1  # seconds
    cat_backup_id = None

    # TODO: THA UGLIEST, discover a way to find the release year in tnt details page
    def standardize_title(self, name, title, year, quality):
        s_y = re.findall(r'(\d{4})', name)
        s_yo = "%d" % year
        if s_yo in s_y:  # if I find the year, I assume that it is indeed the right one, and return the standard title
            ret = "%s (%d) - %s" % (title, year, quality)
            log.info("THA UGLIEST %s -> %s" % (name, ret))
            return ret

        return name



    ### TODO: what about movie year and quality? ###
    def _searchOnTitle(self, title, movie, quality, results):
        #print "//"*40
        #print movie['library']
        #print "//"*40
        self.login()
        log.debug("Searching for %s (imdb: %s) (%s) on %s" % (title,
                                                              movie['library']['identifier'].replace('tt', ''),
                                                              quality['label'],
                                                              self.urls['base_url']))

        # Get italian title
        # First, check cache
        cache_key = 'italiantitle.%s' % movie['library']['identifier']
        italiantitle = self.getCache(cache_key)

        if not italiantitle:
            try:
                dataimdb = self.getHTMLData(
                    'http://www.imdb.com/title/%s/releaseinfo' % (movie['library']['identifier']))
                html = BeautifulSoup(dataimdb)
                try:
                    italiantitle = html.find('table', id='akas').find('td', text="Italy").findNext().text
                except:
                    log.debug(
                        'Failed to find italian title for %s, it has probably never been released in Italy, '
                        'we\'ll try searching for the original title anyways',
                        title)
                    italiantitle = title
            except:
                log.error('Failed parsing iMDB for italian title, using the original one: %s', traceback.format_exc())
                italiantitle = title

            self.setCache(cache_key, italiantitle, timeout=25920000)

        log.debug("Title after searching for the italian one: %s" % italiantitle)

        # remove accents
        simpletitle = simplifyString(italiantitle)
        payload = {'act': 'allreleases', 'st': '0', 'cat': '4', 'filter': simpletitle}
        data = self.sess.get('http://forum.tntvillage.scambioetico.org/index.php', params=payload)
        soup = BeautifulSoup(data.content)
        row = soup.findAll('tr', attrs={'class': 'row4'})

        if row and len(row) == 0:
            log.info("No torrents found for %s on tntvillage.scambioetico.org", italiantitle)
            return

        if row:
                try:
                    self.parseResults(results, row, movie['library']['year'] , quality['label'], title)
                except:
                    log.error('Failed parsing TNTVillage: %s', traceback.format_exc())

        else:
                log.debug('No search results found.')

    # computes days since the torrent release
    def ageToDays(self, age_str):
        # actually a datetime.timedelta object
        tdelta = datetime.datetime.now() - datetime.datetime.strptime(age_str, " %b %d %Y")
        # to int
        return tdelta.days

    # retrieves the magnet link from the detail page of the original torrent result
    def getMagnetLink(self, url):
        data = self.sess.get(url)
        html = BeautifulSoup(data.content)
        magnet = html.find('a', href=re.compile(r'magnet:*'))['href']
        titolo = html.findAll('td', id='sottotitolo')[1].text.strip('&nbsp;')
        datas = html.findAll('span', attrs={"class": "postdetails"})[0].text
        datas = re.findall(r':(.*?),', datas)[0]
        data = self.ageToDays(datas)
        return data, magnet
        
                        
    # filters the <td> elements containing the results, if any
    def parseResults(self, results, entries, year, quality, title):
        print "//"*40
        print year
        new = {}
        for result in entries:
            tds = result.findAll('td')
            if len(tds) != 9:
                log.info("Wrong search result format, skipping.")
                continue
            try:
                new['detail_url'] = tds[0].a['href']
                new['size'] = self.parseSize("%s GB" % tds[7].span.text)
                new['id'] = tds[0].a['href'].split('showtopic=')[1]
                new['age'], new['url'] = self.getMagnetLink(new['detail_url'])
                new['name'] = self.standardize_title(tds[0].a.text, title, year, quality)
                new['seeders'] = tryInt(tds[5].span.text)
                new['leechers'] = tryInt(tds[4].span.text)
                new['score'] = self.conf('extra_score') + 0

            except Exception, e:
                log.info("Search entry processing FAILED!")
                print e
                continue

            results.append(new)
            log.debug("New result %s", new)

    def login(self):
        if not self.sess:
            self.sess = requests.Session()
        # Check if we are still logged in every hour/2
        now = time.time()
        if not self.last_login_check or not self.last_login_check < (now - 1800):
            try:
                login_param = {'act': 'Login', 'CODE': '01'}
                auth = {'UserName': self.conf('username'), 'PassWord': self.conf('password')}
                resp = self.sess.post(self.urls.get('test'),
                                      params=login_param,
                                      data=auth)
                if self.loginCheckSuccess(resp.content):
                    self.last_login_check = now
                    return True
            except:
                pass
            self.last_login_check = None

        if self.last_login_check:
            return True

        try:
            output = self.sess.get(self.urls.get('test'), params={'act': 'allreleases'})

            if self.loginSuccess(output.content):
                self.last_login_check = now
                return True
            error = 'unknown'
        except:
            error = traceback.format_exc()

        self.last_login_check = None
        log.error('Failed to login %s: %s', (self.getName(), error))
        return False

    def loginSuccess(self, output):
        return "Spiacente" in output

    def loginCheckSuccess(self, output):
        return "Attendi mentre viene caricata la pagina..." in output
