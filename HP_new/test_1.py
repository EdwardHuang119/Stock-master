#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from Tkinter import * # for Python2
except ImportError:
    from tkinter import * # for Python3
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk


root=tk.Tk()  #建立主窗口
root.title("My windoe")  #主窗口名字

screenWidth = root.winfo_screenwidth()  # 获取显示区域的宽度
screenHeight = root.winfo_screenheight()  # 获取显示区域的高度
width = 500  # 设定窗口宽度
height = 300  # 设定窗口高度
left = (screenWidth - width) / 2
top = (screenHeight - height) / 2
# root.geometry("500x300") #这里的乘号是小写x
root.geometry("%dx%d+%d+%d" % (width, height, left, top))
#这里是窗口内容
labels = []
for color in ['blue','black','red']:
    f = tk.Frame(root,borderwidth=1,bg='black')
    label=tk.Label(f,text=color,width=18,fg=color,bg='yellow',highlightcolor='white')
    label.pack(side=tk.LEFT)
    labels.append(label)
    f.pack(side=tk.LEFT)

# root.mainloop()  #主窗口循环显示

root=root.mainloop()
# root.SetCenter()  #移动到屏幕中央
# root.iconbitmap('ico/xb.ico')  #设置应用程序图标

#htk.thread_it(logo())  ##用多线程启动定时器