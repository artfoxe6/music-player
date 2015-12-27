#!/usr/bin/python3
# -*- coding: utf8 -*-


import sys,ctypes,os
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QProgressBar,QListWidget, QSystemTrayIcon,QMenu,QAction,QGraphicsDropShadowEffect,QGraphicsBlurEffect,QListWidgetItem,QSlider,QDialog)
from PyQt5.QtCore import Qt,QSize,QUrl,QThread,QPoint,pyqtSignal
from PyQt5.QtGui import QCursor,QIcon,QBrush,QColor,QDesktopServices
from PyQt5.QtMultimedia import (QMediaPlayer, QMediaPlaylist, QMediaContent)
from conf.conf import conf
from mywidget import *
from qss import *
from media import *


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
		self.initplayer()
		self.show()
		
	def initUI(self):
		#设置无边框
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.resize(300,600)
		self.setObjectName("mainBox")
		self.setStyleSheet("QWidget{ border:none }")
		#当前播放歌曲的歌手图片
		songer_img = DragLabel(self)
		songer_img.setParent(self)
		songer_img.resize(300,200)
		# songer_img.setGraphicsEffect(QGraphicsBlurEffect())
		songer_img.setObjectName("songer_img")
		# songer_img.setStyleSheet("#songer_img{ background:none;}")
		#歌曲专辑图片
		self.picture = QLabel(songer_img)
		# picture.setParent(self)
		self.picture.resize(300,200)
		self.picture.setGraphicsEffect(QGraphicsBlurEffect())
		# picture.setObjectName("songer_img")
		self.picture.setStyleSheet("QLabel{ background:#9B0069;border-image:url(image/zhangjie.jpg)}")
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
		#关闭程序按钮
		# btn = QPushButton("背景",top_tools)
		# btn.setGeometry(200,0,40,20)
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		# btn.setStyleSheet("QPushButton{ border:none;color:white;background-color:black } ")
		# btn.clicked.connect(self.setHeaderImg)
		#设置播放按钮
		self.playBtn = QPushButton("",songer_img)
		self.playBtn.setGeometry(126,120,48,48)
		self.playBtn.setStyleSheet("QPushButton{ border-image:url(image/play11.png);border:none }")
		
		self.nextBtn = QPushButton("",songer_img)
		self.nextBtn.setGeometry(198,134,24,24)
		self.nextBtn.setStyleSheet("QPushButton{ border-image:url(image/next11.png);border:none }")
		
		self.prevBtn = QPushButton("",songer_img)
		self.prevBtn.setGeometry(78,134,24,24)
		self.prevBtn.setStyleSheet("QPushButton{ border-image:url(image/pre11.png);border:none }")
		self.songTime = QLabel("",self)
		self.songTime.setGeometry(220,180,80,20)
		self.songTime.setStyleSheet("QLabel{ color:white;}")
		self.songTime.setAlignment(Qt.AlignHCenter)
		#音量
		# self.vol = QSlider(Qt.Horizontal,self)
		# self.vol.setGeometry(10,144,50,5)
		# self.vol.setValue(60)
		# self.vol.setStyleSheet(qss_vol)
		#当前歌曲名   
		self.currentMusicName = QLabel("梦音乐 ^_^ ",songer_img)
		self.currentMusicName.setGeometry(0,50,300,80)
		self.currentMusicName.setAlignment(Qt.AlignHCenter)
		self.currentMusicName.setStyleSheet("QLabel{ color:white ;font-weight:100;font-size:16px;}")
		#歌曲进度条
		self.processSlider = QSlider(Qt.Horizontal,self)
		self.processSlider.setGeometry(0,200,300,10)
		# self.processSlider.setRange(1,100)
		# self.processSlider.setValue(0)
		self.processSlider.setStyleSheet(qss_process_slider)
		#歌曲列表
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 210, 300,370)
		listWgt.setStyleSheet("QWidget{ background:white }")
		#播放列表前面补空
		blank = QWidget(self)
		blank.setGeometry(0, 210, 2,370)
		blank.setStyleSheet("QWidget{ background:#ddd }")
		#列表
		self.songList = QListWidget(listWgt)
		self.songList.setGeometry(2,0,238,370)   
		self.songList.setStyleSheet(qss_songlist)
		self.songList.setContextMenuPolicy(Qt.CustomContextMenu)
		self.songList.customContextMenuRequested.connect(self.rightMenuShow)
		# 
		#歌曲列表右边的功能列表
		funcList = QListWidget(listWgt)
		funcList.setGeometry(250,0,50,370)   
		funcList.setStyleSheet(qss_menu)
		btn = QPushButton("首页",funcList)
		btn.setGeometry(0,0,48,40)
		btn.clicked.connect(self.newwindow)
		btn = QPushButton("电台",funcList)
		btn.setGeometry(0,40,48,40)
		btn = QPushButton("推荐",funcList)
		btn.setGeometry(0,80,48,40)
		btn = QPushButton("MV",funcList)
		btn.setGeometry(0,120,48,40)
		btn = QPushButton("设置",funcList)
		btn.setGeometry(0,160,48,40)
		#底部状态栏
		wg = QWidget(self)
		wg.setGeometry(0, 580, 300,20)
		wg.setStyleSheet("QWidget{ background:grey } ")
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
	#加载播放核心
	def initplayer(self):
		#play_song_list用来方便的维护列表,主要用来记录当前播放列表
		self.play_song_list = {}
		s = Player(self)
		self.songList.itemDoubleClicked.connect(self.playit)
		self.playBtn.clicked.connect(self.play_or_pause)
		self.nextBtn.clicked.connect(self.nextone)
		self.prevBtn.clicked.connect(self.prevone)
		# self.vol.valueChanged.connect(self.)
		# self.player.play()
		# self.playit()
		# s.init_list()
	#双击托盘图标
	def dbclick_tray(self,event):
		if event==QSystemTrayIcon.DoubleClick:
			self.show()
	#打开音乐窗
	def newwindow(self):
		if not hasattr(self,'widget1'):
			self.widget1 = index()
			self.widget1.setParent(self)
			# 获取屏幕宽高
			wh = QApplication.desktop().screenGeometry()
			self.screen_w , self.screen_h = wh.width() ,wh.height()
			self.move(int((self.screen_w-900)/2),int((self.screen_h-600)/2))
			self.widget1.show()
		else:
			self.widget1.show()
		self.resize(900,600)
		
	#创建右键菜单
	def rightMenuShow(self,point):
		self.current_context_item = self.songList.itemAt(point)
		if self.current_context_item is None:
			return False
		rightMenu = QMenu(self.songList)
		removeAction = QAction(u"删除", self, triggered=self.deleteSongItem)
		addAction = QAction(u"重命名", self, triggered=self.deleteSongItem)    
		rightMenu.addAction(removeAction)
		rightMenu.addAction(addAction)
		rightMenu.exec_(QCursor.pos())
	def deleteSongItem(self):
		# 获取当前鼠标右键点击的歌曲名
		songname = self.current_context_item.text()
		p = re.compile(r'\d+')
		r = p.findall(songname)
		item = int(r[0]) - 1;
		mp3path = conf['mp3dir']
		i = 0
		for filename in os.listdir(mp3path):
			if i == item:
				# 删除列表item
				self.songList.takeItem(self.songList.row(self.current_context_item))
				# 删除播放队列item
				self.playlist.removeMedia(item)
				# 删除文件
				os.remove(os.path.join(mp3path, filename))
				break
			i = i+1
			# print(os.path.join(mp3path, filename))

	def openurl(self):
		QDesktopServices.openUrl(QUrl("https://github.com/codeAB/music-player"))
	def myclose(self):
		if hasattr(self,'widget1'):
			self.widget1.close() and self.close()
		else:
			self.close()
	def setHeaderImg(self):
		s = QDialog(self)
		s.resize(600,400)
		s.show()
		
# #定义一个公用类  提供公用的静态方法
# class Myclass():
# 	def __init__(self):
# 		pass
# 	@staticmethod
# 	def newWindow():
# 		itm = QWidget()
# 		return itm
# #自定义线程类
# class MyThread(QThread):
# 	def __init__(self):
# 		super(QThread,self).__init__()
# 	def __del__(self):
# 		self.wait()
# 	def run(self):
# 		print("do somethis")
# 		app = QApplication(sys.argv)
# 		sds = QWidget()
# 		sds.show()
# 		app.exec_()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	music = Music()
	sys.exit(app.exec_())