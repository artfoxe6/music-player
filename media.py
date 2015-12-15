#!/usr/bin/python3
# -*- coding: utf8 -*-

from PyQt5.QtMultimedia import (QMediaPlayer, QMediaPlaylist, QMediaContent)
from conf.conf import conf
import os

class box(QWidget):
  def __init__(self):
    super().__init__()
    
class Media(object):

    def __init__(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.mp3list()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def main(self):
        pass

    def mp3list(self):
        listfile = os.listdir(conf['mp3dir'])
        for name in listfile:
            print(name)

if __name__ == "__main__":
    # listfile = os.listdir(conf['mp3dir'])
    # for name in listfile:
    #   print(os.path.join(conf['mp3dir'],name))
    m = Media()
