#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backtrader as bt
import datetime as dt

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
            self.log('交易失败，交易状态为'%order.status)
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


class my_strategy3(bt.Strategy):
    params = dict(
        buy_limit_percent = 0.01,
        buy_valid_date = 5,
        stoptype=bt.Order.StopTrail,
        trailamount=0.0,
        trailpercent=0.05,
        p_high_period = 5,
        p_fast = 5,
        p_slow = 20,
    )
    def __init__(self):
        slowSMA = bt.ind.SMA(period = self.p.p_slow)
        self.buy_con = bt.And(
            bt.ind.CrossUp(
            bt.ind.SMA(period = self.p.p_fast), slowSMA),
            #slowSMA == bt.ind.Highest(slowSMA, period = self.p.p_high_period, plot = False)
        )
        self.order = None
    def notify_order(self, order):
        if order.status in [order.Completed]:
            print('Completed order: {}: Order ref: {} / Type {} / Status {} '.format(
                self.data.datetime.date(0),
                order.ref, 'Buy' * order.isbuy() or 'Sell',
                order.getstatusname()))
            self.order = None
        if order.status in [order.Expired]:
            self.order = None
        print('{}: Order ref: {} / Type {} / Status {}'.format(
            self.data.datetime.date(0),
            order.ref, 'Buy' * order.isbuy() or 'Sell',
            order.getstatusname()))
    def next(self):
        # 无场内资产
        if not self.position:
            # 未提交买单
            if None == self.order:
                # 金叉到达了买点
                if self.buy_con:
                    self.order = self.buy()
                    '''
                    # 计算订单有效期时间，如果超过有效期，股价仍未回踩，则放弃下买入订单
                    valid = self.data.datetime.date(0)
                    if self.p.buy_valid_date:
                        valid = valid + dt.timedelta(days=self.p.buy_valid_date)
                    # 计算回踩后的买入价格
                    price = self.datas[0].close[0] * (1.0 - self.p.buy_limit_percent)
                    print('Buy order created: {}: close: {} / limit price: {} / valid: {}'.format(
                        self.datetime.date(), self.datas[0].close[0], price, valid) )
                    # 用有效时间及回踩买点提交买入订单
                    price = self.datas[0].close[0]
                    self.order = self.buy(exectype = bt.Order.Limit, price = price, valid = valid)
                    # self.order = self.buy(price=price)
                    # self.order = self.buy_bracket()
                    #o = self.buy()
                    print('*' * 50)
                    '''
        elif self.order is None:
            # 提交stoptrail订单
            self.order = self.sell(exectype=self.p.stoptype,
                                   trailamount=self.p.trailamount,
                                   trailpercent=self.p.trailpercent)
            if self.p.trailamount:
                tcheck = self.data.close - self.p.trailamount
            else:
                tcheck = self.data.close * (1.0 - self.p.trailpercent)
            print('Sell stoptrail order created: {}: \
                close： {} /  \
                Limit price: {} / check price {}'.format(
                self.datetime.date(), self.data.close[0],
                self.order.created.price, tcheck
            ))
            print('-' * 10)
        else:
            if self.p.trailamount:
                tcheck = self.data.close - self.p.trailamount
            else:
                tcheck = self.data.close * (1.0 - self.p.trailpercent)
            print('update limit price: {}: \
                close： {} /  \
                Limit price: {} / check price {}'.format(
                self.datetime.date(), self.data.close[0],
                self.order.created.price, tcheck
            ))
