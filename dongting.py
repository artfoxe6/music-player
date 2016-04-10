#!/usr/bin/python3
# -*- coding: utf8 -*-
import time
import sys
import os
import urllib.request
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,QSystemTrayIcon, QLabel,QMenu,QAction)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtCore import (Qt, QUrl)
from PyQt5.QtGui import ( QCursor, QIcon,QDesktopServices )


class DragLabel(QLabel):
    def __init__(self,window):
        super().__init__()
        self.window = window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_flag = True
            self.begin_position = event.globalPos() - self.window.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.drag_flag:
            self.window.move(QMouseEvent.globalPos() - self.begin_position)
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.drag_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

#音乐窗首页
class index(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowIcon(QIcon("dongting.png"))
        self.setWindowTitle("天天动听 For Linux")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(300,0,900, 600)
        self.setStyleSheet("QWidget{ background:#268FD3 }")
        #窗口初始化居中
        wh = QApplication.desktop().screenGeometry()
        self.screen_w , self.screen_h = wh.width() ,wh.height()
        self.move(int((self.screen_w-900)/2),int((self.screen_h-600)/2))
        # 程序初始化期间显示动听的logo
        Logo = QLabel(self)
        Logo.setGeometry(322,172,256,256)
        Logo.setStyleSheet("QLabel{ border-image:url(dongting.png) }")

        # 天天动听web页面
        self.web = QWebView(self)
        self.web.settings().setAttribute(QWebSettings.PluginsEnabled, True);
        self.web.setStyleSheet("QWidget{ background-color:white }")
        self.web.setGeometry(0, 0, 900, 600)
        # 应为web加载需要时间  所以暂时把web窗口隐藏
        self.web.hide()
        self.web.load(QUrl("http://www.dongting.com"))
        self.web.loadFinished.connect(self.webfinish)

        #左边顶部添加拖动效果
        dg = DragLabel(self)
        dg.setParent(self)
        dg.resize(330,100)
        dg.setStyleSheet("QLabel{background:transparent}")
        #右边顶部添加拖动效果
        dg = DragLabel(self)
        dg.setParent(self)
        dg.setGeometry(620,0,280,40)
        dg.setStyleSheet("QLabel{background:transparent}")

        # 关闭按钮
        self.minibtn = QPushButton("", self)
        self.minibtn.hide()
        self.minibtn.setGeometry(850, 5, 44, 34)
        self.minibtn.setStyleSheet(   "QPushButton{ border-image:url(back.png);background-color:#D21F70 }")
        self.minibtn.clicked.connect(self.hide)

        #设置托盘图标
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon('dongting.png'))
        self.trayIconMenu = QMenu(self)
        qss_tray = """QMenu{ width:100px;border:none;padding:5px;background:#fff; } QMenu::item{ background-color: transparent;width:70px;text-align:center;height:25px; margin:0px 0px;border-bottom:1px solid #EEE;padding-left:20px;color:#333 }  QMenu::item:selected{ color:red;border-bottom:1px solid pink;background:none; }"""
        self.trayIconMenu.setStyleSheet(qss_tray)
        showAction = QAction(QIcon('dongting.png'),u"显示", self,triggered=self.show)
        quitAction = QAction(u"关闭", self,triggered=self.close)
        self.trayIconMenu.addAction(showAction)
        self.trayIconMenu.addAction(quitAction)
        tray.setContextMenu(self.trayIconMenu)
        tray.show()
        tray.activated.connect(self.dbclick_tray)
        # 安利一下我的网站 
        self.author = QLabel(" <a style='color:#DDD;text-decoration:none;font-size:12px;'  href ='www.sylsong.com' >SYL-乐人馆</a>",self)
        self.author.hide()
        self.author.setStyleSheet("QLabel{ background:transparent }")
        self.author.move(830,580)
        self.author.setAlignment(Qt.AlignRight)
        self.author.linkActivated.connect(self.openurl)
    def openurl(self):
    	QDesktopServices.openUrl(QUrl("http://sylsong.com"))
    def dbclick_tray(self,event):
    	if event==QSystemTrayIcon.DoubleClick:
    		pass
    	else:
    		return False
    	if self.isVisible():
    		self.hide()
    	else:
    		self.show()
	# web加载完成  然后改了一些web里面的样式
    def webfinish(self):#8834AE
        self.web.show()
        self.minibtn.show()
        self.author.show()
        self.web.page().mainFrame().findFirstElement("#radiobgImg").takeFromDocument()
        self.web.page().mainFrame().findFirstElement("#userInfo").takeFromDocument()
        self.web.page().mainFrame().findFirstElement(".otherBar").takeFromDocument()
        self.web.page().mainFrame().findFirstElement("#footer").takeFromDocument()
        pos = self.web.page().mainFrame().findAllElements("#nav ul li")
        pos.at(5).takeFromDocument()
        pos.at(6).takeFromDocument()
        pos.at(7).takeFromDocument()
        pos.at(8).takeFromDocument()
        self.web.page().mainFrame().findFirstElement(".logo").setStyleProperty("text-align","center")
        self.web.page().mainFrame().findFirstElement(".logo").setStyleProperty("font-weight","bold")
        self.web.page().mainFrame().findFirstElement(".logo").setStyleProperty("font-size","20px")
        self.web.page().mainFrame().findFirstElement(".head").setStyleProperty("background-color","#D21F70")
        self.web.page().mainFrame().findFirstElement("body").setStyleProperty("background-color","#2C3233")
        pos = self.web.page().mainFrame().findAllElements("#nav ul li a")
        for x in range(pos.count()):
        	pos.at(x).setStyleProperty("color","white")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    music = index()
    music.show()
    sys.exit(app.exec_())
