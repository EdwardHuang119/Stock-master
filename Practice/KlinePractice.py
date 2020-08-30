#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import reduce

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
# from matplotlib.finance import candlestick_ohlc
import mplfinance as mpf
# import mpl_finance as mpf
import talib
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime as dt
import pylab
from Test.TushareProApi import *
from Test.TryTensentCloud import *
import functools



show = True
show_func = print if show else lambda a: a
start_date = '2020-01-01'
time_temp =dt.datetime.now()
end_date = time_temp.strftime('%Y-%m-%d')
# show_func(enddate)

MA1 = 10
MA2 = 20

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

def MA(data, para):
    MAdata = talib.MA(data, para)
    return MAdata

def SMA(vals, n, m) :
    # 算法1
    return functools.reduce(lambda x, y: ((n - m) * x + y * m) / n, vals)

def EMA(vals, n):
    return SMA(vals, n+1, 2)

def get_EMA(df,N):
    for i in range(len(df)):
        if i==0:
            df.ix[i,'ema']=df.ix[i,'close']
        if i>0:
            df.ix[i,'ema']=(2*df.ix[i,'close']+(N-1)*df.ix[i-1,'ema'])/(N+1)
            # df.ix[i,'ena'] = EMA(df.ix[i,'close'],N)
    ema=list(df['ema'])
    return ema


def callMacd(short=12,long=26,M=9):
    # 数据准备
    days = get_data('600004.SH', start_date, end_date)
    data = days.reset_index()
    # data['trade_date'] = mdates.date2num(data['trade_date'])
    data.drop(['ts_code', 'change', 'pct_chg', 'vol', 'amount', 'pre_close'], axis=1, inplace=True)
    data = data.reindex(columns=['trade_date', 'open', 'high', 'low', 'close'])

    a = get_EMA(data,short)
    b = get_EMA(data,long)
    data['diff'] = pd.Series(a) - pd.Series(b)
    # show_func(data)
    # data['dea'] = 0
    for i in range(len(data)):
        if i == 0:
            data.ix[i, 'dea'] = data.ix[i, 'diff']
        if i > 0:
            data.ix[i, 'dea'] = (2 * data.ix[i, 'diff'] + (M - 1) * data.ix[i - 1, 'dea']) / (M + 1)
    data['macd'] = 2 * (data['diff'] - data['dea'])
    return data


def macd():
    days = get_data('600004.SH',start_date,end_date)
    data = days.reset_index()
    data['trade_date'] = mdates.date2num(data['trade_date'])
    data.drop(['ts_code', 'change', 'pct_chg', 'vol', 'amount', 'pre_close'], axis=1, inplace=True)
    data = data.reindex(columns=['trade_date', 'open', 'high', 'low', 'close'])
    nslow = 26
    nfast = 12
    nema = 9
    emaslow, emafast, macd=talib.MACD(data.close.values,fastperiod=nfast, slowperiod=nslow, signalperiod=nema)
    days['emaslow'] = emaslow
    days['enafast'] = emafast
    days['macd'] = macd*2
    Tocsv(days,'','macd(600004)')
    return (emaslow)

def data_clean(data):
    data.drop(['ts_code', 'change', 'pct_chg', 'amount', 'pre_close'], axis=1, inplace=True)
    data = data.reindex(columns=['trade_date', 'open', 'high', 'low', 'close', 'vol'])
    data.columns = ['Date', 'Open','High','Low','Close','Volume']
    pd_date = pd.DatetimeIndex(data['Date'].values)
    data['Date'] = pd_date
    data.set_index(["Date"],inplace=True)
    return data

def main_2():
    days = get_data('000001.SZ',start_date,'2020-06-30')
    data = days.reset_index()
    data = data_clean(data)
    mpf.plot(data,type='candle',mav=(2, 5, 10),volume=True)

def setlist(one_list):
    return list(set(one_list))

