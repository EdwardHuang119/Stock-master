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
from HP_draw import * #菜单栏对应的各个子页面 
import pandas as pd  
#import numpy  as np
#import datetime as dt
#import time
import matplotlib.pyplot as plt
#from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
#from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
#from matplotlib.dates import MonthLocator,MONTHLY
import matplotlib
#from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)    ##matplotlib 3.0.2 
#from matplotlib.backend_bases import key_press_handler
#from matplotlib.figure import Figure
#import math
import HP_tdx as htdx
from HP_formula import *
from HP_sys import *
import tkinter as tk
import HP_global as g 
import HP_data as hp

global CLOSE,LOW,HIGH,OPEN,VOL
ds=g.hcdate_s.get()
de=g.hcdate_e.get()
#de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
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

##HPCPX交易策略 
#在ax区
def HPCPX():
    S0=(CLOSE+OPEN+LOW+HIGH)/4
    S1=EMA(SLOPE(S0,5),60)
    S2=EMA(S1,20)
    S3=IF(S1>=0,S1,DRAWNULL())
    S4=IF(S1>S2 ,S3,DRAWNULL())
    return S1,S2,S4
#使用HPCPX指标，返回x,y,x序列。
x,y,z=HPCPX()

mydf = mydf.join(pd.Series( x,name='CPX'))
mydf = mydf.join(pd.Series( y,name='Y'))
mydf = mydf.join(pd.Series( z,name='Z'))
mydf['Y0']=0

##下面开始生成HPCPX指标买卖点
##买点CPX上穿数值0
b1=CROSS(mydf['CPX'],mydf['Y0'])
b2=CROSS(mydf['CPX'],mydf['Y'])
#b1 或者(b2 且 CPX大于0值)
b3=b1 | (b2 & IF(mydf['CPX']>0,1,0))

##卖点CPX下穿Y
s1=CROSS(mydf['Y'],mydf['CPX'])

mydf = mydf.join(pd.Series( b3,name='B3'))  
mydf = mydf.join(pd.Series( s1,name='S1'))  

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
df3=tt.Trade_testing(mydf,'B3','S1','HL')   #开始回测
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
#matplotlib.use('TkAgg')
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# 开启一个双图例的窗口，定义为211和212
fig=plt.figure(2, figsize=(12,8), dpi=80,facecolor=g.ubg)


g.UserFig=fig
g.UserPlot=plt
ax1 = plt.subplot(311,fc=g.ubg)
ax2 = plt.subplot(312,fc=g.ubg)
ax3 = plt.subplot(313,fc=g.ubg)

# ax1（311窗口）
plt.sca(ax1)
#添加标题
ax_K(ax1,df3,stockn)  
plt.sca(ax1)
plt.suptitle(stockn+' '+g.stock_names[stockn]+'  HPCPX回测结果',color=g.ufg)
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')

# ax2（312窗口）
plt.sca(ax2)
#开始绘图
ax2.plot(df3.date.values,df3.CPX.values, color= 'green', lw=2,label="荷蒲操盘线")
ax2.plot(df3.date.values, df3.Z.values, color= 'red', lw=2)
ax2.plot(df3.date.values, df3.Y0.values, color= 'yellow', lw=2)
text = ax2.text(0.1, 0.01, '红线持股！绿线持币！', fontdict={'size': 10},color='yellow')
plt.ylabel('HPCPX', color='white')
plt.legend() # 显示图中右上角的提示信息。
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
ax2.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分     
ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='upper'))
ax2.grid(True, color='r')
ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')
plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)


# ax3（312窗口）
plt.sca(ax3)
df3.HL.plot(color='orange', grid=True,label="获利")
df3.B3.plot(color='red',label="$B$")
df3.S1.plot(color='blue',label="$S$")
plt.ylabel('获利率', color='white')
plt.legend() # 显示图中右上角的提示信息。
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
ax3.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分     
ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='upper'))
ax3.grid(True, color='r')
ax3.tick_params(axis='y', colors='white')
plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
plt.close()
canvas =FigureCanvasTkAgg(fig, master=g.UserFrame)
#toolbar =NavigationToolbar2TkAgg(canvas, g.UserFrame)
#toolbar.update()

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
g.UserCanvas=canvas
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)






