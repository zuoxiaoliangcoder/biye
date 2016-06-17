#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
这个handler 是
"""

import tornado.web
import tornado.gen


class IndexHandler(tornado.web.RequestHandler):
    """首页"""

    #@tornado.web.removeslash
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        print 'hhhhhhhhhhhhhhhhhhhhhhh\n\n'
        path = self.request.path
        print path
        if path == '/':
            self.render('index/index.html')
        elif path == '/login':
            print ''
            self.render('index/login.html')
        elif path == '/register':
            print 'register'
            self.render('index/register.html')