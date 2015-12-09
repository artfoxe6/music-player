#!/usr/bin/python
#coding=utf-8
__author__ = 'zhm'
import urllib
import urllib2
import re
from json import *
#
SONG_TAG_URL = 'http://music.baidu.com/tag/%E7%BB%8F%E5%85%B8%E8%80%81%E6%AD%8C'
SONG_LINK_URL = 'http://play.baidu.com/data/music/songlink'
def getContent(url,pattern):
    try:
        f=urllib2.urlopen(url)
        result =  f.read();
        content = re.compile(pattern, re.DOTALL)
        style = content.search(result)
        if style:
            result = style.group(0)
            return result
        else:
            return None
    except Exception ,e:
        print e
 
if  __name__=="__main__":
    for i in range(0,1):
        #根据给出的百度音乐分类地址解析出songid
        result = getContent(SONG_TAG_URL+'?start='+unicode(i)+'&size=5&third_type=0','<ul>.*?</ul>')
        sids = []
        sidPattern = re.findall("&quot;sid&quot;:.*?,&quot;",result)
        for sid in sidPattern:
            sids.append(re.sub(',&quot;','',re.sub('&quot;sid&quot;:','',sid)))
        # print sids
        #将songid构造成post请求参数
        formdata = { "songIds" : ",".join(sids)}

        data_encoded = urllib.urlencode(formdata)
        # print data_encoded
        songList = urllib2.urlopen(SONG_LINK_URL,data_encoded)
        songListJson = songList.read()
        # print songListJson
         #json 转字典
        song_dict = JSONDecoder().decode(songListJson)
        #获取songList
        song_data_dict = song_dict.get("data").get("songList")
        for sond_data in song_data_dict:
            song_name = sond_data.get('songName')
            song_artistName = sond_data.get('artistName')
            song_format = sond_data.get('format')
            song_link = sond_data.get('songLink')
            if song_name is None or \
                            song_artistName is None or \
                            song_format is None or \
                            song_link is None:
                continue
            print song_link
            #下载方法此处就省略了。




            # http://play.baidu.com/data/music/songlink?songIds=490468,1533430