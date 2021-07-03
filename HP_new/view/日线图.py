# -*- coding: utf-8 -*-
# 显示日线图的模板
import  tkinter  as  tk   #导入Tkinter
import  tkinter.ttk  as  ttk   #导入Tkinter.ttk
import  tkinter.tix  as  tix   #导入Tkinter.tix
import time
import pandas as pd
import numpy as np
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
if g.tab3!=None:
    g.tabControl.forget(g.tab3)
    g.tab3=None

#用户自建新画面
g.tab3 = tk.Frame(g.tabControl)
g.tabControl.add(g.tab3, text='日线图') 
g.tabControl.select(g.tab3)
axview3x(g.tab3,df2,t=g.stock+' '+g.stock_names[g.stock],n=2,f1='VOL',f2=g.gtype)
g.tabControl.select(g.tab3)
g.tabs=3


