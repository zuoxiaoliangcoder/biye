#!/usr/bin/env python
# -*- coding=utf-8 -*-

import front_handler


front_urls = [
    # 首页
    (r'^/{0,1}$', front_handler.IndexHandler),
    (r'^/login/{0,1}$', front_handler.IndexHandler),
    (r'^/register/{0,1}$', front_handler.IndexHandler),
    (r'^/signup/(?P<accountType>\d)/{0,1}$', front_handler.IndexHandler),
    (r'^/signup_before/{0,1}$', front_handler.IndexHandler),
    (r'^/forget/first/{0,1}$', front_handler.IndexHandler),
    (r'^/forget/second/(?P<accesstoken>.+)/{0,1}$', front_handler.IndexHandler),
    (r'^/change_password/{0,1}$', front_handler.IndexHandler),
    (r'^/helper/{0,1}$', front_handler.IndexHandler),
    (r'^/user_protocol/{0,1}$', front_handler.IndexHandler),
    (r'^/welcome/{0,1}$', front_handler.IndexHandler),
    (r'^/goods/list/(?P<id>\w+)/{0,1}$', front_handler.IndexHandler),
    (r'^/goods/list/$', front_handler.IndexHandler),
    (r'^/history/list/{0,1}$', front_handler.IndexHandler),
    (r'^/history/detail/(?P<id>\w+)/{0,1}$', front_handler.IndexHandler),
    (r'^/404/{0,1}$', front_handler.IndexHandler),
]