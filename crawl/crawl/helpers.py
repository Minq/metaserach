# encoding: utf-8
from __future__ import unicode_literals


def extract(selector, path, default=''):
    elements = selector.css(path).extract()
    return elements[0] if 0 < len(elements) else default

def extract_re(selector, path, pattern, default=''):
    elements = selector.css(path).re(pattern)
    return elements[0] if 0 < len(elements) else default
