# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as Pyq
import threading
from module.book import Books
import Queue
'''
urls = 'http://category.dangdang.com/cp01.54.06.00.00.00.html'
resp = requests.get(urls)
print resp.encoding
resp.text
tmp = resp.text

#file('tmp.html', 'w').write(tmp)

def Gsub(self):
    self = self.strip()
    y = lambda x: '' if (x == '\t') or (x == '\r') or (x == '\n') else x
    self = map(y, self)
    t = str()
    for i in range(len(self)):
        if i == 0 or (i > 0 and self[i-1] != ''):
            t += self[i]
    return t

con = Pyq(tmp)
t = con('.inner')
z = 0
for i in t:
    if z==1:
        break
    title = Pyq(i).find('a').eq(0).attr('title')
    cbs_author = Pyq(i)('.author').find('a').attr('title')
    cbs_time = Pyq(i)('.publishing_time').text()
    cbs_pub = Pyq(i)('.publishing').find('a').attr('title')
    price = Pyq(i)('.price_n').text()
    detial = Pyq(i)('.detail').text()

    print 'title: ', title
    print 'aythor: ', cbs_author
    print 'time: ', cbs_time
    print 'pub: ', cbs_pub
    print "price: ", price
    print 'detail', Gsub(detial)

    #file('data.txt', 'w').write(str(z)+'11111111111111111'+title+'\n\n')

java 类图书
http://category.dangdang.com/cp01.54.06.06.00.00.html
http://category.dangdang.com/pg2-cp01.54.06.06.00.00.html
http://category.dangdang.com/pg3-cp01.54.06.06.00.00.html
http://category.dangdang.com/pg4-cp01.54.06.06.00.00.html
http://category.dangdang.com/pg5-cp01.54.06.06.00.00.html

'''


class NetHttpGetData(threading.Thread):
    def __init__(self, data_que):
        threading.Thread.__init__(self)
        self.data_que = data_que
        self.my_sock = requests.Session()
        self.count = 10

    def urltype(self):
        '''java'''
        urldict = [{'type': 0, 'urlList': ['http://category.dangdang.com/pg{page}-cp01.54.06.06.00.00.html']}]

        '''c/c++ vc++'''
        urldict.append({
            'type': 1,
            'urlList': ['http://category.dangdang.com/pg{page}-cp01.54.06.01.00.00.html']
        })

        '''web develop'''
        urldict.append({
            'type': 2,
            'urlList': ['http://category.dangdang.com/pg{page}-cp01.54.06.12.00.00.html']
        })

        '''yidong develop '''
        urldict.append({
            'type': 3,
            'urlList': ['http://category.dangdang.com/pg{page}-cp01.54.06.17.00.00.html']
        })

        '''html xhtml develop'''
        urldict.append({
            'type': 4,
            'urlList': ['http://category.dangdang.com/pg{page}-cp01.54.06.07.00.00.html']
        })
        return urldict

    def get_url(self):
        res ={}
        urlList = self.urltype()

        def map_func(x):
            url_ = x.get('urlList').pop()
            for n in range(self.count):
                x.get('urlList').append(url_.format(page=n))
        map(map_func, urlList)
        print 'urllist:  ', urlList
        return urlList

    def run(self):
        urls = self.get_url()
        for each_type in urls:
            type_ = each_type.get('type')
            for url in each_type.get('urlList'):
                html = self.my_sock.get(url)
                self.data_que.put(dict(type=type_, text=html.text))


# the blow code is used to handler the recvied data
class DataHandler(threading.Thread):
    def __init__(self, data_que):
        threading.Thread.__init__(self)
        self.data_que = data_que

    def Gsub(s, self):
        self = self.strip()
        y = lambda x: '' if (x == '\t') or (x == '\r') or (x == '\n') else x
        self = map(y, self)
        t = str()
        for i in range(len(self)):
            if i == 0 or (i > 0 and self[i - 1] != ''):
                t += self[i]
        return t

    def data_handler(self, data, type_):
        con_ = Pyq(data)
        t_ = con_('.inner')
        for i in t_:
            title = Pyq(i).find('a').eq(0).attr('title')
            cbs_author = Pyq(i)('.author').find('a').attr('title')
            cbs_time = Pyq(i)('.publishing_time').text()
            cbs_pub = Pyq(i)('.publishing').find('a').attr('title')
            price = Pyq(i)('.price_n').text()
            detail = Pyq(i)('.detail').text()
            try:
                t = Books(
                    title=title,
                    cbs_author=cbs_author,
                    cbs_time=cbs_time,
                    cbs_pub=cbs_pub,
                    price=price,
                    detail=self.Gsub(detail),
                    type=type_,
                )
                t.save()
                print 1111
            except :
                print '数据保存失败'
                t.print_detail()

    def run(self):
        while True:
            try:
                data = self.data_que.get(1, 5)

                self.data_handler(data.get('text'), data.get('type'))
            except Queue.Empty:
                print 'over'
                self.data_que.task_done()
                break

if __name__ == '__main__':
    que = Queue.Queue()
    pro = NetHttpGetData(que)
    cus = DataHandler(que)
    pro.start()
    cus.start()
    que.join()
    pro.join()
    cus.joino()
