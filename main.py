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

    ]

  application = webapp.WSGIApplication(handlers, debug=True)
  wsgiref.handlers.CGIHandler().run(application)
