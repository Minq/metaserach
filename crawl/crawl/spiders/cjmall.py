# encoding: utf-8
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from crawl.items import CrawlCjmallItem
from crawl.helpers import extract, extract_re
from scrapy import log

import exceptions
import scrapy


class CjmallSpider(scrapy.Spider):

    name = "cjmall"
    allowed_domains = ["cjmall.com"]
    BASE_URL = 'http://www.cjmall.com'

    def __init__(self, keyword=None, *args, **kwargs):
        super(CjmallSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        url = ("http://www.cjmall.com"
               "/prd/front/search/search_main.jsp"
               "?srch_gb=&srch_value={0}"
               "&tab_num=1&refer=&srch_disp_value={0}")
        url = url.format(keyword)
        self.start_urls = [
            url.encode('euc-kr')
        ]

    def parse(self, response):
        items = []
        css_path = ('#cjo_content > div '
                    '> div.searchArea > div.galleryType.domainTwo '
                    '> ul > li')
        for sel in response.css(css_path):
            item = CrawlCjmallItem()
            try:
                path = 'div.domainTxt > div.name > a::attr(href)'
                item['id'] = extract_re(sel, path, r'item_cd=(\d*)', '')
                path = 'div.domainTxt > div.name > a::text'
                item['title'] = extract(sel, path, '')
                path = ('div.domainTxt > div.price '
                        '> span > span.blue > strong::text')
                item['price'] = extract(sel, path, 0)
                path = 'a > img::attr(src)'
                item['image_url'] = extract(sel, path, '')
                path = 'div.domainTxt > div.name > a::attr(href)'
                re = r'viewDetailItem\(\'\s*(.*)'
                item['link'] = self.BASE_URL + extract_re(sel, path, re, '')
                items.append(item)
            except exceptions.IndexError:
                msg = 'Out of index, Keyword: {0}'.format(self.keyword)
                log.msg(msg, level=log.WARNING, spider=self)
                log.msg(str(item), level=log.WARNING, spider=self)
            except:
                msg = 'Unknown Error, Keyword: {0}'.format(self.keyword)
                log.msg(msg, level=log.WARNING, spider=self)
        return items
