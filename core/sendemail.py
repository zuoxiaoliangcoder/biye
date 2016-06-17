# -*- coding: utf-8 -*-

from settings import STMPSERVER, EMAILPASSWORD, EMAILUSER, PORT
import const
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

class StmpSend(object):

    from_addr = STMPSERVER
    userf = EMAILUSER
    passf = EMAILPASSWORD
    port = PORT

    @classmethod
    def _format_addr(cls, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    # 根据验证码的类型发送相应的邮件
    @classmethod
    def send_email(cls, username, _text, codetype):
        msg2 = ''
        title = ''
        if codetype == const.VERREG :
            msg2 = u'感谢您使用爱阅读，您本次在爱阅读的注册密码验证码为:' + _text + u'，10分钟内有效，请不要泄露给他人，请尽快完成注册操作；如果非您本人操作，请忽略本邮件。'
            title = u'爱阅读平台用户申请注册'
        else:
            msg2 = u'感谢您使用爱阅读，您本次在爱阅读上申请的找回密码验证码为:' + _text + u'，10分钟内有效，请不要泄露给他人，请尽快完成注册操作；如果非您本人操作，请忽略本邮件。'
            title = u'爱阅读找回密码'

        print 'msg: ', msg2
        msg = MIMEText(msg2, 'plain', 'utf-8')
        msg['From'] = cls._format_addr(u'<%s>' % cls.from_addr)
        msg['To'] = cls._format_addr(u'<%s>' % username)
        msg['Subject'] = Header(title, 'utf-8').encode()
        # to_addr = username
        server = smtplib.SMTP(cls.from_addr, cls.port)
        server.set_debuglevel(1)
        server.login(cls.userf, cls.passf)
        server.sendmail(cls.userf, [username], msg.as_string())
        server.quit()
        print 'email successs\n\n\n'
        return True
