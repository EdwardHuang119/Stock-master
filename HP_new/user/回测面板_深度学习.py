# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架 回测工具
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2019年12月22日
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import math
import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
import HP_tdx as htdx
from HP_view import * #菜单栏对应的各个子页面 
import datetime as dt
import time
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)    ##matplotlib 3.0.2 
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import math
import HP_tdx as htdx
from HP_formula import *
from HP_sys import *
import tkinter as tk
import HP_global as g 
import HP_data as hp

global CLOSE,LOW,HIGH,OPEN,VOL
ds=g.hcdate_s.get()
de=g.hcdate_e.get()
stockname=g.hcstock.get()

#import preprocessing 
'''
LSTM 神经网络 
Long Short Term Mermory network（LSTM）是一种特殊的RNNs，可以很好地解决长时依赖问题。
'''
#用户输出信息
def tprint(txt):
    g.ttmsg.insert(tk.END, txt)
    g.ttmsg.see(tk.END)

# FUNCTION TO CREATE 1D DATA INTO TIME SERIES DATASET
def new_dataset(dataset, step_size):
	data_X, data_Y = [], []
	for i in range(len(dataset)-step_size-1):
		a = dataset[i:(i+step_size), 0]
		data_X.append(a)
		data_Y.append(dataset[i + step_size, 0])
	return np.array(data_X), np.array(data_Y)


# FOR REPRODUCIBILITY
np.random.seed(7)

dataset=htdx.get_k_data(stockname,ktype='D',start=ds,end=de,index=False,autype='qfq')

# IMPORTING DATASET 
#dataset = pd.read_csv('apple_share_price.csv', usecols=[1,2,3,4])
dataset=dataset[['open','high', 'low', 'close']]
#print(dataset)
dataset = dataset.reindex(index = dataset.index[::-1])

# CREATING OWN INDEX FOR FLEXIBILITY
obs = np.arange(1, len(dataset) + 1, 1)

# TAKING DIFFERENT INDICATORS FOR PREDICTION
OHLC_avg = dataset.mean(axis = 1)
HLC_avg = dataset[['high', 'low', 'close']].mean(axis = 1)
close_val = dataset[['close']]

# PREPARATION OF TIME SERIES DATASE
OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg),1)) # 1664
scaler = MinMaxScaler(feature_range=(0, 1))
OHLC_avg = scaler.fit_transform(OHLC_avg)

# TRAIN-TEST SPLIT
train_OHLC = int(len(OHLC_avg) * 0.75)
test_OHLC = len(OHLC_avg) - train_OHLC
train_OHLC, test_OHLC = OHLC_avg[0:train_OHLC,:], OHLC_avg[train_OHLC:len(OHLC_avg),:]

# TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
trainX, trainY = new_dataset(train_OHLC, 1)
testX, testY =new_dataset(test_OHLC, 1)

#trainX, trainY = preprocessing.new_dataset(train_OHLC, 1)
#testX, testY = preprocessing.new_dataset(test_OHLC, 1)

# RESHAPING TRAIN AND TEST DATA
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
step_size = 1

# LSTM MODEL
model = Sequential() #定义
model.add(LSTM(32, input_shape=(1, step_size), return_sequences = True)) 
#添加LSTM神经网络，即在头文件中已经导入了LSTM，输入神经网络数据形状为(1, step_size)
#其中32为神经元个数
model.add(LSTM(16))
model.add(Dense(1)) #定义输出层神经元个数为1个，即输出只有1维
model.add(Activation('linear')) #根据情况添加激活函数

# MODEL COMPILING AND TRAINING
#模型编译和培训
model.compile(loss='mean_squared_error', optimizer='adagrad') # Try SGD, adam, adagrad and compare!!!
model.fit(trainX, trainY, epochs=5, batch_size=1, verbose=2)
#最后一句是对模型进行传值train_X, train_y，定义epochs迭代次数等；

# PREDICTION
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# DE-NORMALIZING FOR PLOTTING
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# TRAINING RMSE
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
tprint('Train RMSE: %.2f' % (trainScore))

# TEST RMSE
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
tprint('Test RMSE: %.2f' % (testScore))

#创建类似的数据集情节训练预测
# CREATING SIMILAR DATASET TO PLOT TRAINING PREDICTIONS
trainPredictPlot = np.empty_like(OHLC_avg)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[step_size:len(trainPredict)+step_size, :] = trainPredict

#创建类似DATASSET情节测试预测
# CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
testPredictPlot = np.empty_like(OHLC_avg)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(step_size*2)+1:len(OHLC_avg)-1, :] = testPredict

#反规范化主要数据集
# DE-NORMALIZING MAIN DATASET 
OHLC_avg = scaler.inverse_transform(OHLC_avg)

tprint(testPredictPlot)


######下面是绘图
if g.UserCanvas!=None:
    g.UserPlot.cla() 
    g.UserPlot.close()
    g.UserCanvas._tkcanvas.pack_forget() 
    g.UserCanvas=None


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
fig=plt.figure(2, figsize=(12,8), dpi=80)
g.UserFig=fig
g.UserPlot=plt

plt.suptitle(stockname+' LSTM 神经网络预测',color='blue')
plt.plot(obs, OHLC_avg, 'r', label = 'OHLC avg')
plt.plot(obs, HLC_avg, 'b', label = 'HLC avg')
plt.plot(obs, close_val, 'g', label = 'Closing price')
plt.legend(loc = 'upper right')
#情节主要OHLC值,预测训练和测试的预测
# PLOT OF MAIN OHLC VALUES, TRAIN PREDICTIONS AND TEST PREDICTIONS
plt.plot(OHLC_avg, 'g', label = 'original dataset')
plt.plot(trainPredictPlot, 'r', label = 'training set')
plt.plot(testPredictPlot, 'b', label = 'predicted stock price/test set')
plt.legend(loc = 'upper right')
plt.xlabel('Time in Days')
plt.ylabel('OHLC Value of Apple Stocks')
#plt.show()
plt.close()
canvas =FigureCanvasTkAgg(fig, master=g.UserFrame)
#toolbar =NavigationToolbar2TkAgg(canvas, g.UserFrame)
#toolbar.update()

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
g.UserCanvas=canvas
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)



#预测未来值
# PREDICT FUTURE VALUES
last_val = testPredict[-1]
last_val_scaled = last_val/last_val
next_val = model.predict(np.reshape(last_val_scaled, (1,1,1)))
print( "Last Day Value:", np.asscalar(last_val))
print( "Next Day Value:", np.asscalar(last_val*next_val))
print( np.append(last_val, next_val))