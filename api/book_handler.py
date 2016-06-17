# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from core.bookmanager import BookManager
import tornado.gen

import pymongo
import tornadoredis
from settings import HIT_BOOKS, COLLECBOOKS
from base.handler import BaseHandler
from module.book import Books, Comments
from module.user import User
import re
from core.auth import admin_login
import const
'''点击量排行榜和收藏帮'''
@tornado.gen.coroutine
def GetHitsSort(db, book_type=1,  redisclient=None, start=0, stop=9, *args):
    print '-----------------\n\n'
    c, ret = redisclient, []
    if c is None:
         c = tornadoredis.Client()
    redis_table = HIT_BOOKS if book_type else COLLECBOOKS
    sort_param = 'hits' if book_type else 'collections'

    res = yield tornado.gen.Task(c.exists, redis_table)
   #　redis中有数据缓存
    if res:
        print 'has redis\n\n\nn\n\n---------------------\n'
        book_list = yield tornado.gen.Task(c.zrevrange, redis_table, start, stop, True)
        for i in book_list:
            book = yield db.books.find_one({'index': int(i[0])})
            if book_type == 1:
                book['hits'] =  yield tornado.gen.Task(c.zscore, redis_table, str(i[0]))
            ret.append(book)
        raise tornado.gen.Return(ret)
    curlst = db.books.find().sort([(sort_param, pymongo.DESCENDING)]).limit(9)
    while (yield curlst.fetch_next):
        ret.append(curlst.next_object())
    
    raise tornado.gen.Return(ret)


'''获取某个用户的关注列表, 或者时收藏列表'''
'''
本身由于收藏列表和关注列表都是用户信息属性，　
在redis中使用hashmap存储的话，会减少hash值的存储，减少空间　
但是由于要动态修改这两个set()，如果set()的量比较大的话那么序列化和反序列化的时间
便会很久。综合考虑为了在本系统还是使用单独的set()　操作更加简单
'''

@tornado.gen.coroutine
def GetUserInfo(user_id, user_info_type, redis_cli=None):
    if redis_cli is None:
        redis_cli = tornadoredis.Client()
    if user_info_type == 1:
        info = 'follows.'
    else:
        info = 'collections.'
    ''' 返回值时一个　list　列表'''
    res = yield tornado.gen.Task(redis_cli.smembers, info + str(user_id))
    print 'res: ', res, '\n'
    raise tornado.gen.Return(set(res))



class BookDetail(BaseHandler):
    @admin_login
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        url = self.request.path
        book_id = re.search(r'/\d+$', self.request.path).group(0)[1:]
        book = Books.objects(index=int(book_id)).first()
        comments = [{'authod'}]
        t = tornadoredis.Client()
        print 'book_id: ', str(book_id)
        #foo = t.zincrby('book_list', 1, str(book_id))
        foo = yield tornado.gen.Task(t.zincrby, 'book_list',  str(book_id), 1)
        print 'foo: ',foo
        self.render('index/book_detail.html', book=book, comments =book.comments, \
                    userId=self.current_user_my['userId'])

class BookCommecnt(BaseHandler):
    @admin_login

    def post(self):
        import datetime
        author = self.parse_body('author', '')
        com_time = datetime.datetime.now()
        theme = self.parse_body('theme', '')
        comment = self.parse_body('comment', '')
        book_id = self.parse_body('bookId', '')
        nickname = User.objects(index=int(author)).first().nickname
        com = Comments(author=author, nickname=nickname, com_time=com_time, theme=theme,\
                 comment=comment)
        com.save()
        print 'book_Id: ', book_id

        print 'debug: ',
        t= Books.objects(index=int(book_id)).first()
        t.comments.append(com)
        t.save()
        self.write({'errorCode': 10000})

#
class BookType(BaseHandler):
    @admin_login
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        url = self.request.path
        if 'java' in url:
            type_ = 0
        elif 'cdouble' in url:
            type_ = 1
        elif 'webDevelop' in url:
            type_ = 2
        elif 'mobile' in url:
            type_ = 3
        elif 'html' in url:
            type_ = 4
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        book_list = Books.objects(type=type_).all().skip(start).limit(count)
        c = tornadoredis.Client()
        each_book_hits = {}
        for i in book_list:
            hits = yield tornado.gen.Task(c.zscore, 'book_list', str(i['index']))
            each_book_hits.update({i['index']: hits})
        book_dict = [i.to_dict() for i in book_list]
        user = self.current_user_my
        #book_list = yield BookManager.get_book_list(self.settings['db'], 0)
        hits = yield GetHitsSort(self.settings['db'], book_type=1)
        collections = yield GetHitsSort(self.settings['db'], book_type=0)
        self.render('index/content.html', booklist=book_dict, obj_str=str, hits=hits, \
                    collections=collections, userId=user['userId'], username=user['username'],
                    start=0, count=10, each_book_hits=each_book_hits)


from core.utils.search import SearchMixin
class BookSearch(BaseHandler, SearchMixin):
    @admin_login
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)

        key_word = self.get_argument('srch-term', '')
        match =  self.get_match(keyword=key_word)
        book_list = self.get_result(match)

        c = tornadoredis.Client()
        each_book_hits = {}
        for i in book_list:
            hits = yield tornado.gen.Task(c.zscore, 'book_list', str(i['index']))
            each_book_hits.update({i['index']: hits})
        user = self.current_user_my

        hits = yield GetHitsSort(self.settings['db'], book_type=1)
        collections = yield GetHitsSort(self.settings['db'], book_type=0)
        self.render('index/content.html', booklist=book_list, obj_str=str, hits=hits, \
                    collections=collections, userId=user['userId'], username=user['username'],
                    start=0, count=10, each_book_hits=each_book_hits)

# 从个人收藏中删除某本书籍
class BookRemove(BaseHandler):
    @admin_login
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        url = self.request.path
        book_id = re.search(r'/[0-9]{1,10}', url).group(0)[1:]
        res_cli = tornadoredis.Client()
        user_id = self.current_user_my['userId']
        
        t = yield tornado.gen.Task(res_cli.srem, 'collections.'+str(user_id), str(book_id))
        print 'debug: ', t, ' \n'
        self.write({'errorCode': const.SUCCESS})
    

if __name__ == '__main__':
    t = GetUserInfo(1, 1)
    print t
