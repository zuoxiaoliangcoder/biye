# -*- coding: utf-8 -*-

from user_handler import UserLogin, UserRegister, GetVerifycode,GetUserFollows,\
    BookCollection, Change_person_info, UserLogout, LoginIndex
from chat import ChatSocketHandler
from book_handler import BookDetail, BookCommecnt, BookType, BookSearch, BookRemove

child_urls = [
    (r'^/api/user_login', UserLogin),
    (r'^/[a-zA-Z0-9]{1,32}/index', LoginIndex),
   #(r'/api/register', UserRegister),
    #(r'/api/get/verify_code', GetVerifycode),
    (r'^/api/chatsocket', ChatSocketHandler),
    (r'^/[a-zA-Z0-9]{1,32}/follows', GetUserFollows),
    (r'^/[a-zA-Z0-9]{1,32}/collection', BookCollection),
    (r'^/[a-zA-Z0-9]{1,32}/info_change', Change_person_info),
    (r'^/[a-zA-Z0-9]{1,32}/logout', UserLogout),
    (r'^/books/detail/[0-9]+$', BookDetail),
    (r'^/book/comment$', BookCommecnt),
    (r'^/book/search', BookSearch),
    (r'^/book/delete/[a-zA-Z0-9]{1,10}', BookRemove),
    (r'/book/[a-zA-Z0-9]{1,10}', BookType),
    ]
print child_urls
