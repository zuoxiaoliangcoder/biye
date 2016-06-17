# -*- coding=utf-8 -*-


class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Can't rebind const{0}".format(name)

        if not name.isupper():
            raise TypeError("Need to bind uppercase")

        self.__dict__[name] = value

import sys
sys.modules[__name__] = _const()

import const

# 状态码
const.SUCCESS = 10000

# 验证码的有效时间
const.VERIFYCODETIME = 10
const.VERTYPEERROR = 12000
# 验证码请求参数类型不对
const.VER_PARAM = 12001
const.VERIFYERROR = 12002
const.VERIFYDEAD = 12003

const.VERREG = 0
const.VERPASS = 1

#const.ERROR_


# add by zuxiaoliang
const.COUNT = 5  # 默认的分页大小

const.INVALID_TOKEN = 13001

const.MSG = {
    const.SUCCESS: 'success',
    const.VERTYPEERROR : u'您在验证码有效期内，连续请求了注册和召回密码两种验证码，此次验证码请求失败',
    const.VER_PARAM: u'验证码参数不对',
    const.VERIFYERROR: u'验证码错误',
    const.VERIFYDEAD: u'验证码过期',
    const.INVALID_TOKEN: u'无效的cookie,获取cookie信息过期'
}
