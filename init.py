# -*- coding: utf-8 -*-
import tornadoredis
from module.user import User
from module.book import Books
from mongoengine import connect
import random
''' redis　初始化程序'''

'''个人收藏和粉丝关注 信息放入'''
def user_info_redis(user_type, redis_cli=None):
    if redis_cli is None:
        redis_cli = tornadoredis.Client()
       
    ino_type_ = 'follows.' if user_type else 'collections.'
    all_user = User.objects().all()
    with redis_cli.pipeline() as pipe:
        for i in all_user:
            if user_type == 1:
                for k in i.follows:
                    print i.index, k
                    pipe.sadd('follows.'+ str(i.index),  int(k))
            else:
                for k in i.collections:
                    pipe.sadd('collections.'+ str(i.index),  int(k))
        pipe.execute()
    print '\ninit redis complated\n'

if __name__ == '__main__':
    connect('biye')
    user_info_redis(0)
    user_info_redis(1)
#    t = Books.objects().all()
 #   for i in t:
 #       i.hits = random.randint(1, 30)
  #      i.save()
