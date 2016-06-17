# -*- coding: utf-8 -*-

from mongoengine import Document, StringField, ListField, IntField,EmailField, DateTimeField, EmbeddedDocumentField

from mongoengine import connect
from bson import ObjectId
import datetime
from book import Books

class User(Document):
    '''用来标示用户序列号，用来存储在redis中，　　而不是使用内置的_id，因为长度太长了，在redis里面占用更大的内存'''
    index = IntField(required=True)
    '''登录帐号'''
    account = StringField(required=True)
    password = StringField(required=True)
    nickname = StringField()
    '''联系方式，暂时支持邮箱'''
    contact = EmailField(required=True)
    '''个性标签'''
    tags = StringField()
    '''注册'''
    reg_time = DateTimeField()
    '''最后登录时间'''
    log_time = DateTimeField()
    # geren
    note = StringField()
    # 关注列表
    follows = ListField()
    # 书籍收藏列表
    collections = ListField(IntField())

    def reg_save(self):
        self.reg_time = datetime.datetime.now()
        self.save()

    def update_info(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)
        self.log_time = datetime.datetime.now()
        self.save()


    def log_save(self):
        if not self.reg_time:
            return None
        self.log_time = datetime.datetime.now()
        self.save()

if __name__ == '__main__':
    connect('biye')
    User(account='547947580@qq.com', password='e10adc3949ba59abbe56e057f20f883e',
         contact='547947580@qq.com', nickname='shawn', reg_time=datetime.datetime.now(), index=1).save()
    
   # User(account='18702809172@163.com', password='e10adc3949ba59abbe56e057f20f883e',
    #     contact='18702809172@163.com', nickname='zzy', reg_time=datetime.datetime.now()).save()
    #User.objects(nickname='shawn').update(index=1)
    #User.objects(nickname='zzy').update(index=2)



