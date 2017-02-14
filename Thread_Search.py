#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, threading
from Search_Webs import Search_Webs
import urllib, urllib2
from bs4 import BeautifulSoup
import traceback
import sys


class Thread_Search(object):
    def __init__(self):
        self.sw = Search_Webs()
        self.data = self.sw.data
        self.hdr = self.sw.hdr
        self.res_urls = []

    def request(self, url, hdr_more, key, should_have_key):
        print('### thread %s is running... url = %s' % (threading.current_thread().name, url))
        hdr = self.hdr
        if hdr_more == 'y':
            hdr['X-Requested-With'] = 'XMLHttpRequest'

        req = urllib2.Request(url, headers=hdr)
        try:
            page = urllib2.urlopen(req)
            f = page.read()
            f = str(BeautifulSoup(f))

        except:
            print('### thread %s failed...\ntraceback: %s' % (threading.current_thread().name, str(traceback.format_exc())))
            # self.ret_content[url] = None
            return


        # print key, f
        findres = f.find(key)
        # print 'findres', findres
        if should_have_key == 'y' and findres != -1:
            # 应该有key而且真的找到了key
            self.res_urls.append(url)
        if should_have_key == 'n' and findres == -1:
            # 不应该有key而且没有找到了key
            self.res_urls.append(url)

        print('### thread %s ended.' % threading.current_thread().name)




    def search(self, key):
        thread_pool = []
        for id in self.data:
            if type(key) == unicode:
                key_encode = key.encode(encoding=id['encoding'])
            elif type(key) == str:
                key_encode = key.decode(sys.stdin.encoding).encode(id['encoding'])
            else:
                continue
            key_quote = urllib.quote(key_encode)
            if id['method'] == 'concat':
                url = id['url'].replace('{#concat#}', key_quote)
            elif id['method'] == 'append':
                url = id['url'] + key_quote
            else:
                continue
            nowthread = threading.Thread(target=self.request, args=(url, id['hdr_more'], id['key'], id['should_have_key']))
            thread_pool.append(nowthread)
            nowthread.start()
        for nowthread in thread_pool:
            nowthread.join()
        return self.res_urls


if __name__ == '__main__':
    Thread_Search().search('homeland')


