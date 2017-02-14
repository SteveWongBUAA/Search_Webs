#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import MySQLdb
import json
from Search_Webs import Search_Webs
import os
import sys
import getopt

class Database(object):
    def __init__(self, dbName="smart_home"):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = 'root'
        self.passwd = '******'
        self.dbName = dbName

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.dbName, port=self.port)
        self.conn.set_character_set('utf8')
        self.conn.autocommit(1)
        print '\n# database connect!\n', self.conn
        #$self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def getdata(self):
	self.cursor.execute("select id, date_format(`updatetime`, '%Y-%m-%d %H:%i:%s')update_time, `key`, val from `smart_dev_1` order by updatetime desc")
	ret = self.cursor.fetchall()
	print ret
	return ret

    def adddata(self, k, v):
	return self.cursor.execute("insert into `smart_dev_1`(`key`, `val`) values('%s', '%s')" % (k, v)) 

    def disconnect(self):
        self.conn.close()
        print '\n# database close!\n'

class MainHandler(tornado.web.RequestHandler):
    def get(self):
	self.render("index.html", urls_json=json.dumps({}), urls={}, open=0)

    def post(self):
	key = self.get_argument('key')
	urls = Search_Webs().search(key)
	#urls = {'s':["baidu.com"]}
	self.render('index.html', urls_json=json.dumps(urls), urls=urls, open=1)

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
