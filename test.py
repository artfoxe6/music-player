#!/usr/bin/python
#encoding:utf-8

# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSignature

class Ui_formDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        uic.loadUi("form.ui", self)        #form.ui  为QT界面文件 QListWidget对象名为 listView1
        self.listDataBind()                  #添加QListWidgetItme
        self.listView1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)   #定义右键菜单
        
    def listDataBind(self):
        item = ['OaK','Banana','Apple','Orange','Grapes','Jayesh']
        for lst in item:
            self.listView1.addItem(QtGui.QListWidgetItem(lst))
   

    #激活菜单事件
   @pyqtSignature("QPoint")
    def on_listView1_customContextMenuRequested(self, point):
        item = self.listView1.itemAt(point)
        #空白区域不显示菜单
        if item != None:

           self.rightMenuShow()


    #创建右键菜单
    def rightMenuShow(self):
        rightMenu = QtGui.QMenu(self.listView1)
        removeAction = QtGui.QAction(u"删除", self, triggered=self.close)       # triggered 为右键菜单点击后的激活事件。这里slef.close调用的是系统自带的关闭事件。
        rightMenu.addAction(removeAction)
       
        addAction = QtGui.QAction(u"添加", self, triggered=self.addItem)       # 也可以指定自定义对象事件
        rightMenu.addAction(addAction)
        rightMenu.exec_(QtGui.QCursor.pos())
       

    def addItem(self):
        pass