#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
	抓取歌手头像
"""

import urllib.parse
import urllib.request
import re
import os
from json import *

class bdmusic(object):
    def __init__(self):
        pass
    def search(self, key):
        k = {'k': key}
        url = "http://www.kuwo.cn/mingxing/"+urllib.parse.urlencode(k)[2:]+"/pic.htm"
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
        req = urllib.request.Request(url)
        req.add_header('Referer', 'http://music.baidu.com/?from=new_mp3')
        req.add_header('User-Agent', user_agent)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        # 关键字搜索结果
        res = the_page.decode("utf8")
        pattern = re.compile(r'lazy_src="(.*)" onerror')
        s = pattern.findall(res)
        print(s[:20])


if __name__ == '__main__':
    q = bdmusic()
    data = q.search("张杰")
    # key = u"张杰"
    # print(key)
    # print(data)
