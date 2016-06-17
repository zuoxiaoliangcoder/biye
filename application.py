# -*- encoding: utf-8 -*-

import tornado.web
import tornado.websocket
from urls import urls
from settings import app_setting
from mongoengine import connect
import motor

# 连接数据库
connect('biye', host='127.0.0.1')
db = motor.motor_tornado.MotorClient().biye



url = (
    r'/(.*)',
    tornado.web.StaticFileHandler,
    dict(path=app_setting['static_path'])
)


urls.append(url)


app = tornado.web.Application(
    handlers=urls,
    db=db,
    **app_setting
)
