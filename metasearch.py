# encoding: utf-8
from __future__ import unicode_literals
from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch import SSLError, RequestError, ConnectionError
from flask import Flask, render_template, jsonify, request

import urllib3

app = Flask(__name__)
urllib3.disable_warnings()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    if not request.is_xhr:
        return render_template('error.html', title='400', msg='Bad'), 400
    query = request.args.get('query', None)
    order = request.args.get('order', None)
    result = {}
    if not query:
        return jsonify(result)
    products = qbox(query, order)
    return jsonify({'products': products})

def qbox(query, order):
    dsl = dict()
    dsl['query'] = {}
    dsl['query']['match'] = {'title': query}
    dsl['size'] = app.config['ES_SEARCH_SIZE']
    dsl['sort'] = []
    products = []
    if order == 'price-asc':
        dsl['sort'].append({'price': {'order': 'asc'}})
    elif order == 'price-desc':
        dsl['sort'].append({'price': {'order': 'desc'}})
    elif order == 'random':
        del dsl['sort']
        del dsl['query']['match']
        dsl['query']['function_score'] = {}
        dsl['query']['function_score']['query'] = {}
        dsl['query']['function_score']['query']['match'] = {'title': query}
        dsl['query']['function_score']['random_score'] = {}
    try:
        es = Elasticsearch(
            host=app.config['ES_HOST'],
            port=443,
            use_ssl=True,
            http_auth=app.config['HTTP_AUTH']
        )
        result = es.search(index='products', body=dsl)
        hits = result.get('hits', None).get('hits', None)
        for item in hits:
            product = dict(item.get('_source', None))
            product['type'] = item['_type']
            products.append(product)
    except (SSLError, RequestError, ConnectionError, NotFoundError):
        pass
    except (AttributeError, TypeError):
        pass
    return products

if __name__ == '__main__':
    app.config.from_object('settings')
    app.run(host=app.config['BIND_ADDRESS'])
