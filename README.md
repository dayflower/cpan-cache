CPAN-Cache
==========

Caching server for CPAN distribution installation.

Usage
-----

    $ python cpan_cache.py
    Serving CPAN Cache on port 8800 ...
    
    # with cpanm
    $ cpanm --mirror=http://localhost:8800/ Foo::Bar
    
    # with carton
    $ PERL_CARTON_MIRROR=http://localhost:8800/ carton install

TODO
----

* better document!
* options
* better logging
* work with Last-Mofified header
* request with If-Modified-Since header
