from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import os.path
import time
import sys


import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

from datetime import timedelta


class OrderExecutionStrategy(bt.Strategy):
    params = (
        ('smaperiod', 15),
        ('exectype', 'StopTrailLimit'),
        #('exectype', 'StopTrail'),
        ('perc1', 0.5),
        ('perc2', 0.2),
        ('valid', 10), 
        ('trailamount', 0.0),
        ('trailpercent', 0.03),
        ('traillimit', 0.02)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime.date(0)
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        #print('%s, %s' % (dt.isoformat(), txt))
        print('%s, %s' % (dt.strftime('%Y-%m-%d'), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            #self.log('ORDER ACCEPTED/SUBMITTED', dt=order.created.dt)
            self.log('ORDER SUBMITTED')
            self.order = order
            return

        if order.status in [order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED')
            self.order = order
            return

        self.log(
            'Open: %.2f, High: %.2f, Low: %.2f, Close: %.2f' %
            (
            self.data.open[0],
            self.data.high[0],
            self.data.low[0], 
            self.data.close[0], 
            ))

        if order.status in [order.Expired]:
            if order.isbuy():
                self.log('BUY EXPIRED')
            else:
                self.log('SELL EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    #'BUY EXECUTED, Price: %.2f, Cost: %.2f' %
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f.' %
                    (order.executed.price,
                     order.executed.value,
                     ))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f.' %
                    (order.executed.price,
                     order.executed.value,
                     ))
            
        # Sentinel to None: new orders allowed
        self.order = None

    def __init__(self):
        # SimpleMovingAverage on main data
        # Equivalent to -> sma = btind.SMA(self.data, period=self.p.smaperiod)
        sma = btind.SMA(period=self.p.smaperiod)

        # CrossOver (1: up, -1: down) close / sma
        self.buysell = btind.CrossOver(self.data.close, sma, plot=False)

        if self.p.exectype in ['Stop', 'Limit']:
            self.p.valid = 4
        elif self.p.exectype in ['StopLimit']:
            self.p.valid = 10

        # Sentinel to None: new ordersa allowed
        self.order = None

    def next(self):
        if self.order:
            # An order is pending ... nothing can be done
            if self.order.issell() and self.p.exectype in ['StopTrail']:
                if self.p.trailamount:
                    check = self.data.close - self.p.trailamount
                else:
                    check = self.data.close * (1.0 - self.p.trailpercent)
                self.log('Open: %.2f, High: %.2f, Low: %.2f, Close: %.2f, Stop Price: %.2f, Check Price: %.2f' %
                    (self.data.open[0],
                    self.data.high[0],
                    self.data.low[0], 
                    self.data.close[0],
                    self.order.created.price,
                    check
                    ))
            elif self.order.isbuy() and self.p.exectype in ['StopTrailLimit']:
                if self.p.trailamount:
                    check = self.data.close + self.p.trailamount
                else:
                    check = self.data.close * (1.0 + self.p.trailpercent)

                self.log('Open: %.2f, High: %.2f, Low: %.2f, Close: %.2f, Stop Price: %.2f, Check Price: %.2f, Limit Price: %.2f' %
                    (self.data.open[0],
                    self.data.high[0],
                    self.data.low[0], 
                    self.data.close[0],
                    self.order.created.price,
                    check,
                    self.order.created.pricelimit
                    ))
                '''
            elif self.order.issell() and self.p.exectype in ['StopTrailLimit']:
                if self.p.trailamount:
                    check = self.data.close - self.p.trailamount
                else:
                    check = self.data.close * (1.0 - self.p.trailpercent)
                self.log('Open: %.2f, High: %.2f, Low: %.2f, Close: %.2f, Stop Price: %.2f, Check Price: %.2f, Limit Price: %.2f' %
                    (self.data.open[0],
                    self.data.high[0],
                    self.data.low[0], 
                    self.data.close[0],
                    self.order.created.price,
                    check,
                    self.order.created.pricelimit
                    ))
            '''
            else:
                self.log('Open: %.2f, High: %.2f, Low: %.2f, Close: %.2f' %
                    (self.data.open[0],
                    self.data.high[0],
                    self.data.low[0], 
                    self.data.close[0],
                    ))
            return

        # 检查是否持仓
        if self.position:
            # 检查是否达到卖出条件
            if self.buysell < 0 and self.p.exectype not in ['StopTrail']:
                if self.p.valid:
                    valid = self.data.datetime.date(0) + \
                            datetime.timedelta(days=self.p.valid)
                else:
                    valid = None
                if self.p.exectype in ['Market', 'StopTrailLimit']:
                    self.sell(exectype = bt.Order.Market)
                    self.log('SELL CREATE, exectype Market, close %.2f' % 
                             self.data.close[0])
                elif self.p.exectype == 'Close':
                    self.sell(exectype = bt.Order.Close)
                    self.log('SELL CREATE, exectype Close, close %.2f' % 
                             self.data.close[0])
                elif self.p.exectype == 'Limit':
                    price = self.data.close * (1.0 + self.p.perc1 / 100.0)
                    self.sell(exectype=bt.Order.Limit, price=price, valid=valid)
                    if self.p.valid:
                        txt = 'SELL CREATE, exectype Limit, close %.2f, price %.2f, valid: %s'
                        self.log(txt % (self.data.close[0], price, valid.strftime('%Y-%m-%d')))
                    else:
                        txt = 'SELL CREATE, exectype Limit, close %.2f, price %.2f'
                        self.log(txt % (self.data.close[0], price))
                elif self.p.exectype == 'Stop':
                    price = self.data.close * (1.0 - self.p.perc1 / 100.0)
                    self.sell(exectype=bt.Order.Stop, price=price, valid=valid)
                    if self.p.valid:
                        txt = 'SELL CREATE, exectype Stop, close %.2f, price %.2f, valid: %s'
                        self.log(txt % (self.data.close[0], price, valid.strftime('%Y-%m-%d')))
                    else:
                        txt = 'SELL CREATE, exectype Stop, close %.2f, price %.2f'
                        self.log(txt % (self.data.close[0], price))
                elif self.p.exectype == 'StopLimit':
                    price = self.data.close * (1.0 - self.p.perc1 / 100.0)
                    plimit = self.data.close * (1.0 - self.p.perc2 / 100.0)
                    self.sell(exectype=bt.Order.StopLimit, price=price, valid=valid, plimit = plimit)
                    if self.p.valid:
                        txt = 'SELL CREATE, exectype StopLimit, close %.2f, price %.2f, pricelimit %.2f, valid: %s'
                        self.log(txt % (self.data.close[0], price, plimit, valid.strftime('%Y-%m-%d')))
                    else:
                        txt = 'SELL CREATE, exectype StopLimit, close %.2f, price %.2f, pricelimit %.2f'
                        self.log(txt % (self.data.close[0], price, plimit))
                '''
                elif self.p.exectype == "StopTrailLimit":
                    price = self.data.close[0]
                    plimit = self.data.close[0] * (1.0 + self.p.traillimit)
                    st_order = self.sell(exectype=bt.Order.StopTrailLimit,
                                   trailamount=self.p.trailamount,
                                   trailpercent=self.p.trailpercent,
                                   #price = price,
                                   plimit = plimit)
                    if self.p.trailamount:
                        check = self.data.close - self.p.trailamount
                    else:
                        check = self.data.close * (1.0 - self.p.trailpercent)
                    txt = 'SELL CREATE, exectype StopTrailLimit, close %.2f, stop price %.2f, check price %.2f, limit price %.2f'
                    self.log(txt % (self.data.close[0], st_order.created.price, check, plimit))
                '''
            elif self.p.exectype in ['StopTrail']:
                st_order = self.sell(exectype=bt.Order.StopTrail,
                                #price = self.data.close[0],
                                trailamount=self.p.trailamount,
                                trailpercent=self.p.trailpercent)
                if self.p.trailamount:
                    check = self.data.close - self.p.trailamount
                else:
                    check = self.data.close * (1.0 - self.p.trailpercent)
                txt = 'SELL CREATE, exectype StopTrail, close %.2f, stop price %.2f, check price %.2f'
                self.log(txt % (self.data.close[0], st_order.created.price, check))


        # 不在场内且出现买入信号
        elif self.buysell > 0:
            if self.p.valid:
                valid = self.data.datetime.date(0) + \
                        datetime.timedelta(days=self.p.valid)
            else:
                valid = None

            if self.p.exectype in ['Market', 'StopTrail']:
                self.buy(exectype=bt.Order.Market)  # Market是默认的订单类型
                self.log('BUY CREATE, exectype Market, close %.2f' %
                         self.data.close[0])

            elif self.p.exectype == 'Close':
                self.buy(exectype=bt.Order.Close)
                self.log('BUY CREATE, exectype Close, close %.2f' %
                         self.data.close[0])

            elif self.p.exectype == 'Limit':
                price = self.data.close * (1.0 - self.p.perc1 / 100.0)
                self.buy(exectype=bt.Order.Limit, price=price, valid=valid)
                if self.p.valid:
                    txt = 'BUY CREATE, exectype Limit, close %.2f, price %.2f, valid: %s'
                    self.log(txt % (self.data.close[0], price, valid.strftime('%Y-%m-%d')))
                else:
                    txt = 'BUY CREATE, exectype Limit, close %.2f, price %.2f'
                    self.log(txt % (self.data.close[0], price))

            elif self.p.exectype == 'Stop':
                price = self.data.close * (1.0 + self.p.perc1 / 100.0)
                self.buy(exectype=bt.Order.Stop, price=price, valid=valid)
                if self.p.valid:
                    txt = 'BUY CREATE, exectype Stop, close %.2f, price %.2f, valid: %s'
                    self.log(txt % (self.data.close[0], price, valid.strftime('%Y-%m-%d')))
                else:
                    txt = 'BUY CREATE, exectype Stop, close %.2f, price %.2f'
                    self.log(txt % (self.data.close[0], price))

            elif self.p.exectype == 'StopLimit':
                price = self.data.close * (1.0 + self.p.perc1 / 100.0)

                plimit = self.data.close * (1.0 + self.p.perc2 / 100.0)

                self.buy(exectype=bt.Order.StopLimit, price=price, valid=valid,
                         plimit=plimit)

                if self.p.valid:
                    txt = ('BUY CREATE, exectype StopLimit, close %.2f, price %.2f,'
                           ' pricelimit %.2f, valid: %s')
                    self.log(txt % (self.data.close[0], price, plimit, valid.strftime('%Y-%m-%d')))
                else:
                    txt = ('BUY CREATE, exectype StopLimit, close %.2f, price %.2f,'
                           ' pricelimit: %.2f')
                    self.log(txt % (self.data.close[0], price, plimit))
            elif 'StopTrailLimit' == self.p.exectype:
                    price = self.data.close[0]
                    plimit = self.data.close[0] * (1.0 - self.p.traillimit)
                    st_order = self.buy(exectype=bt.Order.StopTrailLimit,
                                   trailamount=self.p.trailamount,
                                   trailpercent=self.p.trailpercent,
                                   #price = price,
                                   plimit = plimit)
                    if self.p.trailamount:
                        check = self.data.close + self.p.trailamount
                    else:
                        # 指定price值
                        #check = self.data.close * (1.0 + self.p.trailpercent)
                        # 不指定price值
                        check = plimit * (1.0 + self.p.trailpercent)
                    txt = 'BUY CREATE, exectype StopTrailLimit, close %.2f, stop price %.2f, check price %.2f, limit price %.2f'
                    self.log(txt % (self.data.close[0], st_order.created.price, check, st_order.created.pricelimit))

cerebro = bt.Cerebro()  # 创建cerebro
# 先找到脚本的位置，然后根据脚本与数据的相对路径关系找到数据位置
# 这样脚本从任意地方被调用，都可以正确地访问到数据
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, '../TQDat/day/stk/000001.csv')
# 创建价格数据
data = bt.feeds.GenericCSVData(
        dataname = datapath,
        fromdate = datetime.datetime(2019, 1, 1),
        todate = datetime.datetime(2019, 12, 31),
        nullvalue = 0.0,
        #dtformat = ('%Y/%m/%d'),
        dtformat = ('%Y-%m-%d'),
        datetime = 0,
        open = 1,
        high = 2,
        low = 3,
        close = 4,
        volume = 5,
        openinterest = -1
        )
# 在Cerebro中添加价格数据
cerebro.adddata(data)
# 设置启动资金
cerebro.broker.setcash(100000.0)
# 设置交易单位大小
cerebro.addsizer(bt.sizers.FixedSize, stake = 100)
cerebro.addstrategy(OrderExecutionStrategy)  # 添加策略
cerebro.run()  # 遍历所有数据
#'''
cerebro.plot(start=datetime.date(2019, 4, 1), end=datetime.date(2019, 5, 31), 
            volume = False, style = 'candle',
            barup = 'red', bardown = 'green')  # 绘图
#'''
#cerebro.plot(volume = False, style = 'candle', barup = 'red', bardown = 'green')  # 绘图