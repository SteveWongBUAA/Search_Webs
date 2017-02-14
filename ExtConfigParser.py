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
        res = []
        # s = 'urls'
        for s in sections:
            # o = '1'
            for o in self.options(s):
                v = self.get(s, o)
                #print len(res), int(o)
                if len(res) == int(o):
                    res.append({s: v})
                else:
                    res[int(o)][s] = v
        return res