def marginofma(tscode,start_date,end_date,ma):
    days = get_data(tscode,start_date,end_date)
    data = days.reset_index()
    ts_code_list = data['ts_code'].tolist()
    ts_code_list = setlist(ts_code_list)
    data_2 =pd.DataFrame()
    starttime = dt.datetime.now()
    print('%s已经开始计算均线差值'%(starttime))
    for i in range(len(ts_code_list)):
        data_per = data.loc[data['ts_code'] == ts_code_list[i]].copy()
        # 防止链式调用，所以直接用了一个新的Copy，有可能占用内存
        show_func(data_per.head())
        data_per['MA20'] = MA(data_per.close.values, 20)
        Max_tradedate = data_per['trade_date'].max()
        data_3 = data_per.loc[data_per['trade_date'] == Max_tradedate]
        # data_3['marginochange'] = data_3['close'] - data_3
        data_2 = pd.concat([data_2, data_3],ignore_index=True)
        # print('已经获取%s的数据' % (ts_code_list[i]))
        i = i + 1
    # data_2 = data_2.reset_index()
    endtime = dt.datetime.now()
    Tocsv(data_2,'','data_2_pra_test')
    timeconsuming = endtime-starttime
    print('%s已经开始计算均线差值,共耗时%s' % (endtime,timeconsuming))
    return data_2

