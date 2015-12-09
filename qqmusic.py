#!/usr/bin/python3
# -*- coding: utf8 -*-

import urllib.parse
import urllib.request


class qqmusic(object):
	def __init__(self):
		pass
	def search(self,name):
		url = "http://s.music.qq.com/fcgi-bin/yqq_search_v8_cp?"
		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
		values = {
			'p':'1',
			'catZhida':'1',
			'lossless':'0',
			't':'100',
			'aggr':'0',
			'searchid':'24660856179109491',
			'remoteplace':'txt.yqqlist.top',
			'utf8':'1',
			'tab':'all|'+name,
			'w':name
		}
		url = url+urllib.parse.urlencode(values)
		req = urllib.request.Request(url)
		req.add_header('Referer', 'http://y.qq.com/')
		req.add_header('User-Agent', user_agent)

		response = urllib.request.urlopen(req)
		the_page = response.read()

		print(the_page.decode("utf8"))

if __name__ == '__main__':
	q = qqmusic()
	q.search("zhangjie")