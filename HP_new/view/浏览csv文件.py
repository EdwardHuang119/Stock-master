# -*- coding: utf-8 -*-
# 显示4个K线图的模板
import time
import tkinter as tk   #导入Tkinter
import tkinter.ttk as ttk   #导入Tkinter.ttk
import tkinter.tix as tix   #导入Tkinter.tix
import HP_global as g 
import HP_tk as htk

#系统设定了g.tab1--g.tab9,系统只是用了g.tab1--g.tab6
#控件结构 g.G_root -〉 g.tabControl  -〉g.tab1
#增加tab，用add()
#删除tab,用forget()
#当然用户可以设置更多的tab窗口。必须使用全局变量g.变量名
#重复建立新tab窗会出错，所以我们先检测是否None,不是就先做删除旧tab窗口。


if g.tab10!=None:
    g.tabControl.forget(g.tab10)
    g.tab10=None

#用户自建新画面
g.tab10 = tk.Frame(g.tabControl)
g.tabControl.add(g.tab10, text='浏览CSV文件') 
g.tabControl.select(g.tab10)

global ent,tb

fra=tk.Frame(g.tab10)
fra.pack(side=tix.TOP, fill=tix.X)
frb=tk.Frame(g.tab10)
frb.pack(side=tix.BOTTOM,expand=1, fill = tk.BOTH)
ent =tix.FileEntry(fra, label='选择一个文件: ',width=400,
                   value='')

ent.pack(side=tix.LEFT, padx=5, pady=5)
tb = htk.Table(frb)
tb.pack(expand = 1, fill = tk.BOTH)
def ld2():
    global ent,tb
    var1=ent.entry.get()
    df=pd.read_csv(var1 , encoding= 'gbk')
    columns=df.columns
    column0=columns[0]
    #print(columns,column0)
    df=df.rename(columns={column0:'index'})
    tb.delete_table()
    tb.load_df(df)
    tb.brush()
    
bnt =tk.Button(fra, text="打开数据", cursor='hand2',
                     command=ld2) #带参数函数
bnt.pack(side=tix.LEFT, padx=5, pady=5)
