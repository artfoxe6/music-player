
import sys
import os
import urllib.parse
import urllib.request
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,QListWidget,QListWidgetItem)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot,QTimer


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):     
        s = """
        QScrollBar:vertical {
    border: 2px solid grey;
    background: #32CC99;


}
QScrollBar::handle:vertical {
    background: white;
    min-width: 20px;
}
QScrollBar::add-line:vertical {
    border: 2px solid grey;
    background: #32CC99;
    width: 20px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    border: 2px solid grey;
    background: #32CC99;
    width: 20px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
        """ 
        self.setStyleSheet(s)
        #列表
        songList = QListWidget(self)
        songList.setGeometry(2,0,238,370)  
        for x in range(100):
            item = QListWidgetItem("hucida cdsa%d" % (x))
            songList.addItem(item)
        # songList.setStyleSheet(qss_songlist)
        self.show()
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # music = search()
    music = Example()
    # app.exec_()
    sys.exit(app.exec_())
