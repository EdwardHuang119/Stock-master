# -*- coding: utf-8 -*-
#通通量化包
#tushare 数据测试
#日期：2018-09-26
#QQ：2775205

import tushare as ts
import matplotlib.pyplot as plt
import pandas as pd
import HP_VIEW.HP_global as g
from HP_VIEW.HP_set import *
from HP_VIEW.HP_formula import *
import datetime as dt
import time

#g.datapath='d:/xbdata'  #在HP_set.py中进行配置.

st=ts.get_stock_basics()
print(len(st))

index=False
autype='None'
ktype='D'

pp=''
if autype=='None':
    pp=pp+'none\\'
if autype=='hfq':
    pp=pp+'hfq\\'
if index==True:
    pp=pp+'index'
    
kk=''    
if ktype=='D':
    kk=kk+'\\day\\'
if ktype=='W':
    kk=kk+'\\week\\'
if ktype=='M':
    kk=kk+'\\month\\'    
if ktype=='5':
    kk=kk+'\\minute\\5\\'
       
ds='1991-01-01'
de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
print(ds,de)
i=0
for ss in st.index:
    i=i+1
    print(i,ss)
    for autype in ['qfq','None','hfq']:
        for ktype in ['D','W','M']:
            pp=''
            if autype=='None':
                pp=pp+'none\\'
            if autype=='hfq':
                pp=pp+'hfq\\'
            if index==True:
                pp=pp+'index'
                
            kk=''    
            if ktype=='D':
                kk=kk+'\\day\\'
            if ktype=='W':
                kk=kk+'\\week\\'
            if ktype=='M':
                kk=kk+'\\month\\'    
            if ktype=='5':
                kk=kk+'\\minute\\5\\'
    
            df1 = ts.get_k_data(ss,ktype=ktype,start=ds,end=de,index=index,autype=autype)
            ss1=kk+pp+ss+'.csv'
            print(ss1)
            df1.to_csv(g.datapath+ss1 , encoding = 'gbk')

