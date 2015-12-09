#!/usr/bin/python3
# -*- coding: utf8 -*-

import urllib.parse
import urllib.request
import re
import os
from json import *


class qqmusic(object):

    def __init__(self):
        pass
    # key 搜索的关键字

    def search(self, key):
        url = "http://music.baidu.com/search?key=" + key
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
        req = urllib.request.Request(url)
        req.add_header('Referer', 'http://music.baidu.com/?from=new_mp3')
        req.add_header('User-Agent', user_agent)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        # 关键字搜索结果
        res = the_page.decode("utf8")
        # {"songItem":{"sid":121223583,"author":"<em>\u5f20\u6770<\/em>","sname":"\u5251\u5fc3","oid":121223583,"pay_type":"0","isJump":0}}
        # {&quot;sid&quot;:14944589,&quot;author&quot;:&quot;&lt;em&gt;\u5f20\u6770&lt;\/em&gt;&quot;,&quot;sname&quot;:&quot;\u9006\u6218&quot;,&quot;oid&quot;:14944589,&quot;pay_type&quot;:&quot;0&quot;,&quot;isJump&quot;:0}}
        pattern = re.compile(r'sid&quot;:\d+')
        s = pattern.findall(res)
        songlist = []
        for songid in s:
            songlist.append(str(songid).split(':')[1])
        # 返回关键字搜索结果最多20条  歌曲的 songId
        # print(songlist)
        return songlist

    def download(self, url):
        def Schedule(a, b, c):
            """
            a:已经下载的数据块
            b:数据块的大小
            c:远程文件的大小
                """
            per = 100.0 * a * b / c
            if per > 100:
                per = 100
            print('%.2f%%' % per)
        url = 'http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2'
        #local = url.split('/')[-1]
        local = os.path.join('/data/software', 'Python-2.7.5.tar.bz2')
        urllib.urlretrieve(url, local, Schedule)

    def getSongsData(self, songIds):
        url = "http://play.baidu.com/data/music/songlink"
        formdata = { "songIds" : ",".join(songIds)}

        data_encoded = urllib.parse.urlencode(formdata)
        # print data_encoded
        songList = urllib.request.urlopen(url,data_encoded.encode("utf-8"))
        songListJson = songList.read()
        # print(songListJson)
         #json 转字典
        song_dict = JSONDecoder().decode(songListJson.decode('utf-8'))
        # print(song_dict)
        song_data_dict = song_dict.get("data").get("songList")
        listdata = []
        for sond_data in song_data_dict:
        	#歌曲名称
            song_name = str(sond_data.get('songName'))
            #歌手
            song_artistName = str(sond_data.get('artistName'))
            #时长
            # song_time = round(int(sond_data.get('time'))/60,2)
            # song_time = sond_data.get('time')
            song_time = str(sond_data.get('time'))
            # tim.append(song_time)
            #下载地址
            song_link = str(sond_data.get('songLink'))
            # if song_name is None or \
            #                 song_artistName is None or \
            #                 song_time is None or \
            #                 song_link is None:
            #     continue
            listdata.append(song_name+"&"+song_artistName+"&"+song_time+"&"+song_link)
        # print(listdata)
        return listdata

if __name__ == '__main__':
    q = qqmusic()
    
    data = q.getSongsData(q.search("zhangjie"))
    print(data)
