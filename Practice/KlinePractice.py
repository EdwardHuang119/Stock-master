#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
# from matplotlib.finance import candlestick_ohlc
import mpl_finance as mpf
import talib
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime as dt
import pylab
from Test.TushareProApi import *
from Test.TryTensentCloud import *


show = True
show_func = print if show else lambda a: a
start_date = '2019-06-01'
time_temp =dt.datetime.now()
end_date = time_temp.strftime('%Y-%m-%d')
# show_func(enddate)

MA1 = 10
MA2 = 20

def get_data(ts_code,start_date,end_date):
    engine = connect_db_engine()
    # sql = """select * from stock_china_daily where trade_date >= '2020-01-01'"""
    sql = "select * from stock_china_daily where ts_code = '%s' and trade_date between '%s' and '%s'" %(ts_code,start_date,end_date)
    df = pd.read_sql_query(sql, engine)
    engine.dispose()
    return df

def MA(data, para):
    MAdata = talib.MA(data, para)
    return MAdata

def main():
    data = get_data('000001.SZ','2020-01-01','2020-06-30')
    data['trade_date'] = mdates.date2num(data['trade_date'])
    data.drop(['ts_code', 'change', 'pct_chg', 'vol', 'amount', 'pre_close'], axis=1, inplace=True)
    data = data.reindex(columns=['trade_date', 'open', 'high', 'low', 'close'])

    Av1 = talib.MA(data.close.values, MA1)
    Av2 = talib.MA(data.close.values, MA2)
    # Av1 = movingaverage(data.close.values, MA1)
    # Av2 = movingaverage(data.close.values, MA2)
    SP = len(data.trade_date.values[MA2 - 1:])
    fig = plt.figure(facecolor='#07000d', figsize=(15, 10))

    ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, facecolor='#07000d')
    mpf.candlestick_ohlc(ax1, data.values[-SP:], width=.6, colorup='#ff1717', colordown='#53c156')
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
    plt.show()

if __name__ == "__main__":
    main()


'''
data = get_data('000001.SZ','2020-01-01','2020-06-30')
# daysreshape['DateTime']=mdates.date2num(daysreshape['DateTime'].astype(dt.date))
data['trade_date'] = mdates.date2num(data['trade_date'])
data.drop(['ts_code','change','pct_chg','vol','amount','pre_close'],axis=1,inplace=True)
data = data.reindex(columns=['trade_date', 'open', 'high', 'low', 'close'])
    # data['trade_date']
show_func(data)
show_func(data.close.values)
'''