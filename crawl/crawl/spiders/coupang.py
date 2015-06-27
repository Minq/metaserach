# encoding: utf-8
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from crawl.items import CrawlCoupangItem
from crawl.helpers import extract
from scrapy import log

import exceptions
import scrapy


class CoupangSpider(scrapy.Spider):

    name = "coupang"
    allowed_domains = ["coupang.com"]
    BASE_URL = 'https://www.coupang.com'

    def __init__(self, keyword=None, *args, **kwargs):
        super(CoupangSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        url = ("https://www.coupang.com/np/search"
               "?q={0}&channel=&eventCategory=GNB"
               "&eventLabel=search")
        url = url.format(keyword)
        self.start_urls = [url]

    def parse(self, response):
        items = []
        for sel in response.css('#productList > li'):
            item = CrawlCoupangItem()
            try:
                path = '*::attr(id)'
                item['id'] = extract(sel, path, '')
                path = 'a.detail-link > strong.title > em::text'
                item['title'] = extract(sel, path, '')
                path = ('a.detail-link > em.prod-price '
                        '> span.price-detail > strong.price '
                        '> em::text')
                item['price'] = extract(sel, path, 0)
                path = 'a.detail-link > span.condition > em::text'
                item['condition'] = extract(sel, path, 0)
                path = 'a.detail-link > img::attr(src)'
                item['image_url'] = extract(sel, path, '')
                path = 'a.detail-link::attr(href)'
                item['link'] = self.BASE_URL + extract(sel, path, '')
                items.append(item)
            except exceptions.IndexError:
                msg = 'Out of index, Keyword: {0}'.format(self.keyword)
                log.msg(msg, level=log.WARNING, spider=self)
                log.msg(str(item), level=log.WARNING, spider=self)
            except:
                msg = 'Unknown Error, Keyword: {0}'.format(self.keyword)
                log.msg(msg, level=log.WARNING, spider=self)
        return items
