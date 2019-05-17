import tornado.web
import tornado.httpserver
import tornado.ioloop

import threading
import logging
import os

import config

class PayloadApplication(tornado.web.Application):
    '''payload server application:  serves one static payload file'''
    def __init__(self, filename):
        self.payload_dir = config.PAYLOAD_DIR
        handlers = []
        handlers.append([
            r'/(.*)', tornado.web.StaticFileHandler, {'path': self.payload_dir,'default_filename': filename}
        ])

        tornado.web.Application.__init__(self, handlers)
    

class PayloadServerThread(threading.Thread):
    '''payload server as a thread'''
    def __init__(self, *args, **kwargs):
        try:
            self.port = kwargs.pop('port')
            self.filename = kwargs.pop('filename')
        except:
            raise Exception
        threading.Thread.__init__(self)

    def run(self):
        payload_app = PayloadApplication(filename=self.filename)
        server = tornado.httpserver.HTTPServer(payload_app)
        server.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()