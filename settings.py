# encoding: utf-8
from __future__ import unicode_literals

# Flask
DEBUG = True
SECRET_KEY = '\x86It\xceS\xfc\xb1b\x18\x00\x8e\x1c\xb6Sz\x95x\xf9\xcb\xb95-\xca'
BIND_ADDRESS = '0.0.0.0'

# Elasticsearch, qbox.io
ES_HOST = '51f64cb003f0d52e000.qbox.io'
HTTP_AUTH = ('buzzy', 'metasearch',)
ES_SEARCH_SIZE = 30
