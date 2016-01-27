# coding=utf-8

import re

# 加载歌词
filename = "mp3/后来.lrc"
# print(filename)
f = open(filename, "r")  
while True:
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
        # print(d)
        # 拆分时间点
        pattern2 = re.compile(r'[0-9]{2}:[0-9]{2}\.[0-9]{2}')
        s = pattern2.findall(d[0])
        for k in s:
            t = int(k[0]+""+k[1])*60+int(k[3]+""+k[4])-1
            print(str(t)+":"+c)
            # self.lrcmap[t] = c
    else:
        break
# pattern = re.compile(r'\[.*?\]')
# f = pattern.findall(s)
# print(f)
# print(len(f))