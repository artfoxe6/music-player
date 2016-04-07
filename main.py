#!/usr/bin/python3
# -*- coding: utf8 -*-


import sys,ctypes,os
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QProgressBar,QListWidget, QSystemTrayIcon,QMenu,QAction,QGraphicsDropShadowEffect,QGraphicsBlurEffect,QListWidgetItem,QSlider,QDialog,QGraphicsColorizeEffect)
from PyQt5.QtCore import Qt,QSize,QUrl,QThread,QPoint,pyqtSignal
from PyQt5.QtGui import ( QCursor,QIcon,QBrush,QDesktopServices,QLinearGradient,QLinearGradient,QFont,QPainter,QColor)
from PyQt5.QtMultimedia import (QMediaPlayer, QMediaPlaylist, QMediaContent)
from PyQt5.QtNetwork import *
from conf import conf
from mywidget import *
from qss import *
from media import *
from singer import *

# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
class Music(QWidget):
	def __init__(self):
		s = QSslSocket()
		s.setProtocol(QSsl.TlsV1_0)
		# print(s.protocol())
		# exit()
		super().__init__()
		self.currentSonger = ''
		self.setWindowIcon(QIcon("image/tray.png"))
		self.setWindowTitle("SYL - 乐人馆")
		self.setObjectName("box")
		# 窗口无边框
		self.setWindowFlags(Qt.FramelessWindowHint)
		# 窗口居于所有窗口的顶端 
		# self.setWindowFlags(Qt.WindowOverridesSystemGestures)
		# 窗口居于所有窗口的顶端  针对部分X11
		# self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		# 初始化基本UI界面
		self.initUI()
		# 初始化播放核心
		self.initplayer()
		# 显示主界面
		self.show()
		self.widget1 = index()
		self.widget1.setParent(self)

		
		
	def initUI(self):
		# 获取电脑屏幕宽高 让主界面初始化后处于屏幕中间
		wh = QApplication.desktop().screenGeometry()
		self.screen_w , self.screen_h = wh.width() ,wh.height()
		self.setGeometry(int((self.screen_w-300)/2),int((self.screen_h-600)/2),300,600)
		# self.setWindowOpacity(0.97); 

		#当前播放歌曲的封面 
		songer_img = DragLabel(self)
		# songer_img.setwinflag.connect(self.setwinflag)
		songer_img.setParent(self)
		songer_img.resize(300,200)

		self.picture = QLabel(songer_img)
		self.picture.resize(300,200)
		self.picture.setStyleSheet("QLabel{ border-image:url("+conf['pifu']+")}")

		# syl = QLabel(songer_img)
		# syl.setGeometry(15,5,34,15)
		# syl.setStyleSheet("QLabel{ border-image:url(image/newimg/logo.png);}")

		# ================================
		songinfo = QLabel(songer_img)
		songinfo.setGeometry(0,30,300,80)
		songinfo.setStyleSheet("QLabel{ background:transparent;}")

		songpic = QLabel(songinfo)
		songpic.setGeometry(10,0,80,80)
		songpic.setStyleSheet("QLabel{ border-image:url(image/newimg/user.jpg);border-radius:2px;}")

		self.songname = QLabel("老鼠爱大米 - 香香",songinfo)
		self.songname.setGeometry(105,0,210,25)
		self.songname.setStyleSheet("QLabel{ color:#EEE;font-size:15px;}")
		uploaduser = QLabel("By 张三的歌",songinfo)
		uploaduser.move(105,25)
		# uploaduser.setCursor(QCursor(Qt.PointingHandCursor))
		uploaduser.setStyleSheet("QLabel{ color:yellow;font-size:15px;} QLabel:hover{color:red}")

		fenshu = QLabel("评分 - 7.6",songinfo)
		fenshu.setGeometry(105,50,210,25)
		# self.picture.setGraphicsEffect(QGraphicsBlurEffect())
		fenshu.setStyleSheet("QLabel{ color:#EEE;font-size:15px;}")


		songtool = QLabel(songer_img)
		songtool.setGeometry(0,110,300,35)
		songtool.setStyleSheet("QLabel{ background:transparent;}")

		# 喜欢歌曲
		lovesong = QLabel(songtool)
		lovesong.setGeometry(20,10,25,25)
		lovesong.setStyleSheet("QLabel{ border-image:url(image/newimg/kg_ic_player_liked.png);}")
		# 评论
		pinglun = QLabel(songtool)
		pinglun.setGeometry(50,5,33,33)
		pinglun.setStyleSheet("QLabel{ border-image:url(image/newimg/pinglun.png);}")
		# 歌曲更多信息
		songmore = QLabel("查看这首歌的更多资料",songtool)
		songmore.move(100,10)
		# songmore.setCursor(QCursor(Qt.PointingHandCursor))
		songmore.setStyleSheet("QLabel{ color:#BBB} QLabel:hover{color:pink}")


		# ======================================

		# 顶部工具栏
		# 隐藏
		btn = QPushButton("",self)
		btn.setGeometry(270,0,15,32)
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn.setStyleSheet("QPushButton{ border:none;color:white;background:transparent;border-image:url(image/newimg/mini.png) } QPushButton:hover{ border-image:url(image/newimg/mini_2.png) } ")
		btn.clicked.connect(self.close)

		# 换皮肤
		btn = QPushButton("",self)
		btn.setGeometry(230,10,20,20)
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn.setStyleSheet("QPushButton{ border:none;color:white;background:transparent;border-image:url(image/newimg/fx_slide_menu_change_bg_2.png) } QPushButton:hover{ border-image:url(image/newimg/fx_slide_menu_change_bg.png) } ")
		btn.clicked.connect(self.huanfu)
		# 设置封面
		# btn = QPushButton("",self)
		# btn.setGeometry(230,-10,41,48)
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		# btn.setStyleSheet("QPushButton{ border:none;color:white;background:transparent;border-image:url(image/newimg/fengmian.png) } ")
		# btn.clicked.connect(self.setHeaderImg)
		# 开启/关闭歌词
		# btn = QPushButton("",self)
		# btn.setGeometry(200,0,30,30)
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		# btn.setStyleSheet("QPushButton{ border:none;color:white;background:transparent;border-image:url(image/newimg/geci.png) } ")
		# btn.clicked.connect(self.lrc)
		# 播放组件  ( 播放  前进 后退 播放时间 进度条 歌曲名 音量 )
		# 播放/暂停
		self.playBtn = QPushButton("",songer_img)
		self.playBtn.setGeometry(130,155,32,25)
		self.playBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/statusbar_btn_play.png);border:none } QPushButton:hover{ border-image:url(image/newimg/statusbar_btn_play_2.png)} ")
		# 下一首
		self.nextBtn = QPushButton("",songer_img)
		self.nextBtn.setGeometry(186,159,20,20)
		self.nextBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/statusbar_btn_next.png);border:none } QPushButton:hover{ border-image:url(image/newimg/statusbar_btn_next_2.png)}")
		# 音量调节
		self.songvolume = QPushButton("",songer_img)
		self.songvolume.setGeometry(236,159,20,20)
		self.songvolume.setStyleSheet("QPushButton{ border-image:url(image/newimg/ic_player_menu_volume.png);border:none } QPushButton:hover{ border-image:url(image/newimg/ic_player_menu_volume_2.png)}")
		self.songvolume.clicked.connect(self.setvolume)
		# 音量
		self.volslider = QSlider(Qt.Horizontal,self)
		self.volslider.setCursor(QCursor(Qt.UpArrowCursor))
		self.volslider.setGeometry(250,165,45,6)
		self.volslider.setValue(70)
		self.volslider.setRange(0,100)
		self.volslider.setStyleSheet(qss_vol)
		self.volslider.setVisible(False)

		# 上一首
		self.prevBtn = QPushButton("",songer_img)
		self.prevBtn.setGeometry(85,159,20,20)
		self.prevBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/statusbar_btn_prev.png);border:none } QPushButton:hover{ border-image:url(image/newimg/statusbar_btn_prev_2.png)}")
		# 播放模式
		self.playmodel = QPushButton("",songer_img)
		self.playmodel.setGeometry(35,156,25,25)
		self.playmodel.setStyleSheet("QPushButton{ border-image:url(image/newimg/allmodel.png);border:none } QPushButton:hover{ border-image:url(image/newimg/allmodel_2.png)}")
		self.playmodel.clicked.connect(self.moshi)

		# 当前播放时间
		self.songTime = QLabel("",self)
		self.songTime.setGeometry(240,180,80,20)
		self.songTime.setStyleSheet("QLabel{ color:#AAA;font-size:12px;}")
		self.songTime.setAlignment(Qt.AlignHCenter)
		
		# 当前歌曲名   
		self.currentMusicName = QLabel("",songer_img)
		self.currentMusicName.setGeometry(0,180,200,20)
		self.currentMusicName.setStyleSheet("QLabel{ color:white ;font-weight:100;font-size:12px;margin-left:5px;}")
		# 歌曲进度条
		self.processSlider = QSlider(Qt.Horizontal,self)
		self.processSlider.setGeometry(0,193,300,7)
		# self.processSlider.setRange(1,100)
		self.processSlider.setValue(0)
		self.processSlider.setStyleSheet(qss_process_slider)
		
		self.processSlider.setCursor(QCursor(Qt.UpArrowCursor))

		# 歌曲列表 ---------------------------
		listWgt = QWidget(self)
		listWgt.setGeometry(0, 200, 300,380)
		listWgt.setStyleSheet(qss_scrollbar)

		#列表
		self.songList = QListWidget(listWgt)
		self.songList.setGeometry(5,0,235,380)   
		self.songList.setStyleSheet(qss_songlist)	
		# 列表添加右键菜单
		# self.songList.setContextMenuPolicy(Qt.CustomContextMenu)
		# self.songList.customContextMenuRequested.connect(self.rightMenuShow)

		#歌曲列表右边的功能列表
		funcList = QListWidget(listWgt)
		funcList.setGeometry(240,0,55,380)   
		funcList.setStyleSheet(qss_menu)
		btn = QPushButton("",funcList)
		btn.clicked.connect(self.newwindow)
		btn.setGeometry(15,10,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/home.png)} \
			QPushButton:hover{ border-image:url(image/homehover.png) }")
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn = QPushButton("",funcList)
		btn.setGeometry(15,60,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/tuijian.png) } \
			QPushButton:hover{ border-image:url(image/tuijianhover.png) }")
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn = QPushButton("",funcList)
		btn.setGeometry(15,100,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/shoucang.png) }\QPushButton:hover{ border-image:url(image/shoucanghover.png) }")
		# btn.setCursor(QCursor(Qt.PointingHandCursor))

		btn = QPushButton("",funcList)
		btn.setGeometry(15,140,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/rizhi.png) }\
			QPushButton:hover{ border-image:url(image/rizhihover.png) }")
		# btn.setCursor(QCursor(Qt.PointingHandCursor))

		btn = QPushButton("",funcList)
		btn.setGeometry(17,180,30,30)
		btn.setStyleSheet("QPushButton{ border-image:url(image/mv.png) }\
			QPushButton:hover{ border-image:url(image/mvhover.png) }")
		# btn.setCursor(QCursor(Qt.PointingHandCursor))

		setbtn = QPushButton("",funcList)
		setbtn.setGeometry(15,225,33,33)
		setbtn.setStyleSheet("QPushButton{ border-image:url(image/settinghover.png) }\
			QPushButton:hover{ border-image:url(image/setting.png) }")
		setbtn.clicked.connect(self.openseting)

		#底部状态栏
		wg = QWidget(self)
		wg.setGeometry(0, 580, 300,20)
		wg.setStyleSheet("QWidget{ background:#2D2D2D; } ")
		# ql = QLabel(" <a style='color:#444;text-decoration:none;font-size:12px;'  href ='https://github.com/codeAB/music-player' >S Y L </a>",wg)
		# ql.resize(300,20)
		# ql.setAlignment(Qt.AlignRight)
		# ql.linkActivated.connect(self.openurl)

		#设置托盘图标
		tray = QSystemTrayIcon(self)
		tray.setIcon(QIcon('image/tray.png'))
		self.trayIconMenu = QMenu(self)
		self.trayIconMenu.setStyleSheet(qss_tray)
		showAction = QAction(QIcon('image/tray.png'),u"显示主面板", self,triggered=self.show)
		self.trayIconMenu.addAction(showAction)
		# self.trayIconMenu.addAction(preAction)
		# self.trayIconMenu.addAction(pauseAction)
		# self.trayIconMenu.addAction(nextAction)
		# self.trayIconMenu.addAction(quitAction)
		tray.setContextMenu(self.trayIconMenu)
		tray.show()
		tray.activated.connect(self.dbclick_tray)
	# 重写两个方法实现拖动播放器到屏幕顶端自动隐藏
	def enterEvent(self,QMouseEvent):
		if self.y() < 1 and self.size().width() == 300:
			self.setGeometry(self.x(),0,300,600) 
			# 窗口居于所有窗口的顶端 
			# self.setWindowFlags(Qt.WindowOverridesSystemGestures)
			#针对X11
			# self.setWindowFlags(Qt.X11BypassWindowManagerHint)
	def leaveEvent(self,QMouseEvent):
		if self.y() < 1 and self.size().width() == 300:
			self.setGeometry(self.x(),0,300,1)
			# 窗口居于所有窗口的顶端 
			# self.setWindowFlags(Qt.WindowOverridesSystemGestures)
			#针对X11
			# self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		# else:
			# self.setWindowFlags(Qt.FramelessWindowHint)
	#加载播放核心
	def initplayer(self):
		#play_song_list用来方便的维护列表,主要用来记录当前播放列表
		# self.play_song_list = {}
		self.p = Player(self)
		# self.songList.itemDoubleClicked.connect(self.playit)
		self.playBtn.clicked.connect(self.play_or_pause)
		self.nextBtn.clicked.connect(self.nextone)
		self.prevBtn.clicked.connect(self.prevone)
		# self.lrc()
		# self.vol.valueChanged.connect(self.)
	#双击托盘图标
	def dbclick_tray(self,event):
		if event==QSystemTrayIcon.DoubleClick:
			# self.show()
			if self.isVisible():
				self.hide()
			else:
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
			if self.size().width() == 900:
				self.resize(300,600)
				self.widget1.hide()
				return True
			# wh = QApplication.desktop().screenGeometry()
			# self.screen_w , self.screen_h = wh.width() ,wh.height()
			# self.move(int((self.screen_w-900)/2),int((self.screen_h-600)/2))
			self.widget1.show()
		self.resize(900,600)
		
	#创建右键菜单
	def rightMenuShow(self,point):
		self.current_context_item = self.songList.itemAt(point)
		if self.current_context_item is None:
			return False
		rightMenu = QMenu(self.songList)
		# print(dir(rightMenu))
		rightMenu.setStyleSheet("QMenu{ width:100px;border:none;padding:5px; } QMenu::item{ background-color: transparent;width:70px;text-align:center;height:25px; margin:0px 0px;border-bottom:1px solid #EEE;padding-left:20px;color:#333 }  QMenu::item:selected{ color:red;border-bottom:1px solid pink;background:none; }") 
		loveAction = QAction(u"添加收藏", self, triggered=self.deleteSongItem)
		delAction = QAction(u"删除", self, triggered=self.deleteSongItem)    
		rateAction = QAction(u"我要打分", self, triggered=self.deleteSongItem)    
		cmAction = QAction(u"评论", self, triggered=self.deleteSongItem)  
		moreAction = QAction(u"歌曲详情", self, triggered=self.deleteSongItem)  
		moneyAction = QAction(u"打赏", self, triggered=self.deleteSongItem)  
		rightMenu.addAction(loveAction)
		rightMenu.addAction(delAction)
		rightMenu.addAction(rateAction)
		rightMenu.addAction(cmAction)
		rightMenu.addAction(moreAction)
		rightMenu.addAction(moneyAction)
		rightMenu.exec_(QCursor.pos())
	def deleteSongItem(self):
		item = self.current_context_item
		# print(dir(item))
		item.setBackground(QBrush(QColor("red")))
		return False
		# index = item.text()
		x = self.songList.row(self.current_context_item)
		self.newSort(int(x))
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
	# 当删除或者新增歌曲时更新列表
	def newSort(self,index,flag = 'del'):
		# 删除歌曲
		if flag == 'del':
			v = self.songList.findChildren(QPushButton,'',Qt.FindChildrenRecursively)
			self.songList.removeItemWidget(self.current_context_item)
			# print(len(v))
			# v[index].parent().remove()
			# print(v[index].parent().hide())
			self.songList.update()
			print(self.songList.count())
	def openurl(self):
		QDesktopServices.openUrl(QUrl("http://sylsong.com"))
	def myclose(self):
		if hasattr(self,'widget1'):
			self.widget1.close() and self.close()
		else:
			self.close()
	def setHeaderImg(self):
		cs = self.currentSonger
		if len(cs) > 1:
			self.s = Singer(cs,self)
			self.show()
	# def lrc(self):
	# 	if hasattr(self,'lrctext'):
	# 		if self.lrctext.isVisible():
	# 			self.lrctext.setVisible(False)
	# 			self.p.showgeci(1)
	# 		else:
	# 			self.lrctext.setVisible(True)
	# 			self.p.showgeci()
	# 	else:
	# 		self.lrctext = DLabel(self)
	# 		self.p.showgeci()
	def moshi(self):
		ct = self.playmodel;
		currentModel = self.playlist.playbackMode()
		if currentModel == 1:
			self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
			self.playmodel.setStyleSheet("QPushButton{ border-image:url(image/newimg/ic_player_mode_all_default.png); } QPushButton:hover{ border-image:url(image/newimg/ic_player_mode_all_default_2.png)}")
		elif currentModel == 2:
			self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
			self.playmodel.setStyleSheet("QPushButton{ border-image:url(image/newimg/allmodel.png); } QPushButton:hover{ border-image:url(image/newimg/allmodel_2.png)}")
		elif currentModel == 3:
			self.playlist.setPlaybackMode(QMediaPlaylist.Random)
			self.playmodel.setStyleSheet("QPushButton{ border-image:url(image/newimg/ic_player_mode_random_default.png); } QPushButton:hover{ border-image:url(image/newimg/ic_player_mode_random_default_2.png)}")
		elif currentModel == 4:
			self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
			self.playmodel.setStyleSheet("QPushButton{ border-image:url(image/newimg/ic_player_mode_single_default.png); } QPushButton:hover{ border-image:url(image/newimg/ic_player_mode_single_default_2.png)}")
	def setvolume(self):
		if self.volslider.isVisible():
			self.volslider.setVisible(False)
			self.songvolume.setStyleSheet("QPushButton{ border-image:url(image/newimg/ic_player_menu_volume.png); } QPushButton:hover{ border-image:url(image/newimg/ic_player_menu_volume_2.png)}")
		else:
			self.volslider.setVisible(True)
			self.songvolume.setStyleSheet("QPushButton{ border-image:url(image/newimg/ic_player_menu_volume_click.png); } QPushButton:hover{ border-image:url(image/newimg/ic_player_menu_volume_click.png)}")
	# def setwinflag(self,index):
	# 	if index == 2:
	# 		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
	# 		self.update()
	# 		self.show()
	# 	else:
	# 		self.setWindowFlags(Qt.FramelessWindowHint)
	# 		self.update()
	# 		self.show()
	def openseting(self):
		
		if not hasattr(self,'popwindow'):
			self.popwindow = popWindow(1)
		else:
			self.popwindow.show()
	def huanfu(self):
		# self.picture.setStyleSheet("QLabel{ border-image:url(image/newimg/back.jpg)}")
		fileinput = QFileDialog.getOpenFileName(self,"选择一张图片作为皮肤","/opt/music-player/","Images (*.jpg)")
		if not fileinput[0]:
			return False
		else:
			f=open("conf/conf.py","w+")
			conf['pifu'] = fileinput[0]
			f.write("conf = "+str(conf))
			f.close()
			self.picture.setStyleSheet("QLabel{ border-image:url("+fileinput[0]+")}")
		
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	music = Music()
	sys.exit(app.exec_())