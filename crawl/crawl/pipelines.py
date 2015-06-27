# encoding: utf-8
from __future__ import unicode_literals
from elasticsearch import Elasticsearch, exceptions as ee
from scrapy.exceptions import DropItem
from scrapy import log

import exceptions
import locale
import urllib3

urllib3.disable_warnings()
locale.setlocale(locale.LC_NUMERIC, '')
ES_HOST = '51f64cb003f0d52e000.qbox.io'
HTTP_AUTH = ('buzzy', 'metasearch',)
es = Elasticsearch(host=ES_HOST, port=443, use_ssl=True, http_auth=HTTP_AUTH)
es.indices.create(index='products', ignore=[400])


class StripPipeline(object):
    def process_item(self, item, spider):
        for k, v in item.items():
            if v:
                item[k] = v.strip()
        return item


class EmptyCheckPipeline(object):

    VIP_KEYS = ('id', 'price',)

    def process_item(self, item, spider):
        for k, v in item.items():
            if k in self.VIP_KEYS and not v:
                raise DropItem('EmptyCheckError: {0} is empty'.format(k))
        return item


class NumberCastPipeline(object):

    KEYS = ('id', 'price', 'condition',)

    def process_item(self, item, spider):
        for k, v in item.items():
            if k in self.KEYS:
                try:
                    item[k] = locale.atoi(v)
                except (exceptions.AttributeError, exceptions.ValueError):
                    msg = 'NumberCastError: {0}={1}'.format(k, v)
                    log.msg(msg, level=log.WARNING, spider=self)
        return item


class QboxPipeline(object):
    def process_item(self, item, spider):
        doc = dict(item)
        doc_id = doc.pop('id', None)
        if not doc_id:
            raise DropItem('Attribute id is empty'.format(spider.name))
        try:
            es.index(index='products', doc_type=spider.name,
                     id=doc_id, body=doc)
        except (ee.SSLError, ee.RequestError, ee.ConnectionError):
            msg = 'QboxError: {0} {1}'.format(spider.name, doc)
            log.msg(msg, level=log.WARNING, spider=self)
        return item
