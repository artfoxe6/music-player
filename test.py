#!/usr/bin/python
#coding=utf-8
import sys
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Q_ARG, QAbstractItemModel,
        QFileInfo, qFuzzyCompare, QMetaObject, QModelIndex, QObject, Qt,
        QThread, QTime, QUrl)
from PyQt5.QtGui import QColor, qGray, QImage, QPainter, QPalette
from PyQt5.QtMultimedia import ( QMediaPlayer, QMediaPlaylist,QMediaContent)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog,
        QFormLayout, QHBoxLayout, QLabel, QListView, QMessageBox, QPushButton,
        QSizePolicy, QSlider, QStyle, QToolButton, QVBoxLayout, QWidget)

class Player(QWidget):
    def __init__(self):
        super().__init__()
        btn = QPushButton("选择文件",self)
        btn.clicked.connect(self.openfile)
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
    def openfile(self):
        fileNames,_ = QFileDialog.getOpenFileNames(self, "Open Files")
        # print(fileNames)
        for name in fileNames:
            fileInfo = QFileInfo(name)
            if fileInfo.exists():
                url = QUrl.fromLocalFile(fileInfo.absoluteFilePath())
                if fileInfo.suffix().lower() == 'm3u':
                    # print(fileInfo.suffix().lower())
                    self.playlist.load(url)
                else:
                    self.playlist.addMedia(QMediaContent(url))
                    # print("000")
            else:
                url = QUrl(name)
                if url.isValid():
                    self.playlist.addMedia(QMediaContent(url))
            self.player.play()

        


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    player = Player()
    player.show()

    sys.exit(app.exec_())