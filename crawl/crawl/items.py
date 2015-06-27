# encoding: utf-8
from __future__ import unicode_literals

import scrapy


class CrawlCoupangItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    condition = scrapy.Field()
    image_url = scrapy.Field()
    link = scrapy.Field()


class CrawlCjmallItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    link = scrapy.Field()
