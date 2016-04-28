"""

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain
"""

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os

import www.handler.turbine_handler as tb

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", tb.realtimeHandler),
            (r"/tbwebsocket", tb.WebSocketHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)

    mainLoop = tornado.ioloop.IOLoop.instance()
  
    scheduler_tb = tornado.ioloop.PeriodicCallback(tb.sendmsssage2client, 2000, io_loop=mainLoop)
 
    scheduler_tb.start()
    
    print('Web Server start')
    mainLoop.start()
   
