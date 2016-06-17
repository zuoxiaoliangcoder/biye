# -*- coding: utf-8 -*-

from base.handler import BaseHandler
import tornado.web
from module.book import  Books
from core.bookmanager import BookManager
from core.usermanager import UserManager, VerifyManager
import const
from book_handler import GetHitsSort, GetUserInfo
from settings import JWT_EXP
from core.auth import admin_login
from tornado.escape import json_decode, json_encode
import time
from module.user import User
import tornadoredis
from init import user_info_redis



class UserLogin(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine 
    def post(self):

        print 'gei in '
        username = self.parse_body('username')
        password = self.parse_body('password')

        print 'debug: ', username, password, '\n\n'
        user = yield UserManager.check_account(self.settings['db'], username, password)
        print 'user:  ', user
        if not user:
            print 'fefefefefefe'
            self.render('index/login.html', error=u'what you input is error')
            self.finish()
            return

        # print 'username , ', username, " :: ", password
        # user = UserManager.get_user(account=username)
        # tags = user.tags
        token_cookie = self.gen_token(user['index'], user['nickname'])
        print 'cookie: ',token_cookie
        self.set_secure_cookie('ReaderShawn', token_cookie, expires_days=None, expires=time.time()+JWT_EXP),

        '''这部分需要专门的算法实现, 放在最后来实现了'''
        book_list = yield BookManager.get_book_list(self.settings['db'], 0)
        c = tornadoredis.Client()

        collections = yield GetHitsSort(self.settings['db'], book_type=0)
        each_book_hits = {}
        for i in book_list:
            hits = yield tornado.gen.Task(c.zscore, 'book_list', str(i['index']))
            each_book_hits.update({i['index']: hits})
        hits = yield GetHitsSort(self.settings['db'], book_type=1)
        url = '/' + user['nickname']+'/index'
        '''
        self.render('index/content.html', booklist=book_list, obj_str=str, hits=hits, \
                    collections=collections, userId=user['index'], username=user['nickname'],
                    each_book_hits=each_book_hits,start=0, count=10)
        '''
        self.redirect(url)



class LoginIndex(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    @admin_login
    def get(self):
        start = self.get_argument('start', 0)
        count = self.get_argument('count', 10)
        c = tornadoredis.Client()
        user = self.current_user_my
        book_list = yield BookManager.get_book_list(self.settings['db'], 0)
        each_book_hits = {}
        for i in book_list:
            hits = yield tornado.gen.Task(c.zscore, 'book_list', str(i['index']))
            each_book_hits.update({i['index']: hits})
        print each_book_hits
        hits = yield GetHitsSort(self.settings['db'], book_type=1)
        collections = yield GetHitsSort(self.settings['db'], book_type=0)
        self.render('index/content.html', booklist=book_list, obj_str=str, hits=hits, \
                    collections=collections, userId=user['userId'], username=user['username'],
                    start=int(start), count=int(count), each_book_hits=each_book_hits)

class GetVerifycode(BaseHandler):
    def post(self):
        email = self.parse_body('email', '')
        code_type = int(self.parse_body('type', const.VERREG))
        print 'code_type: ', code_type
        if code_type != const.VERREG and code_type != const.VERPASS:
            self.write({'errorCode': const.VER_PARAM, 'errorMsg': const.MSG[const.VER_PARAM]})
        res = VerifyManager.get_verifycode(email, code_type)
        if isinstance(res, dict):
            # self.write({'errorCode': const.SUCCESS, 'data': res['verify']})
            self.write({'errorCode': const.SUCCESS})

        else:
            self.write({'errorCode': res, 'errorMsg': const.MSG[res]})


class UserRegister(BaseHandler):
    def post(self):
        email = self.parse_body('email', '')
        password = self.parse_body('password', '')
        verify_code = self.parse_body('verifycode', '')

        res = VerifyManager.check_email_vcode(email, verify_code)
        if res['res'] != const.SUCCESS:
            self.write({'errorCode': res['res'], 'errorMsg': const.MSG[res['res']]})
            return
        UserManager.add_one(*{'account': email, 'password': password, 'contact': email})
        self.write({'errorCode': const.SUCCESS})


class GetUserFollows(BaseHandler):
    @admin_login
    @tornado.web.asynchronous
    @tornado.gen.coroutine 
    def get(self):
        from chat import ChatSocketHandler
        '''下面得到都是set()结构, 直接求交集'''
        fans_on_line = ChatSocketHandler.waiters
        ''' １　表示获取　关注'''
        print 'userId: ', self.user_id
        fans_in_redis = yield GetUserInfo(self.user_id, 1) 
        ''' 交集得到的只是 user_id'''
        online_follows = fans_on_line & fans_in_redis  
        user_list = yield UserManager.get_user_info_idlist(list(online_follows), db=self.settings['db'])

        print 'debug zuoxiaoliang'
        res = [ {'username': i['nickname'], 'userId': i['index']} for i in user_list]
        self.write({'errorCode': const.SUCCESS, 'follows': res})

''' get 方法　用户有时可能会直接修改url　链接获取他人收藏列表'''
''' 本系统的认证是：　登录之后可以查看其他人的　收藏'''
class BookCollection(BaseHandler):
    @admin_login
    @tornado.web.asynchronous
    @tornado.gen.coroutine 
    def get(self):
        url =  self.request.path
        import re 
        print 'url: ', url, '\n'
        user_name = re.search(r'/\w{1,32}/', url).group(0)[1:-1]
        print 'username: ', user_name 
        user = yield UserManager.get_user_by_name(user_name, self.settings['db'])
        ''' 0 表示　书记收藏'''
        books = yield GetUserInfo(user['index'], 0) 
        booklist =  BookManager.get_book_by_id( books)
        self.write({'errorCode': const.SUCCESS, 'books': booklist})

    @admin_login
    def post(self):
        book_id = self.parse_body('bookId', '')
        user_id = self.current_user_my
        user = User.objects(index=user_id['userId']).first()
        print 'iss: ', user.collections, book_id
        user.collections.append(int(book_id))
        print user.collections
        user.save()
        user_info_redis(0)
        self.write({'errorCode': 10000})

#　修改个人信息接
class Change_person_info(BaseHandler):
    @admin_login
    def get(self):
        url = self.request.path
        import re
        nickname = re.search(r'/\w{1,32}/', url).group(0)[1:-1]
        user = User.objects(nickname=nickname).first()
        self.render('index/user_info.html', user=user, username='shawn')

    @admin_login
    def post(self):
        nickname = self.parse_body('username', '')
        user = User.objects(nickname=nickname).first()
        email = self.parse_body('email', '')
        kw = {}
        new_pass = self.parse_body('newPass')
        if new_pass:
            kw.update({'password': new_pass})
        note = self.parse_body('note', '')
        if note:
            kw.update({'note': note})
        level = self.parse_body('level')
        telnec = self.parse_body('telnec')
        res = ""
        for i in telnec:
            res = res + str(i) + str(level) + ':'
        if res:
            kw.update({'tags': res[0: -1]})

        user.update_info(**kw)

        self.write({'errorCode': 10000})

# LOGOUT
class UserLogout(BaseHandler):
    def get(self):
        self.clear_cookie("ReaderShawn")
        self.redirect('/login')