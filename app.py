import os
import tornado.web
import tornado.ioloop
import tornado.process
import tornado.websocket
import tornado.httpserver
import subprocess
import logging
import psutil
from subprocess import DEVNULL
from tornado import gen
from tornado.options import define, options
from properties import *

tailed_file = open(FILENAME)
tailed_file.seek(os.path.getsize(FILENAME))
define("port", default=8707, help="run on the given port", type=int)
log_clients = []
cpu_clients = []
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def send_lines():
    where = tailed_file.tell()
    line = tailed_file.readline()
    if not line:
        tailed_file.seek(where)
    else:
        for client in log_clients:
            client.write_message(line.strip())


def cpu_usage():
    for client in cpu_clients:
        client.write_message(dict(cpu=psutil.cpu_percent(percpu=True)))


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('index.html', messages=None)

    def post(self):
        message = self.get_argument('message')
        print(message)


class LogWebSocket(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def open(self):
        logging.info('Log client connected')

    def on_message(self, message):
        print(message)
        if message == 'start':
            log_clients.append(self)
        elif message == 'stop':
            log_clients.remove(self)

    def on_close(self):
        logging.info('Log client disconnected')
        if self in log_clients:
            log_clients.remove(self)


class CPUWebSocket(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def open(self):
        cpu_clients.append(self)
        logging.info('CPU client connected')

    def on_message(self, message):
        pass

    def on_close(self):
        logging.info('CPU client disconnected')
        cpu_clients.remove(self)


class MonitoringHandler(tornado.web.RequestHandler):
    def get(self):
        # self.render('usage.html', messages=None)
        #
        # def post(self):
        #     self.write(json.dumps({'cnt': psutil.cpu_count()}))

        db_part = psutil.disk_usage(DB_PART_PATH)
        ase_part = psutil.disk_usage(ASE_PART_PATH)
        system_memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        load = os.getloadavg()
        self.write(
            dict(
                db={'db_part_total': db_part.total, 'db_part_used': db_part.used, 'db_part_free': db_part.free,
                    'db_part_percent': db_part.percent},
                ase={'ase_part_total': ase_part.total, 'ase_part_used': ase_part.used, 'ase_part_free': ase_part.free,
                     'ase_part_percent': ase_part.percent},
                memory={'memory_total': system_memory.total, 'memory_used': system_memory.used,
                        'memory_percent': system_memory.percent},
                swap={'swap_total': swap.total, 'swap_used': swap.used, 'swap_percent': swap.percent},
                load={'5min': load[0], '10min': load[1], '15min': load[2]}
            )
        )


class ASEHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('ase.html')
        # sub = subprocess.run(["jps | grep AnalyticalServer"], shell=True, stdout=subprocess.PIPE)
        # if not sub.returncode:
        #     pid = sub.stdout.strip().split()[0]
        #     self.render('ase.html', pid=pid)
        # else:
        #     self.render('ase.html', pid=None)

    def post(self):
        sub = subprocess.run(["jps | grep AnalyticalServer"], shell=True, stdout=subprocess.PIPE)
        if not sub.returncode:
            self.write(sub.stdout.strip().split()[0])
        else:
            self.write('0')


class ASEWebSocket(tornado.websocket.WebSocketHandler):
    @gen.coroutine
    def open(self):
        logging.info('ASE client connected')

    def on_message(self, message):
        print(message)
        if message == 'start':
            subprocess.Popen([ASE_START ], shell=True, stdout=DEVNULL, stderr=DEVNULL)
            self.write_message('Запускаю Авточек!')

        if message == 'stop':
            sub = subprocess.Popen(ASE_STOP, shell=True, stdout=subprocess.PIPE)
            line = sub.stdout.readline()
            while line:
                self.write_message(line.strip())
                line = sub.stdout.readline()

        if message == 'restart':
            sub = subprocess.Popen(ASE_RESTART, shell=True, stdout=subprocess.PIPE)
            line = sub.stdout.readline()
            while line:
                self.write_message(line.strip())
                line = sub.stdout.readline()

    def on_close(self):
        logging.info('ASE client disconnected')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/size', MonitoringHandler),
            (r'/ase', ASEHandler),
            (r'/wslog', LogWebSocket),
            (r'/wscpu', CPUWebSocket),
            (r'/wsase', ASEWebSocket),
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
tailed_callback = tornado.ioloop.PeriodicCallback(send_lines, 50)
tailed_callback.start()
cp_callback = tornado.ioloop.PeriodicCallback(cpu_usage, 100)
cp_callback.start()
tornado.ioloop.IOLoop.instance().start()
