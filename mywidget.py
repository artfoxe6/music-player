#!/usr/bin/python3
# -*- coding: utf8 -*-
import time
import sys
import os
import urllib.request
# from PyQt5 import QWebSettings
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,QMenu,QAction,QFileDialog,QMessageBox,QGraphicsColorizeEffect)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import (Qt, QUrl, pyqtSlot,QPropertyAnimation,QRect,pyqtSignal,QThread)
from PyQt5.QtGui import ( QCursor, QIcon,QLinearGradient,QLinearGradient,QFont,QPainter,QColor,QPen )
from PyQt5.QtNetwork import *
from baidumusic import bdmusic
import threading
from qss import *
from conf import conf

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
        self.web.settings().setAttribute(QWebSettings.PluginsEnabled, True);
        self.web.setStyleSheet("QWidget{ background-color:white }")
        self.web.setGeometry(0, 0, 600, 580)
        self.web.load(QUrl.fromLocalFile(os.path.abspath("web/index.html")))
        # self.web.page().setNetworkAccessManager(QNetworkAccessManager())
        # self.web.load(QUrl("http://web.kugou.com/"))
        self.web.loadFinished.connect(self.test)

        

        self.web.page().mainFrame().javaScriptWindowObjectCleared.connect( self.populateJavaScriptWindowObject)
        # 关闭按钮
        btn = QPushButton("", self)
        btn.setGeometry(550, 5, 44, 34)
        # btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet(  
            "QPushButton{ border-image:url(image/newimg/ic_common_title_bar_back_2.png) } QPushButton:hover{ border-image:url(image/newimg/ic_common_title_bar_back.png) } ")
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
    def test(self):
        print("oooo");
        self.web.page().mainFrame().findFirstElement("#userInfo").takeFromDocument()
        self.web.page().mainFrame().findFirstElement(".otherBar").takeFromDocument()
        
        self.web.page().mainFrame().findFirstElement("#footer").takeFromDocument()
        pos = self.web.page().mainFrame().findAllElements("#nav ul li")
        pos.at(5).takeFromDocument()
        pos.at(6).takeFromDocument()
        pos.at(7).takeFromDocument()
        pos.at(8).takeFromDocument()

# 自定义label，用于鼠标拖动主窗口
# 第二个参数就是要拖动的对象


class DragLabel(QLabel):
    setwinflag = pyqtSignal(int)
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
        # if self.window.pos().y() < 100:
        #     self.setwinflag.emit(2)
        # else:
        #     self.setwinflag.emit(1)


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
        self.setText(" S Y L - 让我们用心聆听彼此 ")
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
        # mask_linear_gradient.setColorAt(0.1, QColor(254, 113, 122))
        # mask_linear_gradient.setColorAt(0.3, QColor(224, 246, 242))
        mask_linear_gradient.setColorAt(0.1, QColor(14, 179, 255))
        mask_linear_gradient.setColorAt(0.5, QColor(114, 232, 255))
        # mask_linear_gradient.setColorAt(0.5, QColor(253, 147, 255))
        # mask_linear_gradient.setColorAt(0.7, QColor(1, 1, 1))
        # mask_linear_gradient.setColorAt(0.7, QColor(64, 2, 2))
        mask_linear_gradient.setColorAt(0.9, QColor(14, 179, 255))
        # mask_linear_gradient.setColorAt(1, QColor(0, 0, 0))

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
        index = self.findChild(QPushButton,'',Qt.FindDirectChildrenOnly).text()
        self.doubleclicked.emit(int(index))
    # 设置当前播放的label样式
    def currentplay(self,flag=0):
        if flag == 0:
            self.setStyleSheet("QLabel{ font-weight:100;color:#2D2D2D;background:transparent ;font-size:14px;padding-left:40px;} QLabel:hover{ color:#fff;background:#A448C4  }")
        else:
            self.setStyleSheet("QLabel{ font-weight:100;color:#555;background:#9BFFE0 ;font-size:14px;padding-left:40px;}   }")
    # def enterEvent(self,QMouseEvent):
    #     print("hover")
    # def mouseReleaseEvent(self,QMouseEvent):
    #     self.setStyleSheet("QLabel{ font-weight:100;color:#2D2D2D;background:red ;font-size:14px;padding-left:40px;} \
    #      QLabel:hover{ color:#fff;background:#A448C4  }")


