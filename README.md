# music-player

使用Python3＋Qt5做的音乐播放器

前言：

Linux下一直没找到我满意的音乐播放器（主要是界面老套）
所以就萌发了自己写一个播放器的念头
看了一下python(我本身是从事PHP的)，只了解基本语法，模块不熟悉。就开始自己动手做了，Qt之前也没有了解过

所以。各位在看代码的时候不要太挑剔了，限于对python和qt知识有限，写的较乱
还好的是逻辑是清晰的，代码按功能分割。



<h2 >软件截图</h2>
<img src="https://github.com/codeAB/music-player/blob/master/image/s2.png" />
<img src="https://github.com/codeAB/music-player/blob/master/image/s1.png" />
<img src="https://github.com/codeAB/music-player/blob/master/image/s3.png" />
<img src="https://github.com/codeAB/music-player/blob/master/image/s4.png" />
<img src="https://github.com/codeAB/music-player/blob/master/image/s5.png" />

<h2 >已知的BUG</h2>


部分intel集成显卡的电脑无法渲染滚动条样式<br>
不影响使用,滚动条稍微有点难看,待解决,

*部分机器缺少插件无法播放,提示 not found media server  <br>
解决办法：以ubuntu为例。 sudo apt-get install libqt5multimedia5-plugins


<h2>特色功能：</h2>

歌手封面定义 <br	>
拖动播放器到顶部自动隐藏，鼠标再次移上去显示，类似window下的酷狗 <br	>
桌面歌词 <br	>



