#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import webbrowser
import ExtConfigParser
import traceback
from bs4 import BeautifulSoup
import sys


class Request(object):

    def __init__(self, key):
        self.getConf(key)
        self.raw_key = key
        self.hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        self.hdr_xml = self.hdr
        self.hdr_xml['X-Requested-With'] = 'XMLHttpRequest'

    def getConf(self, key):
        cf = ExtConfigParser.ExtConfigParser()
        cf.read("./conf/urls.conf")
        self.data = cf.getDict(['url', 'res_kw', 'method', 'should_have_key', 'hdr_more', 'encoding', 'post_key'])
        # print self.data
        for id in self.data.keys():
            if type(key) == unicode:
                key_encode = key.encode(encoding=self.data[id]['encoding'])
            elif type(key) == str:
                key_encode = key.decode(sys.stdin.encoding).encode(self.data[id]['encoding'])
            else:
                key_encode = key
            key_quote = urllib.quote(key_encode)

            if self.data[id]['method'] == 'concat':
                url = self.data[id]['url'].replace('{#concat#}', key_quote)
            elif self.data[id]['method'] == 'append':
                url = self.data[id]['url'] + key_quote
            elif self.data[id]['method'] == 'post':
                url = self.data[id]['url']
            else:
                continue

            self.data[id]['url'] = url
            self.data[id]['key_quote'] = key_quote

        # print self.data
        # print self.post
        # print data
        # print self.urls_concat,self.urls_append,self.urls_post,self.urls_post_keys

    def get_full_urls(self, key):
        urls = []
        # input key is unicode should encode
        for one in self.data:
            if type(key) == unicode:
                key_encode = key.encode(encoding=one['encoding'])
            elif type(key) == str:
                key_encode = key.decode(sys.stdin.encoding).encode(one['encoding'])
            else:
                key_encode = key
            key_quote = urllib.quote(key_encode)
            if one['method'] == 'concat':
                url = one['url'].replace('{#concat#}', key_quote)
            elif one['method'] == 'append':
                url = one['url'] + key_quote
            else:
                url = ''
            urls.append(url)
        return urls


    def request1(self, id):

        if self.data[id]['hdr_more'] == 'y':
            hdr = self.hdr_xml
        else:
            hdr = self.hdr

        if self.data[id]['method'] == 'post':
            post_data = urllib.urlencode({self.data[id]['post_key']: self.raw_key})
            req = urllib2.Request(self.data[id]['url'], headers=hdr, data=post_data)
        else:
            req = urllib2.Request(self.data[id]['url'], headers=hdr)

        try:
            # page = urllib2.urlopen(req)
            # f = page.read()
            # bs = BeautifulSoup(f)
            # return str(bs)
            req.post
        except:
            print traceback.format_exc()
            return None

        # input key is unicode should encode

        #     has_res = self.has_res(url, hdr_more=one['hdr_more'], should_have_key=one['should_have_key'], key=one['key'], )
        #     if has_res:
        #         webbrowser.open(url)
        #         urls.append(url)
        # return urls

    def has_res1(self, id):
        f = self.request1(id)
        if f is None:
            return False
        else:
            findres = f.find(self.data[id]['res_kw'])
            if self.data[id]['should_have_key'] == 'y':
                # 应该有key而且真的找到了key
                if findres != -1:
                    return True
                else:
                    return False
            else:
                # 不应该有key但是找到了key
                if findres != -1:
                    return False
                else:
                    return True



if __name__ == '__main__':
    # Search_Webs().search("homeland")
    # Search_Webs().search("xzchkjq")
    # Search_Webs().search("你的名字")
    rqt = Request('homeland')
    # print rqt.data[12]
    print rqt.request1(15)


