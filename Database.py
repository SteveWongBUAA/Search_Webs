#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb


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
