#!/usr/bin/env python
# -*- coding=utf-8 -*-

from settings import JWT_SECRET, JWT_ALGORITHM
import traceback

import tornado.web
import json
from settings import REDIS_HOST, REDIS_TTL
import const
import datetime
from settings import JWT_EXP
import jwt
import redis
import urllib
import hashlib
from tornado.escape import json_decode, json_encode

def encrypt_token(payload, secret=JWT_SECRET, algorithm=JWT_ALGORITHM):
    """加密"""
    return jwt.encode(payload, secret, algorithm)


def decrypt_token(token, secret=JWT_SECRET, algorithms=JWT_ALGORITHM, options=None):

    """解密"""
    if not options:
        options = {
            'verify_signature': True,
            # 'verify_exp': False,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': False,
            'verify_aud': False,
            'require_exp': False,
            'require_iat': False,
            'require_nbf': False
        }

    try:
        res = jwt.decode(
            token, secret, algorithms=algorithms, options=options)
    except jwt.ExpiredSignatureError:
        print 'ExpiredSignatureError'
        return {}
    except jwt.DecodeError:
        print 'DecodeError'
        return {}
    except jwt.InvalidTokenError:
        print 'InvalidTokenError'
        return {}
    except:
        print 'Error'
        return {}
    else:
        return res


def write_error(self, status_code, **kwargs):

    if self.settings.get("serve_traceback") and "exc_info" in kwargs:
        # in debug mode, try to send a traceback
        self.set_header('Content-Type', 'text/plain')
        for line in traceback.format_exception(*kwargs["exc_info"]):
            self.write(line)
        self.finish()
    else:
        if status_code == 404:
            self.render('modules/core/frame.tpl.html')

        else:
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason,
                        })


class BaseHandler(tornado.web.RequestHandler):
    """定制的RequestHandler"""
    def parse_body(self, k, v=None):
        body = self.request.body
        headers =  self.request.headers
        if 'x-www-form-urlencoded' in headers['content-Type']:
            username = self.get_argument('form-username')
            password = self.get_argument('form-password')
            m2 = hashlib.md5()
            m2.update(password)
            t =  {'username': username, 'password': m2.hexdigest()}
            return t.get(k, v)

        print type(body)
        print 'body', urllib.unquote(body)
        body = json.loads(body)
        return body.get(k, v)

    def parse_token(self, token):
        if token is None:
            token = self.request.headers.get('token')

        res = decrypt_token(token, JWT_SECRET, JWT_ALGORITHM)
        return res

    def raise_error(self, msgcode):
        res = {'errorCode': msgcode, 'errorMsg': const.MSG[msgcode]}
        self.write(res)
        return

    def gen_token(self, u_id, username):
        """生成token"""

        t = datetime.datetime.utcnow() + \
            datetime.timedelta(seconds=JWT_EXP)

        payload = {
            'userId': str(u_id),
            'exp': t,
            'username': username,
        }

        return encrypt_token(payload)
    
    @property
    def current_user_my(self):
        '''开启serure_cookie　必须在　配置中加入 cookie_secret　'''
        user_json = self.get_secure_cookie('ReaderShawn') 
        print 'base handle cookie:  ', user_json
        res =  decrypt_token(user_json)
        if res:
            print 'res: ', res, '\n over\n'
            return res
        else:
            self.raise_error(const.INVALID_TOKEN) 
    




