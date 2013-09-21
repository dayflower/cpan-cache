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

Illustration
------------

    $ cat cpanfile
    requires 'Amon2' => '0';
    
    
    ### First time (not cached)
    $ time PERL_CARTON_MIRROR=http://localhost:9800/ carton install --path local1
    Installing modules using cpanfile
    Successfully installed ExtUtils-MakeMaker-6.76 (upgraded from 6.57_05)
    Successfully installed HTML-FillInForm-Lite-1.13
    ...
    ...
    44 distributions installed
    Complete! Modules were installed into /home/ito/tmp/amon2-install/local1
    
    PERL_CARTON_MIRROR=http://localhost:9800/ carton install --path local1
      67.58s user 11.66s system 43% cpu 3:03.79 total
    
    
    ### Second time (cache used)
    $ time PERL_CARTON_MIRROR=http://localhost:9800/ carton install --path local2
    Installing modules using cpanfile
    Successfully installed ExtUtils-MakeMaker-6.76 (upgraded from 6.57_05)
    Successfully installed HTML-FillInForm-Lite-1.13
    ...
    ...
    44 distributions installed
    Complete! Modules were installed into /home/ito/tmp/amon2-install/local2
    PERL_CARTON_MIRROR=http://localhost:9800/ carton install --path local2
      63.44s user 11.27s system 92% cpu 1:20.56 total

TODO
----

* better document!
* daemonize
* better logging
* work with Last-Mofified header
* request with If-Modified-Since header
