# -*- coding: utf-8 -*-
#软件信息
p_sname='小白量化3模块'
p_aname='独狼'
p_edate='20200808'
p_ver=1.00

#小白量化全局
class Context(object):
    ''' 用户信息全局变量转储 '''
    security=''          #证券代码
    start_date = '2017-01-01'                       # 回测起始时间
    end_date = '2020-06-24'                         # 回测结束时间
    stocks=[]       #板块
    run_type=None  #运行方式
    frequency=None  #运行频率
    cash=100000.00    #现金
    i=0        #i是起始位置
    start=0        #i是起始位置
    end=1500        #i是结束位置


class Data(object):
    ''' 用户行情全局变量转储 '''
    date=None
    time=None
    bar={}
    bar['DATE']=''
    bar['OPEN']=0.0
    bar['CLOSE']=0.0
    bar['HIGH']=0.0
    bar['LOW']=0.0
    bar['VOL']=0.0
    bar['AMO']=0.0
    
    pass


class GlobalVars(object):
    '''用户自定义全局变量G.处理模块'''
    pass




#开盘前(9:00)运行
def run_daily():
    pass

def run_weekly():
    pass

def run_monthly():
    pass

#开盘前运行策略(可选)
def before_trading_start(context):
    pass

#策略运行结束时调用(可选)
def on_strategy_end(context):
    pass

#每次程序启动时运行函数(可选)
def process_initialize(context):
    pass

#模拟交易更换代码后运行函数(可选)
def after_code_changed(context):
    pass

##取消所有定时运行(可选)
#def after_code_changed(context):
#    # 取消所有定时运行
#    pass

#设置基准
def set_benchmark(security):
    pass

#设置佣金/印花税
def set_order_cost(cost, type, ref=None):
    pass

#设定滑点，回测/模拟时有效.
def set_slippage(object,type=None, ref=None):
    pass






# 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    #g.text = '用户自定义变量'
    pass


def tick(context, data):
    ''' 实时tick 级别数据 '''
    pass

def bar(context, data):
    ''' 实时单根K线数据 '''
    pass

def buy(context, data):
    ''' 买入多单 '''
    pass

def sell(context, data):
    ''' 卖出空单 '''
    pass




# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次    
def handle_data(context, data):
    ''' 实时带300根按bar递增历史K线数据 '''
    pass

