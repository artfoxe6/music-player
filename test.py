#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget,QListWidget,QListWidgetItem
from PyQt5.QtGui import *
class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 220)  
        self.setWindowTitle('Simple') 
        style = """
        QScrollBar:horizontal {
    border: 2px solid grey;
    background: #32CC99;
    height: 15px;
    margin: 0px 20px 0 20px;
}
QScrollBar::handle:horizontal {
    background: white;
    min-width: 20px;
}
QScrollBar::add-line:horizontal {
    border: 2px solid grey;
    background: #32CC99;
    width: 20px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    border: 2px solid grey;
    background: #32CC99;
    width: 20px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
        """
        l = QListWidget(self)
        item = ['OaK','Banana','Apple','Orange','Grapes','Jayesh']
        for lst in range(100):
            # print(lst)
            l.addItem(QListWidgetItem(str(lst)))
        self.setStyleSheet(style)
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())