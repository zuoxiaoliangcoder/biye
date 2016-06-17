# -*- coding: utf-8 -*-
import tornado.websocket
import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 10

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        print self.path_args
        self.id_card = self.get_argument('userId')
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                #if waiter.id_card == chat['user_id']:
                    #waiter.write_message(chat)
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            'user_id': parsed['userId'],
            'username': parsed['username']
            }
        print 'user_id: ', parsed['userId'], '\n'
        print 'toUser_id', parsed['toUser'], '\n'
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("index/comment.html", message=chat))
        print chat
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)
