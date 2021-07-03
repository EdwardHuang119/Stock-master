# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架 回测工具
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2019年12月22日
"""
from HP_view import * #菜单栏对应的各个子页面 
import pandas as pd  
import numpy  as np
import datetime as dt
import time
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
#from matplotlib.finance import candlestick_ohlc
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import matplotlib
from numpy import arange, sin, pi
#from matplotlib.backends.backend_tkagg import FigureCanvasTk,NavigationToolbar2Tk  #matplotlib 2.0.2 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)    ##matplotlib 3.0.2 
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import math
import HP_tdx as htdx
from HP_formula import *
from HP_sys import *
import tkinter as tk
import HP_global as g 
import HP_data as hp

global CLOSE,LOW,HIGH,OPEN,VOL
global C,L,H,O,V
ds=g.hcdate_s.get()
de=g.hcdate_e.get()
stockn=g.hcstock.get()
df2=htdx.get_k_data(stockn,ktype='D',start=ds,end=de,index=False,autype='qfq')
df3=df2

##数据规格化 
df3.dropna(inplace=True)

mydf=df3.copy()
CLOSE=mydf['close']
LOW=mydf['low']
HIGH=mydf['high']
OPEN=mydf['open']
VOL=mydf['volume']
C=mydf['close']
L=mydf['low']
H=mydf['high']
O=mydf['open']
V=mydf['volume']

#HPYYX python HPYYX指标
def HPYYX():
    RSV= (C-LLV(L,9))/(HHV(H,9)-LLV(L,9))*100
    FASTK=SMA(RSV,3,1)
    RSV1= (HHV(H,9)-C)/(HHV(H,9)-LLV(L,9))*100
    LC = REF(C,1)
    RSI1=SMA(MAX(C-LC,0),13,1)/SMA(ABS(C-LC),13,1)*100
    RSI2=SMA(MAX(C-LC,0),6,1)/SMA(ABS(C-LC),6,1)*100
    RSI3=IF(RSI2>50,RSI2*1.05,RSI2)
    RSV3=(C-LLV(L,54))/(HHV(H,54)-LLV(L,54))*100
    #mydf['YB']=100
    HT=IF(RSI3>100,100,RSI3)
    YIN=SMA((SMA(RSV1,3,1)/2)*1.1,3,1)
    YANG=SMA(((SMA(FASTK,3,1))/2+40)*1.1,3,1)
    ZL2=EMA(RSI2,13)
    ZL=IF(ZL2>50,ZL2*1.3,ZL2*0.9)
    return YIN, YANG,HT,ZL


#使用HPYYX指标，返回YIN, YANG,HT,ZL序列。
YIN, YANG,HT,ZL=HPYYX()
    
mydf = mydf.join(pd.Series( YIN,name='YIN'))
mydf= mydf.join(pd.Series( YANG,name='YANG'))
mydf = mydf.join(pd.Series( ZL,name='ZL'))
mydf = mydf.join(pd.Series( HT,name='HT'))
mydf['SG']=85  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线
mydf['Z50']=50  #增加中轨50轨迹线

##下面开始生成HPYYX指标买卖点
##买点ZL上穿数值YIN
b1=CROSS(mydf['ZL'],mydf['YIN'])
mydf = mydf.join(pd.Series( b1,name='B1'))  

##卖点ZL下穿80
s1=CROSS(mydf['SG'],mydf['ZL'])

#卖点ZL下穿50
s2=CROSS(mydf['Z50'],mydf['ZL'])

#合并所有卖点信号
s3=s1 | s2

mydf = mydf.join(pd.Series( s1,name='S1'))  
mydf = mydf.join(pd.Series( s2,name='S2'))  
mydf = mydf.join(pd.Series( s3,name='S3'))  

g.tabControl.select(g.tab5)
##回测
tt=hpQuant()   ##初始化类

#下面是用户可设置信息。
#        self.money2=1000000.00  #总资金
#        self.code=""   #证券代码
#        self.stamp_duty=0.001   #印花税 0.1%
#        self.trading_Commission=0.0005    #交易佣金0.05%
#        self.stop_loss_on=True #允许止损
#        self.stop_loss_max=50 #止损3次,就停止交易
#        self.stop_loss_range=0.05   #止损幅度

tt.code=stockn  #证券代码，必须输入
tt.stop_loss_on=False    #关闭自动止损
df3=tt.Trade_testing(mydf,'B1','S3','HL')   #开始回测
#print('\n打印交易过程')
tt.PrintTrade()    #打印交易过程
print('\n打印持仓信息')
tt.PrintSecurity()   #打印持仓信息
#print('\n 打印内部交易记录信息')
#print(tt.text)     #打印交易信息

if g.UserCanvas!=None:

    g.UserPlot.cla() 
    g.UserPlot.close()
    g.UserCanvas._tkcanvas.pack_forget() 
    g.UserCanvas=None


######下面是绘图
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# 开启一个双图例的窗口，定义为211和212
fig=plt.figure(2, figsize=(12,8), dpi=80)
g.UserFig=fig
g.UserPlot=plt
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

# ax1（211窗口）
plt.sca(ax1)
#添加标题
ax_K(ax1,df3,stockn)  
plt.suptitle(stockn+' '+g.stock_names[stockn]+'  HPYYX回测结果')

# ax2（212窗口）
plt.sca(ax2)
df3.HL.plot(color='orange', grid=True,label="获利")
df3.B1.plot(color='red',label="$B$")
df3.S3.plot(color='blue',label="$S$")

plt.legend() # 显示图中右上角的提示信息。
ax2.grid(True)
ax2.axhline(0, color='blue')
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
ax2.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分     
ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='upper'))
plt.close()
canvas =FigureCanvasTkAgg(fig, master=g.UserFrame)
#toolbar =NavigationToolbar2TkAgg(canvas, g.UserFrame)
#toolbar.update()

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
g.UserCanvas=canvas
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)





