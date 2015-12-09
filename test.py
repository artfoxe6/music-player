#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget,QDialog


class Demo(QWidget):

	def __init__(self):
		super().__init__()
		self.main()
		self.show()

	def main(self):
		self.setGeometry(500,200,400,400)
		btn = QPushButton('new window',self)
		btn.clicked.connect(self.func)
	def func(self):
		dia = QDialog(self)
		dia.setGeometry(400,0,200,400)
		# self.dia.setParent(self)
		dia.show()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = Demo()
	sys.exit(app.exec_())
