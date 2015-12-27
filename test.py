
import sys
import os
import urllib.parse
import urllib.request
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot,QTimer


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.w= QWidget(self)
        self.setGeometry(300,100,1000,600)
        self.web = QWebView(self)
        self.web.loadFinished.connect(self.test)
        
        self.web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.web.page().linkClicked.connect(self.linkClicked)

        self.web.setGeometry(0, 0, 1000, 500)
        self.btn = QPushButton("测试",self);
        self.btn.clicked.connect(self.test)
        self.btn.move(300,550)
        self.web.load(QUrl("http://image.baidu.com/"))
        self.show()
    def test(self):
        print("jiazaijieshu")
        frame = self.web.page().currentFrame()
        searchinput = frame.findFirstElement('#kw')
        searchinput.setAttribute("value","张杰")
        searchinput.setAttribute("readonly","readonly")
    def linkClicked(self,url):
        # print(url.toString())
        url = url.toString()
        pattern = re.compile(r'&word=(.*?)&')
        s = pattern.findall(url)
        k = {'word': s[0]}
        kv = urllib.parse.urlencode(k)
        url = url.replace("word="+s[0], kv)

        res = urllib.request.urlopen(url).read().decode("utf8")
        pattern = re.compile(r'currentImg(.*)<div>',re.S)
        s = pattern.findall(res)
        src="http://img3.imgtn.bdimg.com/it/u=673176467,634723054&amp;fm=21&amp;gp=0.jpg"
        pattern = re.compile(r'src="(.*?)"')
        s = pattern.findall(s[0])
        img_url = s[0].replace("&amp;","&")

        local = os.path.join('./cache/', '张杰.jpg')
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
        req = urllib.request.Request(img_url)
        req.add_header('Referer', 'http://music.baidu.com/?from=new_mp3')
        req.add_header('User-Agent', user_agent)
        f = urllib.request.urlopen(req)
        data = f.read() 
        with open(local, "wb") as code:     
            code.write(data)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # music = search()
    music = Example()
    # app.exec_()
    sys.exit(app.exec_())
