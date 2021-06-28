# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架窗口模块
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

from tkinter import * 
from tkinter.messagebox import * 
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
# from matplotlib.finance import candlestick_ohlc
# from mplfinance import candlestick_ohlc
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
# from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import datetime as dt
import pylab
import matplotlib
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from tkinter import ttk
from PIL import Image, ImageTk
import HP_VIEW.HP_lib as mylib
import HP_VIEW.HP_draw as mydraw
from Test.TryTensentCloud import *

################################
#import HP_zwdata as sd
#import tushare as ts
# import jqdatasdk as jq
############################
from HP_VIEW.HP_global import *
from HP_VIEW.HP_set import *
import HP_VIEW.HP_lib as mylib
import HP_VIEW.HP_draw as mydraw
from Test.TushareProApi import *


def get_data(ts_code,start_date,end_date):
    engine = connect_db_engine()
    starttime = dt.datetime.now()
    print('%s开始获取数据'%(starttime))
    # sql = """select * from stock_china_daily where trade_date >= '2020-01-01'"""
    if type(ts_code) == str and str(ts_code) !='':
        sql = "select * from stock_china_daily where ts_code = '%s' and trade_date between '%s' and '%s'" %(ts_code,start_date,end_date)
    elif type(ts_code) == list:
        ts_code_tuple = tuple(ts_code)
        sql = "select * from stock_china_daily where ts_code in %s and trade_date between '%s' and '%s'" % (ts_code_tuple, start_date, end_date)
    elif type(ts_code) == str and str(ts_code) =='':
        sql = "select * from stock_china_daily where trade_date between '%s' and '%s'" % (start_date, end_date)
    df = pd.read_sql_query(sql, engine)
    engine.dispose()
    endtime = dt.datetime.now()
    print('%s数据已经获取'%(endtime))
    return df

def data_clean(data):
    data.drop(['ts_code', 'change', 'pct_chg', 'amount', 'pre_close'], axis=1, inplace=True)
    data = data.reindex(columns=['trade_date', 'open', 'high', 'low', 'close', 'vol'])
    data.columns = ['date', 'open','high','low','close','volume']
    pd_date = pd.DatetimeIndex(data['date'].values)
    data['date'] = pd_date
    data.set_index(["date"],inplace=True)
    return data

  
class plotFrame3(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.canvas=None
        self.root.config(bg='black')
        self.createPage()  
   
    def createPage(self):  
        ds=g.sday
        de=g.eday
        stockn=g.stock
        matplotlib.use('TkAgg')
        # df1 = jq.get_price(stockn,start_date=ds,end_date=de, frequency='daily') # 聚宽获取股票数据
        # df1 = ts.get_hist_data(stockn,start=ds,end=de)   # tushare获取股票 数据
        # df1 = Getdailyfromtscode(stockn,ds,de)
        df1 = get_data(stockn, ds, de)
        df1['trade_date'] = mdates.date2num(df1['trade_date'])
        df2=df1.copy()
        # df2.dropna(inplace=True)
        # df2.insert(0,'date',df2.index)
        df2 = df2.reset_index()
        # df2 = data_clean(df2)
        print(df1)
        print(df2)
        days=df2
        g.df=df2
        MA1 = g.MA1
        MA2 = g.MA2
        Av1=mylib.G_MA(days['close'],MA1)
        Av2=mylib.G_MA(days['close'],MA2)
        SP = len(days.trade_date.values[MA2-1:])
        SP1 = len(days.trade_date.values[MA1-1:])
        fig = plt.figure(facecolor='#07000d',figsize=(7,4))
        ax1 = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, facecolor='#07000d')
        daysreshape = days.reset_index()
        print(daysreshape)
        # daysreshape['trade_date']=mdates.date2num(daysreshape['trade_date'].astype(dt.date))
        daysreshape = daysreshape.reindex(columns=['date','open','high','low','close'])
        candlestick_ohlc(ax1, daysreshape.values, width=.6, colorup='#ff1717', colordown='#53c156')
        # candlestick_ohlc(ax1, daysreshape.values, width=.6, colorup='#ff1717', colordown='#53c156')
        Label1 = str(MA1)+' MA'
        Label2 = str(MA2)+' MA'
        ax1.plot(days.trade_date.values,Av1,'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(days.trade_date.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
        ax1.grid(True, color='r')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock price')
        ax1v = ax1.twinx()
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors='w')
        ax1v.tick_params(axis='y', colors='w')
        ax0 = plt.subplot2grid((7,4), (4,0),sharex=ax1,rowspan=1, colspan=4, facecolor='#07000d')
        v1=mylib.G_MA(days['vol'],g.MA1)
        v2=mylib.G_MA(days['vol'],g.MA2)
        v3=mylib.G_MA(days['vol'],g.MA3)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        ax0.plot(days.trade_date.values, v1, rsiCol, linewidth=1)
        ax0.plot(days.trade_date.values, v2, posCol, linewidth=1)
        ax0.bar(days.trade_date.values,days.vol.values, facecolor='yellow', alpha=.4)
        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))#plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(nbins=4,prune='upper'))
        ax0.tick_params(axis='x', colors='w')
        plt.ylabel('volume')                     
        if g.index=='KDJ' :
            mydraw.draw_KDJ(ax1,days,9,3,3)
        if g.index=='MACD' :
            mydraw.draw_MACD(ax1,days,12,26,9)
        if g.index=='RSI' :
            mydraw.draw_RSI(ax1,days,6,12,24)
        if g.index=='OBV' :
            mydraw.draw_OBV(ax1,days,6,12)               
        plt.suptitle(stockn,color='w')
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.subplots_adjust(left=.04, bottom=.04, right=.96, top=.96, wspace=.15, hspace=0)
        self.canvas =FigureCanvasTkAgg(fig, master=self.root)
        toolbar =NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

           
