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
        k = {'key': key}
        url = "http://www.kuwo.cn/mingxing/"+key+"/pic.htm"
        # url = "http://music.baidu.com/search?" + urllib.parse.urlencode(k)

        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
        req = urllib.request.Request(url)
        req.add_header('Referer', 'http://music.baidu.com/?from=new_mp3')
        req.add_header('User-Agent', user_agent)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        # 关键字搜索结果
        res = the_page.decode("utf8")
        print(res) 
        # {"songItem":{"sid":121223583,"author":"<em>\u5f20\u6770<\/em>","sname":"\u5251\u5fc3","oid":121223583,"pay_type":"0","isJump":0}}
        # {&quot;sid&quot;:14944589,&quot;author&quot;:&quot;&lt;em&gt;\u5f20\u6770&lt;\/em&gt;&quot;,&quot;sname&quot;:&quot;\u9006\u6218&quot;,&quot;oid&quot;:14944589,&quot;pay_type&quot;:&quot;0&quot;,&quot;isJump&quot;:0}}
        # pattern = re.compile(r'sid&quot;:\d+')
        # s = pattern.findall(res)
        # songlist = []
        # for songid in s:
        #     songlist.append(str(songid).split(':')[1])
        # # 返回关键字搜索结果最多20条  歌曲的 songId
        # # print(songlist)
        # return songlist


if __name__ == '__main__':
    q = bdmusic()
    data = q.search("张杰".encode('utf-8'))
    # key = u"张杰"
    # print(key)
    # print(data)
