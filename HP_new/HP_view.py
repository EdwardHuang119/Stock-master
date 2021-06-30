# -*- coding: utf-8 -*-
"""
#功能：小白股票分析软件框架窗口模块
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2018年9月14日
#主程序：HP_main.py
"""


#from pandas import DataFrame, Series
import time
import threading, time
import pandas as pd
import numpy as np
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
import matplotlib.ticker as ticker# 先设定一个日期转换方法
#from matplotlib.finance import candlestick_ohlc  #matplotlib2.0.0用
# from mpl_finance import candlestick_ohlc #matplotlib3.0.0用
from mplfinance.original_flavor import candlestick_ohlc
#from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
#from matplotlib.dates import MonthLocator,MONTHLY
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTk,NavigationToolbar2Tk  #matplotlib 2.0.2 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)    ##matplotlib 3.0.2 
#matplotlib.use('TkAgg')  #只有matplotlib 2.0.2需要，高版本可不用设置
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor

import datetime as dt
#import time
#import pylab
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Frame
from PIL import Image, ImageTk, ImageDraw, ImageFont
#import threading
#import HP_zwdata as sd
#import jqdatasdk as jq   #聚宽数据包
import HP_global as g 
#from HP_set import *
import HP_lib as mylib
import HP_draw as mydraw
import HP_data as hp
from  HP_draw import *

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def RGB(color):
    r=eval('0x'+color[1:3])
    g=eval('0x'+color[3:5])
    b=eval('0x'+color[5:7])
    return r,g,b
    
def drawFont (im,x,y,txt,size=30,r=255,g=255,b=255): #显示汉字
    #im图像对象,坐标(x,y),txt文字,size字体大小;颜色r,j,b=0-255
    font = ImageFont.truetype("simfang.ttf", size)
	#font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simfang.ttf", 40)    
    draw = ImageDraw.Draw(im)
    draw.ink = r + 256*g + 256*256*b
    draw.text((x, y), txt, font=font)

def drawFont2 (im,x,y,txt,size=30,r=255,g=255,b=255): #显示汉字
    #im图像对象,坐标(x,y),txt文字,size字体大小;颜色r,j,b=0-255
    font = ImageFont.truetype("SIMLI.TTF", size)
	#font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simfang.ttf", 40)    
    draw = ImageDraw.Draw(im)
    draw.ink = r + 256*g + 256*256*b
    draw.text((x, y), txt, font=font)

def drawFont3(im,x,y,txt,size=30,r=255,g=255,b=255): #显示汉字
    #im图像对象,坐标(x,y),txt文字,size字体大小;颜色r,j,b=0-255
    font = ImageFont.truetype("STXINGKA.TTF", size)
	#font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simfang.ttf", 40)    
    draw = ImageDraw.Draw(im)
    draw.ink = r + 256*g + 256*256*b
    draw.text((x, y), txt, font=font)

    
def resize(w, h, w_box, h_box, pil_image):  
  ''' 
  resize a pil_image object so it will fit into 
  a box of size w_box times h_box, but retain aspect ratio 
  对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例 
  '''  
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
  f2 = 1.0*h_box/h  
  factor = min([f1, f2])  
  #print(f1, f2, factor) # test  
  # use best down-sizing filter  
  width = int(w*factor)  
  height = int(h*factor)  
  return pil_image.resize((width, height), Image.ANTIALIAS)  



