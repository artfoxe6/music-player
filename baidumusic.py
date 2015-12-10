#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
	播放器的在线搜索下载功能，是从第三方音乐平台抓取的，
	众所周知，目前音乐平台页面更新较快，今天还可以正常使用，可能下个月它页面就改版了，搜索
	就用不了了，所以我把搜索模块作为一个插件使用，可自动更新，可添加其他下载插件支持
	，当软件搜索功能失效后，可到设置里面更新当前插件（当然这个插件需要有人维护），
	或者选择其他开发者提供的插件。

	开发插件注意事项：
		软件的逻辑是这样的： 用户搜索一个关键字，然后软件就会去调用当前用户设定的插件的main方法
		main方法接收一个搜索关键字，返回一个歌曲列表，过程没有任何要求。
		歌曲列表格式：
		歌名 + "&" + 歌手 + "&" + 时长 + "&" + 下载地址
		例子： [倩女幽魂&张国荣&252&http://xx.com/xxxxxx,水手&郑智化&272&http://xx.com/xxxxxx]

	* 请使用python3


"""

import urllib.parse
import urllib.request
import re
import os
from json import *


class bdmusic(object):

    def __init__(self):
        pass

    """
    	通过搜索关键字key 返回由歌曲songid组成的列表
    	注意，songid不是固定的，比如qq音乐是mid，总之这些细节都不重要，
    	最重要的是返回结果，过程不必按照此模块形式，可能其他音乐平台更复杂，过程肯定要多很多
    	如果你要扩展其他搜索支持，请看文件顶部详细说明
    """

    def search(self, key):
        k = {'key': key}
        url = "http://music.baidu.com/search?" + urllib.parse.urlencode(k)

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

    # def download(self, url):
    #     def Schedule(a, b, c):
    #         """
    #         a:已经下载的数据块
    #         b:数据块的大小
    #         c:远程文件的大小
    #             """
    #         per = 100.0 * a * b / c
    #         if per > 100:
    #             per = 100
    #         print('%.2f%%' % per)
    #     url = 'http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2'
    #     local = os.path.join('/data/software', 'Python-2.7.5.tar.bz2')
    #     urllib.urlretrieve(url, local, Schedule)

    """
		通过songid列表获取歌曲的相关信息列表，包括歌曲名，歌手，下载地址，时长，等等
		
    """

    def getSongsData(self, songIds):
        url = "http://play.baidu.com/data/music/songlink"
        formdata = {"songIds": ",".join(songIds)}

        data_encoded = urllib.parse.urlencode(formdata)
        # print data_encoded
        songList = urllib.request.urlopen(url, data_encoded.encode("utf-8"))
        songListJson = songList.read()
        # print(songListJson)
         # json 转字典
        song_dict = JSONDecoder().decode(songListJson.decode('utf-8'))
        print(song_dict)
        song_data_dict = song_dict.get("data").get("songList")
        listdata = []
        for sond_data in song_data_dict:
            # 歌曲名称
            song_name = sond_data.get('songName')
            #歌词
            song_lrc = sond_data.get('lrcLink')
            # 歌手
            song_artistName = sond_data.get('artistName')
            # 时长
            song_time = sond_data.get('time')
            # 下载地址
            song_link = sond_data.get('songLink')
            # print(sond_data)
            if song_name is None or \
                    song_artistName is None or \
                    song_time is None or \
                    song_link is None:
                continue
            listdata.append(
                song_name + "&"+ song_lrc +"&"+ song_artistName + "&" + str(song_time) + "&" + song_link)
        # print(listdata)
        return listdata

    def main(self, keyworld):
        return self.getSongsData(self.search("tinghai"))

if __name__ == '__main__':
    q = bdmusic()

    data = q.getSongsData(q.search("流年"))
    # print(len(data))
    # print(data)
