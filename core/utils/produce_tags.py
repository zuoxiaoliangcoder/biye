# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
sys.path.append('../../')

reload(sys)
sys.setdefaultencoding('utf-8')
import  elasticsearch 
from module.book import Books
import json
from settings import ES_HOST, ES_INDEX, ES_ANALYZER 
from mongoengine import connect

connect('biye')

def ProductTags():
    client = elasticsearch.Elasticsearch(ES_HOST)
    es = elasticsearch.client.IndicesClient(client)
    booklist = Books.objects().all()
    k = 0
    for book in booklist:
        context = book.detail
        print context, '\n\n'
        res = es.analyze(index=ES_INDEX, body=context, analyzer='ik_smart')
        print 'res: ', res, '\n'
        with open('tt', 'w') as f:
            f.write(json.dumps(res, ensure_ascii=False))
        if k == 0:
            break
        k = k + 1

if __name__ == '__main__':
    ProductTags()
