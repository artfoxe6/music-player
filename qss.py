#!/usr/bin/python3
# -*- coding: utf8 -*-
# 歌曲列表

qss_scrollbar = """

QWidget{ background:#F9F9F9 }
QScrollBar:vertical{width:4px;background:white; margin:0px,0px,0px,0px;padding-top:9px;  padding-bottom:9px;}
QScrollBar::handle:vertical{width:4px;background:#009BB7; border-radius:2px;  }
QScrollBar::handle:vertical:hover{width:4px;background:grey;border-radius:2px;}
QScrollBar::add-line:vertical {height:9px;width:4px;background:white;subcontrol-position:bottom;}
QScrollBar::sub-line:vertical {height:9px;width:4px;background:white;subcontrol-position:top;}
QScrollBar::add-line:vertical:hover {height:9px;width:4px;background:white;subcontrol-position:bottom;}
QScrollBar::sub-line:vertical:hover{ height:9px;width:4px; background:white;subcontrol-position:top; }
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical {background:white;border-radius:4px;} 

"""
qss_songlist = """

QListWidget{ background:#F9F9F9;font-size:12px;border:none;margin-left:0px;} 
QListWidget::item{ color:grey ;height:40px;margin-left:5px;}  

"""

"""
QListWidget::item{ color:grey ;height:40px;margin-left:5px;}  
QListWidget::item:hover{background:pink} 
QListWidget::item:selected{background:#E8FFE3;} 
"""

# 菜单
qss_menu = """

QListWidget{ background:#F9F9F9;color:red ;border:none;} 
QPushButton{ background:#F9F9F9;border:none;color:grey } 
QPushButton:hover{ background:pink;color:black }

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
    background: #EAD9EA;
    position: absolute;

}

QSlider::handle:horizontal {
    width: 0px;
    background:transparent;
    margin:0 0px;
}

QSlider::add-page:horizontal {
    background: #141414;
}

QSlider::sub-page:horizontal {
    background: #A70A0A;
    margin-left:0px;
}

"""

qss_vol = """

QSlider::groove:horizontal {
    background: #5FF199;
    position: absolute;
}

QSlider::handle:horizontal {
    width: 10px;
    background: white;
    margin:0 2px;
}

QSlider::add-page:horizontal {
    background: #5FF199;
}

QSlider::sub-page:horizontal {
    background: #5FF199;
    margin-left:2px;
}


"""