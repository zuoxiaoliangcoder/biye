# -*- coding: utf-8 -*-
import tornadoredis
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.gen
import logging
from mongoengine import connect
from hits import HitsHandler


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('app')


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        c = tornadoredis.Client()
        print c.get('book_list1')
        foo = yield tornado.gen.Task(c.get, 'foo')
        bar = yield tornado.gen.Task(c.get, 'bar')
        test = yield tornado.gen.Task(c.smembers, 'book_list')
        print 'test: \n',  test
        print '\nhahha'
        self.set_header('Content-Type', 'text/html')
        #self.render("template.html", title="Simple demo",foo=foo, bar=bar, zar=zar)
        print 'over'
        self.write({'foo': foo, 'bar': bar})


application = tornado.web.Application([
    (r'/', MainHandler),
])

@tornado.gen.coroutine
def create_test_data():
    c = tornadoredis.Client()
    '''
    rs = yield tornado.gen.Task(c.exists, 'book_list')
    print rs, 'fefefefe'
    if  rs:
        book_list = yield tornado.gen.Task(c.get, 'book_list')

        print 'deg', book_list, 'right n\n\n'
        #Books.objects()       
    '''
    with c.pipeline() as pipe:
        book_list = [2, 5, 6]
        for i in book_list:
            pipe.sadd('book_list', i)
        '''
        pipe.zadd('test', 21, 'b')
        pipe.zadd('test', 36, 'c')
        pipe.set('book_list', book_list, 12 * 60 * 60)
        '''
        yield tornado.gen.Task(pipe.execute)
    print 'Test data initialization completed.'


if __name__ == '__main__':
    # Start the data initialization routine
    connect('biye')
    create_test_data()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print 'Demo is runing at 0.0.0.0:8888\nQuit the demo with CONTROL-C'
    tornado.ioloop.IOLoop.instance().start()
   

