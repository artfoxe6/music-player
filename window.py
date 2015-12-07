

import sys,os
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLineEdit)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtGui import QCursor,QIcon

class mywindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		self.show()
	def initUI(self):
		self.setWindowIcon(QIcon("image/tray.png"))
		self.setWindowTitle("梦音乐")
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setObjectName("window")
		style=""" 
				#window{ background:grey }	
		"""
		self.setStyleSheet(style)
		self.resize(600,600)
		#菜单
		# wg = QWidget(self)
		# wg.setGeometry(0,0,600,40)
		# # wg.setStyleSheet("QWidget{ background:red }")
		# btn = QPushButton("关闭",wg)
		# btn.setGeometry(540,5,60,30)
		# btn.setCursor(QCursor(Qt.PointingHandCursor))
		# # btn.setStyleSheet("QPushButton{ border:none;color:white;background-color:transparent } ")
		# btn.clicked.connect(self.myclose)
		# #
		# btn = QPushButton("首页",wg)
		# btn.setGeometry(5,5,60,30)
		# btn = QPushButton("推荐",wg)
		# btn.setGeometry(65,5,60,30)
		# btn = QPushButton("发帖",wg)
		# btn.setGeometry(125,5,60,30)
		# btn = QPushButton("设置",wg)
		# btn.setGeometry(185,5,60,30)
		# ql = QLineEdit(wg)
		# ql.setGeometry(245,5,150,30)
		# btn = QPushButton("搜歌",wg)
		# btn.setGeometry(400,5,60,30)
		#内嵌web网页
		web = QWebEngineView(self)
		web.setGeometry(0,0,600,580)
		web.load(QUrl.fromLocalFile(os.path.abspath("web/index.html")))
		#

	def mousePressEvent(self, event):
		if event.button()==Qt.LeftButton:
			self.drag_flag=True
			self.begin_position=event.globalPos()-self.pos()
			event.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))
	def mouseMoveEvent(self, QMouseEvent):
		if Qt.LeftButton and self.drag_flag:
			self.move(QMouseEvent.globalPos()-self.begin_position)
			QMouseEvent.accept()
	def mouseReleaseEvent(self, QMouseEvent):
		self.drag_flag=False
		self.setCursor(QCursor(Qt.ArrowCursor))
	def myclose(self):
		self.close()





if __name__ == '__main__':
	app = QApplication(sys.argv)
	music = mywindow()
	# app.exec_()
	sys.exit(app.exec_())