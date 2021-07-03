# -*- coding: utf-8 -*-
# 显示2个K线图的模板

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
global xxx
global xxx2
global view_price2


#g.login=True

class view_price2(Frame): # 继承Frame类  
    def __init__(self, master=None,t=0):  
        self.txt2=['卖五','卖四','卖三','卖二','卖一','买一','买二','买三','买四','买五','最新','涨跌','外盘','成交量','','','','','','']
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.t=t
        self.l=[]
        self.l2=None
        self.config(width=239)
        self.config(height=11)
        self.config(bd=0)
        self.config(bg='#2A2A2A')
        for l3 in range(3):
            if l3==0:
                tt=self.txt2[self.t]
            else:
                tt='text_%d_%d'%(self.t,l3)
            if t<5:
                co='green'
            elif t<10:
                co='red'
            else:
                co='yellow'
            self.l2=Label(self,text=tt,fg=co,width=12,bg='black',font = 'Helvetica -14')
            self.l2.pack(side=LEFT)
            self.l.append(self.l2)
            
            
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.pack(fill=tk.BOTH, expand=1)


if g.tab6!=None:
    g.tabControl.forget(g.tab6)
    g.tab6=None

#用户自建新画面
g.tab6 = tk.Frame(g.tabControl)


txt2=['卖五','卖四','卖三','卖二','卖一','买一','买二','买三','买四','买五']


###黑底色
#g.ubg='#07000d'
#g.ufg='w'
#g.utg='w'
#g.uvg='#FFD700'

def printSize(event):
    print(event)
    print (event.width,event.height)



style = ttk.Style()
style.configure("BW.TLabel", font=("Times", "11",), foreground="black", background="white")
style.configure("BR.TLabel", font=("Times", "10",'bold'), background='black',foreground='red')
style.configure("bk", background='black',foreground='red')
style.configure("BB.TLabel", font=("仿宋", "10",'bold'), background='black',foreground='blue')

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
df2b.to_csv('temp/day01.csv' , encoding= 'gbk')
#else:
#    #print('读本地数据！')
#    df2b=pd.read_csv('temp/day01.csv' , encoding= 'gbk')
#    st2=st


xxx=view2c(g.tab6)
axview3x_m(xxx.v[0],df2b,g.stock+' '+g.stock_names[g.stock]+' 分时图',6) 
xxx2=view2d(xxx.v[1])

class view_price(Frame): # 继承Frame类  
    def __init__(self, master=None,t=''):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.l=[]
        self.l2=None
        self.label=tk.Label(xxx2.v[0],text=t+' '+g.stock_names[t],height=1,font = 'Helvetica -24 bold',)
        self.label.pack(side=TOP,fill=tk.X)
        for l3 in range(14):
            self.l2=view_price2(self,l3)
            self.l2.pack(side=TOP)
            self.l.append(self.l2)
            
            
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.pack(fill=tk.BOTH, expand=1)




mmp=view_price(xxx2.v[0],st2)

bss=htdx.get_security_quotes(st)
mmp.l[0].l[1]['text']=str(bss[0]['ask5'])
mmp.l[0].l[2]['text']=str(bss[0]['ask_vol5'])
mmp.l[1].l[1]['text']=str(bss[0]['ask4'])
mmp.l[1].l[2]['text']=str(bss[0]['ask_vol4'])
mmp.l[2].l[1]['text']=str(bss[0]['ask3'])
mmp.l[2].l[2]['text']=str(bss[0]['ask_vol3'])
mmp.l[3].l[1]['text']=str(bss[0]['ask2'])
mmp.l[3].l[2]['text']=str(bss[0]['ask_vol2'])
mmp.l[4].l[1]['text']=str(bss[0]['ask1'])
mmp.l[4].l[2]['text']=str(bss[0]['ask_vol1'])

