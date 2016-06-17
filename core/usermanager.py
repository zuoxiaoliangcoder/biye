# -*- coding: utf-8 -*-

from module.book import Books,VerifyCode
from module.user import User
from core.utils.asnystasks import send_email
from bson import ObjectId
import random
import datetime
import const
import tornado
import motor


class UserManager(object):

    ''' 得到一个用户的所有信息, 没有则返回None '''
    @classmethod
    def get_user(cls, user_id=None, account=None):
        if user_id is not None and not isinstance(user_id, ObjectId):
            user_id = ObjectId(user_id)
        match = dict(id=user_id) if user_id else dict(account=account)
        user = User.objects(match).first()
        return user

    @classmethod
    def add_one(cls, email, password, nickname=None, contact=None):
        User(email=email, password=password, contact=contact).reg_save()
        # use once, delete it at once!
        VerifyCode.objects.filter(account=email).delete()

    @classmethod
    @tornado.gen.coroutine
    def check_account(cls, db, email, password):
        print email, '\n', 'password: ', password
        doc = yield db.user.find_one({'account': email, 'password': password})
        raise tornado.gen.Return(doc)

    @classmethod
    @tornado.gen.coroutine
    def get_user_info_idlist(cls,  id_list, db=None):
        if db is None:
            db = motor.motor_tornado.MotorCLient().biye
        if isinstance(id_list, list):
            id_list = [id_list,]
        user_list = []
        cur = db.user.find({'index': {'$in': id_list}})
        while (yield cur.fetch_next):
            user_list.append(cur.next_onject())
        raise tornado.gen.Return(user_list)

    @classmethod
    @tornado.gen.coroutine
    def get_user_by_name(cls, uname, db=None):
        if db is None:
            db = motor.motor_tornado.MotorCLient().biye
        user = yield  db.user.find_one({'nickname': uname})
        raise tornado.gen.Return(user)


class VerifyManager(object):
    '''生成验证码'''
    '''在本系统中不允许一个用户在验证码有效时间内同时获取注册验证码和找回密码验证码'''

    @classmethod
    def get_verifycode(cls, email, type_):
        verifycode = str(random.randint(100000, 999999))

        ver = VerifyCode.objects(account=email).first()
        deadtime = datetime.datetime.now() + datetime.timedelta(minutes=const.VERIFYCODETIME)
        if not ver:
            VerifyCode(account=email, verifycode=verifycode, deadtime=deadtime, code_type=type_).save()
            send_email.apply_async(args=[email, verifycode, type_],
                               queue='email_queue')
            return {'verify': verifycode}
        else:
            '''在验证码有效期期内连续请求不同类型的验证码'''
            if ver.code_type != type and ver.deadtime < datetime.datetime.now():
                return const.VERTYPEERROR
            else:
                ver.verifycode = verifycode
                ver.deadtime = deadtime
                ver.code_type = type_
                ver.save()
        print 'start celery'
        send_email.apply_async(args=[email, verifycode, type_],
                               queue='email_queue')
        return {'verify': verifycode}

    @classmethod
    def check_email_vcode(cls, email, verify_code):
        record = VerifyCode.objects(account=email).first()
        now_time = datetime.datetime.now()
        if verify_code != record.verifycode:
            return {'res': const.VERIFYERROR}
        if record.deadtime < now_time:
            return {'res': const.VERIFYDEAD}
        return {'res': const.SUCCESS}





