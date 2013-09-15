#!/usr/bin/python
# -*- coding: utf-8 -*-
# vi: et ts=2 sw=2 sts=0

import sys, os, os.path, shutil
import urllib2
import BaseHTTPServer

class CPANCache:
  SOURCE_URL = 'http://cpan.metacpan.org'

  class Option:
    def __init__(self):
      self.port       = 8800
      self.cache_dir  = 'cache'
      self.source_url = CPANCache.SOURCE_URL
      self.flat       = True
      self.cache_meta = False

  class FetchError(Exception):
    def __init__(self, code):
      self.code = code
    def __str__(self):
      return 'Status %u' % code

  class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    option = None

    def do_GET(self):
      url = self.option.source_url
      if url.endswith('/'):
        url = url[0:-1]
      url = url + self.path

      need_reload = not self.option.cache_meta \
                    and self.path.startswith('/modules/')

      cache_file = self.path
      if self.option.flat:
        cache_file = os.path.basename(cache_file)
      else:
        if cache_file.startswith('/'):
          cache_file = cache_file[1:]
      cache_file = os.path.join(self.option.cache_dir, cache_file)

      #print >>sys.stderr, "url = %s, cache_file = %s" % (url, cache_file)

      cache_file_dir = os.path.dirname(cache_file)
      if not os.path.isdir(cache_file_dir):
        os.makedirs(cache_file_dir)

      try:
        cache_file = self.retrieve_path_from_url(url, cache_file, need_reload)
      except CPANCache.FetchError, e:
        self.send_error(e.code)
        return

      content_length = os.stat(cache_file).st_size
      try:
        fh = open(cache_file, 'rb')
        try:
          self.send_response(200)

          self.send_header('Content-Type',
                           self.content_type_from_filename(cache_file))
          self.send_header('Content-Length', '%d' % content_length)
          self.end_headers()

          shutil.copyfileobj(fh, self.wfile)
        finally:
          fh.close()
      except IOError, (errno, strerror):
        self.send_error(500)

    def content_type_from_filename(self, filename):
      if filename.endswith('.gz'):
        return 'application/x-gzip'
      else:
        return 'application/octet-stream'

    def retrieve_path_from_url(self, url, path, reload=False):
      if reload and os.path.isfile(path):
        os.unlink(path)

      if not os.path.isfile(path):
        code = self.fetch_from_url(url, path)
        if code != 200:
          raise FetchError, code

      return path

    def fetch_from_url(self, url, path):
      try:
        res = urllib2.urlopen(url)
      except urllib2.HTTPError, e:
        return e.code
      except urllib2.URLError, e:
        print >> sys.stderr, 'fetch_url(%s) failed: %s' % (url, e.reason)
        return 500
      else:
        try:
          fh = open(path, 'wb')
          try:
            shutil.copyfileobj(res, fh)
          except IOError, (errno, strerror):
            print >> sys.stderr, 'fetch_url(%s) failed: %s' % (url, strerror)
            fh.close()
            os.unlink(path)
            return 500
          except:
            print >> sys.stderr, 'fetch_url(%s) failed: %s' % (url, sys.exc_info()[0])
            fh.close()
            os.unlink(path)
            raise
          else:
            fh.close()
            return 200
        finally:
          res.close()

  def run(self, option = None):
    if option == None:
      option = CPANCache.Option()
    CPANCache.RequestHandler.option = option
    httpd = BaseHTTPServer.HTTPServer(("", option.port),
                                      CPANCache.RequestHandler)
    print >>sys.stderr, "Serving CPAN Cache on port %d ..." % (option.port)
    httpd.serve_forever()

if __name__ == '__main__':
  CPANCache().run()
