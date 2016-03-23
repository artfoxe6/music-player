#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from mutagen import easyid3
from PyQt5.QtWidgets import QApplication, QWidget

class myWidget(QWidget):
	def __init(self):
		super().__init__()
	def closeEvent(self,event):
		print("ooo")
		event.accept()


class Example(myWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 220)  
        self.setWindowTitle('Simple') 
        self.show()


        
if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # ex = Example()
    # sys.exit(app.exec_()) 
    print(dir(easyid3))

