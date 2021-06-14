# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架 指标公式绘图库
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

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import datetime as dt
import pylab
import matplotlib
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from tkinter import ttk
from PIL import Image, ImageTk
import HP_VIEW.HP_zwdata as sd
from HP_VIEW.HP_global import *
from HP_VIEW.HP_set import *
import HP_VIEW.HP_lib as mylib


def draw_OBV(ax1,days,x,y):
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        df=mylib.OBVX(days,x,y)
        ax2 = plt.subplot2grid((7,4), (5,0), sharex=ax1, rowspan=2, colspan=4, axisbg='#07000d')
        fillcolor = '#00ffe8'
        ax2.plot(df.date.values, df.OBV_6.values, color=rsiCol, lw=2)
        ax2.plot(df.date.values, df.OBV_12.values, color=posCol, lw=2)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        ax2.grid(True, color='r')
        plt.ylabel('OBV', color='w')
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6, prune='upper'))
        return

def draw_RSI(ax1,days,x,y,z):
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        df=mylib.RSIX(days,x,'RSI1')
        df=mylib.RSIX(df,y,'RSI2')
        df=mylib.RSIX(df,z,'RSI3')
        ax2 = plt.subplot2grid((7,4), (5,0), sharex=ax1, rowspan=2, colspan=4, axisbg='#07000d')
        fillcolor = '#00ffe8'
        ax2.plot(df.date.values, df.RSI1.values, color=rsiCol, lw=2)
        ax2.plot(df.date.values, df.RSI2.values, color=posCol, lw=2)
        ax2.plot(df.date.values, df.RSI3.values, color=negCol, lw=2)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        ax2.axhline(80, color=negCol)
        ax2.axhline(20, color=posCol)
        plt.ylabel('RSI', color='w')
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6, prune='upper'))
        return

def draw_KDJ(ax1,days,x,y,z):
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        df=mylib.KDJ(days,x,y,z)
        ax2 = plt.subplot2grid((7,4), (5,0), sharex=ax1, rowspan=2, colspan=4, axisbg='#07000d')
        fillcolor = '#00ffe8'
        ax2.plot(df.date.values, df.K.values, color=rsiCol, lw=2)
        ax2.plot(df.date.values, df.D.values, color=posCol, lw=2)
        ax2.plot(df.date.values, df.J.values, color=negCol, lw=2)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        ax2.axhline(80, color=negCol)
        ax2.axhline(20, color=posCol)
        plt.ylabel('KDJ', color='w')
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6, prune='upper'))
        return
        
def draw_MACD(ax1,days,x,y,z):
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        df=mylib.MACD(days,x,y)
        ax2 = plt.subplot2grid((7,4), (5,0), sharex=ax1, rowspan=2, colspan=4, axisbg='#07000d')
        fillcolor = '#00ffe8'
        ax2.plot(df.date.values, df.MACDsign_12_26.values, color=rsiCol, lw=1)
        ax2.plot(df.date.values, df.MACD_12_26.values, color=negCol, lw=1)
        ax2.fill_between(df.date.values, df.MACDdiff_12_26.values, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        ax2.axhline(0, color=negCol)
        plt.ylabel('MACD', color='w')
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='upper'))
        return     

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