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
#最后修改日期:2018年9月22日
#主程序：HP_main.py
"""

import sys,os
import numpy as np
import pandas as pd

from HP_VIEW.HP_global import *
from HP_VIEW.HP_set import *

#交易回测类
class hpQuant(object):
    def __init__(self): #类初始化
        self.order_df=None   #下单流水
        self.trade_df=None   #交易流水
        self.security_df=None   #持仓清单
        self.money2=1000000.00  #总资金
        self.money=1000000.00  #资金
        self.priceBuy=0.00    #最后一次买入价格
        self.priceSell=999999.00  #最后一次卖出价格
        self.amount=0.00   #证券数量
        self.code=""   #证券代码
        self.stamp_duty=0.001   #印花税 0.1%
        self.trading_Commission=0.0005    #交易佣金0.05%
        self.priceStopLoss=0.00   #止损价
        self.position=False   #持仓状态
        self.stop_loss_on=True #允许止损
        self.stop_loss_num=0   #当前止损次数
        self.stop_loss_max=50 #最大允许止损次数.到止损次数,就停止交易
        self.stop_loss_range=0.05   #止损幅度
        self.trade=True   #允许交易
        self.Init()

    def Init(self): #初始化交易数据
        self.order_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price']) 
        self.order_df =self.order_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.trade_df = pd.DataFrame(columns = ['date', 'time','mode','code','amount','price','money']) 
        self.trade_df =self.trade_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        self.security_df = pd.DataFrame(columns = ['code','amount','price','money']) 
        self.security_df =self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  

    def PrintOrder(self): #输出下单流水
        print(self.order_df)

    def PrintTrade(self): #输出交易流水
        print(self.trade_df)

    def PrintSecurity(self): #输出持仓清单
        print(self.security_df)

    def Order(self,date,time,mode,code,amount,price): #交易函数
        ln=len(self.order_df)
        df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price},index=[ln])
        self.order_df=self.order_df.append( df_new,ignore_index=True)

        ln=len(self.trade_df)
        if mode==1:   #买入
            se=amount*price*(1+self.trading_Commission)
            self.money=self.money-se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            if len(self.security_df[self.security_df.code==code])==0 :
                df_new = pd.DataFrame({'code':code,'amount':amount,'price':se/amount,'money':se},index=[ln])
                self.security_df=self.security_df.append( df_new,ignore_index=True)
            else:
                self.security_df.index=self.security_df['code']
                self.security_df.loc[code,'amount']=self.security_df.loc[code,'amount']+amount
                self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  
        
        ln=len(self.security_df[self.security_df.code==code])
        if mode==2 and ln>0:  #卖出
            self.security_df.index=self.security_df['code']
            am=self.security_df.loc[code,'amount']
            
            if am<amount :
                amount=am
            se=amount*price*(1-self.trading_Commission-self.stamp_duty)
            self.money=self.money+se
            df_new = pd.DataFrame({'date':date,'time':time,'mode':mode,'code':code,'amount':amount,'price':price,'money':self.money},index=[ln])
            self.trade_df=self.trade_df.append( df_new,ignore_index=True)
            am2=self.security_df.loc[code,'amount']-amount
            self.security_df.loc[code,'amount']=am2
            if am2==0:
                self.security_df=self.security_df.drop(code, axis = 0) # 在行的维度上删除行
            self.security_df=self.security_df.reset_index(level=None, drop=True ,col_level=0, col_fill='')  


#####################回测功能#########################
    def Trade_testing(self,df,tp1,tp2,al=''):   #回测函数
        self.Init()
        self.trade=True   #允许交易
        myMoney=self.money2
        if (al.strip()==''):
            na='property'
        else:
            na=al 
        self.text='    ----开始回测-----\n'
        i = 0  
        ZB_l = []
        while i < len(df):  
            close=df.close.at[i]
            if (df[tp1].at[i] >0 and self.position==False and self.trade==True) :  #买点
                self.priceBuy=close
                x=int(myMoney/(self.priceBuy*(1+self.trading_Commission))/100)
                self.amount=x*100.00
                self.Order(df.date.at[i],'14:45:01',1,self.code,self.amount,close)
                myMoney=myMoney-self.amount*self.priceBuy*(1.00+self.trading_Commission)
                self.position=True
                self.priceStopLoss=self.priceBuy*(1-self.stop_loss_range)
                self.text=self.text+'日期:'+df.date.at[i]+' 买入:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceBuy,2))+'\n'
            
            if (df[tp2].at[i] >0 and self.position==True and self.trade==True) : #卖点
                self.priceSell=close
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 卖出:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
            
            if (close<=self.priceStopLoss and self.position==True and self.trade  and self.stop_loss_on):  #止损
                self.priceSell=self.priceStopLoss-0.01
                myMoney=myMoney+self.amount*self.priceSell*(1.00-self.trading_Commission-self.stamp_duty)
                self.position=False
                self.stop_loss_num=self.stop_loss_num+1
                self.Order(df['date'].at[i],'14:45:02',2,self.code,self.amount,self.priceSell)
                self.text=self.text+'日期:'+df.date.at[i]+' 止损:'+str(round(self.amount,0))+'股, 价格:'+str(round(self.priceSell,2))+'获利:'+str(round((myMoney-self.money2)/self.money2*100,2))+'%\n'
                self.amount=0.00
                if (self.stop_loss_num>=self.stop_loss_max):
                    self.trade=False

            y= (myMoney+self.amount*close-self.money2)/self.money2 *100 
            ZB_l.append(y)  
            i = i + 1          
            
        ZB_s = pd.Series(ZB_l)  
        ZB = pd.Series(ZB_s, name = na)  
        df = df.join(ZB)  
        self.money=myMoney
        y= (myMoney+self.amount*close-self.money2)/self.money2  *100
        self.text=self.text+'总投入'+str(round(self.money2,2))+',最终获利幅度'+str(round(y,0))+'%\n'
            
        return df

#####################################################
################独狼荷蒲软件版权声明###################
'''
独狼荷蒲软件(或通通软件)版权声明
1、独狼荷蒲软件(或通通软件)均为软件作者设计,或开源软件改进而来，仅供学习和研究使用，不得用于任何商业用途。
2、用户必须明白，请用户在使用前必须详细阅读并遵守软件作者的“使用许可协议”。
3、作者不承担用户因使用这些软件对自己和他人造成任何形式的损失或伤害。
4、作者拥有核心算法的版权，未经明确许可，任何人不得非法复制；不得盗版。作者对其自行开发的或和他人共同开发的所有内容，
    包括设计、布局结构、服务等拥有全部知识产权。没有作者的明确许可，任何人不得作全部或部分复制或仿造。

独狼荷蒲软件
QQ: 2775205
Tel: 18578755056
公众号:独狼股票分析
'''