class youjianWidget(QWidget):
    deletesong = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        
    def contextMenuEvent(self,event):
        # print(dir(event))
        rightMenu = QMenu(self)
        # rightMenu.setWindowOpacity(0.9); 
        # pos = QGraphicsColorizeEffect(rightMenu)
        # pos.setColor(QColor("red"))
        # pos.setStrength()
        # rightMenu.setGraphicsEffect(pos)
        

        # print(dir(rightMenu))
        rightMenu.setStyleSheet(qss_rightmenu) 
        loveAction = QAction(u"添加收藏", self, triggered=self.noexc)
        delAction = QAction(u"删除文件", self, triggered=self.deleteSongItem)    
        rateAction = QAction(u"我要打分", self, triggered=self.noexc)    
        cmAction = QAction(u"评论", self, triggered=self.noexc)  
        moreAction = QAction(u"歌曲详情", self, triggered=self.noexc)  
        moneyAction = QAction(u"打赏", self, triggered=self.noexc)  
        rightMenu.addAction(loveAction)
        rightMenu.addAction(delAction)
        rightMenu.addAction(rateAction)
        rightMenu.addAction(cmAction)
        rightMenu.addAction(moreAction)
        rightMenu.addAction(moneyAction)
        rightMenu.exec_(QCursor.pos())
    def noexc(self):
        pass
    def deleteSongItem(self):
        print(help(self.findChildren))
        listlabelitem = self.findChildren(QLabel,'songitem',Qt.FindChildrenRecursively)
        # 要删除的行  实际上要减一
        index = listlabelitem[0].findChild(QPushButton,'',Qt.FindDirectChildrenOnly).text()
        self.deletesong.emit(int(index))
        # 删除后随即刷新编号
        allitem = self.parent().findChildren(QLabel,'songitem',Qt.FindChildrenRecursively)
        for x in allitem:
            xbtn = x.findChild(QPushButton,'',Qt.FindDirectChildrenOnly)
            if int(xbtn.text()) > int(index):
                xbtn.setText(str(int(xbtn.text())-1))
        # removeItemWidget

# 弹出框 
class popWindow(QLabel):
    setwinflag = pyqtSignal(int)
    def __init__(self,func):
        super().__init__()
        # 窗口居于所有窗口的顶端 
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 窗口居于所有窗口的顶端 
        # self.setWindowFlags(Qt.WindowOverridesSystemGestures)
        # 窗口居于所有窗口的顶端  针对部分X11
        # self.setWindowFlags(Qt.X11BypassWindowManagerHint)
        self.resize(600,450)

        self.title = QLabel(self);
        self.title.setGeometry(0,0,600,40)
        self.title.setStyleSheet("QLabel{ background:#252C34 }")
        self.setStyleSheet("QWidget{ background:#fff }")
        closebtn = QPushButton(self.title)
        closebtn.setGeometry(550, 0, 44, 34)
        # btn.setCursor(QCursor(Qt.PointingHandCursor))
        closebtn.setStyleSheet(  
            "QPushButton{ background:#252C34;border-image:url(image/newimg/ic_common_title_bar_back_2.png) } QPushButton:hover{ border-image:url(image/newimg/ic_common_title_bar_back.png) } ")
        closebtn.clicked.connect(self.close)

        wh = QApplication.desktop().screenGeometry()
        screen_w , screen_h = wh.width() ,wh.height()
        self.move(int((screen_w-600)/2),int((screen_h-450)/2))
        if func == 1:
            self.setting()
        elif func == 2:
            self.other()
        self.show()

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
        # self.close()
    def setting(self):
        label = QLabel("设置音乐文件目录（确保目录有读写权限）",self)
        label.move(10,50)
        label.setStyleSheet("QLabel{ color:#252C34;font-size:18px; }")

        btn = QPushButton("选择",self)
        btn.move(10,80)
        btn.clicked.connect(self.selectdir) 
        btn.setStyleSheet("QPushButton{ border:1px solid #333;background:white;height:25px;width:70px;border-radius:2px;margin-left:5px;color:#333 } QPushButton:hover{ background:#DDD }")

        self.currentdir = QLabel(conf['mp3dir'],self)
        self.currentdir.move(100,85)

        tip = QLabel(" ● 所有设置下次生效",self)
        tip.move(5,10)
        tip.setStyleSheet("QLabel{ color:white;background:transparent;font-size:16px; }")

        label = QLabel("解决乱码(只针对Linux/Mac系统),开始后请耐心等待几秒",self)
        label.move(10,125)
        label.setStyleSheet("QLabel{ color:#252C34;font-size:18px; }")

        btn = QPushButton("执行",self)
        btn.move(10,160)
        btn.clicked.connect(self.luanma) 
        btn.setStyleSheet("QPushButton{ border:1px solid #333;background:white;height:25px;width:70px;border-radius:2px;margin-left:5px;color:#333 } QPushButton:hover{ background:#DDD }")

    def selectdir(self):
        # pos = QFileDialog(self)
        # pos.setWindowFlags(Qt.FramelessWindowHint)
        # 窗口居于所有窗口的顶端  针对部分X11
        # pos.setWindowFlags(Qt.X11BypassWindowManagerHint)
        fileinput = QFileDialog.getExistingDirectory(self,"选择你的音乐目录","/")
        
        if not fileinput:
            return False
        else: 
            f=open("conf/conf.py","w+")
            conf['mp3dir'] = fileinput
            f.write("conf = "+str(conf))
            f.close()
            self.currentdir.setText(fileinput)
    def other(self):
        print("other")
    def luanma(self):
        pos = QMessageBox(self)

        x = os.system('find . -iname "*.mp3" -execdir mid3iconv -e GBK {} \;')
        if x == 0:
            pos.information(self, "提示", "所有文件编码已刷新", QMessageBox.Yes)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # music = search()
    # music = popWindow(1)
    music = index()
    music.show()
    # print(dir(music))
    # app.exec_()
    sys.exit(app.exec_())
