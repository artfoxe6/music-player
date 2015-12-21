#!/usr/bin/python3
# -*- coding: utf8 -*-
import time
import sys
import os
import urllib.request
from conf.conf import conf
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtGui import QCursor, QIcon
from baidumusic import bdmusic
import threading

#音乐窗首页
class index(QWidget):

    def __init__(self):
        super().__init__()
        self.download_id = threading.local()
        self.download_pro = {}
        self.initUI()
        self.show()

    def initUI(self):
        # self.setWindowIcon(QIcon("image/tray.png"))
        # self.setWindowTitle("梦音乐")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("window")
        self.setGeometry(300,0,600, 600)
  #       style = """
		# 		#window{ background:red }
		# """
  #       self.setStyleSheet(style)
        
        # 内嵌web网页
        ql = QLabel(self)
        ql.setGeometry(0,580,600,20)
        ql.setStyleSheet("QLabel{ background:grey }")
        self.web = QWebView(self)
        self.web.setGeometry(0, 0, 600, 580)
        self.web.load(QUrl.fromLocalFile(os.path.abspath("web/index.html")))
        
        # web.linkClicked.connect(self.close)
        self.web.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.populateJavaScriptWindowObject)
        # self.web.loadFinished.connect(self.pp)
        #
        btn = QPushButton("关闭", self)
        btn.setGeometry(540, 5, 60, 30)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet(  
            "QPushButton{ border:none;color:white;background-color:black } ")
        btn.clicked.connect(self.myclose)
    # 接收一个字符串参数

    @pyqtSlot(str)
    def qsearch(self, strs):
        
        b = bdmusic()
        self.songlist = b.main(strs) 
        self.web.setUrl(QUrl.fromLocalFile(os.path.abspath("web/list.html")))

    @pyqtSlot()
    def qtnotify(self):
        self.backbtn = QPushButton("back", self)
        self.backbtn.setGeometry(540, 5, 60, 30)
        self.backbtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.backbtn.setStyleSheet(  
            "QPushButton{ border:none;color:white;background-color:black } ")
        self.backbtn.clicked.connect(self.goback)
        self.backbtn.show()

        frame = self.web.page().currentFrame()
        # print(self.songlist)
        s = "#&#".join(self.songlist)
        # 把字符串里面的单引号转意  否则会导致js函数错误
        s = s.replace("'","\\'")
        frame.evaluateJavaScript("insertlist('"+s+"')")

    def download_music(self, item,url,lrc,name,author):
        self.download_id.item = item
        # print("ssss")
        # frame = self.web.page().currentFrame()
        # frame.evaluateJavaScript("setpro('ssss')")
        urllib.request.urlretrieve(url,conf['mp3dir']+name+"-"+author+".mp3",self.schedule)
        # print(item,url,lrc,name)
        
        # print(threading.current_thread())
        # print(self.download_id.item)
        
    @pyqtSlot(str,str,str,str,str)
    def qtdown(self, item,url,lrc,name,author):
        # print(item,url,lrc,name)
        t = threading.Thread(target=self.download_music,args=(item,url,lrc,name,author))
        # p = Process(target=self.download_music, args=(item,url,lrc,name,author))
        t.start()
        
    def schedule(self,a,b,c):
        per = 100.0 * a * b / c
        if per > 100 :
            per = 100
        # print('%.2f%%' % per)
        per = round(per, 2);
        self.download_pro[self.download_id.item] = per
        # frame = self.web.page().currentFrame()
        # s = str(per)+"&"+self.download_id.item
        # frame.evaluateJavaScript("setpro('"+s+"')")
        # print(s)
    @pyqtSlot()
    def qtjindu(self):
        s = str(self.download_pro)
        # print(s)
        frame = self.web.page().currentFrame()
        # s = str(item)+"&"+str(jindu);
        s = s.replace("'","\\'")
        frame.evaluateJavaScript("getjindu('"+s+"')")

    def populateJavaScriptWindowObject(self):
        self.web.page().mainFrame().addToJavaScriptWindowObject(
            'Qtsearch', self)

    def myclose(self):
        # self.close()
        # print(dir(self))
        self.destroy()
        self.parentWidget().resize(300,600)
    def goback(self):
         # print(dir(self.web))
         self.backbtn.close()
         self.web.back()
         self.download_pro = {}
         # print("oooo")

# 自定义label，用于鼠标拖动主窗口
# 第二个参数就是要拖动的对象


class DragLabel(QLabel):

    def __init__(self, window):
        super().__init__()
        self.window = window

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_flag = True
            # if hasattr(self.window, 'widget1'):
            #     self.begin_position2 = event.globalPos() - \
            #         self.window.widget1.pos()
            self.begin_position = event.globalPos() - self.window.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.drag_flag:
            # if hasattr(self.window, 'widget1'):
            #     self.window.widget1.move(
            #         QMouseEvent.globalPos() - self.begin_position2)
            #     self.window.move(QMouseEvent.globalPos() - self.begin_position)
            # else:
            self.window.move(QMouseEvent.globalPos() - self.begin_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.drag_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # music = search()
    music = index()
    # app.exec_()
    sys.exit(app.exec_())
