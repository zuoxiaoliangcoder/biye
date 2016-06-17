# -*- coding: utf-8 -*-
from __future__ import absolute_import 
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
from celery import Celery
from settings import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_USERNAME,\
    RABBITMQ_NAME
from core.sendemail import  StmpSend
from datetime import timedelta
from celery.schedules import crontab
import tornadoredis
from module.book import Books
from api.hits import HitsHandler

app_celery = Celery(
    RABBITMQ_NAME,
    #include=['core.utils.asnystasks'],
   # broker='amqp://{0}:{1}@{2}/{3}'.format(
        #RABBITMQ_USERNAME, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_NAME,)
    broker='redis://localhost:6379/0'
)
app_celery.conf.update(
      CELERY_TIMEZONE= 'UTC',
        CELERYBEAT_SCHEDULE={
        'add-every-3-minutes': {
        'task': 'core.utils.asnystasks.store_data_to_redis', 
        'schedule': timedelta(seconds=100),
        'options': {'queue': 'email_queue'}
    }
        }
)
print 'debug '
# 邮件请求异步任务
@app_celery.task
def send_email(to_username, text_, v_type):
    StmpSend.send_email(to_username, text_, v_type)

@app_celery.task
def store_data_to_redis():
    c = tornadoredis.Client()

    res = c.exists('book_list')
    if  res:
        book_list = c.zrevrange('book_list')
        for i in book_list:
            Books.objects(index=int(i[0])).first().hits = int(i[1]).save()
        c.delete('book_list')
    res = c.exists('collections') #　书籍收藏排行
    if res:
        book_list = c.zrevrange('collections')
        for i in book_list:
            Books.objects(index=int(i[0])).first().collections = int(i[1]).save()
        c.delete('collections')
    print 'delete the redis cached \n\n'
    # redis cached is so big that clean in time
    with c.pipeline() as pipe:
        bookobj = HitsHandler()    
        book_list = bookobj.quickSort(bookobj.book_list, 0, bookobj.len_booklist-1)
        for i in book_list:
            print 'hits: ', i['hits'], ' ', i['index'], '\n'
            pipe.zadd('book_list', int(i['hits']),  str(i['index']))
        collections = Books.objects().all()
        for i in collections:
            pipe.zadd('collections', int(i['collections']), str(i['index']))
        pipe.execute()
    print 'Test data initialization completed.'



