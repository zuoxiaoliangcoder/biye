
'''

curl -XPOST localhost:9200/book/test/_mapping -d '{
        "test" : {
            "_all":{
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart"
            },
            "properties" : {
                "title" : { "type" : "string",
                            "include_in_all": "true",
                            "index" : "not_analyzed",
                            "boost": 8
                            },
                "cbs_author" : { "type" : "string",
                            "include_in_all": "true",
                            "index" : "not_analyzed",
                            "boost": 8
                            },
                "detail" : { "type" : "string",
                            "include_in_all": "true",
                            "boost": 8
                            },
                "cbs_pub" : { "type" : "string",
                            "include_in_all": "true",
                            "index" : "not_analyzed",
                            "boost": 8
                            },
                "cbs_time" : { "type" : "string",
                            "include_in_all": "false",
                            "index" : "not_analyzed",
                             "date_detection" : false,
                            "boost": 8
                            },
                ''


            }
        }
    }
}'
'''
from module.book  import Books
import elasticsearch

from settings import ES_INDEX, ES_DOCTYPE, ES_HOST, ES_ANALYZER
from mongoengine import connect
connect("biye")



es  = elasticsearch.Elasticsearch(ES_HOST)
booklist = Books.objects().all()
k = 0
for i in booklist:
    doc= {
            'index': i.index,
            "title": i.title,
            "cbs_author": i.cbs_author,
            "cbs_pub": i.cbs_pub,
            "detail": i.detail,
            'price': i.price,
            'cbs_time': i.cbs_time,
    }
    try:
        es.index(index = ES_INDEX, doc_type = ES_DOCTYPE, id = k, body = doc)
        print 'k data is success', k
    except Exception:
        print 'k data is error\n'
    k = k + 1

