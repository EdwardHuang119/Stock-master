#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backtrader as bt
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
#正常显示画图时出现的中文和负号
from pylab import mpl
from Test.TushareProApi import *
from Test.TryTensentCloud import *

show = True
show_func = print if show else lambda a: a

# print(bt.__file__)
# class my_strategy2(bt.Strategy)


class my_strategy1(bt.Strategy):
    #全局设定交易策略的参数
    params=(
        ('maperiod',20),
           )

    def __init__(self):
        #指定价格序列
        self.dataclose=self.datas[0].close
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None
        #添加移动均线指标，内置了talib模块
        self.sma = bt.indicators.SimpleMovingAverage(
                      self.datas[0], period=self.params.maperiod)

    def next(self):
        if self.order: # 检查是否有指令等待执行,
            return
        # 检查是否持仓
        if not self.position: # 没有持仓
            #执行买入条件判断：收盘价格上涨突破20日均线
            if self.dataclose[0] > self.sma[0]:
                #执行买入
                self.order = self.buy(size=500)
        else:
            #执行卖出条件判断：收盘价格跌破20日均线
            if self.dataclose[0] < self.sma[0]:
                #执行卖出
                self.order = self.sell(size=500)

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


df=get_data('600000.SH','2015-01-01','2020-05-01')
df.index=pd.to_datetime(df.trade_date)
df['openinterest']=0
df = df.rename(columns={'vol':'volume'})
df=df[['open','high','low','close','volume','openinterest']]
start=dt(2015, 1, 1)
end=dt(2020, 3, 31)
# 加载数据
data = bt.feeds.PandasData(dataname=df,fromdate=start,todate=end)
# show_func(df.head())

# 初始化cerebro回测系统设置
cerebro = bt.Cerebro()
#将数据传入回测系统
cerebro.adddata(data)
# 将交易策略加载到回测系统中
cerebro.addstrategy(my_strategy1)
# 设置初始资本为10,000
startcash = 10000
cerebro.broker.setcash(startcash)
# 设置交易手续费为 0.2%
cerebro.broker.setcommission(commission=0.002)
# print(f'净收益: {round(pnl,2)}')

d1=start.strftime('%Y%m%d')
d2=end.strftime('%Y%m%d')
print(f'初始资金: {startcash}\n回测期间：{d1}:{d2}')
#运行回测系统
cerebro.run()
#获取回测结束后的总资金
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash
#打印结果
print(f'总资金: {round(portvalue,2)}')
