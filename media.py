#!/usr/bin/python3
# -*- coding: utf8 -*-

from PyQt5.QtMultimedia import (QMediaPlayer, QMediaPlaylist, QMediaContent,QMediaMetaData)
from conf.conf import conf
from PyQt5.QtCore import QUrl,Qt,QTime,QSize,QTimer
from PyQt5.QtWidgets import QListWidgetItem,QMenu,QAction,QWidget,QPushButton,QLabel
from PyQt5.QtGui import QBrush,QIcon,QCursor
import os
import re
from mutagen.mp3 import MP3
from mywidget import listlabel


class Player():
  # 参数music是mainnwindow对象 
  def __init__(self,music):
    self.duration = 0  #当前歌曲时长
    self.music = music
    self.lrcmap = {}
    self.music.player = QMediaPlayer()
    
    # print(dir(self.music.player))
    self.music.playlist = QMediaPlaylist()
    # print(dir(self.music.playlist))
    # print(dir(self.music.playlist))
    #单曲循环
    self.music.playlist.setPlaybackMode(QMediaPlaylist.Loop)
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

    preAction = QAction(u"上一曲 ", self.music,triggered=self.prevone)
    pauseAction = QAction(u"暂停|播放 ", self.music,triggered=self.play_or_pause)
    nextAction = QAction(u"下一曲 ", self.music,triggered=self.nextone)
    quitAction = QAction(u"退出 ", self.music,triggered=self.music.close)
    self.music.trayIconMenu.addAction(preAction)
    self.music.trayIconMenu.addAction(pauseAction)
    self.music.trayIconMenu.addAction(nextAction)
    self.music.trayIconMenu.addAction(quitAction)

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
    # print(progress)
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
        item = QListWidgetItem()
        item.setSizeHint(QSize(210,40))
        lwg = QWidget()
        # lwg.setParent(item)
        lwg.setObjectName("songlist")
        lwg.setCursor(QCursor(Qt.PointingHandCursor))
        lwg.setGeometry(20,0,140,30)
        lwg.setObjectName("hehe")
        # lwg.clicked.connect(self.playit)
        lwg.setStyleSheet("QWidget#hehe:hover{ background:#999; }\
          QWidget#hehe{border-radius:2px;} \
          ")
        btn = QPushButton(str(x),lwg)
        btn.setGeometry(5,8,24,24)
        btn.setStyleSheet("QPushButton{ border-radius:12px;background:#5E0000;color:#DDD;font-size:10px;opacity:0.5;font-weight:bold; }")
        ql = listlabel()
        ql.setText(songname)
        ql.setParent(lwg)
        ql.setGeometry(40,0,190,40)  #transparent
        ql.setStyleSheet("QLabel{ font-weight:bold;color:#666;background:transparent } \
         QLabel:hover{ color:#fff }")
        ql.doubleclicked.connect(self.playit)
        self.music.songList.addItem(item)
        self.music.songList.setItemWidget(item, lwg)

        url = QUrl.fromLocalFile(os.path.join(conf['mp3dir'],name))
        self.music.playlist.addMedia(QMediaContent(url))
        
  def playit(self,index):
    # print(eve)
    # print(index)
    # 播放序号从0开始
    self.music.playlist.setCurrentIndex(index-1)
    self.music.player.play()

    # s = eve.text()
    # p = re.compile(r'\d+')
    # r = p.findall(s)
    # self.music.playlist.setCurrentIndex(int(r[0])-1)
    # self.music.player.play()
    # 
    # 
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
      # s = str(audio.get('TIT2'))+"-"+str(audio.get('TPE1'))
      s = str(audio.get('TIT2'))
      if len(s) > 12:
          s = s[0:12]+"..."
      # print(s)
      self.music.currentMusicName.setText(s)
      self.music.currentSonger = str(audio.get('TPE1'))
      local = os.path.join('./cache/', str(audio.get('TPE1'))+'.jpg')
      if not os.path.isfile(local):
        local = os.path.join('.', 'image/caijianya.jpg')
      self.music.picture.setStyleSheet("QLabel{ background:#9B0069;border-image:url("+local+")}")
      # 加载歌词
      filename = conf['mp3dir']+"123.lrc"
      # print(filename)
      f = open(filename, "r")  
      while True:  
        line = f.readline()  
        if line:  
          # [02:56.00]如果真的有一天
          # time = line.split("]")[0]
          res = re.findall(r'[0-9]',line)
          if len(res) >= 6 :
            # print(res[0])
            t = int(res[0]+res[1])*60+int(res[2]+res[3])-1
            # print(t)
            self.lrcmap[t] = line.split("]")[1].strip('\n')
        else:  
          break  
      f.close()

  def stateChanged(self):
    if self.music.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
      self.setPlayBtn('play11')
      if hasattr(self,'timer'):
        self.timer.stop()
      # print(self.lrcmap)
    elif self.music.player.state() == QMediaPlayer.PlayingState:
      self.setPlayBtn('pause11')
      if hasattr(self.music,'lrctext'):
        self.timer = QTimer()
        self.timer.timeout.connect(self.refreshlrc)
        self.timer.start(100)

  def setPlayBtn(self,stat):
    self.music.playBtn.setStyleSheet("QPushButton{ border-image:url(image/%s.png);border:none }" % stat)
  def refreshlrc(self):
    # print("333")
    # current = self.songpro
    k = int(self.songpro)
    if k in list(self.lrcmap.keys()):
      if self.lrcmap[k] != '':
        self.music.lrctext.setText(self.lrcmap[k])
    else:
      while(k not in list(self.lrcmap.keys())):
        k = k - 1 
      self.music.lrctext.setText(self.lrcmap[k])
      # print(self.lrcmap[k])
    # else:
      # print(k)
      # x = self.lrcmap.keys()
      # print(list(x))
    # print(self.songpro+"=="+self.lrcmap[self.songpro])

  

if __name__ == "__main__":
    # listfile = os.listdir(conf['mp3dir'])
    # for name in listfile:
    #   print(os.path.join(conf['mp3dir'],name))
    m = Player()
    # print("oooo")
