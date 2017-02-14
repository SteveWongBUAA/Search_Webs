#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.gen
import json
from Thread_Search import Thread_Search
import os
import sys
import getopt



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", urls_json=json.dumps({}), urls={}, open=0, isPhone=True)

    def post(self):
        headers = str(self.request.headers)
        isPhone = False
        if headers.find('iPhone') != -1 or headers.find('Android') != -1:
            isPhone = True

        headers, type(headers)
        key = self.get_argument('key')
        # urls = Search_Webs().search(key)
        urls = Thread_Search().search(key)
        #urls = {'s':["baidu.com"]}
        self.render('index.html', urls_json=json.dumps(urls), urls=urls, open=1, isPhone=isPhone)

class Settings(object):
    PORT = 11121 
    settings = {"template_path": os.path.join(os.path.dirname(__file__),"templates"),
                "debug": True}

def argv_get():
    '''
    server.py
    Usage:run a website to modify password for SVN, before run, you should
    configure passwd.conf correctly
    -P port
    -h help file
    --port port
    --help help file
    python server.py -P 8888 or python server.py --port 8888
    '''
    try:
        opts,args = getopt.getopt(sys.argv[1:], "hP:", ["help","port="])
    except:
        print "argv read error"
        print argv_get.__doc__
        sys.exit()
    for option,parameter in opts:
        if option in ("-h","--help"):
            print argv_get.__doc__
            sys.exit()
        elif option in ("-P","--port"):
            Settings.PORT = parameter
            return 0

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], **Settings.settings)

if __name__ == "__main__":
    argv_get()
    app = make_app()
    app.listen(Settings.PORT)
    tornado.ioloop.IOLoop.current().start()
