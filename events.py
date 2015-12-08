#!/usr/bin/python3
# -*- coding: utf8 -*-


"""
	自定义信号 和事件
"""
import sys
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton


class signals(QObject):
    closeApp = pyqtSignal(list)
    printApp = pyqtSignal(QPushButton)


# class Example(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.c = mysignal()
#         self.resize(400,400)
#         self.btn = QPushButton("hehe",self)
#         self.c.printApp.connect(self.myclose)
#         self.show()

#     def mousePressEvent(self, event):
#         hehe = list(range(10))
#         self.c.printApp.emit(self.btn)

#     def myclose(self, btn):
#         # print(btn)
#         btn.move(100,100)
#         # btn.
#         # self.close()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
