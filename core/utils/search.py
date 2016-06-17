# -*- coding: utf-8 -*-
import elasticsearch
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
from settings import ES_INDEX, ES_DOCTYPE, ES_HOST, ES_ANALYZER

class SearchMixin(object):
    """搜索的Mixin"""

    def get_result(self, match, page=1, count=10):
        """得到elasticsearch的搜索结果"""

        es = elasticsearch.Elasticsearch(ES_HOST)
        start = page
        result = es.search(
            ES_INDEX, ES_DOCTYPE, body=match, size=count, from_=start,
        )
        data_list = [ i['_source'] for i in result['hits']['hits']]
        print data_list
        return data_list

    def get_keyword(self, content):
        """得到关键词"""
        if not content:
            return []
        es = elasticsearch.Elasticsearch(ES_HOST)
        result = es.indices.analyze(ES_INDEX, content, analyzer=ES_ANALYZER)

        keywords = [i['token'] for i in result['tokens']]

        return keywords

    def get_match(self, **kwargs):
        """生成elasticsearch的query"""

        match = {}

        keys_string = kwargs['keyword']
        # 先实现根据关键词的文本类型做优化
        key_list = keys_string.split()
        import re
        #print 're', re.__dict__
        for i in key_list:
            if re.match(r"\d+", i): # 全数字则说明是UID的可能性非常大
                query = {
                    'query':
                        {
                            'multi_match': {
                                'query': i,
                                'fields': [
                                    'id', 'mid', 'reposts_count',
                                    'comments_count', 'attiudes_count'
                                ],
                                #'analyzer': ES_ANALYZER,
                            }
                        }
                }
                #常规的url地址
            elif re.match('^http://(\w|\_|\.)+\/?(\w|\_|\.)+$', i):  # 如果是网址链接， 那么就使用用这个query
                query = {
                    'query':
                        {
                            'multi_match': {
                                'query': i,
                                'fields': [
                                    'thumbnail_pic', 'bmiddle_pic', 'origin_pic',
                                    'comments_count', 'attiudes_count',
                                    'pic_ids'
                                ],
                                'analyzer': ES_ANALYZER,
                                # duan yu  sousuo
                                'type': 'phrase'
                            }
                        }
                }

        if 'keyword' in kwargs and kwargs['keyword']:
            print 'kwyeord:::::::  ',  kwargs['keyword']
            match = {
                'query':
                    {
                        'multi_match': {
                            'query': kwargs['keyword'],
                            'fields': [
                               'text', 'title^4', 'detail^3', 'cbs_author', 'cbs_pub'],
                            'analyzer': 'chinese',

                        }
                    }
                }
            '''
            match = {
                'query':{
                    'bool':
                        {
                           'should':[{
                               'multi_match': {
                                   'query': 'hha',
                                   'fields': [
                                       'thumbnail_pic', 'bmiddle_pic', 'origin_pic',
                                       'comments_count', 'attiudes_count',
                                       'pic_ids','statuses.text'],
                                   'analyzer': ES_ANALYZER,
                               }
                           }],
                            'should':[{
                                'multi_match': {
                                    'query': u'哈哈',
                                    'fields': [
                                        'thumbnail_pic', 'bmiddle_pic', 'origin_pic',
                                        'comments_count', 'attiudes_count',
                                        'pic_ids', 'statuses.text', 'marks'],
                                    'analyzer': ES_ANALYZER,
                                }
                            }]
                        }
                }
            }
        '''
        print '\n\nmatch: \n', match
        return match
if __name__ == '__main__':
    t = SearchMixin()
    match =  t.get_match(keyword="Head First HTML")
    l = t.get_result(match)
    import json
    print json.dumps(l, ensure_ascii=False)


