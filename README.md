tntvillage-cp-provider ![logo](http://forum.tntvillage.scambioetico.org/style_images/mkportal-636/loghino.gif)
======================

TNTVillage ([italian ethical sharing forum](http://www.tntvillage.scambioetico.org/index.php) ) CouchPotato torrent provider.

####SETUP INSTRUCTIONS

```
cd $CouchPotatoServerdir/custom_plugins  # you can find $CouchPotatoServerdir path in settings -> about
git clone https://github.com/autoscatto/tntvillage-cp-provider.git tntvillage

# Now you should see **TNT Village** as one of the prodivers for Torrents. (Settings -> Searcher)
# set your username/password in tntvillage module preference (same view Settings -> Searcher)
# set *ita, italian (or similar) as preferred keywords (Settings -> Categories, Preferred field)
# to get higher score for italian movie.
# *OPTIONAL:* set additional score for tntvillage results in module preference
```

####SHOUT OUT

Thanks to RuudBurger (https://github.com/RuudBurger) for developing CouchPotato, 
and to bateman (https://github.com/bateman), for its corsaronero-cp-provider, that I used as a skeleton and from where I copied the function for title translation.



License
=========

```
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2013 Romain Lespinasse <romain.lespinasse@gmail.com>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
