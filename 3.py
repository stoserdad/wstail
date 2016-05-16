import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
import subprocess
import tornado.httpclient
from tornado import gen
import time
import threading

# class MainHandler(tornado.web.RequestHandler):
#     @tornado.web.asynchronous
#     def get(self):
#         cmd = 'sleep 5; echo "qwerty"'
#
#         def send(data):
#             if data:
#                 self.write(data)
#                 self.flush()
#             else:
#                 self.finish()
#
#         self.subprocess(cmd, send)
#
#     def subprocess(self, cmd, callback):
#         ioloop = tornado.ioloop.IOLoop.instance()
#         PIPE = subprocess.PIPE
#         pipe = subprocess.Popen(cmd , shell=True, stdin=PIPE, stdout=PIPE,
#                             stderr=subprocess.STDOUT, close_fds=True)
#         fd = pipe.stdout.fileno()
#
#         def recv(*args):
#             data = pipe.stdout.readline()
#             if data: callback(data)
#             elif pipe.poll() is not None:
#                 ioloop.remove_handler(fd)
#                 callback(None)
#
#         ioloop.add_handler(fd, recv, ioloop.READ)


class AsyncHandler(tornado.web.RequestHandler):

    def get(self):
        # self.fetch('http://httpbin.org/delay/10')
        t = threading.Thread(target=self.fetch, args=('http://httpbin.org/delay/10',))
        t.daemon = True
        t.start()
        self.write('qwe')

    @gen.coroutine
    def fetch(self, url):
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield http_client.fetch(url)
        while True:
            time.sleep(2)
            print(response.body)

    def on_fetch(self, response):
        print(response)


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Test')

application = tornado.web.Application([
    (r"/", AsyncHandler),
    (r"/test/", TestHandler),
], debug=True)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8858)
    tornado.ioloop.IOLoop.instance().start()
