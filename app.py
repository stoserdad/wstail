import os
import time
import tornado.web
import tornado.ioloop
import tornado.process
import tornado.websocket
import tornado.httpserver
import logging
from tornado import gen
from tornado.options import define, options
from logView import tail
from tornado.ioloop import IOLoop


tile = open('/tmp/123')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
clients = []
status = False


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('index.html', messages=None)

    def post(self):
        message = self.get_argument('message')
        print(message)


class WebSocket(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def open(self):
        clients.append(self)
        logging.info('client connected')

    def on_message(self, message):
        print(message)
        while message == 'start':
            time.sleep(2)
            print(message)



    @staticmethod
    def send_log():
        tile.seek(0, 2)
        while True:
            where = tile.tell()
            line = tile.readline()
            if not line:
                time.sleep(0.1)
                tile.seek(where)
            else:
                for client in clients:
                    client.write_message(line.strip())

    def on_close(self):
        clients.remove(self)


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []
        handlers = [
            (r'/', MainHandler),
            (r'/websocket', WebSocket),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'})
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static')
        )
        tornado.web.Application.__init__(self, handlers, **settings)

application = Application()
define("port", default=8707, help="run on the given port", type=int)
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(options.port)
tornado.ioloop.IOLoop.instance().start()

# application = Application()
#
# if __name__ == "__main__":
#     server = tornado.httpserver.HTTPServer(application)
#     server.bind(8707)
#     server.start(0)
#     tornado.ioloop.IOLoop.instance().start()
