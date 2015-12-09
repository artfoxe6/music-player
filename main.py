#!/usr/bin/python3
# -*- coding: utf8 -*-


import sys,ctypes
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QProgressBar,QListWidget,
	QSystemTrayIcon,QMenu,QAction,QGraphicsDropShadowEffect,QGraphicsBlurEffect,QListWidgetItem)
from PyQt5.QtCore import Qt,QSize,QUrl,QThread
from PyQt5.QtGui import QCursor,QIcon,QBrush,QColor,QDesktopServices 
from conf.conf import conf
from mywidget import *


# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
class Music(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QIcon("image/tray.png"))
		self.setWindowTitle("梦音乐")
		shadow_effect = QGraphicsDropShadowEffect()
		shadow_effect.setOffset(-50, -50)
		# shadow_effect.setColor(Qt.green)
		shadow_effect.setBlurRadius(80)
		self.setGraphicsEffect(shadow_effect)
		self.initUI()
		self.show()

	def initUI(self):
		self.mianUI()
		
	def mianUI(self):
		#设置无边框
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.resize(300,600)
		self.setObjectName("mainBox")
		self.setStyleSheet("#mainBox{ background-color:white; } QWidget{ border:none }")
		#当前播放歌曲的歌手图片
		songer_img = DragLabel(self)
		songer_img.setParent(self)
		songer_img.resize(300,200)
		# songer_img.setGraphicsEffect(QGraphicsBlurEffect())
		songer_img.setObjectName("songer_img")
		# songer_img.setStyleSheet("#songer_img{ background:none;}")
		#歌曲专辑图片
		picture = QLabel(songer_img)
		# picture.setParent(self)
		picture.resize(300,200)
		picture.setGraphicsEffect(QGraphicsBlurEffect())
		# picture.setObjectName("songer_img")
		picture.setStyleSheet("QLabel{ background:#9B0069;border-image:url(image/caijianya.jpg)}")
		#顶部工具栏（最小化，缩小到托盘，设置）
		top_tools = QWidget(songer_img)
		top_tools.setGeometry(0,0,300,20)
		top_tools.setObjectName("top_tools")
		top_tools.setStyleSheet("QWidget{ background-color:transparent; }")
		#关闭程序按钮
		btn = QPushButton("x",top_tools)
		btn.setGeometry(260,0,40,20)
		btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn.setStyleSheet("QPushButton{ border:none;color:white;background-color:black } ")
		btn.clicked.connect(self.myclose)
		#设置播放按钮
		btn = QPushButton("",songer_img)
		btn.setGeometry(126,120,48,48)
		btn.setStyleSheet("QPushButton{ border-image:url(image/play11.png);border:none }")
		btn.clicked.connect(self.close)
		btn = QPushButton("",songer_img)
		btn.setGeometry(198,134,24,24)
		btn.setStyleSheet("QPushButton{ border-image:url(image/next11.png);border:none }")
		btn.clicked.connect(self.close)
		btn = QPushButton("",songer_img)
		btn.setGeometry(78,134,24,24)
		btn.setStyleSheet("QPushButton{ border-image:url(image/pre11.png);border:none }")
		btn.clicked.connect(self.close)
		progressBar = QProgressBar(self)
		progressBar.setGeometry(100,178,100,5)
		progressBar.setValue(60)
		progressBar.setTextVisible(False)
		progressBar.setStyleSheet("QProgressBar{ background:transparent;border:none;border-radius:2px; } QProgressBar::chunk { background:transparent; border-radius:2px } QProgressBar:hover{background:#B4FFA3;} QProgressBar::chunk:hover{ background:pink }")
		#当前歌曲名
		label = QLabel("红色高跟鞋 - 蔡健雅",songer_img)
		# print(dir(label))
		label.setGeometry(0,50,300,40)
		label.setAlignment(Qt.AlignHCenter)
		label.setStyleSheet("QLabel{ color:white ;font-weight:100;font-size:16px;}")
		#歌曲进度条
		progressBar = QProgressBar(self) 
		progressBar.setGeometry(0,200,300,10)
		progressBar.setValue(30)
		progressBar.setTextVisible(False)
		progressBar.setStyleSheet("QProgressBar{ background:pink;border:none } QProgressBar::chunk { background-color: #B4FFA3;  }")
		#歌曲列表
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 210, 300,370)
		listWgt.setStyleSheet("QWidget{ background:white }")
		#播放列表前面补空
		blank = QWidget(self)
		blank.setGeometry(0, 210, 2,370)
		blank.setStyleSheet("QWidget{ background:#ddd }")
		#列表
		songList = QListWidget(listWgt)
		songList.setGeometry(2,0,258,370)   
		songList.setStyleSheet("QListWidget{ background:white;font-size:14px;border:none;margin-left:10px;} \
		QListWidget::item{ color:#789EFF ;height:40px;}  QListWidget::item:hover{background:#E8FFE3} QListWidget::item:selected{background:#E8FFE3;} QScrollBar:vertical{width:5px;background:white; margin:0px,0px,0px,0px;padding-top:9px;  padding-bottom:9px;}\
QScrollBar::handle:vertical{width:5px;background:#A6D8F8; border-radius:2px;  }\
QScrollBar::handle:vertical:hover{width:5px;background:grey;border-radius:2px;}\
QScrollBar::add-line:vertical {height:9px;width:5px;background:white;subcontrol-position:bottom;}\
QScrollBar::sub-line:vertical {height:9px;width:5px;background:white;subcontrol-position:top;}\
QScrollBar::add-line:vertical:hover {height:9px;width:5px;background:white;subcontrol-position:bottom;}\
QScrollBar::sub-line:vertical:hover{ height:9px;width:5px; background:white;subcontrol-position:top; }\
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical {background:white;border-radius:4px;} ")
		for x in range(10):
			item = QListWidgetItem(" %02d 越来越不懂爱 - 蔡健雅" % (x+1))
			songList.addItem(item)
		#歌曲列表右边的功能列表
		funcList = QListWidget(listWgt)
		funcList.setGeometry(250,0,50,370)   
		funcList.setStyleSheet("QListWidget{ background:white;color:red ;border:none;border-right:2px solid #EAD9EA} QPushButton{ background:white;border:none;color:grey } QPushButton:hover{ background:white;color:black } ")
		btn = QPushButton("首页",funcList)
		btn.setGeometry(0,0,48,40)
		btn.clicked.connect(self.newwindow)
		btn = QPushButton("设置",funcList)
		btn.setGeometry(0,40,48,40)
		btn = QPushButton("推荐",funcList)
		btn.setGeometry(0,80,48,40)
		btn = QPushButton("聊天",funcList)
		btn.setGeometry(0,120,48,40)
		btn = QPushButton("其他",funcList)
		btn.setGeometry(0,160,48,40)
		btn = QPushButton("站位",funcList)
		
		btn.setGeometry(0,200,48,40)
		#底部状态栏
		wg = QWidget(self)
		wg.setGeometry(0, 580, 300,20)
		wg.setStyleSheet("QWidget{ background:%s } QLabel{ color:white }" % conf['footer'])
		# ql = QLabel(" <a style='color:white;text-decoration:none;'  href ='https://github.com/codeAB/music-player' >:）加入我们&nbsp;</a>",wg)
		# ql.resize(300,20)
		# ql.setAlignment(Qt.AlignRight)
		# ql.linkActivated.connect(self.openurl)


		#设置托盘图标
		tray = QSystemTrayIcon(self)
		tray.setIcon(QIcon('image/tray.png'))
		trayIconMenu = QMenu(self)
		preAction = QAction(u"上一曲 ", self,triggered=self.close)
		pauseAction = QAction(u"暂停|播放 ", self,triggered=self.close)
		nextAction = QAction(u"下一曲 ", self,triggered=self.close)
		quitAction = QAction(u"退出 ", self,triggered=self.close)
		showAction = QAction(QIcon('image/tray.png'),u"显示主面板", self,triggered=self.close)
		trayIconMenu.addAction(showAction)
		trayIconMenu.addAction(preAction)
		trayIconMenu.addAction(pauseAction)
		trayIconMenu.addAction(nextAction)
		trayIconMenu.addAction(quitAction)
		tray.setContextMenu(trayIconMenu)
		tray.show()
		tray.activated.connect(self.dbclick_tray)

		self.destroyed.connect(self.func)
	def dbclick_tray(self,event):
		if event==QSystemTrayIcon.DoubleClick:
			self.show()
	def newwindow(self):
		if not hasattr(self,'widget1'):
			self.widget1 = index()
			self.widget1.show()
			self.widget1.destroyed.connect(self.func)
		else:
			self.widget1.show()
		# 获取屏幕宽高
		wh = QApplication.desktop().screenGeometry()
		self.screen_w , self.screen_h = wh.width() ,wh.height()
		self.move(int((self.screen_w-900)/2),int((self.screen_h-600)/2))
		# print(dir(self))
		self.widget1.move(int((self.screen_w-900)/2)+300,int((self.screen_h-600)/2))

	def func():
		print("close")
	def openurl(self):
		QDesktopServices.openUrl(QUrl("https://github.com/codeAB/music-player"))
	def myclose(self):
		if hasattr(self,'widget1'):
			self.widget1.close() and self.close()
		else:
			self.close()
		
#定义一个公用类  提供公用的静态方法
class Myclass():
	def __init__(self):
		pass
	@staticmethod
	def newWindow():
		itm = QWidget()
		return itm
#自定义线程类
class MyThread(QThread):
	def __init__(self):
		super(QThread,self).__init__()
	def __del__(self):
		self.wait()
	def run(self):
		print("do somethis")
		app = QApplication(sys.argv)
		sds = QWidget()
		sds.show()
		app.exec_()
		# fun()




if __name__ == '__main__':
	app = QApplication(sys.argv)
	music = Music()
	# app.exec_()
	sys.exit(app.exec_())