###############
#             #
#     1       #
#             #
###############
class view1(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.m=1
        self.v=[]
        self.v1=tk.Frame(self)
        self.v1.pack(side=tk.TOP, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)


###############
#     1       #
###############
#     2       #
###############
class view2(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.m=2
        self.v=[]
        self.v1=tk.Frame(self)
        self.v2=tk.Frame(self)
        self.v1.pack(side=tk.TOP, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)

################
#      #       #
#   1  #   2   #
#      #       #
################
class view2b(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.m=2
        self.v=[]
        self.v1=tk.Frame(self)
        self.v2=tk.Frame(self)
        self.v1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)


################
#      #       #
#   1  #   2   #
#      #       #
################
class view2c(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.m=2
        self.v=[]
        self.v1=tk.Frame(self,relief=tk.SUNKEN,bg='blue')
        self.v2=tk.Frame(self,relief=tk.SUNKEN,bg='green',width = 240)
        self.v1.grid(row = 0, column = 0,sticky=tk.NSEW,columnspan=3)
        self.v2.grid(row = 0, column = 4,sticky=tk.NSEW,columnspan=1)
        self.v.append(self.v1)
        self.v.append(self.v2)


###############
#     1       #
###############
#     2       #
###############
class view2d(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master,bd=0)  
        self.root = master #定义内部变量root  
        self.m=2
        self.v=[]
        self.v1=tk.Frame(self,relief=tk.SUNKEN,bg='black',height=240,bd=0)
        self.v2=tk.Frame(self,relief=tk.SUNKEN,bg='black',bd=0)
        self.v1.pack(side=tk.TOP, fill=tk.Y)
        self.v2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)


###############
#  1  #   2   #
###############
#     3       #
###############
class view3(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.m=3
        self.v=[]
        self.vm=tk.Frame(self)
        self.v1=tk.Frame(self.vm)
        self.v2=tk.Frame(self.vm)
        self.v3=tk.Frame(self)
        
        self.vm.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.v3.pack(side=tk.BOTTOM,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)        
        self.v1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v2.pack(side=tk.RIGHT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)
        self.v.append(self.v3)

###############
#     1       #
###############
#   2  #  3  #
##############
class view3b(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.m=3
        self.v=[]
        self.v1=tk.Frame(self)
        self.vm=tk.Frame(self)
        self.v2=tk.Frame(self.vm)
        self.v3=tk.Frame(self.vm)
        self.v1.pack(side=tk.TOP, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.vm.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.v2.pack(side=tk.LEFT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v3.pack(side=tk.RIGHT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)
        self.v.append(self.v3)

###############
#  1  #   2   #
###############
#  3  #   4   #
###############
class view4(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.m=4
        self.v=[]
        self.vm1=tk.Frame(self)
        self.vm2=tk.Frame(self)
        self.v1=tk.Frame(self.vm1)
        self.v2=tk.Frame(self.vm1)
        self.v3=tk.Frame(self.vm2)
        self.v4=tk.Frame(self.vm2)
        
        self.vm1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.vm2.pack(side=tk.BOTTOM,expand=1,fill=tk.BOTH)        
        self.v1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v2.pack(side=tk.RIGHT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v3.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v4.pack(side=tk.RIGHT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)
        self.v.append(self.v3)
        self.v.append(self.v4)


#状态栏
class StatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='0000').place(x=0, y=0, relwidth=1,bordermode=tk.OUTSIDE)
        self.m=6  #有6个子栏
        self.l=[]
        self.l1 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.CENTER,width=7,text='状态栏',justify=tk.CENTER)
        self.l1.pack(side=tk.LEFT,padx=1,pady=1)
        self.l.append(self.l1)
        self.l2 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,width=20,text='2')
        self.l2.pack(side=tk.LEFT,padx=1,pady=1)
        self.l.append(self.l2)
        self.l3 = tk.Label(self, bd=1, anchor=tk.W,relief=tk.SUNKEN,text='3')
        self.l3.pack(side=tk.LEFT,fill=tk.X)
        self.l.append(self.l3)
        self.l4 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,width=10,text='6')
        self.l4.pack(side=tk.RIGHT,padx=1,pady=1)
        self.l5 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,width=10,text='5')
        self.l5.pack(side=tk.RIGHT,padx=1,pady=1)
        self.l6 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,width=10,text='4')
        self.l6.pack(side=tk.RIGHT,padx=2,pady=1)
        self.l.append(self.l6)
        self.l.append(self.l5)
        self.l.append(self.l4)
    
    def text(self,i,t): #输出文字信息
        self.l[i].config(text=t)
        self.l[i].update_idletasks()
        
    def config(self,i,**kargs):  #配置长度 和 颜色
        for x,y in kargs.items():
            if x=='text':
                self.l[i].config(text=y)
            if x=='color':
                self.l[i].config(fg=y)        
            if x=='width':
                self.l[i].config(width=y)        

    def clear(self):  #清除所有信息
        for i in range(0,self.m):
            self.l[i].config(text='')
            self.l[i].update_idletasks()


    def set(self,i, format, *args):   #输出格式信息
        self.l[i].config(text=format % args)
        self.l[i].update_idletasks()


#定义我的窗口基类
class myWindow:
    def __init__(self, root, myTitle,w=300, h=200):
        self.width=w
        self.height=h
        self.top = Toplevel(root, width=w, height=h)
        self.top.title(myTitle)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False

    def destroy(self):
        #销毁应用程序窗口
        self.top.destroy()   

    def overturn(self):
        self.top.update_idletasks()
        self.top.overrideredirect(self.flag)
        self.flag=not self.flag #switch

    #移动窗口到屏幕中央       
    def setCenter(self,w,h):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int( (ws/2) - (w/2) )
        y = int( (hs/2) - (h/2) )
        self.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    
    #移动窗口到屏幕坐标x,y       
    def setPlace(self,x, y,w,h):
        self.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    
    
    #显示窗口ico图标
    def showIco(self,Ico):
        self.iconbitmap(Ico)    
    
    #是否禁止修改窗口大小
    def reSizable(self,x,y):
        self.resizable(x, y)   #是否禁止修改窗口大小



#移动窗口到屏幕中央       
def setCenter(root,w,h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int( (ws/2) - (w/2) )
    y = int( (hs/2) - (h/2) )
    root.geometry('{}x{}+{}+{}'.format(w, h, x, y))

#移动窗口到屏幕坐标x,y       
def setPlace(root,x, y,w,h):
    root.geometry('{}x{}+{}+{}'.format(w, h, x, y))


#显示窗口ico图标
def showIco(root,Ico):
    root.iconbitmap(Ico)    

#是否禁止修改窗口大小
def reSizable(root,x,y):
    root.resizable(x, y)   #是否禁止修改窗口大小


def axview1(v,df,t,n=2):
    #显示K线,带6条均线
    df2=df.copy()
    #date_tickers=df2['date']  #刻度值
    # 生成横轴的刻度名字
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax=plt.subplot(fc=g.ubg)
    #fig, ax = plt.subplots()
    days = df2.reindex(columns=['date','open','high','low','close'])   

    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  

#    ax.set_xticks(range(len(date_tickers)))
#    ax.set_xticklabels(date_tickers)
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
    if n>=3:
        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    if n>=4:
        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
    if n>=5:
        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
    if n>=6:
        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    #ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.06, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax

def axview1a(v,df,t):
    #无均线 K线图
    df2=df.copy()
    #date_tickers=df2['date']  #刻度值
    # 生成横轴的刻度名字
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax=plt.subplot(fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))      
#    ax.set_xticks(range(len(date_tickers)))
#    ax.set_xticklabels(date_tickers)
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.grid(True, color='r')
    #ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    #plt.legend() # 显示图中右上角的提示信息。
    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.06, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax

def axview1b(v,df,t):
    #叠加成交量的均线
    df2=df.copy()
    #date_tickers=df2['date']  #刻度值
    # 生成横轴的刻度名字
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax=plt.subplot(fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))   
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    ax.grid(True, color='r')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    plt.suptitle(t,color=g.ufg)
    
    ax0 = ax.twinx()
    ax0.tick_params(axis='y', colors=g.ufg)
    v1=mylib.g.MA(df2['volume'],g.MA1)
    v2=mylib.g.MA(df2['volume'],g.MA2)
    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    ax0.plot(days.date.values, v1, rsiCol, linewidth=1,label="$MA5$", alpha=.5)
    ax0.plot(days.date.values, v2, posCol, linewidth=1,label="$MA10$", alpha=.5)
    ax0.bar(days.date.values,df2.volume.values, facecolor='#386d13', alpha=.5)
    ax0.yaxis.label.set_color(g.ufg)
    
    ax0.tick_params(axis='y', colors=g.ufg)
    ax0.tick_params(axis='x', colors=g.ufg)
    ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
    ax0.tick_params(axis='x', colors=g.ufg)    
    
    plt.subplots_adjust(left=.06, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax

def axview1c(v,df,t):
    #叠加成交密度的K线
    df2=df.copy()
    #df2.dropna(inplace=True)  #删除无效数据
    dfmax=df2.close.max()
    dfmin=df2.close.min()
    l=len(df2)
    if l<80:
        l=int(l/2)
    else:
        l=40
        
    a=(dfmax-dfmin)/l
    x=dfmin
    mm=[]
    while x<=dfmax:
        mm.append(x)
        x+=a

    mma=pd.Series( mm,name='m')
    df4=mma.to_frame('p')
    df4['v']=0
    for i in df2.index:
        j=int((df2.close.loc[i]-dfmin)/a)
        if j>=l:
            j-=1
        df4.v.loc[j]=df4.v.loc[j]+df2.close.loc[i]

    # 生成横轴的刻度名字
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax=plt.subplot(fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    ax.grid(True, color='r')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    plt.suptitle(t,color=g.ufg)
   
    ax0 = ax.twiny()
    ax0.barh(df4.p,df4.v, height=0.05, align='center', color='#ACACAC', alpha=.6)
    #ax0.yaxis.label.set_color(g.ufg)
    #ax0.tick_params(axis='y', colors=g.ufg)
    #ax0.tick_params(axis='x', colors=g.ufg)
    ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
    
    
    plt.subplots_adjust(left=.065, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax


def axview2t(v,df,t,n=2):
    #显示K线,带6条均线
    data=df.copy()
    data.sort_values(by='date',ascending=True,inplace=True)
    df2=df.copy()
    df2.sort_values(by='date',ascending=True,inplace=True)
    del df2['date']   
    df2['date']=df2.index
    days =df2.reindex(columns=['date','open','high','low','close'])  
    data=data[['date','open','close','high','low','volume']]

    # 生成横轴的刻度名字
    date_tickers=data.date.values
    
    weekday_quotes=[tuple([i]+list(quote[1:])) for i,quote in enumerate(data.values)]
   

    ma5=pd.Series.rolling(data.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(data.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    #ax=plt.subplot(fc=g.ubg)
    ax = plt.subplot2grid((7,4), (0,0), rowspan=5, colspan=4, fc=g.ubg)


    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))    
    #candlestick_ohlc(ax,weekday_quotes,colordown='#53c156', colorup='#ff1717',width=0.2)
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')  
    
#    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
#    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
#    if n>=3:
#        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
#        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
#    if n>=4:
#        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
#        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
#    if n>=5:
#        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
#        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
#    if n>=6:
#        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
#        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    #ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    
    ax1=plt.subplot2grid((7,4), (5,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ax2=ax_VOL1t(ax1,data) 
    ax.yaxis.label.set_color(g.ufg)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))

    
    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1,padx=2,pady=2)
    return ax


def axview2(v,df,t,n=2):
    #显示K线,带6条均线
    df2=df.copy()
    #date_tickers=df2['date']  #刻度值
    # 生成横轴的刻度名字
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    #ax=plt.subplot(fc=g.ubg)
    ax = plt.subplot2grid((7,4), (0,0), rowspan=5, colspan=4, fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  

    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
    if n>=3:
        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    if n>=4:
        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
    if n>=5:
        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
    if n>=6:
        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    #candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')  
    ax1=plt.subplot2grid((7,4), (5,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ax2=ax_VOL(ax1,df2) 
    
    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口

#    global myly,mylx,canvas    
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
#    w1=800
#    h1=600
#    w2=int(w1/2)
#    h2=int(h1/2)
#    print(w2,h2)
#    myly=canvas.create_line(0,h2,w1,h2,fill ="blue",dash =(4,4))
#    mylx=canvas.create_line(w2,0,w2,h1,fill ="red",dash =(4,4))
    
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax


def axview2b(v,df,t,n=2):
    #叠加成交密度的K线
    df2=df.copy()
    #df2.dropna(inplace=True)  #删除无效数据
    dfmax=df2.close.max()
    dfmin=df2.close.min()
    l=len(df2)
    if l<80:
        l=int(l/2)
    else:
        l=40
        
    a=(dfmax-dfmin)/l
    x=dfmin
    mm=[]
    while x<=dfmax:
        mm.append(x)
        x+=a

    mma=pd.Series( mm,name='m')
    df4=mma.to_frame('p')
    df4['v']=0
    for i in df2.index:
        j=int((df2.close.loc[i]-dfmin)/a)
        if j>=l:
            j-=1
        df4.v.loc[j]=df4.v.loc[j]+df2.close.loc[i]
        
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax = plt.subplot2grid((7,4), (0,0), rowspan=5, colspan=4, fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
    if n>=3:
        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    if n>=4:
        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
    if n>=5:
        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
    if n>=6:
        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    
    ax0 = ax.twiny()
    ax0.barh(df4.p,df4.v, height=0.05, align='center', color='#ACACAC', alpha=.6)
    #ax0.yaxis.label.set_color(g.ufg)
    #ax0.tick_params(axis='y', colors=g.ufg)
    #ax0.tick_params(axis='x', colors=g.ufg)
    ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=8, prune='upper'))
    
    ax1=plt.subplot2grid((7,4), (5,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ax2=ax_VOL(ax1,df2) 
    
    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax

#其中参数v是tkinter的子窗口id，df是股票数据库。
#t是ax画面标题，f是指标名称，例如VOL，KDJ，MACD等等。
def axview2x(v,df,t,n=2,f='VOL'):
    #叠加成交密度的K线
    df2=df.copy()
    #df2.dropna(inplace=True)  #删除无效数据
    dfmax=df2.close.max()
    dfmin=df2.close.min()
    l=len(df2)
    if l<80:
        l=int(l/2)
    else:
        l=40
        
    a=(dfmax-dfmin)/l
    x=dfmin
    mm=[]
    while x<=dfmax:
        mm.append(x)
        x+=a

    mma=pd.Series( mm,name='m')
    df4=mma.to_frame('p')
    df4['v']=0
    for i in df2.index:
        j=int((df2.close.loc[i]-dfmin)/a)
        if j>=l:
            j-=1
        df4.v.loc[j]=df4.v.loc[j]+df2.close.loc[i]
        
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax = plt.subplot2grid((7,4), (0,0), rowspan=5, colspan=4, fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
    if n>=3:
        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    if n>=4:
        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
    if n>=5:
        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
    if n>=6:
        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    
    ax0 = ax.twiny()
    ax0.barh(df4.p,df4.v, height=0.05, align='center', color='#ACACAC', alpha=.6)
    #ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
    
    ax1=plt.subplot2grid((7,4), (5,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ss='ax2=ax_'+f.strip()+'(ax1,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax


#鼠标事件
def OnClick(event):
    global Coords1x,Coords1y
    global Coords3x,Coords3y
    #ax = plt.gca()
    if event.button ==1:
        Coords1x = event.xdata
        Coords1y = event.ydata
    if event.button == 3:
        Coords3x = event.xdata
        Coords3y = event.ydata
        
def OnMouseMotion(event):
    global Coords2x,Coords2y,x1,y1
    if event.button == 1:
        Coords2x = event.xdata
        Coords2y = event.ydata
        x1 = [Coords1x,Coords2x]
        y1 = [Coords1y,Coords2y]
        ax = plt.gca()
        lines = ax.plot(x1,y1,picker = 20)
        ax.figure.canvas.draw()
        #删除之前的线条，进行更新
        l = lines.pop(0)
        l.remove()
        del l
    elif event.button == 3:
        Coords4x = event.xdata
        Coords4y = event.ydata
        x2 = [Coords3x,Coords4x]
        y2 = [Coords3y,Coords4y]
        ax1 = plt.gca()
        #lines = ax1.plot(x1,y1,picker = 5)
        lines1 = ax1.plot(x2,y2,picker = 20)
        ax1.figure.canvas.draw()
        #删除之前的线条，进行更新
        l = lines1.pop(0)
        l.remove()
        del l





def axview3x_m(v,df,t,n=2,f1='VOL',f2='MACD'):
    #叠加成交密度的K线
    df2=df.copy()
    #df2.dropna(inplace=True)  #删除无效数据
    #df2.date=df2.date.astype('str')
    date_tickers=df2.date.values
    for i in range(len(date_tickers)):
        date_tickers[i]=date_tickers[i][11:16]
    #date_tickers.insert(0,'09:30')
    date_tickers=np.insert(date_tickers, 0, values='09:30', axis=0)
    df2['ma']=0.0
    va=0
    pa=0
    maa=[]
    for i in df2.index:
        va=va+df2.at[i,'volume']
        pa=pa+df2.at[i,'volume']*df2.at[i,'close']
        j=round(pa/va,4)
        maa.append(j)
    df2['ma']=maa
    #print(df2.ma)    
    date_tickers2=[]
    for dm in date_tickers:
        #dm=dm3.astype('str')
        dm2=dm[0:10]+' '+dm[11:16]
        #print(dm2,type(dm2))
        date_tickers2.append(dm2)
    date_tickers=date_tickers2.copy()    
    #print(date_tickers)
    del df2['date']   
    df2['date']=df2.index
#    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
#    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]
    
    #print(date_tickers)
    text = ax.text(0.5, 0.5, 'event', ha='center', va='center', fontdict={'size': 20})
    ax.xaxis.set_major_locator(mticker.MaxNLocator(9))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    #candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156') 
    ax.plot(days.date.values,days.close.values,label='close', linewidth=1.5,color='y')     
    ax.plot(days.date.values,df2.ma.values,label='MA', linewidth=1.5,color='w')
    ax.grid(True, color='r')
    #ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    

    ax1=plt.subplot2grid((7,4), (4,0),sharex=ax,rowspan=1, colspan=4, fc=g.ubg)
    ss='axx1=ax_'+f1.strip()+'(ax1,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    ax2 =plt.subplot2grid((7,4), (5,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ss='axx2=ax_'+f2.strip()+'(ax2,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.98, wspace=.15, hspace=0.01)

    #plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#    toolbar =NavigationToolbar2Tk(canvas, v)
#    toolbar.update()

#    menubar=tk.Menu(v)
#    toolbarName2 = ('日线图','分时图')
#    toolbarCommand2 = (None,None)
#    def addPopButton(name,command):
#        for (toolname ,toolcom) in zip(name,command):
#            menubar.add_command(label=toolname,command=toolcom)
#
#    def pop(event):
##        print(g.root.winfo_rootx(),g.root.winfo_rooty())
##        print(g.root.winfo_x(),g.root.winfo_y())
#        if event.button==3:
#            # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
#            ws = g.root.winfo_screenwidth() #获取屏幕宽度
#            hs = g.root.winfo_screenheight() #获取屏幕高度
#            w2=g.root.winfo_width()   #获取窗口宽度（单位：像素）
#            h2=g.root.winfo_height()  #获取窗口高度（单位：像素）
#            x2 = int( (ws/2) - (w2/2) )+event.x
#            y2 = int( (hs/2) - (h2/2) )+h2-event.y
#            x3=g.root.winfo_x()+event.x
#            y3=g.root.winfo_y()+h2-event.y
#            #menubar.post(event.x_root,event.y_root)
#            menubar.post(x3,y3)

    #addPopButton(toolbarName2,toolbarCommand2) #创建弹出菜单
    #self.tree.bind("<Button-3>",pop)


#    text = ax2.text(0.5, 0.5, 'event', ha='center', va='center', fontdict={'size': 20},color='yellow')
#    def call_back(event):
#        info = 'name:{}\n button:{}\n x,y:{},{}\n xdata,ydata:{}{}'.format(event.name, event.button,event.x, event.y,event.xdata, event.ydata)
#        print(info)
        #text.set_text(info)
        #canvas.draw_idle()    
    ##关联鼠标点击事件
#    fig.canvas.mpl_connect('button_press_event',OnClick)
#    fig.canvas.mpl_connect('motion_notify_event',OnMouseMotion)
    #canvas.mpl_connect('button_press_event', call_back)
    #canvas.mpl_connect('button_release_event', pop)
    #canvas.mpl_connect('motion_notify_event', call_back)    
   
#    # Set cursor        
#    cursor = Cursor(v, useblit=False, color='red', linewidth=1)
#    def onclick(event):
#        cursor.onmove(event)
#    canvas.mpl_connect('button_press_event', onclick)
    
    plt.close() # 关窗口
    
    return ax


def axview3x(v,df,t,n=2,f1='VOL',f2='MACD'):
    #叠加成交密度的K线
    df2=df.copy()
    #df2.dropna(inplace=True)  #删除无效数据
#    dfmax=df2.close.max()
#    dfmin=df2.close.min()
#    l=len(df2)
#    if l<80:
#        l=int(l/2)
#    else:
#        l=40
#        
#    a=(dfmax-dfmin)/l
#    x=dfmin
#    mm=[]
#    while x<=dfmax:
#        mm.append(x)
#        x+=a
#
#    mma=pd.Series( mm,name='m')
#    df4=mma.to_frame('p')
#    df4['v']=0
#    for i in df2.index:
#        j=int((df2.close.loc[i]-dfmin)/a)
#        if j>=l:
#            j-=1
#        df4.v.loc[j]=df4.v.loc[j]+df2.close.loc[i]
        
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
    if n>=3:
        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    if n>=4:
        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
    if n>=5:
        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
    if n>=6:
        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    #ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    
#    ax0 = ax.twiny()
#    ax0.barh(df4.p,df4.v, height=0.05, align='center', color='#ACACAC', alpha=.6)
#    ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
    
    ax1=plt.subplot2grid((7,4), (4,0),sharex=ax,rowspan=1, colspan=4, fc=g.ubg)
    ss='axx1=ax_'+f1.strip()+'(ax1,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    ax2 =plt.subplot2grid((7,4), (5,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ss='axx2=ax_'+f2.strip()+'(ax2,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax

def axview3x2(v,df,t,n=2,f1='VOL',f2='MACD'):
    #叠加成交密度的K线
    df2=df.copy()
       
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
    ax.tick_params(axis='y', colors=g.ufg)
    #ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
    if n>=3:
        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    if n>=4:
        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
    if n>=5:
        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
    if n>=6:
        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    #ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    
    ax1=plt.subplot2grid((7,4), (4,0),sharex=ax,rowspan=1, colspan=4, fc=g.ubg)
    ax1.tick_params(axis='y', colors=g.ufg)
    ss='axx1=ax_'+f1.strip()+'(ax1,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    ax2 =plt.subplot2grid((7,4), (5,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)

    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
#    #plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax,ax2


def axview4x(v,df,t,n=2,f1='VOL',f2='MACD',f3='KDJ'):
    #叠加成交密度的K线
    df2=df.copy()
    #df2.dropna(inplace=True)  #删除无效数据
#    dfmax=df2.close.max()
#    dfmin=df2.close.min()
#    l=len(df2)
#    if l<80:
#        l=int(l/2)
#    else:
#        l=40
#        
#    a=(dfmax-dfmin)/l
#    x=dfmin
#    mm=[]
#    while x<=dfmax:
#        mm.append(x)
#        x+=a
#
#    mma=pd.Series( mm,name='m')
#    df4=mma.to_frame('p')
#    df4['v']=0
#    for i in df2.index:
#        j=int((df2.close.loc[i]-dfmin)/a)
#        if j>=l:
#            j-=1
#        df4.v.loc[j]=df4.v.loc[j]+df2.close.loc[i]
        
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax = plt.subplot2grid((9,4), (0,0), rowspan=4, colspan=4, fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
    if n>=3:
        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    if n>=4:
        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
    if n>=5:
        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
    if n>=6:
        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    
#    ax0 = ax.twiny()
#    ax0.barh(df4.p,df4.v, height=0.05, align='center', color='#ACACAC', alpha=.6)
#    ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
    
    ax1=plt.subplot2grid((9,4), (4,0),sharex=ax,rowspan=1, colspan=4, fc=g.ubg)
    ss='axx1=ax_'+f1.strip()+'(ax1,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    ax2 =plt.subplot2grid((9,4), (5,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ss='axx2=ax_'+f2.strip()+'(ax2,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    ax3 =plt.subplot2grid((9,4), (7,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ss='axx3=ax_'+f3.strip()+'(ax3,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax


def axview5x(v,df,t,n=2,f1='VOL',f2='MACD',f3='KDJ',f4='RSI'):
    #叠加成交密度的K线
    df2=df.copy()
    #df2.dropna(inplace=True)  #删除无效数据
#    dfmax=df2.close.max()
#    dfmin=df2.close.min()
#    l=len(df2)
#    if l<80:
#        l=int(l/2)
#    else:
#        l=40
#        
#    a=(dfmax-dfmin)/l
#    x=dfmin
#    mm=[]
#    while x<=dfmax:
#        mm.append(x)
#        x+=a
#
#    mma=pd.Series( mm,name='m')
#    df4=mma.to_frame('p')
#    df4['v']=0
#    for i in df2.index:
#        j=int((df2.close.loc[i]-dfmin)/a)
#        if j>=l:
#            j-=1
#        df4.v.loc[j]=df4.v.loc[j]+df2.close.loc[i]
        
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    fig = plt.figure(facecolor=g.ubg,figsize=(1,1))
    ax = plt.subplot2grid((10,4), (0,0), rowspan=3, colspan=4, fc=g.ubg)
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
    ax.tick_params(axis='y', colors=g.ufg)
    ax.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    candlestick_ohlc(ax, days.values, width=.6, colorup='#ff1717', colordown='#53c156')      
    ax.plot(days.date.values,ma5,label='MA5', linewidth=1.5)
    ax.plot(days.date.values,ma10,label='MA10', linewidth=1.5)
    if n>=3:
        ma20=pd.Series.rolling(df2.close, 20).mean() #股票收盘价20日平均线 
        ax.plot(days.date.values,ma20,label='MA20', linewidth=1.5)
    if n>=4:
        ma30=pd.Series.rolling(df2.close, 30).mean() #股票收盘价30日平均线 
        ax.plot(days.date.values,ma30,label='MA30', linewidth=1.5)
    if n>=5:
        ma60=pd.Series.rolling(df2.close, 60).mean() #股票收盘价60日平均线 
        ax.plot(days.date.values,ma60,label='MA60', linewidth=1.5)
    if n>=6:
        ma120=pd.Series.rolling(df2.close, 120).mean() #股票收盘价120日平均线 
        ax.plot(days.date.values,ma120,label='MA120', linewidth=1.5)    
    ax.grid(True, color='r')
    #ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    
#    ax0 = ax.twiny()
#    ax0.barh(df4.p,df4.v, height=0.05, align='center', color='#ACACAC', alpha=.6)
#    ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
    
    ax1=plt.subplot2grid((10,4), (3,0),sharex=ax,rowspan=1, colspan=4, fc=g.ubg)
    ss='axx1=ax_'+f1.strip()+'(ax1,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    ax2 =plt.subplot2grid((10,4), (4,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ss='axx2=ax_'+f2.strip()+'(ax2,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    ax3 =plt.subplot2grid((10,4), (6,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ss='axx3=ax_'+f3.strip()+'(ax3,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))

    ax4 =plt.subplot2grid((10,4), (8,0),sharex=ax,rowspan=2, colspan=4, fc=g.ubg)
    ss='axx4=ax_'+f4.strip()+'(ax4,df2)'
    try:
        exec(ss)
    except Exception as e:
        print('用户代码'+ss+'出错:', str(e))
    plt.suptitle(t,color=g.ufg)
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    plt.close() # 关窗口
    canvas =FigureCanvasTkAgg(fig, master=v)  # 设置tkinter绘图区
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return ax

def ax_radar(ax,labels_,data_,label_='雷达图'):
    #ax=plt.subplot(fc='yellow', polar=True)
    #=======自己设置开始============
    #标签
    labels = np.array(labels_)
    #数据个数
    dataLenth = 6
    #数据
    data = np.array(data_)
    n = len(labels)
    #========自己设置结束============
    
    
    angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False)
    data = np.concatenate((data, [data[0]])) # 闭合
    angles = np.concatenate((angles, [angles[0]])) # 闭合
    

    #ax.plot(angles, data, 'bo-', linewidth=2,label='股票综合分析')# 画线
    ax.plot(angles, data, 'bo-', linewidth=2,label=label_)# 画线
    ax.fill(angles, data, facecolor='r', alpha=0.25)# 填充

    ax.set_thetagrids(angles * 180/np.pi, labels, fontproperties="SimHei",color='yellow')
    #ax.set_title("股票六芒星", va='bottom', fontproperties="SimHei")
    ax.set_rlim(0,10)
    ax.grid(True)
    
    
    # 自己画grid线（5条环形线）
    for i in [2,4,6,8,10]:
        ax.plot(angles, [i]*(n+1), 'b-',lw=0.5) # 之所以 n +1，是因为要闭合！
    
    # 填充底色
    ax.fill(angles, [10]*(n+1), facecolor='g', alpha=0.5)
    
    # 自己画grid线（6条半径线）
    for i in range(n):
        ax.plot([angles[i], angles[i]], [0, 10], 'b-',lw=0.5)
        
    ax.fill(angles, data, facecolor='r')
    
    plt.legend(loc='lower right', bbox_to_anchor=(1.3, 0.0)) # 设置图例的位置，在画布外
    ax.set_theta_zero_location('N')        # 设置极坐标的起点（即0°）在正北方向，即相当于坐标轴逆时针旋转90°
    ax.spines['polar'].set_visible(False)  # 不显示极坐标最外圈的圆
    ax.grid(False)                         # 不显示默认的分割线
    ax.set_yticks([])                      # 不显示坐标间隔
    #ax.spines['left'].set_posttion(('axes',0.35))


class plotFrame1(Frame): # 继承Frame类  
    def __init__(self, master,df,stn):  

        self.df1=df
        self.stockn=stn
        self.canvas=None
        self.root = master #定义内部变量root 
        
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.createPage()  
   
    def createPage(self):  
        df2=self.df1.copy()
        df2.dropna(inplace=True)
        df2.insert(0,'date',df2.index)
        df2=df2.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        days=df2.copy()
        g.df=df2
        MA1 = g.MA1
        MA2 = g.MA2
        Av1=mylib.g.MA(days['close'],MA1)
        Av2=mylib.g.MA(days['close'],MA2) 
        SP = len(days.date.values[MA2-1:])
        matplotlib.use('TkAgg')
        #fig = plt.figure(facecolor=g.ubg,figsize=(7,4))
        fig = plt.figure(facecolor=g.ubg)
        #self.canvas =FigureCanvasTkAgg(fig, master=self.root)
        ax1 = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, fc=g.ubg)
        #ax1=plt.subplot(fc=g.ubg)
        
        days = df2.reindex(columns=['date','open','high','low','close','volume'])   
        daysreshape = days.reset_index()
        daysreshape['date']=mdates.date2num(daysreshape['date'].astype(dt.date))
        daysreshape = daysreshape.reindex(columns=['date','open','high','low','close'])   
        candlestick_ohlc(ax1, daysreshape.values, width=.6, colorup='#ff1717', colordown='#53c156')  
                         
        Label1 = str(MA1)+' MA'
        Label2 = str(MA2)+' MA'
        ax1.plot(days.date.values,Av1,'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(days.date.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
        ax1.grid(True, color='r')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(8))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color(g.utg)

        ax1.tick_params(axis='y', colors=g.ufg)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors=g.ufg)
        plt.ylabel('Stock price')
        plt.legend() # 显示图中右上角的提示信息。

        plt.suptitle(self.stockn,color=g.ufg)
        #plt.setp(ax1.get_xticklabels(), visible=False)
        
        plt.subplots_adjust(left=.04, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
        plt.legend() # 显示图中右上角的提示信息。
        self.canvas =FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        #self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #g.canvas= self.canvas
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        plt.close() # 关窗口


class UplotFrame(Frame): # 继承Frame类  
    def __init__(self, master):  
        self.canvas=None
        self.root = master #定义内部变量root 
        Frame.__init__(self, master)  
        self.createPage()  
   
    def createPage(self):  
        matplotlib.use('TkAgg')
        fig = plt.figure(facecolor=g.ubg,figsize=(7,4))
        self.canvas =FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        #self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #g.canvas= self.canvas
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        plt.close() # 关窗口
        
        
class plotFrame(Frame): # 继承Frame类  
    def __init__(self, master,df,stn,index):  

        self.df1=df
        self.stockn=stn
        self.index=index
        g.index=index
        self.canvas=None
        self.root = master #定义内部变量root 
        
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.createPage()  
   
    def createPage(self):  
        df2=self.df1.copy()
        print(df2)
        #df2.dropna(inplace=True)
        #if 'date' not in df2.columns :
        #df2.insert(0,'date',df2.index)
        df2=df2.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        days=df2.copy()
        g.df=df2
        MA1 = g.MA1
        MA2 = g.MA2
        Av1=mylib.G_MA(days['close'],MA1)
        Av2=mylib.G_MA(days['close'],MA2) 
        SP = len(days.close.values[MA2-1:])
        matplotlib.use('TkAgg')
        fig = plt.figure(facecolor=g.ubg,figsize=(7,4))
        #self.canvas =FigureCanvasTkAgg(fig, master=self.root)
        ax1 = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, fc=g.ubg)
        days = df2.reindex(columns=['date','open','high','low','close','volume'])   
        daysreshape = days.reset_index()
        daysreshape['date']=mdates.date2num(daysreshape['date'].astype(dt.date))
        daysreshape = daysreshape.reindex(columns=['date','open','high','low','close'])   
        
        
        candlestick_ohlc(ax1, daysreshape.values, width=.6, colorup='#ff1717', colordown='#53c156')  
                         
        Label1 = str(MA1)+' MA'
        Label2 = str(MA2)+' MA'
        ax1.plot(days.date.values,Av1,'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(days.date.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
        ax1.grid(True, color='r')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color(g.utg)

        ax1.tick_params(axis='y', colors=g.ufg)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors=g.ufg)
        plt.ylabel('Stock price')
        plt.legend() # 显示图中右上角的提示信息。
        ax1v = ax1.twinx()

        ax1v.tick_params(axis='y', colors=g.ufg)
        ax0 = plt.subplot2grid((7,4), (4,0),sharex=ax1,rowspan=1, colspan=4, fc=g.ubg)
        v1=mylib.G_MA(days['volume'],g.MA1)
        v2=mylib.G_MA(days['volume'],g.MA2)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        ax0.plot(days.date.values, v1, rsiCol, linewidth=1,label="$MA5$")
        ax0.plot(days.date.values, v2, posCol, linewidth=1,label="$MA10$")
        #ax0.bar(days.date.values,days.volume.values, facecolor='#386d13', alpha=.4)
        ax0.bar(days.date.values,days.volume.values, facecolor='yellow', alpha=.4)
        ax0.yaxis.label.set_color(g.ufg)

        ax0.tick_params(axis='y', colors=g.ufg)
        ax0.tick_params(axis='x', colors=g.ufg)
        ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
        ax0.tick_params(axis='x', colors=g.ufg)
        plt.ylabel('volume')    
        plt.legend() # 显示图中右上角的提示信息。                 
        if self.index=='KDJ' :
            mydraw.draw_KDJ(ax1,days,9,3,3)
        if self.index=='MACD' :
            mydraw.draw_MACD(ax1,days,12,26,9)
        if self.index=='RSI' :
            mydraw.draw_RSI(ax1,days,6,12,24)
        if self.index=='OBV' :
            mydraw.draw_OBV(ax1,days,6,12)   
        if self.index=='BOLL' :
            mydraw.draw_BOLL(ax1,days,26)       
        if self.index=='自定义' :
            mydraw.draw_UFN(ax1,days)   
        if self.index=='HPYYX' :
            mydraw.draw_HPYYX(ax1,days)   
        plt.suptitle(self.stockn,color=g.ufg)
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.subplots_adjust(left=.04, bottom=.04, right=.96, top=.96, wspace=.15, hspace=0)
        plt.legend() # 显示图中右上角的提示信息。
        self.canvas =FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        #self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #g.canvas= self.canvas
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        plt.close() # 关窗口

           
class MainFrame(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.canvas=None
        self.stock = StringVar()
        self.stock.set('  ')
        self.root = master #定义内部变量root  
        self.createPage() 
        
    def rtnkey(self,event=None):
        aa=self.stock.get()
        aa=mylib.jqsn(aa)
        g.stock=jq.normalize_code(aa)
        self.stock.set(g.stock)
        self.st3()


   
    def createPage(self):  
        # 日期
        Label(self , text='    ').grid(row=0, column=0)
        label1 = Label(self , text='开始日期:  ',ancho=S)
        label1.grid(row=0, column=1)
        # 输入框 (Entry)
        self.date_s = StringVar()
        entrydates = Entry(self, textvariable=self.date_s)
        entrydates.grid(row=0, column=2)
        self.date_s.set(g.sday)
        Label(self , text='    ').grid(row=0, column=3)
        
        label2 = Label(self , text='结束日期:  ')
        label2.grid(row=0, column=4)
        # 输入框 (Entry)
        self.date_e = StringVar()
        entrydatee = Entry(self, textvariable=self.date_e)
        self.date_e.set(g.eday)
        entrydatee.grid(row=0, column=5)
        Label(self , text='    ').grid(row=0, column=6)
        label3 = Label(self , text='股票代码:  ')
        label3.grid(row=0, column=7)
        # 输入框 (Entry)
        
        entrystock = Entry(self, textvariable=self.stock)
        entrystock.grid(row=0, column=8)
        entrystock.bind('<Key-Return>', self.rtnkey)   
        
        
        Label(self , text='    ').grid(row=0, column=9)
        # 按钮  (Button)
        getname = Button(self , text='确认' ,command=self.st)
        getname.grid(row=0, column=10)

        Label(self , text='    ').grid(row=0, column=11)
        label4 = Label(self , text='指标: ')
        label4.grid(row=0, column=12)
        
        # Adding a Combobox
        self.book = tk.StringVar()
        bookChosen = ttk.Combobox(self , width=10, textvariable=self.book)
        bookChosen['values'] = ('KDJ', 'MACD','RSI','OBV','BOLL','自定义')
        bookChosen.grid(row=0, column=13)
        bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标
        bookChosen.config(state='readonly')  #设为只读模式

    def st(self):  
        ds=self.date_s.get()
        de=self.date_e.get()
        stockn=self.stock.get()
        g.index=self.book.get()
        stockn=mylib.jqsn(stockn)
        self.canvas._tkcanvas.pack_forget()
        g.stock=stockn
        matplotlib.use('TkAgg')
        df1 = jq.get_price(stockn,start_date=ds,end_date=de, frequency='daily') # 获取000001.XSHE的2015年的按天数据
        #print(df1)
        df2=df1.copy()
        #df2.dropna(inplace=True)
        df2.insert(0,'date',df2.index)
        df2=df2.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        days=df2
        g.df=df2
        #print(df2)
        MA1 = g.MA1
        MA2 = g.MA2
        Av1=mylib.MA(days['close'],MA1)
        Av2=mylib.MA(days['close'],MA2) 
        SP = len(days.date.values[MA2-1:])
        SP1 = len(days.date.values[MA1-1:])
        fig = plt.figure(facecolor='#07000d',figsize=(7,4))
        ax1 = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, fc=g.ubg)
        daysreshape = days.reset_index()
        daysreshape['date']=mdates.date2num(daysreshape['date'].astype(dt.date))
        daysreshape = daysreshape.reindex(columns=['date','open','high','low','close'])   
        candlestick_ohlc(ax1, daysreshape.values, width=.6, colorup='#ff1717', colordown='#53c156')                
        Label1 = str(MA1)+' MA'
        Label2 = str(MA2)+' MA'
        ax1.plot(days.date.values,Av1,'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(days.date.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
        ax1.grid(True, color='r')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.label.set_color(g.utg)
        ax1.yaxis.label.set_color(g.utg)
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors=g.utg)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors=g.utg)
        plt.ylabel('Stock price')
        ax1v = ax1.twinx()
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors=g.utg)
        ax1v.tick_params(axis='y', colors=g.utg)
        ax0 = plt.subplot2grid((7,4), (4,0),sharex=ax1,rowspan=1, colspan=4, fc=g.ubg)
        v1=mylib.MA(days['volume'],g.MA1)
        v2=mylib.MA(days['volume'],g.MA2)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        ax0.plot(days.date.values, v1, rsiCol, linewidth=1)
        ax0.plot(days.date.values, v2, posCol, linewidth=1)
        ax0.bar(days.date.values,days.volume.values, facecolor='yellow', alpha=.4)
        ax0.yaxis.label.set_color(g.utg)
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors=g.utg)
        ax0.tick_params(axis='x', colors=g.utg)
        ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))#plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(nbins=4,prune='upper'))
        ax0.tick_params(axis='x', colors=g.utg)
        plt.ylabel('volume')                     
        if g.index=='KDJ' :
            mydraw.draw_KDJ(ax1,days,9,3,3)
        if g.index=='MACD' :
            mydraw.draw_MACD(ax1,days,12,26,9)
        if g.index=='RSI' :
            mydraw.draw_RSI(ax1,days,6,12,24)
        if g.index=='OBV' :
            mydraw.draw_OBV(ax1,days,6,12)    
        if g.index=='BOLL' :
            mydraw.draw_BOLL(ax1,days,26)   
        if g.index=='自定义' :
            mydraw.draw_UFN(ax1)   
        plt.suptitle(stockn,color=g.utg)
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.subplots_adjust(left=.04, bottom=.04, right=.96, top=.96, wspace=.15, hspace=0)
        self.canvas =FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        plt.close() # 关窗口

      

#由于tkinter中没有ToolTip功能，所以自定义这个功能如下
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
 
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
 
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
 
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
             

#===================================================================          
def createToolTip( widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def deltreeitem(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)

def deltree(tree):
    g.scrollBarA.pack_forget() 
    g.scrollBarB.pack_forget() 
    tree.pack_forget()
    g.ttree=None
    g.scrollBarA =None
    g.scrollBarB =None

def creattree(w,df):
    grid_df=df
    grid_ss=grid_df.columns
    grid_colimns=[]
    for s in grid_ss:
        grid_colimns.append(s)
    
    #滚动条
    scrollBarA =tk.Scrollbar(w)
    g.scrollBarA=scrollBarA
    g.scrollBarA.pack(side=tk.RIGHT, fill=tk.Y)

    #Treeview组件，6列，显示表头，带垂直滚动条
    tree = ttk.Treeview(w,columns=(grid_colimns),
                      show="headings",
                      yscrollcommand=g.scrollBarA.set)
    
    for s in grid_colimns:
        #设置每列宽度和对齐方式
        #tree.column(s, anchor='center')
        tree.column(s,width=len(s)*30,  anchor='center')
        #设置每列表头标题文本
        tree.heading(s, text=s)
        
    g.scrollBarA.config(command=tree.yview)

    scrollBarB  = tk.Scrollbar(w,orient = HORIZONTAL)
    g.scrollBarB=scrollBarB
    g.scrollBarB.set(0.5,0.2)
    g.scrollBarB.pack(side=tk.TOP, fill=tk.X)
    g.scrollBarB.config(command=tree.xview)
    
    #定义并绑定Treeview组件的鼠标单击事件
    #插入演示数据
    for i in range(len(grid_df)):
        v=[]
        for s in grid_ss:
            #v.append(grid_df.get_value(i, s))
            v.append(grid_df.at[i,s])
        tree.insert('', i, values=v)

    tree.pack(fill=tk.BOTH,expand=tk.YES)


    def pop2():
        g.tabControl.select(g.ta3)
        de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        df1=hp.get_k_data(g.g.stock,ktype='D',start='2018-01-01',end=de,index=False,autype='qfq')
        df2=hp.tstojq(df1)
        if g.plotPage !=None:
            g.plotPage.canvas._tkcanvas.pack_forget() 
            g.plotPage.pack_forget() 
            g.plotPage=None

        g.plotPage = plotFrame(g.tab2,df2,g.stock,g.formula)  
        g.plotPage.pack(fill=X)

    
    # 创建菜单
    menubar=Menu(w)
    # 创建第四个菜单项，并 绑定事件
    menubar.add_command(label='历史行情',command=pop2)


    
    def onDBClick(event):
        item = tree.selection()[0]
        aa=tree.item(item, "values")
        #print("you clicked on  "+item, tree.item(item, "values"))
        bb=list(aa)
        #print(bb[0])
        g.g.stock=bb[0]


    tree.bind("<Button-1>", onDBClick)
    tree.bind("<Double-1>", onDBClick)



    return tree 

def mygrid(w,df):
    grid_df=df
    grid_ss=grid_df.columns
    grid_colimns=[]
    for s in grid_ss:
        grid_colimns.append(s)
    
    #滚动条
    scrollBarA =tk.Scrollbar(w)
    g.scrollBarA=scrollBarA
    g.scrollBarA.pack(side=tk.RIGHT, fill=tk.Y)

    #Treeview组件，6列，显示表头，带垂直滚动条
    tree = ttk.Treeview(w,columns=(grid_colimns),
                      show="headings",
                      yscrollcommand=g.scrollBarA.set)
    
    for s in grid_colimns:
        #设置每列宽度和对齐方式
        #tree.column(s, anchor='center')
        tree.column(s,width=len(s)*30,  anchor='center')
        #设置每列表头标题文本
        tree.heading(s, text=s)
        
    g.scrollBarA.config(command=tree.yview)

    scrollBarB  = tk.Scrollbar(w,orient = HORIZONTAL)
    g.scrollBarB=scrollBarB
    g.scrollBarB.set(0.5,0.2)
    g.scrollBarB.pack(side=tk.TOP, fill=tk.X)
    g.scrollBarB.config(command=tree.xview)
    
    #定义并绑定Treeview组件的鼠标单击事件

    #插入演示数据
    for i in range(len(grid_df)):
        v=[]
        for s in grid_ss:
            #v.append(grid_df.get_value(i, s))
            v.append(grid_df.at[i,s])
        tree.insert('', i, values=v)


    #tree.pack(fill=X,ipady=g.winH-200)
    tree.pack(fill=tk.BOTH,expand=tk.YES)
    
    def onDBClick(event):
        item = tree.selection()[0]
        aa=tree.item(item, "values")
        #print("you clicked on  "+item, tree.item(item, "values"))
        bb=list(aa)
        #print(bb[0])
        g.g.stock=bb[0]

        
        
        
    tree.bind("<Double-1>", onDBClick)
    
    def pop1():
        g.tabControl.select(g.tab2)
        de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        df1=hp.get_k_data(g.g.stock,ktype='D',start='2018-01-01',end=de,index=False,autype='qfq')
        df2=hp.tstojq(df1)
        if g.plotPage !=None:
            g.plotPage.canvas._tkcanvas.pack_forget() 
            g.plotPage.pack_forget() 
            g.plotPage=None

        g.plotPage = plotFrame(g.tab2,df2,g.g.stock,g.g.index)  
        g.plotPage.pack(fill=X)

        

    def topwin():
        author_ui = Toplevel()
        author_ui.title('子窗口测试')
        #author_ui.iconbitmap('icons/48x48.ico')
        author_ui.geometry('200x80')
        about_string = Label(author_ui, text = '这是一个测试！')
        confirmButton = Button(author_ui, text = '确定',
                               command = lambda: self.destroy_ui(author_ui))
        about_string.pack()
        confirmButton.pack()
    
    # 创建菜单
    menubar=Menu(w)
    # 创建第四个菜单项，并 绑定事件
    menubar.add_command(label='历史行情',command=pop1)
    #menubar.add_command(label='子窗口 ',command=topwin)
    
    def pop(event):
        # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
        menubar.post(event.x_root,event.y_root)
    
    # 鼠标右键是用的<Button-3>
    # 使用 Menu 类的 pop 方法来弹出菜单
    tree.bind("<Button-3>",pop)    
    return tree
    
    

def myplot(master,df1,stockn='',zb='KDJ'):
    myroot=master
    matplotlib.use('TkAgg')
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    g.g.index=zb
    
    df2=df1.copy()
    df2.dropna(inplace=True)
    df2.insert(0,'date',df2.index)
    df2=df2.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
    #print(df2)
    days=df2
    g.df=df2
    MA1 = g.MA1
    MA2 = g.MA2
    Av1=mylib.g.MA(days['close'],MA1)
    Av2=mylib.g.MA(days['close'],MA2) 
    SP = len(days.date.values[MA2-1:])
    SP1 = len(days.date.values[MA1-1:])
#    plt.cla()
#    plt.clf()fc=g.ubg
#    plt.close('all') # 关闭图 0
    fig = plt.figure(facecolor=g.ubg,figsize=(7,4))
    plt.close()
    #plt.close('all') # 关闭图 0
    plt.clf()
    fig = plt.figure(facecolor=g.ubg,figsize=(7,4))
    ##关联鼠标点击事件
    #fig.canvas.mpl_connect('button_press_event',OnClick)
    #fig.canvas.mpl_connect('motion_notify_event',OnMouseMotion)
    ax1 = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, fc=g.ubg)
    daysreshape = days.reset_index()
    daysreshape['date']=mdates.date2num(daysreshape['date'].astype(dt.date))
    daysreshape = daysreshape.reindex(columns=['date','open','high','low','close'])   
    candlestick_ohlc(ax1, daysreshape.values, width=.6, colorup='#ff1717', colordown='#53c156')                
    Label1 = str(MA1)+' MA'
    Label2 = str(MA2)+' MA'
    ax1.plot(days.date.values,Av1,'#e1edf9',label=Label1, linewidth=1.5)
    ax1.plot(days.date.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
    ax1.grid(True, color='r')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color(g.ufg)
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors=g.ufg)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('Stock price')
    ax1v = ax1.twinx()
    ax1v.spines['bottom'].set_color("#5998ff")
    ax1v.spines['top'].set_color("#5998ff")
    ax1v.spines['left'].set_color("#5998ff")
    ax1v.spines['right'].set_color("#5998ff")
    ax1v.tick_params(axis='x', colors=g.ufg)
    ax1v.tick_params(axis='y', colors=g.ufg)
    ax0 = plt.subplot2grid((7,4), (4,0),sharex=ax1,rowspan=1, colspan=4, fc=g.ubg)
    v1=mylib.g.MA(days['volume'],g.MA1)
    v2=mylib.g.MA(days['volume'],g.MA2)
    v3=mylib.g.MA(days['volume'],g.MA3)
    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    negCol = '#8f2020'
    ax0.plot(days.date.values, v1, rsiCol, linewidth=1)
    ax0.plot(days.date.values, v2, posCol, linewidth=1)
    ax0.bar(days.date.values,days.volume.values, facecolor='yellow', alpha=.4)
    ax0.yaxis.label.set_color(g.ufg)
    ax0.spines['bottom'].set_color("#5998ff")
    ax0.spines['top'].set_color("#5998ff")
    ax0.spines['left'].set_color("#5998ff")
    ax0.spines['right'].set_color("#5998ff")
    ax0.tick_params(axis='y', colors=g.ufg)
    ax0.tick_params(axis='x', colors=g.ufg)
    ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))#plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(nbins=4,prune='upper'))
    ax0.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('volume')                     
    if g.g.index=='KDJ' :
        ax3=mydraw.draw_KDJ(ax1,days,9,3,3)
    if g.g.index=='MACD' :
        ax3=mydraw.draw_MACD(ax1,days,12,26,9)
    if g.g.index=='RSI' :
        ax3=mydraw.draw_RSI(ax1,days,6,12,24)
    if g.g.index=='OBV' :
        ax3=mydraw.draw_OBV(ax1,days,6,12)   
    if g.g.index=='BOLL' :
        ax3=mydraw.draw_BOLL(ax1,days,26)                  
    plt.suptitle(stockn,color='w')
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.subplots_adjust(left=.04, bottom=.04, right=.96, top=.96, wspace=.15, hspace=0)
    #frame_root.pack(side=tk.TOP, fill=tk.BOTH, expand=1)  
    canvas =FigureCanvasTkAgg(fig, master=myroot)
    #toolbar =NavigationToolbar2TkAgg(canvas, master)
    #toolbar.update()
    my=canvas.get_tk_widget()  
    #my.pack(side=tk.TOP, fill=tk.BOTH, expand=1)    
    my.pack(fill=tk.BOTH, expand=1)
    plt.close() # 关窗口
    #plt.savefig('temp.png')
#    ax1.clear()
#    ax0.clear()
#    ax1v.clear()
#    plt.close(fig)  
    return my


class gridFrame(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.parenta = master
        self.tree=None
        self.dd=1
        self.n=1
        self.timer=None
        self.gn=None
        self.classA=None
        self.stocks=None
        self.root.config(bg='black')
        self.itemName = StringVar()  
        self.createPage()  
   
    
    def createPage(self):  
        self.LBtext=StringVar()
        self.LBtext.set('指数列表')
        self.LB=Label(self, textvariable = self.LBtext,bg="blue",fg="white").pack(fill=X)  



class gridFramejq(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
      
        self.root = master #定义内部变量root  
        self.parenta = master
        self.tree=None
        self.dd=1
        self.n=1
        self.bt='指数列表'
        self.timer=None
        #self.gn=StringVar()
        self.gn=None
        self.classA=None
        self.stocks=None
        self.itemName = StringVar()  
        self.createPage()  
   
    def rxt(self):
        ds='2018-01-01'
        de=time.strftime('%Y-%m-%d',time.localtime(time.time()))+' 15:01:00'
        g.gtype=g.vbook.get()
        g.sday=ds.strip()
        g.eday=de.strip()
        item = self.tree.selection()[0]
        aa=self.tree.item(item, "values")
        #print("you clicked on  "+item, tree.item(item, "values"))
        bb=list(aa)        
        g.stock=bb[0] 
        g.vtitle=bb[1]
        print(bb[0])
        if g.login:
            g.stock=jq.normalize_code(g.stock)
            df3 = jq.get_price(g.stock, start_date=g.sday, end_date=g.eday,frequency='daily') # 获得000001.XSHG的2015年01月的分钟数据, 只获取open+close字段
            df2=hp.jqtots(df3)
            df2.date=df2.date.astype('str')
            if g.tab3!=None:
                g.tabControl.forget(g.tab3)
                g.tab3=None
            
            #用户自建新画面
            g.tab3 = tk.Frame(g.tabControl)
            g.tabControl.add(g.tab3, text='日线图') 
            g.tabControl.select(g.tab3)
            axview3x(g.tab3,df2,t=g.stock,n=2,f1='VOL',f2=g.gtype)
            #df2.to_csv('temp/000001.csv' , encoding= 'gbk')
        else:
            print('未登陆，不能操作！')
            g.status.text(1,'查看日线数据') #在状态栏2输出信息
            g.status.text(2,'未登陆，不能操作！')
        self.tabControl.select(g.tab3)


    def fst(self):
        item = self.tree.selection()[0]        
        aa=self.tree.item(item, "values")
        bb=list(aa)
        print("you popmenu on  "+item, bb[0])
        g.stock=bb[0]
        #self.timer.cancel()
        g.mstock=bb[0]
        g.vtitle=bb[1]
        try:
            filename='view/聚宽分时图.py'
            g.status.text(1,'')
            g.status.text(2,'查看'+bb[0]+'分时图！')
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            msg=f.read()
            f.close()
            exec(msg)
        except Exception as e:
            g.status.text(1,'')
            g.status.text(2,'用户代码出错:'+str(e))
            ttprint('用户代码出错:'+str(e)+'\n','red')
            print('用户代码出错:'+str(e)+'\n')

       
    
    def createPage(self):  
        self.LBtext=StringVar()
        self.LBtext.set(self.bt)
        self.LB=Label(self, textvariable = self.LBtext,bg="blue",fg="white").pack(fill=X)  
        if g.login:
            df4=jq.get_all_securities(types=['index'], date=None)
            df4.insert(0,'jkname',df4.index)
            df4.to_csv('temp/index.csv' , encoding= 'gbk')
        else:
            print('读本地index数据！')
            df4=pd.read_csv('temp/index.csv' , encoding= 'gbk')
        
        #滚动条
        scrollBar =tk.Scrollbar(self)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        #Treeview组件，6列，显示表头，带垂直滚动条
        self.tree = ttk.Treeview(self,columns=('c1', 'c2', 'c3','c4', 'c5', 'c6'),
                          show="headings",
                          yscrollcommand=scrollBar.set)

        #设置每列宽度和对齐方式
        self.tree.column('c1',  anchor='center')
        self.tree.column('c2', width=100,  anchor='center')
        self.tree.column('c3',width=100,   anchor='center')
        self.tree.column('c4',width=100,   anchor='center')
        self.tree.column('c5', width=100,  anchor='center')
        self.tree.column('c6',  anchor='center')
        #设置每列表头标题文本
        self.tree.heading('c1', text='聚宽代码')
        self.tree.heading('c2', text='指数名称')
        self.tree.heading('c3', text='指数缩写')
        self.tree.heading('c4', text='开始日期')
        self.tree.heading('c5', text='结束日期')
        self.tree.heading('c6', text='数据类型')
        
        #Treeview组件与垂直滚动条结合
        scrollBar.config(command=self.tree.yview)
        #scrollBar.config(command=tree.xview)
        #定义并绑定Treeview组件的鼠标单击事件

        def fun_timer():
            #print('Hello Timer!')
            self.n=self.n+1
            self.LBtext.set(self.bt)
            
            flash()
            self.timer = threading.Timer(60, fun_timer)
            self.timer.start()

        def delButton(tree):
            x=tree.get_children()
            for item in x:
                tree.delete(item)
                
        def flash():
                #self.tree.pack_forget() 
                n1=[]
                o1=[]
                c1=[]
                h1=[]
                l1=[]
                v1=[]
                m1=[]
                self.df=pd.DataFrame({'name':[s for s in self.stocks]})  
                ds=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                for s in self.stocks:
                    w=jq.get_price(s,start_date=ds,end_date=de, frequency='daily') # 获取000001.XSHE的2015年的按天数据
                    n1.append(s)
                    o1.append(w['open'][0])
                    c1.append(w['close'][0])
                    h1.append(w['high'][0])
                    l1.append(w['low'][0])
                    v1.append(w['volume'][0])
                    m1.append(w['money'][0])
                    
            
                #df=pd.DataFrame({'name':[s for s in stocks]})  
                ZB = pd.Series(o1, name = 'open')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(c1, name = 'close')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(h1, name = 'high')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(l1, name = 'low')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(v1, name = 'volume')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(m1, name = 'money')  
                self.df = self.df.join(ZB)                                   
    
                delButton(self.tree)  
                #设置每列表头标题文本
                self.tree.heading('c1', text='聚宽代码')
                self.tree.heading('c2', text=g.ec['open'])
                self.tree.heading('c3', text=g.ec['close'])
                self.tree.heading('c4', text=g.ec['high'])
                self.tree.heading('c5', text=g.ec['low'])
                self.tree.heading('c6', text=g.ec['volume'])                  
                #插入演示数据
                for i in range(len(self.df)):
                    self.tree.insert('', i, values=[self.df.name[i],self.df.open[i],self.df.close[i],self.df.high[i],self.df.low[i],self.df.volume[i]])
                self.tree.pack(fill=X,ipady=g.winH-20) 
        


        def onDBClick(event):
            if g.login==False:
                return
            g.status.text(1,'正在获取数据...') #在状态栏2输出信息
            item = self.tree.selection()[0]
            if self.dd==1:
                aa=self.tree.item(item, "values")
                #print("you clicked on  "+item, tree.item(item, "values"))
                bb=list(aa)
                #print(bb[0])
                self.LBtext.set(bb[1]+'  '+bb[0])
                self.stocks = jq.get_index_stocks(bb[0])
                g.status.text(2,'查看'+bb[0]+'股票列表！')
                self.bt='指数'+bb[0]+'股票列表'
                #print(self.stocks)

                
                #self.tree.pack_forget() 
                n1=[]
                o1=[]
                c1=[]
                h1=[]
                l1=[]
                v1=[]
                m1=[]
                self.df=pd.DataFrame({'name':[s for s in self.stocks]})  
                ds=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                de=ds='2019-02-01'
                for s in self.stocks:
                    w1=jq.get_price(s,start_date=ds,end_date=de, frequency='daily') # 获取000001.XSHE的2015年的按天数据
                    w=hp.jqtots(w1)
                    #print(w)
                    n1.append(s)
                    o1.append(w.at[0,'open'])
                    c1.append(w.at[0,'close'])
                    h1.append(w.at[0,'high'])
                    l1.append(w.at[0,'low'])
                    v1.append(w.at[0,'volume'])
                    m1.append(w.at[0,'money'])
                    
            
                #df=pd.DataFrame({'name':[s for s in stocks]})  
                ZB = pd.Series(o1, name = 'open')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(c1, name = 'close')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(h1, name = 'high')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(l1, name = 'low')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(v1, name = 'volume')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(m1, name = 'money')  
                self.df = self.df.join(ZB)                                   
    
                delButton(self.tree)  
                #设置每列表头标题文本
                self.tree.heading('c1', text='聚宽代码')
                self.tree.heading('c2', text=g.ec['open'])
                self.tree.heading('c3', text=g.ec['close'])
                self.tree.heading('c4', text=g.ec['high'])
                self.tree.heading('c5', text=g.ec['low'])
                self.tree.heading('c6', text=g.ec['volume'])                   
                #插入演示数据
                for i in range(len(self.df)):
                    self.tree.insert('', i, values=[self.df.name[i],self.df.open[i],self.df.close[i],self.df.high[i],self.df.low[i],self.df.volume[i]])
                self.tree.pack(fill=X,ipady=g.winH-20) 
                self.dd=2
                g.status.text(1,'') #在状态栏2输出信息
            elif self.dd==2:
                aa=self.tree.item(item, "values")
                bb=list(aa)
                print("you clicked on  "+item, bb[0])
                
                g.stock=bb[0]
                self.timer.cancel()
                g.mstock=bb[0]
                
                try:
                    filename='view/聚宽分时图.py'
                    g.status.text(1,'')
                    g.status.text(2,'查看'+bb[0]+'分时图！')
                    f = open(filename,'r',encoding='utf-8',errors='ignore')
                    msg=f.read()
                    f.close()
                    exec(msg)
                except Exception as e:
                    g.status.text(1,'')
                    g.status.text(2,'用户代码出错:'+str(e))
                    ttprint('用户代码出错:'+str(e)+'\n','red')
                    print('用户代码出错:'+str(e)+'\n')
                
#                self.tree.pack_forget() 
#                self.pack_forget() 
#                self.gn.set(g.stock)
#                self.classA.st3()
#                self.parenta.mainPage.pack(fill=X) 
#                self.parenta.mainPage.st()
#                self.parenta.plotPage.canvas._tkcanvas.pack(fill=X)
#                self.parenta.plotPage.pack(fill=X)

                
                
                
            self.timer = threading.Timer(1, fun_timer)
            self.timer.start()
    

        self.tree.bind("<Double-1>", onDBClick)
        


        #插入演示数据
        for i in range(len(df4)):
            self.tree.insert('', i, values=[df4.jkname[i],df4.display_name[i],df4.name[i],df4.start_date[i],df4.end_date[i],df4.type[i]])

        self.tree.pack(fill=X,ipady=g.winH-20)
        # 创建弹出菜单
        self.menubar=tk.Menu(self)
        self.toolbarName2 = ('日线图','分时图')
        self.toolbarCommand2 = (self.rxt,self.fst)
        def addPopButton(name,command):
            for (toolname ,toolcom) in zip(name,command):
                self.menubar.add_command(label=toolname,command=toolcom)
    
        def pop(event):
            # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
            self.menubar.post(event.x_root,event.y_root)
    
        addPopButton(self.toolbarName2,self.toolbarCommand2) #创建弹出菜单
        self.tree.bind("<Button-3>",pop)
      

      
'''
独狼荷蒲软件(或通通软件)版权声明
1、独狼荷蒲软件(或通通软件)均为软件作者设计,或开源软件改进而来，仅供学习和研究使用，不得用于任何商业用途。
2、用户必须明白，请用户在使用前必须详细阅读并遵守软件作者的“使用许可协议”。
3、作者不承担用户因使用这些软件对自己和他人造成任何形式的损失或伤害。
4、作者拥有核心算法的版权，未经明确许可，任何人不得非法复制；不得盗版。作者对其自行开发的或和他人共同开发的所有内容，
    包括设计、布局结构、服务等拥有全部知识产权。没有作者的明确许可，任何人不得作全部或部分复制或仿造。

独狼荷蒲软件
QQ: 2775205
Tel: 18578755056
公众号:独狼股票分析
'''