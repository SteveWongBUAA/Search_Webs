#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import webbrowser
import ExtConfigParser
import traceback
from bs4 import BeautifulSoup
import sys
import json


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
        self.data = cf.getDict(['url', 'res_kw', 'method', 'should_have_key', 'hdr_more', 'encoding',
                                'post_key', 'more_formdata', 'must_fully_match'])
        # print self.data[12]
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

            if self.data[id].has_key('more_formdata'):
                self.data[id]['more_formdata'] = json.loads(self.data[id]['more_formdata'])

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
            post_data = {self.data[id]['post_key']: self.raw_key}
            if self.data[id].has_key('more_formdata'):
                # merge
                post_data = dict(self.data[id]['more_formdata'], **post_data)
            post_data = urllib.urlencode(post_data)


            req = urllib2.Request(self.data[id]['url'], headers=hdr, data=post_data)
        else:
            req = urllib2.Request(self.data[id]['url'], headers=hdr)

        try:
            page = urllib2.urlopen(req, timeout=5)
            f = page.read()
            bs = BeautifulSoup(f)
            # webbrowser.open(page.geturl())
            return page.geturl(), str(bs)

        except:
            print id, traceback.format_exc()
            return None

        # input key is unicode should encode
        #     has_res = self.has_res(url, hdr_more=one['hdr_more'], should_have_key=one['should_have_key'], key=one['key'], )
        #     if has_res:
        #         webbrowser.open(url)
        #         urls.append(url)
        # return urls

    def check1(self, id):
        """
        check 1 url, if ok, return the final url(maybe redirected), else return None
        :param id:
        :return:
        """
        res_url, f = self.request1(id)
        print id, 'res_url', res_url
        # print f
        if f is None:
            print id, '# fail f is none'
            return None
        # 如果这个网站需要完全匹配关键字 但是 并不是完全匹配(没找到)(还要过滤掉第一个在搜索框里匹配的)，就返回None
        if self.data[id]['must_fully_match'] == 'y' and f.find(self.raw_key, f.find(self.raw_key)+1) == -1:
            print id, '# fail must fully match but no'
            return None

        findres = f.find(self.data[id]['res_kw'])
        if self.data[id]['should_have_key'] == 'y':
            # 应该有key而且真的找到了key
            if findres != -1:
                return res_url
            else:
                print id, '# fail should have key but no'
                return None
        else:
            # 不应该有key但是找到了key
            if findres != -1:
                print id, '# fail should not have key but yes'
                return None
            else:
                return res_url


    def test_reqs(self, id, post_data):
        import requests
        r = requests.post(self.data[id]['url'], post_data)
        print r.history
        print r.headers
        print r.is_redirect
        print r.links
        print r.text


if __name__ == '__main__':
    # Search_Webs().search("homeland")
    # Search_Webs().search("xzchkjq")
    # Search_Webs().search("你的名字")
    # rqt = Request('你的名字')
    rqt = Request('你的名字')
    # print rqt.data[12]
    for i in range(0, 20):
        try:
            data = rqt.data[i]
            print i, data['url']
            res = rqt.check1(i)
            print res
            if res is not None:
                # print 'res', res
                webbrowser.open(res)
        except:
            print traceback.format_exc()


