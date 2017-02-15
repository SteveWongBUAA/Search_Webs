#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reference: Peter Smit: http://stackoverflow.com/questions/335695/lists-in-configparser
Note that there are a few things to look out for when using this technique
New lines that are items should start with whitespace (e.g. a space or a tab)
All following lines that start with whitespace are considered to be part of the previous item. Also if it has an = sign or if it starts with a ; following the whitespace.
"""
from ConfigParser import ConfigParser


class ExtConfigParser(ConfigParser):
    def getlist(self, section, option):
        value = self.get(section, option)
        return list(filter(None, (x.strip() for x in value.splitlines())))

    def getDict(self, sections):
        """
        以sections[0]的id为准，sections中所有元素的信息，返回字典
        :param sections:
        :return:
        """
        res = {}
        for id in self.options(sections[0]):
            res[int(id)] = {}
        # print res
        for s in sections:
            # print s
            # s = 'url' ...
            for o in self.options(s):
                # print o
                # o = '0', '1', ...
                if int(o) in res:
                    res[int(o)][s] = self.get(s, o)
        return res



