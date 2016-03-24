#!/usr/bin/python3
# -*- coding: utf8 -*-

from PyQt5.QtMultimedia import (QMediaPlayer, QMediaPlaylist, QMediaContent,QMediaMetaData)
from conf import conf
from PyQt5.QtCore import QUrl,Qt,QTime,QSize,QTimer
from PyQt5.QtWidgets import QListWidgetItem,QMenu,QAction,QWidget,QPushButton,QLabel,QDialog,QGraphicsColorizeEffect
from PyQt5.QtGui import QBrush,QIcon,QCursor,QColor
import os
import re
from mutagen.mp3 import MP3
from mywidget import listlabel,youjianWidget
import random

class Player():
  # 参数music是mainnwindow对象 
  def __init__(self,music):
    self.duration = 0  #当前歌曲时长
    self.music = music
    # self.music.setWindowFlags(Qt.X11BypassWindowManagerHint)
    self.lrcmap = {}
    self.filename = ""
    self.music.player = QMediaPlayer()
    self.music.player.setVolume(self.music.volslider.value())
    
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
    self.music.volslider.valueChanged.connect(self.songvol)

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
  def songvol(self,vl):
    self.music.player.setVolume(vl)
    # print(self.music.player.volume())
  def durationChanged(self,duration):
    # 清空前一首歌词
    self.lrcmap = {}
    duration /= 1000
    self.duration = duration
    self.music.processSlider.setMaximum(duration)
    # print(self.duration)
    # print(self.music.processSlider.maximum())
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
      # tStr = currentTime.toString(format) + " / " + totalTime.toString(format)
      tStr = currentTime.toString(format)
    else:
      Str = ""
    self.music.songTime.setText(tStr)

  def displayErrorMessage(self):
    print(self.music.player.errorString())
  def init_list(self):
    #读取配置歌曲目录里面的音乐文件
    try:
      listfile = os.listdir(conf['mp3dir'])
    except Exception:
      return False
    x = 0
    for name in listfile:
      # print(name)
      s = os.path.splitext(name)[1][1:]
      if(s.upper() == 'MP3'):
        x+=1
        songname = name[0:-4]
        item = QListWidgetItem()
        item.setFlags(Qt.NoItemFlags)

        item.setSizeHint(QSize(210,40))
        lwg = youjianWidget()
        

        lwg.deletesong.connect(self.deletesong)
        # print(dir(lwg))
        # return False
        # lwg.setObjectName("songlist")
        lwg.setGeometry(20,0,140,30)
        # lwg.setObjectName("songitem")
        # lwg.clicked.connect(self.playit)
        # lwg.setStyleSheet("QWidget#songitem:hover{background:#A448C4;margin-left:-5px} \
        #   QWidget#songitem{border-radius:0px;} \
        #   ")
        
        # 使用自定义list组件  响应自定义信号
        ql = listlabel()
        ql.setObjectName("songitem")
        ql.setText(songname)
        ql.setParent(lwg)
        ql.setGeometry(0,0,240,40)  #transparent
        ql.setStyleSheet("QLabel{ font-weight:100;color:#2D2D2D;background:transparent ;font-size:14px;padding-left:40px;} \
         QLabel:hover{ color:#fff;background:#A448C4  }")
        ql.doubleclicked.connect(self.playit)
        btn = QPushButton(str(x),ql)
        btn.setGeometry(5,8,24,24)
        btn.setStyleSheet("QPushButton{ border-radius:12px;background:#3698DB;color:#DDD;font-size:12px;font-weight:blod }")

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
    # 当前播放的文件索引
    currentindex = self.music.playlist.currentIndex()
    # x = self.music.songList.findChildren(QListWidgetItem,'',Qt.FindChildrenRecursively)
    # print(x)
    if self.music.player.isMetaDataAvailable(): 
      current_song_path = self.music.playlist.currentMedia().canonicalUrl().toString()
      #当前播放的是item index
      ci = self.music.playlist.currentIndex()
      # print(ci)
      playitem = self.music.songList.item(ci)
      # playitem.setSelected(True)
      songitemlabel = self.music.songList.findChildren(QLabel,'songitem',Qt.FindChildrenRecursively)
      # print(len(songitemlabel))
      # songitemlabel[0]
      # currentplay
      for x in songitemlabel:
        x.currentplay()
      songitemlabel[ci].currentplay(1)
      # print(dir(playitem))
      #把qt的路径格式转换为绝对路径
      audio = MP3(current_song_path[7:])
      # print(audio)
      # print(audio.get('TIT2'))  #歌名
      # print(audio.get('TPE1'))  #歌手
      # print(audio.get('TALB'))  #专辑
      # s = str(audio.get('TIT2'))+"-"+str(audio.get('TPE1'))
      # pos = audio.get('TIT2')
      # print(dir())
      # pos.encode("utf-8").decode("utf-8")
      # print(pos)
      sname = str(audio.get('TIT2'))
      if not sname or sname == 'None':
        sname = songitemlabel[ci].text()
      
      self.filename = sname
      ssinger = str(audio.get('TPE1'))
      if not ssinger or ssinger == 'None':
        ssinger = ""
      else:
        ssinger = " - "+ssinger
      # print(self.music.currentSonger)
      self.music.songname.setText(sname+" "+str(ssinger))
      
  # 播放状态改变
  def stateChanged(self):
    if self.music.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
      self.setPlayBtn('statusbar_btn_play')
      if hasattr(self,'timer'):
        self.timer.stop()
      # print(self.lrcmap)
    elif self.music.player.state() == QMediaPlayer.PlayingState:
      self.setPlayBtn('kg_ic_playing_bar_pause_pressed')
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
    self.music.playBtn.setStyleSheet("QPushButton{ border-image:url(image/newimg/"+stat+".png);border:none } QPushButton:hover{ border-image:url(image/newimg/"+stat+"_2.png)} ")
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
  def deletesong(self,index):
    item = self.music.songList.item(index-1)
    # print(index-1)
    
    # print(self.music.songList.count())
    allitem = self.music.songList.findChildren(QLabel,'songitem',Qt.FindChildrenRecursively)
    songpath = self.music.playlist.media(index-1).canonicalUrl().toString()
    # print(songpath[7:])
    self.music.playlist.removeMedia(index-1)
    self.music.songList.takeItem(index-1)
    # os.remove(songpath[7:])
    # QDialog().exec()
    # if not os.remove(songpath[7:]):
        # QDialog("cdcds").exec()
  

if __name__ == "__main__":
    # listfile = os.listdir(conf['mp3dir'])
    # for name in listfile:
    #   print(os.path.join(conf['mp3dir'],name))
    m = Player()
    # print("oooo")
