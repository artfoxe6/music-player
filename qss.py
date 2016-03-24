#!/usr/bin/python3
# -*- coding: utf8 -*-
# 歌曲列表

qss_scrollbar = """

QWidget{ background:#fff }
QScrollBar:vertical{width:2px;background:white; margin:0px,0px,0px,0px;padding-top:9px;  padding-bottom:9px;}
QScrollBar::handle:vertical{width:2px;background:#777; border-radius:2px;  }
QScrollBar::handle:vertical:hover{width:2px;background:#009BB7;border-radius:2px;}
QScrollBar::add-line:vertical {height:9px;width:2px;background:#fff;subcontrol-position:bottom;}
QScrollBar::sub-line:vertical {height:9px;width:2px;background:#fff;subcontrol-position:top;}
QScrollBar::add-line:vertical:hover {height:9px;width:2px;background:#fff;subcontrol-position:bottom;}
QScrollBar::sub-line:vertical:hover{ height:9px;width:2px; background:#fff;subcontrol-position:top; }
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical {background:#fff;border-radius:4px;} 

"""
qss_songlist = """

QListWidget{ background:#fff;font-size:12px;border:none;margin-left:0px;} 
QListWidget::item{ color:grey ;height:40px;margin-left:0px;}  

"""

"""
QListWidget::item{ color:red ;height:40px;margin-left:5px;}  
QListWidget::item:hover{color:red} 
QListWidget::item:selected{color:red;} 
QListWidget::item:checked{color:red;} 
"""

# 菜单  
# QPushButton:hover{ background:pink;color:black }
qss_menu = """

QListWidget{ background:#fff;color:red ;border:none; } 
QPushButton{ background:#fff;border:none;color:grey; } 


"""
# 进度
qss_process = """

QProgressBar{ background:pink;border:none } 
QProgressBar::chunk { background-color: #B4FFA3;  }

"""
# 音量
qss_process2 = """

QProgressBar{ background:transparent;border:none;border-radius:2px; } 
QProgressBar::chunk { background:transparent; border-radius:2px } 
QProgressBar:hover{background:#B4FFA3;} 
QProgressBar::chunk:hover{ background:pink }

"""

qss_process_slider = """

QSlider::groove:horizontal {
    background: transparent;
    position: absolute;
    margin-left:-1px
}

QSlider::handle:horizontal {
    width: 0px;
    background:transparent;
    margin:0 0px;
}

QSlider::add-page:horizontal {
    background: transparent;
}

QSlider::sub-page:horizontal {
    background: #888;
    border-radius:2px;
}

"""

qss_vol = """

QSlider::groove:horizontal {
    background: #A4A4A4;
    position: absolute;
    border-radius:2px;
}

QSlider::handle:horizontal {
    width: 10px;
    background: #CCC;
    margin:0 2px;
}

QSlider::add-page:horizontal {
    background: #A4A4A4;
    border-radius:2px;
}

QSlider::sub-page:horizontal {
    background: #A4A4A4;
    margin-left:2px;
    border-radius:2px;
}


"""

qss_rightmenu = """
    QMenu{ width:100px;border:none;padding:5px;background:#fff } QMenu::item{ background-color: transparent;width:70px;text-align:center;height:25px; margin:0px 0px;border-bottom:1px solid #EEE;padding-left:20px;color:#333 }  QMenu::item:selected{ color:red;border-bottom:1px solid pink;background:none; }
"""


qss_tray = """
QMenu{ width:100px;border:none;padding:5px;background:#fff; } QMenu::item{ background-color: transparent;width:70px;text-align:center;height:25px; margin:0px 0px;border-bottom:1px solid #EEE;padding-left:20px;color:#333 }  QMenu::item:selected{ color:red;border-bottom:1px solid pink;background:none; }

"""