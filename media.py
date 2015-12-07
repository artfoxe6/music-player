import sys,ctypes
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QProgressBar,QListWidget,
	QSystemTrayIcon,QMenu,QAction,QGraphicsDropShadowEffect,QGraphicsBlurEffect,QListWidgetItem)
from PyQt5.QtCore import Qt,QSize,QUrl,QThread
from PyQt5.QtGui import QCursor,QIcon,QBrush,QColor,QDesktopServices 
from conf.conf import conf

class mywindow(QWidget):
	def __init__(self):
		super().__init__()
