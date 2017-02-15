#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, threading
from Request import Request
import urllib, urllib2
from bs4 import BeautifulSoup
import traceback
import sys
import webbrowser

class Thread_Search(object):
    def __init__(self, key):
        self.sw = Request(key)
        self.data = self.sw.data
        self.hdr = self.sw.hdr
        self.res_urls = []

    def request(self, id):
        url = self.sw.data[id]['url']
        print('### thread %s is running... url = %s' % (threading.current_thread().name, url))

        res = self.sw.check1(id)
        if res is not None:
            webbrowser.open(res)
            self.res_urls.append(res)

        # hdr = self.hdr
        # if hdr_more == 'y':
        #     hdr['X-Requested-With'] = 'XMLHttpRequest'
        #
        # req = urllib2.Request(url, headers=hdr)
        # try:
        #     page = urllib2.urlopen(req)
        #     print('### thread %s url open end... url = %s' % (threading.current_thread().name, url))
        #     f = page.read()
        #     f = str(BeautifulSoup(f))
        #
        # except:
        #     print('### thread %s failed...\ntraceback: %s' % (threading.current_thread().name, str(traceback.format_exc())))
        #     # self.ret_content[url] = None
        #     return
        #
        #
        # # print key, f
        # findres = f.find(key)
        # # print 'findres', findres
        # if should_have_key == 'y' and findres != -1:
        #     # 应该有key而且真的找到了key
        #     self.res_urls.append(url)
        # if should_have_key == 'n' and findres == -1:
        #     # 不应该有key而且没有找到了key
        #     self.res_urls.append(url)

        print('### thread %s ended.' % threading.current_thread().name)




    def search(self, num):
        thread_pool = []
        for id in range(num):
            nowthread = threading.Thread(target=self.request, args=(id, ))
            thread_pool.append(nowthread)
            nowthread.start()
        for nowthread in thread_pool:
            nowthread.join()
        return self.res_urls


if __name__ == '__main__':
    Thread_Search('homeland').search(20)


