# -*- coding: utf-8 -*-
"""

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain

"""
import tornado.web
import tornado.websocket
import json

import redis
import codecs
import os

conn = redis.Redis('localhost')

turbineclients = []
clients_machine_ip = []

taglist = []

def GetTagDefInfo(tagfile):
    taglist = []
    file = codecs.open(tagfile, 'r', 'utf-8')
    with file:
        discardline = file.readline()
        for line in  file:
            desc, id, si = line.split()
            taglist.append({'desc':desc, 'id':id, 'si':si, 'value': '-10000', }) 
    
    print(taglist)
    
    return taglist

def TagSnapshot(taglist):
   
    pipe = conn.pipeline()
    for element in taglist:
        pipe.hget(element['id'], 'value')
    tagvaluelist = pipe.execute()

    tagvalue = list()
    for element in  tagvaluelist:
        try: 
            tagvalue.append(float(element))
        except:
            tagvalue.append(-1000.0)

    return tagvalue


def turbine_gettagdata(taglist):
    tagvalue = TagSnapshot(taglist)

    response_to_send = {}
    response_to_send['value'] = tagvalue
    return response_to_send


def sendmsssage2client():
    
    if (len(taglist) > 0):
        response_to_send = turbine_gettagdata(taglist)
        for c in turbineclients:
            c.write_message(json.dumps(response_to_send))

class initHandler(tornado.web.RequestHandler):

    def get(self):

        title = '在线监视客户端： 高压缸效率'
        
        global  taglist 
        
        tagfile = "./handler/demo_turbine_tag.txt"
        print(tagfile)
        
        taglist = GetTagDefInfo(tagfile)
        
        tagvalue = TagSnapshot(taglist)
        
        for i in range(len(tagvalue)):
            taglist[i]['value'] = '{:.2f}'.format(tagvalue[i])
        
        print(taglist)

        clients_machine_ip.append(self.request.remote_ip)
        print('Client IP:', self.request.remote_ip)

        self.render("demo_turbine_ui.html", title=title, tagname=taglist)

    def post(self):
        pass

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print("message received " + message)

    def open(self):
        if self not in turbineclients:
            turbineclients.append(self)
            self.write_message(u"Connected")
            print("Turbine WS Clients" + str(len(turbineclients)))

    def on_close(self):
        if self in turbineclients:
            turbineclients.remove(self)
            print("Turbine WS Clientse " + str(len(turbineclients)))
