# -*- coding: utf-8 -*-

from mongoengine import Document, StringField, ListField, IntField, DateTimeField
from mongoengine import connect
import random


class Books(Document):
    # the type of the book
    '''
    0: java
    1: c/c++/vc
    2: web
    3: yidong develop
    4: html xhtml develop
    '''
    type = IntField()
    # 用来给书表示序列号, 用来唯一区分书记即可
    index = IntField()
    title = StringField(required=True)
    cbs_author = StringField()
    cbs_time = StringField()
    cbs_pub = StringField()
    price = StringField()
    detail = StringField()
    label = ListField(StringField)
    # 书籍点击量
    hits = IntField(default=0)
    # 书籍被收藏的次数
    collections = IntField(default=0)
    comments = ListField()

    def to_dict(self):
        res = {
            'index': self.index,
            'type': self.type,
            'title': self.title,
            'cbs_author': self.cbs_author,
            'cbs_time': self.cbs_time,
            'cbs_pub': self.cbs_pub,
            'price': self.price,
            'detail': self.detail,
            'label': self.label,
            'hits': self.hits,
            'collections': self.collections,
            'comments': self.comments
        }
        return res


class Comments(Document):
    author = IntField()
    nickname = StringField()
    com_time = DateTimeField()
    theme = StringField()
    comment = StringField()

class VerifyCode(Document):
    '''验证码'''

    account = StringField(required=True)
    verifycode = StringField(required=True)
    '''验证码失效时间'''
    deadtime = DateTimeField()
    '''验证码类型'''
    code_type = IntField()

if __name__ == '__main__':
    connect('biye')
    booklist, index  = Books.objects().all(), 1
    for book in booklist:
        book.collections = random.randint(0, 100)
        book.index = index
        index += 1
        book.save()
