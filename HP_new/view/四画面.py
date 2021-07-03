# -*- coding: utf-8 -*-
# 显示4个K线图的模板
import time
import tkinter as tk
import HP_global as g 
import HP_data as hp
from HP_view import * #菜单栏对应的各个子页面 
import HP_tdx as htdx

#系统设定了g.tab1--g.tab9,系统只是用了g.tab1--g.tab6
#控件结构 g.G_root -〉 g.tabControl  -〉g.tab1
#增加tab，用add()
#删除tab,用forget()
#当然用户可以设置更多的tab窗口。必须使用全局变量g.变量名
#重复建立新tab窗会出错，所以我们先检测是否None,不是就先做删除旧tab窗口。


if g.tab8!=None:
    g.tabControl.forget(g.tab8)
    g.tab8=None

#用户自建新画面
g.tab8 = tk.Frame(g.tabControl)
g.tabControl.add(g.tab8, text='四画面') 
g.tabControl.select(g.tab8)

#把window划分4个子容器,在不同子容器中显示不同股票K线图
xxx=view4(g.tab8)

g.gtype=g.book_s.get()
stockn=g.stock_i.get()
stockn=stockn.strip()
stockn=stockn.zfill(6)
g.stock_i.set(stockn)
g.stock=stockn
ds=g.date_s.get()
de=g.date_e.get()
g.sday=ds.strip()
g.eday=de.strip()
df2=htdx.get_k_data(g.stock,ktype='D',start=g.sday,\
                  end=g.eday,index=False,autype='qfq')

ds=g.mds
de2=time.strftime('%Y-%m-%d',time.localtime(time.time()))
de=time.strftime('%Y-%m-%d',time.localtime(time.time()))+' 15:01:00'
g.mde=de

st=g.stock

#nCategory -> K 线种类 
#0 5 分钟K 线 
#1 15 分钟K 线 
#2 30 分钟K 线 
#3 1 小时K 线 
#4 日K 线 
#5 周K 线 
#6 月K 线 
#7 1 分钟 
#8 1 分钟K 线 
#9 日K 线 
#10 季K 线 
#11 年K 线 
#读取股票数据
mk=htdx.get_market(g.stock)
df2a=htdx.get_security_bars(nCategory=6,nMarket =mk,code=st,nStart=0, nCount=240)
df2b=htdx.get_security_bars(nCategory=5,nMarket =mk,code=st,nStart=0, nCount=240)
df2c=htdx.get_security_bars(nCategory=4,nMarket =mk,code=st,nStart=0, nCount=240)
df2d=htdx.get_security_bars(nCategory=1,nMarket =mk,code=st,nStart=0, nCount=240)

#6均线2指标图,K线算一个指标
axview4x(xxx.v[0],df2a,g.stock+' '+g.stock_names[g.stock]+' 月线图',n=4,f1='VOL',f2='HPYYX',f3=g.gtype)
axview4x(xxx.v[1],df2b,g.stock+' '+g.stock_names[g.stock]+' 周线图',n=4,f1='VOL',f2='HPYYX',f3=g.gtype)
axview4x(xxx.v[2],df2c,g.stock+' '+g.stock_names[g.stock]+' 日线图',n=4,f1='VOL',f2='HPYYX',f3=g.gtype)
axview4x(xxx.v[3],df2d,g.stock+' '+g.stock_names[g.stock]+' 15分钟图',n=4,f1='VOL',f2='HPYYX',f3=g.gtype)

xxx.pack(fill=tk.BOTH, expand=1)