class MainFrame(Frame): # 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.createPage()  
   
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
        self.stock = StringVar()
        entrystock = Entry(self, textvariable=self.stock)
        entrystock.grid(row=0, column=8)
         
        Label(self , text='    ').grid(row=0, column=9)
        # 按钮  (Button)
        getname = Button(self , text='确认' ,command=self.st3)
        getname.grid(row=0, column=10)

        Label(self , text='    ').grid(row=0, column=11)
        label4 = Label(self , text='指标: ')
        label4.grid(row=0, column=12)
        
        # Adding a Combobox
        self.book = tk.StringVar()
        bookChosen = ttk.Combobox(self , width=10, textvariable=self.book)
        bookChosen['values'] = ('MACD', 'KDJ','RSI','OBV')
        bookChosen.grid(row=0, column=13)
        bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标
        bookChosen.config(state='readonly')  #设为只读模式

    def st3(self):  
        ds=self.date_s.get()
        de=self.date_e.get()
        stockn=self.stock.get()
        g.index=self.book.get()
        # stockn=mylib.jqsn(stockn)  # 聚宽股票代码转换，不是聚宽数据，要注释掉
        # self.canvas._tkcanvas.pack_forget()
        g.stock=stockn
        matplotlib.use('TkAgg')
        # df1 = jq.get_price(stockn,start_date=ds,end_date=de, frequency='daily') # 聚宽获取股票数据
        df1 = Getdailyfromtscode(stockn, ds, de)
        
        print(df1)
        df2=df1.copy()
        df2.dropna(inplace=True)
        df2.insert(0,'date',df2.index)
        df2=df2.sort_values(axis=0,ascending=True,by='trade_date')
        df2=df2.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        print(df2)

        days=df2
        g.df=df2
        MA1 = g.MA1
        MA2 = g.MA2
        Av1=mylib.G_MA(days['close'],MA1)
        Av2=mylib.G_MA(days['close'],MA2)
        SP = len(days.trade_date.values[MA2-1:])
        SP1 = len(days.trade_date.values[MA1-1:])
        fig = plt.figure(facecolor='#07000d',figsize=(7,4))
        ax1 = plt.subplot2grid((7,4), (0,0), rowspan=4, colspan=4, facecolor='#07000d')
        daysreshape = days.reset_index()
        # daysreshape['date']=mdates.date2num(daysreshape['date'].astype(dt.date))
        daysreshape = daysreshape.reindex(columns=['date','open','high','low','close'])   
        candlestick_ohlc(ax1, daysreshape.values, width=.6, colorup='#ff1717', colordown='#53c156')
        Label1 = str(MA1)+' MA'
        Label2 = str(MA2)+' MA'
        ax1.plot(days.trade_date.values,Av1,'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(days.trade_date.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
        ax1.grid(True, color='r')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock price')
        ax1v = ax1.twinx()
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors='w')
        ax1v.tick_params(axis='y', colors='w')
        ax0 = plt.subplot2grid((7,4), (4,0),sharex=ax1,rowspan=1, colspan=4, facecolor='#07000d')
        v1=mylib.G_MA(days['vol'],g.MA1)
        v2=mylib.G_MA(days['vol'],g.MA2)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        ax0.plot(days.trade_date.values, v1, rsiCol, linewidth=1)
        ax0.plot(days.trade_date.values, v2, posCol, linewidth=1)
        ax0.bar(days.trade_date.values,days.vol.values, facecolor='yellow', alpha=.4)
        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        ax0.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))#plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(nbins=4,prune='upper'))
        ax0.tick_params(axis='x', colors='w')
        plt.ylabel('volume')                     
        if g.index=='KDJ' :
            mydraw.draw_KDJ(ax1,days,9,3,3)
        if g.index=='MACD' :
            mydraw.draw_MACD(ax1,days,12,26,9)
        if g.index=='RSI' :
            mydraw.draw_RSI(ax1,days,6,12,24)
        if g.index=='OBV' :
            mydraw.draw_OBV(ax1,days,6,12)    
        plt.suptitle(stockn,color='w')
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.subplots_adjust(left=.04, bottom=.04, right=.96, top=.96, wspace=.15, hspace=0)
        self.canvas =FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
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