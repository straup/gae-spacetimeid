#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp

import spacetime

if __name__ == '__main__' :

  handlers = [
    ('/', spacetime.Main),
    (r'/encode/(-?\d+(?:\.\d+)?)/(-?\d+(?:\.\d+)?)/(\d+)/?$', spacetime.Encode),
    (r'/decode/(\d+)/?$', spacetime.Decode),

    (r'/woe/encode/(\d+)/(\d+)/?$', spacetime.EncodeWOE),
    (r'/woe/decode/(\d+)/?$', spacetime.DecodeWOE),

    # Note the order here seems to matter - something about the
    # 'encode' regexp confuses django/appengine... who knows...

    (r'/ip/decode/(\d+)/?$', spacetime.DecodeIP),
    (r'/ip/encode/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d+)/?$', spacetime.EncodeIP)

    ]

  application = webapp.WSGIApplication(handlers, debug=True)
  wsgiref.handlers.CGIHandler().run(application)
