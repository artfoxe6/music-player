#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
	抓取歌手头像
"""

import sys
import os
import urllib.parse
import urllib.request
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot,QTimer
from PyQt5.QtGui import ( QCursor)


class Singer(QWidget):
    
    # def __init__(self,singer,music):
    def __init__(self,singer):
        super().__init__()
        # 窗口居于所有窗口的顶端 
        # self.setWindowFlags(Qt.WindowOverridesSystemGestures)
        #针对X11
        # self.setWindowFlags(Qt.X11BypassWindowManagerHint)
        self.singer = singer
        # self.music = music
        self.initUI()
        self.show()
        
    def initUI(self):      

        self.w= QWidget(self)
        self.setGeometry(300,100,1000,600)
        # l = QLabel("实用说明,搜索需要的图片，在搜索结果页面点击选择的图片即可设置。。双击此处退出",self)
        # l.move(0,0)
        self.web = QWebView(self)
        # self.web.loadFinished.connect(self.test)
        
        self.web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.web.page().linkClicked.connect(self.linkClicked)

        self.web.setGeometry(0, 0, 1000, 600)
        self.web.load(QUrl("http://image.baidu.com/"))
        frame = self.web.page().currentFrame()
        allimg = frame..findAllElements("")
        
    def test(self):
        print("jiazaijieshu")
        frame = self.web.page().currentFrame()
        searchinput = frame.findFirstElement('#kw')
        d = frame.findFirstElement('.img_area_container_box')
        d.removeAllChildren()
        searchinput.setAttribute("value",self.singer)
        # searchinput.setAttribute("readonly","readonly")
    def linkClicked(self,url):
    	print(url.toString())
    	return False
    	url = url.toString()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = Singer("")
    sys.exit(app.exec_())
