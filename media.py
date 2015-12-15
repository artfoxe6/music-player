#!/usr/bin/python3
# -*- coding: utf8 -*-

from PyQt5.QtMultimedia import ( QMediaPlayer, QMediaPlaylist,QMediaContent)




class Media(object):
	def __init__(self):
		self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
    #播放
	def play(self):
		self.player.play()
	def pause(self):
		self.player.pause()
	def main(self):
		pass
		# controls = PlayerControls()
  #       controls.setState(self.player.state())
  #       controls.setVolume(self.player.volume())
  #       controls.setMuted(controls.isMuted())

  #       controls.play.connect(self.player.play)
  #       controls.pause.connect(self.player.pause)
  #       controls.stop.connect(self.player.stop)
  #       controls.next.connect(self.playlist.next)
  #       controls.previous.connect(self.previousClicked)
  #       controls.changeVolume.connect(self.player.setVolume)
  #       controls.changeMuting.connect(self.player.setMuted)
  #       controls.changeRate.connect(self.player.setPlaybackRate)
  #       controls.stop.connect(self.videoWidget.update)

