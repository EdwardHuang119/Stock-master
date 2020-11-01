#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backtrader as bt

class my_strategy2(bt.Strategy):
    # 均线的交叉策略
    #全局设定交易策略的参数
    params=(
        ('pfast',10),  # 短期均线周期
        ('pslow',60),  # 长期均线周期
        ('printlog', True)  # 默认打印日志
           )

    def __init__(self):
        #指定价格序列
        self.dataclose=self.datas[0].close
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None
        sma1 = bt.ind.SMA(period=self.p.pfast)  # 短期均线
        sma2 = bt.ind.SMA(period=self.p.pslow)  # 长期均线
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # 交叉信号

    def next(self):
        if self.order: # 检查是否有指令等待执行,
            return
        # 检查是否持仓
        if not self.position: # 没有持仓
            #执行买入条件判断：收盘价格上涨突破20日均线
            if self.crossover > 0:
                #执行买入
                self.order = self.buy(size=500)
        else:
            #执行卖出条件判断：收盘价格跌破20日均线
            if self.crossover < 0:
                #执行卖出
                self.order = self.sell(size=500)

    #交易记录日志（可省略，默认不输出结果）
    '''
    def log(self, txt, dt=None,doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()},{txt}')
    '''
    def log(self, txt, dt=None,doprint=False):
        # 所有的要打印出来的数据都通过传入的txt方法来实现。但是每次调用的时候默认输入一个日期作为基本的记录
        # 函数内的调用默认是self.params.printlog来表示
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.data.datetime.date(0)
            if isinstance(dt, float):
                dt = bt.num2date(dt)
            #print('%s, %s' % (dt.isoformat(), txt))
            print('%s, %s' % (dt.strftime('%Y-%m-%d'), txt))

    #记录交易执行情况（可省略，默认不输出结果）
    def notify_order(self, order):
        # 如果order为submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}')
            self.bar_executed = len(self)
        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None

    #记录交易收益情况（可省略，默认不输出结果）
    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')

    #回测结束后输出结果（可省略，默认输出结果）
    def stop(self):
        self.log('(均线%2d日和均线%2d日交叉) 期末总资金 %.2f' %
                 (self.params.pfast,self.params.pslow, self.broker.getvalue()), doprint=True)