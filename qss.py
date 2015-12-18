#!/usr/bin/python3
# -*- coding: utf8 -*-
# 歌曲列表
qss_songlist = """

QListWidget{ background:white;font-size:12px;border:none;margin-left:10px;} 
QListWidget::item{ color:grey ;height:40px;}  
QListWidget::item:hover{background:#E8FFE3} 
QListWidget::item:selected{background:#E8FFE3;} 
QScrollBar:vertical{width:5px;background:white; margin:0px,0px,0px,0px;padding-top:9px;  padding-bottom:9px;}
QScrollBar::handle:vertical{width:5px;background:#A6D8F8; border-radius:2px;  }
QScrollBar::handle:vertical:hover{width:5px;background:grey;border-radius:2px;}
QScrollBar::add-line:vertical {height:9px;width:5px;background:white;subcontrol-position:bottom;}
QScrollBar::sub-line:vertical {height:9px;width:5px;background:white;subcontrol-position:top;}
QScrollBar::add-line:vertical:hover {height:9px;width:5px;background:white;subcontrol-position:bottom;}
QScrollBar::sub-line:vertical:hover{ height:9px;width:5px; background:white;subcontrol-position:top; }
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical {background:white;border-radius:4px;} 

"""
# 菜单
qss_menu = """

QListWidget{ background:white;color:red ;border:none;border-right:2px solid #EAD9EA} 
QPushButton{ background:white;border:none;color:grey } 
QPushButton:hover{ background:white;color:black }

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
    background: pink;
    position: absolute;
}

QSlider::handle:horizontal {
    width: 5px;
    background: white;
    margin:0 -5px;
}

QSlider::add-page:horizontal {
    background: white;
}

QSlider::sub-page:horizontal {
    background: pink;
}

"""