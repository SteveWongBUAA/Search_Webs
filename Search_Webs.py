#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import webbrowser
import ExtConfigParser
import traceback
from bs4 import BeautifulSoup
import sys


class Search_Webs(object):

    def __init__(self):
        self.getConf()

    def getConf(self):
        cf = ExtConfigParser.ExtConfigParser()
        cf.read("./conf/urls.conf")
        self.data = cf.getDict(['url', 'key', 'method', 'should_have_key', 'hdr_more', 'encoding'])
        # print data
        # print self.urls_concat,self.urls_append,self.urls_post,self.urls_post_keys

    def search(self, key):
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
            has_res = self.has_res(url, hdr_more=one['hdr_more'], should_have_key=one['should_have_key'], key=one['key'])
            #print url, key, has_res
            if has_res:
                webbrowser.open(url)
                urls.append(url)
        return urls

    def get_content(self, url, hdr_more):
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        if hdr_more == 'y':
            hdr['X-Requested-With'] = 'XMLHttpRequest'
        req = urllib2.Request(url, headers=hdr)
        try:
            page = urllib2.urlopen(req)
            f = page.read()
            body = BeautifulSoup(f)
            return str(body)
        except:
            print traceback.format_exc()
            return None

    def has_res(self, url, should_have_key, hdr_more, key):
        f = self.get_content(url, hdr_more=hdr_more)
        if f is None:
            return False
        else:
            findres = f.find(key)
            if should_have_key == 'y':
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
    Search_Webs().search("你的名字")
    #Search_Webs().getConf()


