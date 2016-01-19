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
from PyQt5.QtCore import (Qt, QUrl, pyqtSlot,QPropertyAnimation,QRect,pyqtSignal,QThread)
from PyQt5.QtGui import ( QCursor, QIcon,QLinearGradient,QLinearGradient,QFont,QPainter,QColor,QPen )
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
        self.setWindowIcon(QIcon("image/tray.png"))
        self.setWindowTitle("梦音乐")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("window")
        self.setGeometry(300,0,600, 600)
        # 底部
        ql = QLabel(self)
        ql.setGeometry(0,580,600,20)
        ql.setStyleSheet("QLabel{ background:#2D2D2D }")

        # 内嵌web网页
        self.web = QWebView(self)
        self.web.setGeometry(0, 0, 600, 580)
        self.web.load(QUrl.fromLocalFile(os.path.abspath("web/index.html")))
        
        self.web.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.populateJavaScriptWindowObject)
        # 关闭按钮
        btn = QPushButton("关闭", self)
        btn.setGeometry(540, 5, 60, 30)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet(  
            "QPushButton{ border:none;color:white;background-color:black } ")
        btn.clicked.connect(self.myclose)
    # 接收一个字符串参数

    @pyqtSlot(str)
    def qsearch(self, strs):
        self.keyworld = strs
        self.web.setUrl(QUrl.fromLocalFile(os.path.abspath("web/list.html")))
    @pyqtSlot()
    def qtnotify(self):

        b = bdmusic()
        self.songlist = b.main(self.keyworld) 

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

        urllib.request.urlretrieve(url,conf['mp3dir']+name+"-"+author+".mp3",self.schedule)

    @pyqtSlot(str,str,str,str,str)
    def qtdown(self,item,url,lrc,name,author):
        # print(item,url,lrc,name)
        # t = threading.Thread(target=self.download_music,args=(item,url,lrc,name,author))
        # p = Process(target=self.download_music, args=(item,url,lrc,name,author))
        # t.start()
        d = DownThread()
        # d.run(item,url,lrc,name,author)
        d.start()
        d.begindown.connect(self.setprocess)
    # 更新下载进度
    def setprocess(self):
        # print(per)
        print("oooookkkkkkkk")
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
            'Qtindex', self)

    def myclose(self):
        try:
            self.parentWidget().resize(300,600)
        except Exception:
            print("no parent")
        self.close()
        
    def goback(self):
         self.backbtn.close()
         self.web.back()
         self.download_pro = {}

# 自定义label，用于鼠标拖动主窗口
# 第二个参数就是要拖动的对象


class DragLabel(QLabel):

    def __init__(self,window):
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


