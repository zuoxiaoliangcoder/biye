# -*- coding: utf-8 -*-

import functools
from tornado.options import define, options
from settings import LOGIN_URL
import tornado.web

def admin_login(method):
    '''权限认证，　如果没有登录，那么重定向到登录界面'''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user_my:
            if self.request.method == "GET":
                self.redirect(LOGIN_URL)
                return
            raise tornado.web.HTTPError(403)
        else:
            setattr(self, 'user_id', self.current_user_my['userId'])
            return method(self, *args, **kwargs)
    return wrapper


