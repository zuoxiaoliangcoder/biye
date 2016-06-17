import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from application import app
from tornado.options import define, options


define("port", default=8004, help="run on the given port", type=int)


if __name__ == "__main__":

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    # connect('test')
    tornado.ioloop.IOLoop.instance().start()