class DLabel(QLabel):

    def __init__(self,window = None):
        super().__init__()
        # 窗口居于所有窗口的顶端 
        self.setWindowFlags(Qt.WindowOverridesSystemGestures)
        #针对X11
        self.setWindowFlags(Qt.X11BypassWindowManagerHint)
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint);
        self.setAttribute(Qt.WA_TranslucentBackground);
        wh = QApplication.desktop().screenGeometry()
        self.screen_w , self.screen_h = wh.width() ,wh.height()
        self.setGeometry(int((self.screen_w-900)/2),int((self.screen_h-120)),900,60)
        # self.resize(800,60)
        self.setStyleSheet("QLabel{ border:2px solid red }")
        # btn = QPushButton("close",self.q)
        # btn.clicked.connect(self.q.close)
        self.setText("")
        self.show()
        # self.setText("简易音乐播放器")

        
    def paintEvent(self,e):
        # print(e)

        linear_gradient = QLinearGradient()
        linear_gradient.setStart(0, 10) #填充的起点坐标
        linear_gradient.setFinalStop(0, 40) #填充的终点坐标
        #第一个参数终点坐标，相对于我们上面的区域而言，按照比例进行计算
        linear_gradient.setColorAt(0.1, QColor(14, 179, 255))
        linear_gradient.setColorAt(0.5, QColor(114, 232, 255))
        linear_gradient.setColorAt(0.9, QColor(14, 179, 255))

        mask_linear_gradient = QLinearGradient()
        #遮罩的线性渐变填充
        mask_linear_gradient.setStart(0, 10)
        mask_linear_gradient.setFinalStop(0, 40)
        mask_linear_gradient.setColorAt(0.1, QColor(255, 190, 190))
        # mask_linear_gradient.setColorAt(0.3, QColor(1, 1, 1))
        mask_linear_gradient.setColorAt(0.3, QColor(253, 147, 255))
        # mask_linear_gradient.setColorAt(0.7, QColor(1, 1, 1))
        mask_linear_gradient.setColorAt(0.9, QColor(231, 88, 210))

        # print(e)
        
        # 设置字体
        font = QFont()
        font.setFamily("文泉驿等宽微米黑")
        font.setBold(True)
        font.setPointSize(30)
        # self.q.setFont(font)
        p = QPainter(self)
        p.setFont(font);

        # p.setPen(QColor(0, 0, 0, 200));
        # p.drawText(1, 1, 700, 60, Qt.AlignHCenter, "梦音乐梦音乐梦音乐"); #//左对齐

        # // 再在上面绘制渐变文字
        # p.setPen(QPen(linear_gradient, 0));
        # p.drawText(0, 0, 800, 60, Qt.AlignHCenter, "梦音乐梦音乐梦音乐");
        # SYL - 让我们用声音聆听彼此～
        # if not self.s:
            # self.s = str("SYL - 让我们用声音聆听彼此～")
        # // 设置歌词遮罩
        p.setPen(QPen(mask_linear_gradient, 0));
        p.drawText(0, 0, 900, 60, Qt.AlignHCenter, self.text());


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_flag = True
            # if hasattr(self.window, 'widget1'):
            #     self.begin_position2 = event.globalPos() - \
            #         self.window.widget1.pos()
            self.begin_position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.drag_flag:
            # if hasattr(self.window, 'widget1'):
            #     self.window.widget1.move(
            #         QMouseEvent.globalPos() - self.begin_position2)
            #     self.window.move(QMouseEvent.globalPos() - self.begin_position)
            # else:
            self.move(QMouseEvent.globalPos() - self.begin_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.drag_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # def mouseDoubleClickEvent(self,e):
        # self.setVisible(False)


# 线程包装
class DownThread(QThread):
    # 多线程之间使用信号相互通信
    begindown = pyqtSignal()
    # self.trigger.emit()  # 循环完毕后发出信号
    def __int__(self):
        super(DownThread, self).__init__()
        

    def run(self):
        # self,item,url,lrc,name,author
        print("run")
        # self.begindown.emit()
        # urllib.request.urlretrieve(url,conf['mp3dir']+name+"-"+author+".mp3",self.schedule)
        
    def schedule(self,a,b,c):
        per = 100.0 * a * b / c
        if per > 100 :
            per = 100
            print("done !")
        # print('%.2f%%' % per)

        # per = round(per, 2);
        # print(per)
        # if per > 50:
            # self.trigger.emit(str(per))
        # self.download_pro[self.download_id.item] = per
        # frame = self.web.page().currentFrame()
        # s = str(per)+"&"+self.download_id.item
        # frame.evaluateJavaScript("setpro('"+s+"')")
        # print(s)


class listlabel(QLabel):
    doubleclicked = pyqtSignal(int)
    def __init__(self):
        super().__init__()
    def mouseDoubleClickEvent(self, QMouseEvent):
        index = self.parent().findChild(QPushButton,'',Qt.FindDirectChildrenOnly).text()
        self.doubleclicked.emit(int(index))
    # def enterEvent(self,QMouseEvent):
    #     print("hover")



# if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # # music = search()
    # music = index()
    # music.show()
    # # app.exec_()
    # sys.exit(app.exec_())
