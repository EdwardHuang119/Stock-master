# -*- coding: utf-8 -*-
# 显示3个K线图的模板
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
g.tabControl.add(g.tab8, text='三画面') 
g.tabControl.select(g.tab8)

#把window划分4个子容器,在不同子容器中显示不同股票K线图
xxx=view3(g.tab8)

#ds='2018-01-01'
#de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
#
##读取股票数据
#df2a=htdx.get_k_data('000001',ktype='D',start=ds,end=de,index=False,autype='qfq')
#df2b=htdx.get_k_data('000001',ktype='D',start=ds,end=de,index=False,autype='qfq')
#df2c=htdx.get_k_data('600030',ktype='D',start=ds,end=de,index=False,autype='qfq')
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

stockn=g.stock_i.get()
stockn=stockn.strip()
stockn=stockn.zfill(6)
g.stock_i.set(stockn)
g.stock=stockn
st=g.stock
st2=st

if int(time.strftime('%H%M',time.localtime(time.time())))<=930:
    ds=time.strftime('%Y-%m-%d',time.localtime(time.time()-24*60*60))+' 09:30:00'
    de=time.strftime('%Y-%m-%d',time.localtime(time.time()-24*60*60))+' 15:00:00'
else:
    ds=time.strftime('%Y-%m-%d',time.localtime(time.time()))+' 09:30:00'
    de=time.strftime('%Y-%m-%d',time.localtime(time.time()))+' 15:00:00'
     

#if g.login:
df2b=htdx.get_security_bars(7,code=st)
a=[x[0:10] for x in df2b.date]
df2b['date2']=a
df2b=df2b[df2b.date2==de2]
df2b=df2b.reset_index(level=None, drop=True ,col_level=0, col_fill='') 
#df2b.to_csv('data/day01.csv' , encoding= 'gbk')
#else:
#    #print('读本地数据！')
#    df2b=pd.read_csv('temp/day01.csv' , encoding= 'gbk')
#    st2=st



axview3x_m(xxx.v[0],df2b,g.stock+' '+g.stock_names[g.stock]+' 分时图',6) 


#axview2(xxx.v[1],df2a,'000001  六均线K线演示',6)  

df3=htdx.get_security_bars(nCategory=5,nMarket = 0,code=g.stock,\
                    nStart=0, nCount=240)
df3.date=[x[0:10] for x in df3.date.astype(str)]
#6均线2指标图,现实KDJ指标线
axview2x(xxx.v[1],df3,g.stock+' '+g.stock_names[g.stock]+' 周线图',6)  
# 3指标图
axview4x(xxx.v[2],df2,g.stock+' '+g.stock_names[g.stock]+' 日线图',f1='VOL',f2='HPYYX',f3=g.gtype)

xxx.pack(fill=tk.BOTH, expand=1)

