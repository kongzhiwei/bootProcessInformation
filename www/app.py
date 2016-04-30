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

try:
    import www.handler.demo_turbine_handler as demo_tb
except:
    import handler.demo_turbine_handler as demo_tb

# import you handler 

class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")
        
class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
           
            (r"/", indexHandler),
           
            # demo handler
            (r"/demo_tb/", demo_tb.initHandler),
            (r"/demo_tbwebsocket", demo_tb.WebSocketHandler),
            
            # add your handler，： 
            
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
  
    scheduler_demo_tb = tornado.ioloop.PeriodicCallback(demo_tb.sendmsssage2client, 2000, io_loop=mainLoop)
    scheduler_demo_tb.start()
    
    # add your  scheduler_
    
    print('Web Server start')
    mainLoop.start()
   
