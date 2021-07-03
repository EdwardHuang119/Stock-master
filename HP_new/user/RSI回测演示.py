# -*- coding: utf-8 -*-
import pandas as pd  
import numpy  as np
import datetime as dt
import time
import matplotlib.pyplot as plt
import math
import tushare as ts
from HP_formula import *
from HP_sys import *

global CLOSE,LOW,HIGH,OPEN,VOL
def RSI(N1=6, N2=12, N3=24):
    """
    RSI 相对强弱指标
    """
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100

    return RSI1, RSI2, RSI3

##code股票代码
code='600030'
#首先要对数据预处理
df = ts.get_k_data(code,ktype='D')
mydf=df.copy()
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


#生成均线 5日均线
ma5=MA(C,5)
mydf = mydf.join(pd.Series( ma5,name='MA5')) 
#生成均线 10日均线
ma10=MA(C,10)
mydf = mydf.join(pd.Series( ma10,name='MA10')) 

#获取RSI指标
r1,r2,r3=RSI(5,10,20)

mydf = mydf.join(pd.Series( r1,name='RSI1'))  
mydf = mydf.join(pd.Series( r2,name='RSI2'))  
mydf = mydf.join(pd.Series( r3,name='RSI3')) 
mydf['S80']=80  #增加上轨80轨迹线
mydf['X20']=20  #增加下轨20轨迹线
mydf['Z50']=50  #增加中轨50轨迹线

#mydf=mydf.tail(100)  #显示最后100条数据线 
##下面开始生成RSI指标买卖点
##买点RSI1上穿数值20
b1=CROSS(mydf['RSI1'],mydf['X20'])
mydf = mydf.join(pd.Series( b1,name='B1'))  

##卖点RSI1下穿80
s1=CROSS(mydf['S80'],mydf['RSI1'])

#卖点RSI1下穿50
s2=CROSS(mydf['Z50'],mydf['RSI1'])

#合并所有卖点信号
s3=s1 | s2

mydf = mydf.join(pd.Series( s1,name='S1'))  
mydf = mydf.join(pd.Series( s2,name='S2'))  
mydf = mydf.join(pd.Series( s3,name='S3'))  




##回测
tt=hpQuant()   ##初始化类

#下面是用户可设置信息。
#        self.money2=1000000.00  #总资金
#        self.code=""   #证券代码
#        self.stamp_duty=0.001   #印花税 0.1%
#        self.trading_Commission=0.0005    #交易佣金0.05%
#        self.stop_loss_on=True #允许止损
#        self.stop_loss_max=50 #止损3次,就停止交易
#        self.stop_loss_range=0.05   #止损幅度

tt.code=code   #证券代码，必须输入
tt.stop_loss_on=False    #关闭自动止损

#参数表说明:股票数据表,买点序列名称,卖点序列名称,返回获利序列名称
df3=tt.Trade_testing(mydf,'B1','S3','HL')   #开始回测
print('\n打印交易过程')
tt.PrintTrade()    #打印交易过程
print('\n打印持仓信息')
tt.PrintSecurity()   #打印持仓信息
print('\n 打印内部交易记录信息')
print(tt.text)     #打印交易信息


######下面是绘图
# 开启一个双图例的窗口，定义为211和212
plt.figure(figsize=(12,8), dpi=100)
ax1 = plt.subplot(311)
ax2 = plt.subplot(312)
ax3 = plt.subplot(313)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# ax1（311窗口）
plt.sca(ax1)
plt.title(code+'  RSI指标买卖策略回测图')   
# 显示网格：grid='on'
df3.close.plot(color='red', grid='on',legend=True)
df3['MA5'].plot(color='blue', grid='on',legend=True)
df3['MA10'].plot(color='green', grid='on',legend=True)
ax2.axhline(0, color='blue')

# ax2（312窗口）
plt.sca(ax2)

mydf.S80.plot.line()
mydf.X20.plot.line()
mydf.RSI1.plot.line(legend=True)
mydf.RSI2.plot.line(legend=True)
mydf.RSI3.plot.line(legend=True)

# ax3（313窗口）
plt.sca(ax3)
df3.HL.plot(color='orange', grid='on',legend=True)
df3.B1.plot(color='red',legend=True)
df3.S1.plot(color='blue',legend=True)
#添加标题
plt.title(code+'  获利')
plt.show()

