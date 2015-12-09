#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtGui import QCursor, QIcon

#音乐窗首页
class index(QWidget):

    def __init__(self):
        super().__init__()
        # print(dir(QWebView))
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowIcon(QIcon("image/tray.png"))
        self.setWindowTitle("梦音乐")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("window")
        style = """
				#window{ background:grey }
		"""
        self.setStyleSheet(style)
        self.resize(600, 600)
        # 内嵌web网页
        self.web = QWebView(self)
        self.web.setGeometry(0, 0, 600, 580)
        self.web.load(QUrl.fromLocalFile(os.path.abspath("web/index.html")))
        # web.linkClicked.connect(self.close)
        self.web.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.populateJavaScriptWindowObject)
        # self.web.loadFinished.connect(self.pp)
        #
        btn = QPushButton("<", self)
        btn.setGeometry(540, 5, 60, 30)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet(
            "QPushButton{ border:none;color:white;background-color:black } ")
        btn.clicked.connect(self.myclose)
    # 接收一个字符串参数

    @pyqtSlot(str)
    def myfunc(self, str):
        frame = self.web.page().mainFrame()
        search = frame.findFirstElement(('#search'))
        print(search.evaluateJavaScript("this.value"))

    @pyqtSlot(str)
    def myfunc2(self, str):
        frame = self.web.page().mainFrame()
        search = frame.findFirstElement(('#search'))
        search.evaluateJavaScript("xin(this,'qt')")

    def populateJavaScriptWindowObject(self):
        self.web.page().mainFrame().addToJavaScriptWindowObject(
            'nihao', self)

    def pp(self):
        self.pg.evaluateJavaScript("hehe('你好吗')")
        print('ok')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_flag = True
            self.begin_position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.drag_flag:
            self.move(QMouseEvent.globalPos() - self.begin_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.drag_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def myclose(self):
        self.close()

# 自定义label，用于鼠标拖动主窗口
# 第二个参数就是要拖动的对象


class DragLabel(QLabel):

    def __init__(self, window):
        super().__init__()
        self.window = window

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_flag = True
            if hasattr(self.window, 'widget1'):
                self.begin_position2 = event.globalPos() - \
                    self.window.widget1.pos()
            self.begin_position = event.globalPos() - self.window.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.drag_flag:
            if hasattr(self.window, 'widget1'):
                self.window.widget1.move(
                    QMouseEvent.globalPos() - self.begin_position2)
                self.window.move(QMouseEvent.globalPos() - self.begin_position)
            else:
                self.window.move(QMouseEvent.globalPos() - self.begin_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.drag_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

#搜索列表类
class search(QWidget):

    def __init__(self):
        super().__init__()
        # print(dir(QWebView))
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowIcon(QIcon("image/tray.png"))
        self.setWindowTitle("梦音乐")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("window")
        style = """
				#window{ background:grey }
		"""
        self.setStyleSheet(style)
        self.resize(600, 600)
        top = QWidget(self)
        top.setGeometry(0,0,600,50)
        top.setStyleSheet("QWidget{ background:none ;font-size:14px;color:green;line-height:50px;height:50px;}")
        author = " 搜索结果来自于QQ音乐  作者-许嵩 "
        ql = QLabel(author,top)
        ql.setGeometry(0,20,600,25)
        ql.setAlignment(Qt.AlignHCenter)
        ql.setStyleSheet("QLabel{ background:none ;font-size:14px;color:white;height:30px;}")
        # 内嵌web网页
        self.web = QWebView(self)
        self.web.setGeometry(0, 50, 600, 550)
        self.web.load(QUrl.fromLocalFile(os.path.abspath("web/list.html")))
        # web.linkClicked.connect(self.close)
        self.web.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.populateJavaScriptWindowObject)
        # self.web.loadFinished.connect(self.pp)
        #
        btn = QPushButton("x", self)
        btn.setGeometry(540, 5, 60, 30)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet(
            "QPushButton{ border:none;color:white;background-color:black } ")
        btn.clicked.connect(self.myclose)
    # 接收一个字符串参数

    @pyqtSlot(str)
    def myfunc(self, str):
        frame = self.web.page().mainFrame()
        search = frame.findFirstElement(('#search'))
        print(search.evaluateJavaScript("this.value"))

    @pyqtSlot(str)
    def myfunc2(self, str):
        frame = self.web.page().mainFrame()
        search = frame.findFirstElement(('#search'))
        search.evaluateJavaScript("xin(this,'qt')")

    def populateJavaScriptWindowObject(self):
        self.web.page().mainFrame().addToJavaScriptWindowObject(
            'nihao', self)

    def pp(self):
        self.pg.evaluateJavaScript("hehe('你好吗')")
        print('ok')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_flag = True
            self.begin_position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.drag_flag:
            self.move(QMouseEvent.globalPos() - self.begin_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.drag_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def myclose(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    music = search()
    # music = index()
    # app.exec_()
    sys.exit(app.exec_())
