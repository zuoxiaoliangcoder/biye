# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from module.book import Books
from mongoengine import connect
import tornado


# 从mongoDB中取出数据,然后排序json格式传给任务执行单元
class HitsHandler(object):
    def __init__(self, *args, **kwargs):
        connect('biye')
        
        def getbooklist():
            (b_list, res) = Books.objects().all(), []
            for i in b_list:
                res.append({'index': i.index, 'hits': i.hits})
            return res
        t = getbooklist()
        self.__book_list = t

    @property
    def book_list(self):
        if self.__book_list:
            return self.__book_list 

    ''' return book的长度'''
    @property
    def len_booklist(self):
        return len(self.__book_list)

    def quickSort(self, sort_list, left, right, *args, **kw):
        mid = sort_list[left]
        temp = sort_list[left]['hits']
        p, i, j = left, left, right
     
        while i <= j :
            while j >= p and sort_list[j]['hits'] >= temp :
                j -= 1

            if j >= p:
                sort_list[p] = sort_list[j]
                p = j
     
            if sort_list[i]['hits'] <= temp and i <= p:
                i += 1
            if i <= p:
                sort_list[p] = sort_list[i]
                p = i

        sort_list[p] = mid
        if p-left > 1:
            self.quickSort(sort_list, left, p-1)
        if right-p > 1:
            self.quickSort(sort_list, p+1, right)
        return sort_list

        '''
    def store_data_to_redis():
    c = tornadoredis.Client()
    if  c.exists('book_list'):
        book_list = c.get('book_list')
        print 'deg', book_list, 'right n\n\n'
        #Books.objects()       
        c.delete('book_list')
     
    with c.pipeline() as pipe:
        bookobj = HitsHandler()    
        book_list = bookobj.quickSort(bookobj.book_list, 0, bookobj.len_booklist-1)
        for i in book_list:
            pipe.zadd('book_list1', int(i['hits']),  str(i['index']))


        pipe.set('book_list', book_list, 12 * 60 * 60)
        yield tornado.gen.Task(pipe.execute)
    print 'Test data initialization completed.'
        '''


if '__main__' == __name__:
    t= []
    t.append({'index': 1, 'hits': 5})
    t.append({'index': 2, 'hits': 6})
    t.append({'index': 3, 'hits': 2})
    t.append({'index': 4, 'hits': 10})
    t.append({'index': 5, 'hits': 8})
    t.append({'index': 6, 'hits': 8})
    t = HitsHandler().quickSort(t, 0, 5)    
    print '\n\n', HitsHandler().book_list









