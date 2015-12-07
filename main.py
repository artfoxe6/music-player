#!/usr/bin/python3
# -*- coding: utf8 -*-


import sys,ctypes
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QProgressBar,QListWidget,
	QSystemTrayIcon,QMenu,QAction,QGraphicsDropShadowEffect,QGraphicsBlurEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor,QIcon

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
		self.setStyleSheet("#mainBox{ background-color:white;padding:10px }")
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
		btn = QPushButton("关闭",top_tools)
		btn.setGeometry(260,0,40,20)
		btn.setStyleSheet("QPushButton{ color:white;border:none }")
		btn.clicked.connect(self.close)
		#最小化程序按钮
		btn = QPushButton("最小化",top_tools)
		btn.setGeometry(220,0,40,20)
		btn.setStyleSheet("QPushButton{ color:white;border:none }")
		btn.clicked.connect(self.hide)
		#设置按钮
		btn = QPushButton("设置",top_tools)
		btn.setGeometry(180,0,40,20)
		btn.setStyleSheet("QPushButton{ color:white;border:none }")
		btn.clicked.connect(self.newwindow)
		#设置播放按钮
		btn = QPushButton("",songer_img)
		btn.setGeometry(126,140,48,48)
		btn.setStyleSheet("QPushButton{ border-image:url(image/play11.png);border:none }")
		btn.clicked.connect(self.close)
		btn = QPushButton("",songer_img)
		btn.setGeometry(198,154,24,24)
		btn.setStyleSheet("QPushButton{ border-image:url(image/next11.png);border:none }")
		btn.clicked.connect(self.close)
		btn = QPushButton("",songer_img)
		btn.setGeometry(78,154,24,24)
		btn.setStyleSheet("QPushButton{ border-image:url(image/pre11.png);border:none }")
		btn.clicked.connect(self.close)
		#歌曲进度条
		progressBar = QProgressBar(self)
		progressBar.setGeometry(0,200,300,5)
		progressBar.setStyleSheet("QProgressBar{ background:#B4FFA3;border:none }")
		#歌曲列表
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 205, 300,370)
		listWgt.setStyleSheet("QWidget{ background:pink }")
		songList = QListWidget(listWgt)
		songList.resize(300,370)   
		songList.setStyleSheet("QListWidget{ background:white }")
		songList.setObjectName("songlist")
		#底部状态栏
		wg = QWidget(self)
		wg.setGeometry(0, 575, 300,25)
		wg.setStyleSheet("QWidget{ background:grey }")
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
	def dbclick_tray(self,event):
		if event==QSystemTrayIcon.DoubleClick:
			self.show()
	def newwindow(self):
		te = QWidget()
		te.setGeometry(100,100,300,300)
		te.show()
		# print("qwe")
	
#自定义label，用于鼠标拖动主窗口
#第二个参数就是要拖动的对象
class DragLabel(QLabel):
	def __init__(self,window):
		super().__init__()
		self.window = window
	def mousePressEvent(self, event):
		if event.button()==Qt.LeftButton:
			self.drag_flag=True
			self.begin_position=event.globalPos()-self.window.pos()
			event.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))
	def mouseMoveEvent(self, QMouseEvent):
		if Qt.LeftButton and self.drag_flag:
			self.window.move(QMouseEvent.globalPos()-self.begin_position)
			QMouseEvent.accept()
	def mouseReleaseEvent(self, QMouseEvent):
		self.drag_flag=False
		self.setCursor(QCursor(Qt.ArrowCursor))



if __name__ == '__main__':
	app = QApplication(sys.argv)
	music = Music()
	sys.exit(app.exec_())