def main():
    days = get_data('000001.SZ',start_date,'2020-06-30')
    data = days.reset_index()
    data['trade_date'] = mdates.date2num(data['trade_date'])

    data.drop(['ts_code', 'change', 'pct_chg', 'vol', 'amount', 'pre_close'], axis=1, inplace=True)
    data = data.reindex(columns=['trade_date', 'open', 'high', 'low', 'close'])
    '''
    data.drop(['ts_code', 'change', 'pct_chg', 'amount', 'pre_close'], axis=1, inplace=True)
    # data = data.reindex(columns=['Date', 'Open', 'High', 'Low', 'Close','Volume'])
    show_func(data.head())
    '''
    Av1 = talib.MA(data.close.values, MA1)
    Av2 = talib.MA(data.close.values, MA2)
    # Av1 = movingaverage(data.close.values, MA1)
    # Av2 = movingaverage(data.close.values, MA2)
    SP = len(data.trade_date.values[MA2 - 1:])
    fig = plt.figure(facecolor='#07000d', figsize=(15, 10))

    ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, facecolor='#07000d')
    mpf.candlestick_ohlc(ax1, data.values[-SP:], width=.6, colorup='#ff1717', colordown='#53c156')
    # mpf.plot(data)
    Label1 = str(MA1) + ' SMA'
    Label2 = str(MA2) + ' SMA'

    ax1.plot(data.trade_date.values[-SP:], Av1[-SP:], '#e1edf9', label=Label1, linewidth=1.5)
    ax1.plot(data.trade_date.values[-SP:], Av2[-SP:], '#4ee6fd', label=Label2, linewidth=1.5)
    ax1.grid(True, color='w')
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
    plt.ylabel('Stock price and Volume')
    # 绘制成交量图
    volumeMin = 0
    # 先通过twinx来表达和ax1公用一个x轴
    ax1v = ax1.twinx()
    # 通过fill——between这个函数来表达准备把这个数据全部弄成某个颜色
    ax1v.fill_between(data.trade_date.values[-SP:], volumeMin, days.vol.values[-SP:], facecolor='#00ffe8',
                      alpha=.4)
    ax1v.axes.yaxis.set_ticklabels([])
    ax1v.grid(False)
    ###Edit this to 3, so it's a bit larger
    ax1v.set_ylim(0, 3 * days.vol.values.max())
    ax1v.spines['bottom'].set_color("#5998ff")
    ax1v.spines['top'].set_color("#5998ff")
    ax1v.spines['left'].set_color("#5998ff")
    ax1v.spines['right'].set_color("#5998ff")
    ax1v.tick_params(axis='x', colors='w')
    ax1v.tick_params(axis='y', colors='w')
    # 我们画一下RSI图
    # plot an RSI indicator on top
    maLeg = plt.legend(loc=9, ncol=2, prop={'size': 7},
                       fancybox=True, borderaxespad=0.)
    maLeg.get_frame().set_alpha(0.4)
    textEd = pylab.gca().get_legend().get_texts()
    pylab.setp(textEd[0:5], color='w')

    ax0 = plt.subplot2grid((6, 4), (0, 0), sharex=ax1,rowspan=1, colspan=4,facecolor='#07000d')
    # rsi = rsiFunc(data.Close.values)
    rsi = talib.RSI(data.close.values)
    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    negCol = '#8f2020'

    ax0.plot(data.trade_date.values[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
    ax0.axhline(70, color=negCol)
    ax0.axhline(30, color=posCol)
    ax0.fill_between(data.trade_date.values[-SP:], rsi[-SP:], 70, where=(rsi[-SP:] >= 70), facecolor=negCol,
                     edgecolor=negCol, alpha=0.5)
    ax0.fill_between(data.trade_date.values[-SP:], rsi[-SP:], 30, where=(rsi[-SP:] <= 30), facecolor=posCol,
                     edgecolor=posCol, alpha=0.5)
    ax0.set_yticks([30, 70])
    ax0.yaxis.label.set_color("w")
    ax0.spines['bottom'].set_color("#5998ff")
    ax0.spines['top'].set_color("#5998ff")
    ax0.spines['left'].set_color("#5998ff")
    ax0.spines['right'].set_color("#5998ff")
    ax0.tick_params(axis='y', colors='w')
    ax0.tick_params(axis='x', colors='w')
    plt.ylabel('RSI')

    # MACD图
    # plot an MACD indicator on bottom
    ax2 = plt.subplot2grid((6, 4), (5, 0), sharex=ax1, rowspan=1, colspan=4, facecolor='#07000d')
    fillcolor = '#00ffe8'
    nslow = 26
    nfast = 12
    nema = 9
    emaslow, emafast, macd=talib.MACD(data.close.values,fastperiod=nfast, slowperiod=nslow, signalperiod=nema)
    ax2.plot(data.trade_date.values[-SP:], emaslow[-SP:], color='#4ee6fd', lw=2)
    ax2.plot(data.trade_date.values[-SP:], emafast[-SP:], color='#e1edf9', lw=1)
    # bar = np.where(macd,2*macd,0)
    '''
    bar_red = np.where(macd > 0, 2 * macd, 0)  # 绘制BAR>0 柱状图
    bar_green = np.where(macd < 0, 2 * macd, 0)  # 绘制BAR<0 柱状图
    show_func(bar_red)
    ax2.bar(data.trade_date.values[-SP:], bar_red[-SP:], facecolor='red')
    ax2.bar(data.trade_date.values[-SP:], bar_green[-SP:], facecolor='green')
    '''
    # ax2.bar(data.trade_date.values[-SP:], macd[-SP:],facecolor=fillcolor)
    ax2.fill_between(data.trade_date.values[-SP:], macd[-SP:]*2, 0, alpha=0.5, facecolor=fillcolor,
                     edgecolor=fillcolor)
    # ax2.fill_between(data.trade_date.values[-SP:], macd[-SP:] - ema9[-SP:], 0, alpha=0.5, facecolor=fillcolor,edgecolor=fillcolor)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax2.spines['bottom'].set_color("#5998ff")
    ax2.spines['top'].set_color("#5998ff")
    ax2.spines['left'].set_color("#5998ff")
    ax2.spines['right'].set_color("#5998ff")
    ax2.tick_params(axis='x', colors='w')
    ax2.tick_params(axis='y', colors='w')
    plt.ylabel('MACD', color='w')
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))
    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)
    # 展示图
    plt.ylabel('MACD')
    plt.show()

if __name__ == "__main__":
    # main()
    # main_2()
    # marginofma(['000001.SZ','601398.SH'],'2020-02-01','2020-08-25',10)
    index_code = index_
    '''
    
    days = get_data(['000001.SZ','601398.SH'],start_date,'2020-06-30')
    data = days.reset_index()
    data['MA5'] = MA(data.close.values,5)
    Tocsv(data,'','Practise')
    show_func(data.head())
    '''
