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
import random

class Player():
  # 参数music是mainnwindow对象 
  def __init__(self,music):
    self.duration = 0  #当前歌曲时长
    self.music = music
    self.lrcmap = {}
    self.filename = ""
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
    self.lrcmap = {}
    duration /= 1000
    self.duration = duration
    # print(duration)
    # 加载歌词
    filename = conf['mp3dir']+self.filename+".lrc"
    # print(filename)
    # self.lrcmap.clear()
    # 清空之前的歌词内容
    
    # 如果歌词文件不存在
    if not os.path.exists(filename):
      # 桌面歌词清空内容
      if hasattr(self.music,'lrctext'):
        self.music.lrctext.setText("")
      # 停止刷新歌词
      if hasattr(self,'timer'):
        self.timer.stop()
      return False
    else:
      # 开始刷新歌词
      if hasattr(self,'timer'):
        self.timer.start(100)
    # 读取歌词文件
    f = open(filename, "r")  
    while True:  
      # 读取每一行
      line = f.readline()
      if line:
          pattern = re.compile(r'\[.*\]')
          # 匹配一行中所有的时间点
          d = pattern.findall(line)
          p = line.split("]");
          # 当前行的歌词
          c = p[len(p)-1].strip("\n")
          if c == '':
            continue
          # 拆分时间点
          pattern2 = re.compile(r'[0-9]{2}:[0-9]{2}\.[0-9]{2}')
          if len(d) != 0 :
            s = pattern2.findall(d[0])
            # print(s)
            for k in s:
                t = int(k[0]+""+k[1])*60+int(k[3]+""+k[4])-1
                # print(t)
                self.lrcmap[t] = c
      else:
        break 
    f.close()

    # totalTime = QTime((duration/3600)%60, (duration/60)%60, duration%60, (duration*1000)%1000);
    # format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
    # tStr = totalTime.toString()
    self.music.processSlider.setMaximum(duration)
  def positionChanged(self,progress):
    progress /= 1000
    self.songpro = progress
    # print(progress)
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
    self.music.playlist.setCurrentIndex(index-1)
    self.music.player.play()

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
  # 当前播放文件改变
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
      self.filename = s
      self.music.currentSonger = str(audio.get('TPE1'))
      # print(self.music.currentSonger)
      local = os.path.join('./cache/', str(audio.get('TPE1'))+'.jpg')
      if not os.path.isfile(local):
        local = os.path.join('.', 'image/zhangjie.jpg')
      self.music.picture.setStyleSheet("QLabel{ background:#9B0069;border-image:url("+local+")}")
      
  # 播放状态改变
  def stateChanged(self):
    if self.music.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
      self.setPlayBtn('play11')
      if hasattr(self,'timer'):
        self.timer.stop()
      # print(self.lrcmap)
    elif self.music.player.state() == QMediaPlayer.PlayingState:
      self.setPlayBtn('pause11')
      if hasattr(self.music,'lrctext'):
        if self.music.lrctext.isVisible():
          if not hasattr(self,'timer'):
            self.timer = QTimer()
            self.timer.timeout.connect(self.refreshlrc)
        self.timer.start(100)
  # 歌词显示控制
  def showgeci(self,flag = None):
    # 检查播放状态
    if self.music.lrctext.isVisible():
      if not hasattr(self,'timer'):
        self.timer = QTimer()
        self.timer.timeout.connect(self.refreshlrc)
      self.timer.start(100)
    else:
      if hasattr(self,'timer'):
        self.timer.stop()

  def setPlayBtn(self,stat):
    self.music.playBtn.setStyleSheet("QPushButton{ border-image:url(image/%s.png);border:none }" % stat)
  def refreshlrc(self):
    # print(random.randint(0,99))
    if self.music.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
      return False
    # 当前播放的时间点
    k = int(self.songpro)
    if k in list(self.lrcmap.keys()):
      if self.lrcmap[k] != '':
        self.music.lrctext.setText(self.lrcmap[k])
    else:
      # pass
      i = 10
      while(i):
        i = i-1
        k = k - 1 
        if k in list(self.lrcmap.keys()):
          if self.lrcmap[k] != '':
            self.music.lrctext.setText(self.lrcmap[k])
            break


  

if __name__ == "__main__":
    # listfile = os.listdir(conf['mp3dir'])
    # for name in listfile:
    #   print(os.path.join(conf['mp3dir'],name))
    m = Player()
    # print("oooo")