mmp.l[5].l[1]['text']=str(bss[0]['bid1'])
mmp.l[5].l[2]['text']=str(bss[0]['bid_vol1'])
mmp.l[6].l[1]['text']=str(bss[0]['bid2'])
mmp.l[6].l[2]['text']=str(bss[0]['bid_vol2'])
mmp.l[7].l[1]['text']=str(bss[0]['bid3'])
mmp.l[7].l[2]['text']=str(bss[0]['bid_vol3'])
mmp.l[8].l[1]['text']=str(bss[0]['bid4'])
mmp.l[8].l[2]['text']=str(bss[0]['bid_vol4'])
mmp.l[9].l[1]['text']=str(bss[0]['bid5'])
mmp.l[9].l[2]['text']=str(bss[0]['bid_vol5'])

mmp.l[10].l[1]['text']=str(bss[0]['price'])
mmp.l[10].l[2]['text']=str(bss[0]['cur_vol'])
mmp.l[11].l[1]['text']=str(round((bss[0]['price']-bss[0]['last_close'])*100/bss[0]['last_close'],3))+'%'
mmp.l[11].l[2]['text']=str(round(bss[0]['price']-bss[0]['last_close'],2))
mmp.l[12].l[1]['text']=str(bss[0]['b_vol'])
mmp.l[12].l[2]['text']=str(bss[0]['s_vol'])
mmp.l[13].l[1]['text']=str(bss[0]['vol'])
mmp.l[13].l[2]['text']=str(round(bss[0]['amount']/100000000,2))+u'亿元'


df3=htdx.get_transaction_data(nMarket = g.gmarket,code=st)
if len(df3)>0:
    grid_df=df3[['time','price','vol','num']]
    grid_ss=grid_df.columns
    grid_colimns=[]
    for s in grid_ss:
        grid_colimns.append(s)
    
    #滚动条
    scrollBarA =tk.Scrollbar(xxx2.v[1])
    g.scrollBarA=scrollBarA
    g.scrollBarA.pack(side=tk.RIGHT, fill=tk.Y)
    xxx2.v[1].config(bd=0,bg='black')
    
    #Treeview组件，6列，显示表头，带垂直滚动条
    tree = ttk.Treeview(xxx2.v[1],columns=(grid_colimns),style='BW.TLabel',
                      show="headings",yscrollcommand=g.scrollBarA.set)
    
    tree.tag_configure('oddrow', background='green',foreground='yellow')
    tree.tag_configure('item_up', background='black',foreground='red')
    tree.tag_configure('item_down', background='black',foreground='green')
    tree.tag_configure('item_m', background='black',foreground='white')
    #print(grid_colimns)
    for s in grid_colimns:
        #设置每列宽度和对齐方式
        tree.column(s,width=80,  anchor='center')
        #设置每列表头标题文本
        tree.heading(s, text=s)
    
    tree.column('time',width=72,  anchor='w')
    tree.column('price',width=70)
    tree.column('vol',width=70)
    tree.column('num',width=70)
    g.scrollBarA.config(command=tree.yview)
    
    #scrollBarB  = tk.Scrollbar(xxx2.v[1],orient = tk.HORIZONTAL)
    #g.scrollBarB=scrollBarB
    #g.scrollBarB.set(0.5,0.2)
    #g.scrollBarB.pack(side=tk.TOP, fill=tk.X)
    #g.scrollBarB.config(command=tree.xview)
    
    #定义并绑定Treeview组件的鼠标单击事件
    closetags='item_up'
    
    #插入演示数据
    for i in range(len(grid_df)):
        v=[]
        closetags='item_m'
        for s in grid_ss:
            v.append(grid_df.at[i,s])
        if df3.at[i,'buyorsell']==1:
            closetags='item_up'
        if df3.at[i,'buyorsell']==0:
            closetags='item_down'
        #close=grid_df.at[i,'close']
        item=tree.insert('', i, values=v, tags=(closetags))
        aa=tree.item(item, "values")
        
        bb=list(aa)
    
    tree.pack(fill=tk.Y,expand=tk.YES)
    #tree.bind('<Configure>',printSize)


xxx2.pack(fill=tk.BOTH, expand=1)

xxx.rowconfigure(0,weight=1)
xxx.columnconfigure(0,weight=1)
xxx.pack(fill=tk.BOTH, expand=1)

g.tabControl.add(g.tab6, text='分时图') 
g.tabControl.select(g.tab6)
g.tabs=6