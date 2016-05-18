import os
import tornado.web
import tornado.ioloop
import tornado.process
import tornado.websocket
import tornado.httpserver
import logging
from tornado import gen
from tornado.options import define, options


FILENAME = '/tmp/123'
tailed_file = open(FILENAME)
tailed_file.seek(os.path.getsize(FILENAME))
define("port", default=8707, help="run on the given port", type=int)
clients = []

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def send_log():
    where = tailed_file.tell()
    line = tailed_file.readline()
    if not line:
        tailed_file.seek(where)
    else:
        for client in clients:
            client.write_message(line.strip())


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
        logging.info('client connected')

    def on_message(self, message):
        print(message)
        if message == 'start':
            clients.append(self)
        elif message == 'stop':
            clients.remove(self)

    def on_close(self):
        logging.info('client disconnected')
        if self in clients:
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
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(options.port)
tailed_callback = tornado.ioloop.PeriodicCallback(send_log, 5)
tailed_callback.start()
tornado.ioloop.IOLoop.instance().start()
