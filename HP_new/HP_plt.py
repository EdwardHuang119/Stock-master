# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架 指标公式绘图库
#版本：Ver2.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2020年12月27日
#主程序：
"""

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
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
import datetime as dt
import pylab
import matplotlib
from PIL import Image, ImageTk
#import HP_zwdata as sd
import HP_global as g
#import HP_lib as mylib
from HP_formula import *
import matplotlib.ticker as ticker# 先设定一个日期转换方法
def format_date(x,pos=None): 
    # 由于前面股票数据在 date 这个位置传入的都是int 
    # 因此 x=0,1,2,... 
    # date_tickers 是所有日期的字符串形式列表 
    if x<0 or x>len(date_tickers)-1: 
        return '' 
    return date_tickers[int(x)]
# 用 set_major_formatter() 方法来修改主刻度的文字格式化方式
#ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
#ax.xaxis.set_major_locator(ticker.MultipleLocator(6))    

#在ax区绘制K线
def ax_K(ax,df,t,n=2):
    #显示K线,带6条均线
    df2=df.copy()
    date_tickers=df2.date.values
    del df2['date']   
    df2['date']=df2.index
    ma5=pd.Series.rolling(df2.close, 5).mean()   #股票收盘价5日平均线 
    ma10=pd.Series.rolling(df2.close, 10).mean() #股票收盘价10日平均线 
    days = df2.reindex(columns=['date','open','high','low','close'])   
    def format_date(x,pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分 
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  
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
    ax.xaxis.label.set_color(g.ufg)
    ax.yaxis.label.set_color(g.ufg)
    plt.legend() # 显示图中右上角的提示信息。
    plt.suptitle(t,color=g.ufg)
    return ax

#在ax区绘制VOL
def ax_VOL(ax1,df):
    df2=df.copy()
    v1=pd.Series.rolling(df2.volume, 5).mean() #5日平均线 
    v2=pd.Series.rolling(df2.volume, 10).mean() #10日平均线 
    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    ax1.plot(df2.date.values, v1, rsiCol, linewidth=1,label="VMA5")
    ax1.plot(df2.date.values, v2, posCol, linewidth=1,label="VMA10")
    ax1.bar(df2.date.values,df2.volume.values, facecolor=g.uvg, alpha=.8)
    ax1.yaxis.label.set_color(g.ufg)
    ax1.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('volume')    
    plt.legend() # 显示图中右上角的提示信息。 
    ax1.grid(True, color='r')
    return ax1

#在ax区绘制VOL,K阳线红柱,K阴线绿柱
def ax_VOL2(ax1,df):
    df2=df.copy()
    v1=pd.Series.rolling(df2.volume, 5).mean() #5日平均线 
    v2=pd.Series.rolling(df2.volume, 10).mean() #10日平均线 
    i1=df2.index[df2.close>=df2.open]
    df2['vol1']=df2.volume[i1]
    i2=df2.index[df2.close<df2.open]
    df2['vol2']=df2.volume[i2]   
    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    ax1.plot(df2.date.values, v1, rsiCol, linewidth=1,label="VMA5")
    ax1.plot(df2.date.values, v2, posCol, linewidth=1,label="VMA10")
    #ax1.bar(df2.date.values,df2.volume.values, facecolor=g.uvg, alpha=.8)
    ax1.bar(df2.date.values,df2.vol1.values, facecolor='red', alpha=.8)
    ax1.bar(df2.date.values,df2.vol2.values, facecolor='green', alpha=.8)
    ax1.yaxis.label.set_color(g.ufg)
#    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
#    ax1.tick_params(axis='y', colors=g.ufg)
#    ax1.tick_params(axis='x', colors=g.ufg)
#    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
    ax1.tick_params(axis='x', colors=g.ufg)
    plt.ylabel('volume')    
    plt.legend() # 显示图中右上角的提示信息。 
    ax1.grid(True, color='r')
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6, prune='upper'))
    return ax1

#在ax区绘制KDJ
def ax_KDJ(ax1,mydf):
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
    
    #df格式必须使用tushare数据格式,
    df=mydf.copy()
    #KDJ python随机指标
    def KDJ(N=9, M1=3, M2=3):
        RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
        K = SMA(RSV,M1,1)
        D = SMA(K,M2,1)
        J = 3*K-2*D
        return K, D, J

    #使用KDJ指标，返回K，D，J序列。
    K,D,J=KDJ(9,3,3)
    
    df = df.join(pd.Series( K,name='K'))
    df = df.join(pd.Series( D,name='D'))
    df = df.join(pd.Series( J,name='J'))

    ax1.plot(df.date.values, df.K.values, color= 'green', lw=2,label="K")
    ax1.plot(df.date.values,df.D.values, color= 'red', lw=2,label="D")
    ax1.plot(df.date.values, df.J.values, color= 'blue', lw=2,label="J")
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors=g.utg)
    ax1.tick_params(axis='y', colors=g.utg)
    ax1.grid(True, color='r')
    plt.ylabel('KDJ', color=g.utg)
    plt.legend() # 显示图中右上角的提示信息。
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6, prune='upper'))
    return ax1



def ax_MACD(ax1,mydf):
    x=12
    y=26
    z=9    
    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    negCol = '#8f2020'
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
    def MACD(SHORT=12, LONG=26, M=9):
        """
        MACD 指数平滑移动平均线
        """
        DIFF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
        DEA = EMA(DIFF, M)
        MACD = (DIFF - DEA) * 2

        return DIFF,DEA,MACD
    
    d1,d2,d3=MACD(x,y,z)
    
    mydf = mydf.join(pd.Series( d1,name='DIFF'))  
    mydf = mydf.join(pd.Series( d2,name='DEA'))  
    mydf = mydf.join(pd.Series( d3,name='MACD')) 
    mydf['S0']=0  #增加上轨80轨迹线
    df=mydf.copy()
    fillcolor = '#00ffe8'
    ax1.plot(df.date.values, df.DIFF.values, color=rsiCol, lw=1,label="$DIFF$")
    ax1.plot(df.date.values, df.MACD.values, color=negCol, lw=1,label="$DEA$")
    ax1.fill_between(df.date.values, df.MACD.values, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='x', colors=g.utg)
    ax1.tick_params(axis='y', colors=g.utg)
    ax1.axhline(0, color=negCol)
    plt.ylabel('MACD', color=g.utg)
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='upper'))
    plt.legend() # 显示图中右上角的提示信息。
    return  ax1



def ax_HPYYX(ax2,mydf):
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
    
    #df格式必须使用tushare数据格式,
    df=mydf.copy()

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
        mydf['YB']=100
        HT=IF(RSI3>100,mydf['YB'],RSI3)
        YIN=SMA((SMA(RSV1,3,1)/2)*1.1,3,1)
        YANG=SMA(((SMA(FASTK,3,1))/2+40)*1.1,3,1)
        ZL=EMA(RSI2,13)
  
        return YIN, YANG,HT,ZL
    
    #使用KDJ指标，返回K，D，J序列。
    YIN, YANG,HT,ZL=HPYYX()
    
    df = df.join(pd.Series( YIN,name='YIN'))
    df = df.join(pd.Series( YANG,name='YANG'))
    df = df.join(pd.Series( ZL,name='ZL'))
    df = df.join(pd.Series( HT,name='HT'))


    ax2.plot(df.date.values, df.YIN.values, color= 'b', lw=1,label="$YIN$")
    ax2.plot(df.date.values,df.YANG.values, color= 'b', lw=1,label="$YANG$")
    ax2.plot(df.date.values, df.ZL.values, color= g.cns['cornflowerblue'], lw=3,label="$ZL$")
    ax2.plot(df.date.values, df.HT.values, color= g.cns['plum'], lw=2,label="$HT$",linestyle=':')
    
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax2.tick_params(axis='x', colors=g.utg)
    ax2.tick_params(axis='y', colors=g.utg)
    ax2.grid(True, color='r')
    plt.ylabel('HPYYX', color=g.utg)
    plt.legend() # 显示图中右上角的提示信息。
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6, prune='upper'))
    return ax2


#用户自定义指标绘图
def draw_UFN(ax1,mydf):
    ax2 = plt.subplot2grid((7,4), (5,0), sharex=ax1, rowspan=2, colspan=4,fc=g.ubg)
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
    
    #df格式必须使用tushare数据格式,
    df=mydf.copy()
    #KDJ python随机指标
    def KDJ(N=9, M1=3, M2=3):
        RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
        K = SMA(RSV,M1,1)
        D = SMA(K,M2,1)
        J = 3*K-2*D
        return K, D, J

    #使用KDJ指标，返回K，D，J序列。
    K,D,J=KDJ(9,3,3)
    
    df = df.join(pd.Series( K,name='K'))
    df = df.join(pd.Series( D,name='D'))
    df = df.join(pd.Series( J,name='J'))

    ax2.plot(df.date.values, df.K.values, color= 'green', lw=2,label="$K$")
    ax2.plot(df.date.values,df.D.values, color= 'red', lw=2,label="$D$")
    ax2.plot(df.date.values, df.J.values, color= 'blue', lw=2,label="$J$")
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax2.tick_params(axis='x', colors=g.utg)
    ax2.tick_params(axis='y', colors=g.utg)
    ax2.grid(True, color='r')
    plt.ylabel('UserFun', color='w')
    plt.legend() # 显示图中右上角的提示信息。
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6, prune='upper'))
    return ax2



#在ax区绘制荷蒲操盘线HPCPX
def ax_HPCPX(ax1,mydf):
    CLOSE=mydf['close']
    LOW=mydf['low']
    HIGH=mydf['high']
    OPEN=mydf['open']
    VOL=mydf['volume']
    df=mydf.copy()

    def HPCPX():
        S0=(CLOSE+OPEN+LOW+HIGH)/4
        S1=EMA(SLOPE(S0,5),60)
        S2=EMA(S1,20)
        S3=IF(S1>=0,S1,DRAWNULL())
        S4=IF(S1>S2 ,S3,DRAWNULL())
        return S1,S2,S4
    #使用KDJ指标，返回K，D，J序列。
    x,y,z=HPCPX()
    
    df = df.join(pd.Series( x,name='CPX'))
    df = df.join(pd.Series( y,name='Y'))
    df = df.join(pd.Series( z,name='Z'))
    df['Y0']=0
    
    
    #开始绘图
    ax1.plot(df.date.values,df.CPX.values, color= 'green', lw=2,label="荷蒲操盘线")
    ax1.plot(df.date.values, df.Z.values, color= 'red', lw=2)
    ax1.plot(df.date.values, df.Y0.values, color= 'yellow', lw=2)
    #text = ax1.text(0.05, 0.05, '红线持股！绿线持币！', fontdict={'size': 20},color='yellow')
    plt.ylabel('HPCPX', color='white')
    plt.legend() # 显示图中右上角的提示信息。
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(8))  #x轴分成几等分     
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='upper'))
    ax1.grid(True, color='r')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    plt.subplots_adjust(left=.075, bottom=.08, right=.96, top=.96, wspace=.15, hspace=0.1)
    #plt.close() # 关窗口
    return ax1

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