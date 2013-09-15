CPAN-Cache
==========

Caching server for CPAN distribution installation.

Usage
-----

    $ python cpan_cache.py -h
    
    Usage: cpan_cache.py [options]
    
    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  port number (default: 9800)
      -c CACHE_DIR, --cache-dir=CACHE_DIR
                            cache directory (default: "cache")
      -f, --flat            cache objects into a single flat directory
      -m, --cache-metadata  cache metadata (02packages.details.txt.gz)
      -s SOURCE_URL, --source-url=SOURCE_URL
                            CPAN source URL (default: "http://cpan.metacpan.org")
    
    $ python cpan_cache.py --flat
    Serving CPAN Cache on port 9800 ...
    
    # with cpanm
    $ cpanm --mirror=http://localhost:9800/ Foo::Bar
    
    # with carton
    $ PERL_CARTON_MIRROR=http://localhost:9800/ carton install

TODO
----

* better document!
* daemonize
* better logging
* work with Last-Mofified header
* request with If-Modified-Since header
