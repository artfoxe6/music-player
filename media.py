#!/usr/bin/python3
# -*- coding: utf8 -*-

from PyQt5.QtMultimedia import (QMediaPlayer, QMediaPlaylist, QMediaContent,QMediaMetaData)
from conf.conf import conf
from PyQt5.QtCore import QUrl,Qt,QTime
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QBrush
import os
import re
from mutagen.mp3 import MP3


class Player():
  # 参数music是mainnwindow对象 
  def __init__(self,music):
    self.duration = 0
    self.music = music
    self.music.player = QMediaPlayer()
    
    # print(dir(self.music.player))
    self.music.playlist = QMediaPlaylist()
    # print(dir(self.music.playlist))
    # print(dir(self.music.playlist))
    #单曲循环
    self.music.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
    self.music.player.setPlaylist(self.music.playlist)

    self.init_list()
    self.music.playit = self.playit
    self.music.play_or_pause = self.play_or_pause
    self.music.nextone = self.nextone
    self.music.prevone = self.prevone


    self.music.player.metaDataChanged.connect(self.metaDataChanged)
    self.music.player.stateChanged.connect(self.stateChanged)
    self.music.player.positionChanged.connect(self.positionChanged)
    self.music.player.durationChanged.connect(self.durationChanged)
    self.music.player.error.connect(self.displayErrorMessage)
    self.music.processSlider.valueChanged.connect(self.song_pro)
    # self.music.processSlider.valueChanged.connect(self.song_pro)
  # 快进后退
  def song_pro(self,pro):
    if hasattr(self,'songpro'):
      if abs(pro - self.songpro) > 5:
        self.music.player.setPosition(pro*1000)
    else:
      self.music.processSlider.setValue(0)
    # print(pro,self.songpro)

  def durationChanged(self,duration):
    duration /= 1000
    self.duration = duration
    # totalTime = QTime((duration/3600)%60, (duration/60)%60, duration%60, (duration*1000)%1000);
    # format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
    # tStr = totalTime.toString()
    self.music.processSlider.setMaximum(duration)
  def positionChanged(self,progress):
    progress /= 1000
    self.songpro = progress
    if not self.music.processSlider.isSliderDown():
      self.music.processSlider.setValue(progress)
    self.updateDurationInfo(progress)
  def updateDurationInfo(self, currentInfo):
    duration = self.duration
    tStr = ""
    if currentInfo or duration:
      currentTime = QTime((currentInfo/3600)%60, (currentInfo/60)%60, currentInfo%60, (currentInfo*1000)%1000)
      totalTime = QTime((duration/3600)%60, (duration/60)%60, duration%60, (duration*1000)%1000);
      format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
      tStr = currentTime.toString(format) + " / " + totalTime.toString(format)
    else:
      Str = ""
    self.music.songTime.setText(tStr)

  def displayErrorMessage(self):
    print(self.music.player.errorString())
  def init_list(self):
    #读取配置歌曲目录里面的音乐文件
    listfile = os.listdir(conf['mp3dir'])
    x = 0
    for name in listfile:
      s = os.path.splitext(name)[1][1:]
      if(s.upper() == 'MP3'):
        x+=1
        songname = name.split(".")[0]
        if len(songname) > 12:
          songname = songname[0:12]+"..."
        item = QListWidgetItem("%02d  %s" % (x,songname))
        
        self.music.songList.addItem(item)
        url = QUrl.fromLocalFile(os.path.join(conf['mp3dir'],name))
        self.music.playlist.addMedia(QMediaContent(url))
        
  def playit(self,eve):
    s = eve.text()
    p = re.compile(r'\d+')
    r = p.findall(s)
    self.music.playlist.setCurrentIndex(int(r[0])-1)
    self.music.player.play()
    # duration = self.music.player.duration()
    # totalTime = QTime((duration/3600)%60, (duration/60)%60,
    #                 duration%60, (duration*1000)%1000)
    # # format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
    # tStr = totalTime.toString()
    # print(tStr)

  def play_or_pause(self):
      if self.music.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
          self.music.player.play()
      elif self.music.player.state() == QMediaPlayer.PlayingState:
          self.music.player.pause()

  def nextone(self):
    self.music.playlist.next()
    self.music.player.play()
  def prevone(self):
    self.music.playlist.previous()
    self.music.player.play()

  def metaDataChanged(self):
    if self.music.player.isMetaDataAvailable(): 
      current_song_path = self.music.playlist.currentMedia().canonicalUrl().toString()
      #当前播放的是item index
      ci = self.music.playlist.currentIndex()
      playitem = self.music.songList.item(ci)
      playitem.setSelected(True)
      #把qt的路径格式转换为绝对路径
      audio = MP3(current_song_path[7:])
      # print(audio)
      # print(audio.get('TIT2'))  #歌名
      # print(audio.get('TPE1'))  #歌手
      # print(audio.get('TALB'))  #专辑
      s = str(audio.get('TIT2'))+"-"+str(audio.get('TPE1'))
      # print(s)
      self.music.currentMusicName.setText(s)
      local = os.path.join('./cache/', str(audio.get('TPE1'))+'.jpg')
      if not os.path.isfile(local):
        local = os.path.join('.', 'image/caijianya.jpg')
      self.music.picture.setStyleSheet("QLabel{ background:#9B0069;border-image:url("+local+")}")

  def stateChanged(self):
    if self.music.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
      self.setPlayBtn('play11')
    elif self.music.player.state() == QMediaPlayer.PlayingState:
      self.setPlayBtn('pause11')

  def setPlayBtn(self,stat):
    self.music.playBtn.setStyleSheet("QPushButton{ border-image:url(image/%s.png);border:none }" % stat)

  

if __name__ == "__main__":
    # listfile = os.listdir(conf['mp3dir'])
    # for name in listfile:
    #   print(os.path.join(conf['mp3dir'],name))
    m = Player()
    # print("oooo")
