from .main import TNTVillage


def autoload():
    return TNTVillage()

config = [{
    'name': 'tntvillage',
    'groups': [
        {
            'tab': 'searcher',
            'list': 'torrent_providers',
            'name': 'TNT Village',
            'description': 'See <a href="http://www.tntvillage.scambioetico.org/">TNT Village</a>',
            'icon':'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gYbCDIHkb9iqwAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAJ7SURBVDjLfZLNS1RRGMZ/596Zq16/wmyslDFJLSExP3ZaobWpTQlmLqQPaBFECf4FbcKgXZTQIjRSiDLRFhLKGAhRotiANUYlpcJoUw2NM+Pc63jvaeNoDuaBszjvw/u8z/nxCiADUNn+rAEO0p0CG4jF7YrDJXpo0W8rIHRFjYqrdwsnVKeoSe6Mr5lcP/uIle43fOzqQsvMpP5hJ99eDPClvx+AJWvtuWLbrEgbkm/+7jKqik+TX1uLkq5zxefjwIkGMtxuLCmxgYhla4oQCCFAiM3pEpuGyksAKA4HMf8iP7xeALLcboRtIwABtuPnvLlgWTKgpagOV6GWA7DweTl4rK0lByBoGGawoCCaV1WVg5RkHyzmQyT8S9N1FuLxP46X95euAVkNrXvqXQe0J4oiqNzfOqUq2imAQGrqVOPAwARw0z8+zrvOTh5EovVEostAzAGEgfC+opSglGCuGjSfv3A88Z3I8vL3IyUlzQC+nh7mhocBFoHfAMo/4AWAru2i4lCdlijqul6qqupegK+DgwhVBTASupLUT115CwBerzcKUF1dXQ4wNzKCZZqbnJMNnM5UaaxGOFl5GYCxsbFpAJfLpQFM9PZaqqb93+DWxRFZU3qG3Gw3s7Oz5OXlvU5otpQM9/f7tlvVDYNgxC9unHsMgMfjedvU1BRMaB6Px1/kdE7taGDb1kasvledT8PhcG7iPTo62peVlmYmA98KcX0VLWkSis+HpJQhAMMwuNPR0R2X0rljglg0FvN9mmZmxmfebntWNzk5OQowNDQ0B7wPSTsasCwjYK1tgUhSrCqgAigDaG9vv6coSuO6ng0cBSpzVXVj8F8TPQGTxruMMQAAAABJRU5ErkJggg==',
            'wizard': True,
            'options': [
                {
                    'name': 'enabled',
                    'type': 'enabler',
                    'default': False,
                },
                {
                    'name': 'username',
                    'default': '',
                    'description': 'Enter your site username.',
                },
                {
                    'name': 'password',
                    'default': '',
                    'type': 'password',
                    'description': 'Enter your site password',
                },
                {
                    'name': 'seed_ratio',
                    'label': 'Seed ratio',
                    'type': 'float',
                    'default': 1,
                    'description': 'Will not be (re)moved until this seed ratio is met.',
                },
                {
                    'name': 'seed_time',
                    'label': 'Seed time',
                    'type': 'int',
                    'default': 40,
                    'description': 'Will not be (re)moved until this seed time (in hours) is met.',
                },
                {
                    'name': 'extra_score',
                    'advanced': True,
                    'label': 'Extra Score',
                    'type': 'int',
                    'default': 0,
                    'description': 'Starting score for each release found via this provider.',
                }
            ],
        },
    ],
}]
