# -*- coding: utf-8 -*-

from module.book import Books
import tornado
import tornado.gen

''''core模块只提供数据方便的处理，不涉及业务流程'''
class BookManager(object):
    '''该方法提供书籍分类的书籍列表功能'''
    
    @classmethod
    @tornado.gen.coroutine
    def get_book_list(cls, db, book_type, page=1, count=8):
        ret = []
        curlst = db.books.find({'type': book_type}).skip((page-1)*count).limit(count)
        while (yield curlst.fetch_next):
            ret.append(curlst.next_object())

        raise tornado.gen.Return(ret)

    '''使用tags标签选择'''
    @classmethod
    @tornado.gen.coroutine
    def get_book_by_tags(cls, tags, page=1, count=10):
        if not isinstance(tags, list):
            tags = list(tags)
        '''返回满足搜索标签的书籍'''
        book_list = Books.objects(__raw__={'$all': tags}).all()
        return dict(total=len(book_list), booklist=book_list.skip((page-1)*count).limit(count))

    @classmethod
    def get_book_by_id(cls, b_id_list):
        print  ' fid: ', b_id_list
        b_id_list = [int(i) for i in b_id_list]
        ret = []
        curlst = Books.objects(__raw__={'index': {'$in': b_id_list}}).all()
        for i in curlst:
            ret.append({'index': i.index, 'title': i.title})
        return ret 
