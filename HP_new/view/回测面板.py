# -*- coding: utf-8 -*-
# 回测模板
import time
import tkinter as tk
import  tkinter.ttk  as  ttk   #导入Tkinter.ttk
import  tkinter.tix  as  tix   #导入Tkinter.tix
import  HP_tk  as  htk   #导入htk
import HP_global as g 
import HP_data as hp
from HP_view import * #菜单栏对应的各个子页面 
import HP_tdx as htdx

#系统设定了g.tab1--g.tab9,系统只是用了g.tab1--g.tab6
#控件结构 g.root -〉 g.tabControl  -〉g.tab1
#增加tab，用add()
#删除tab,用forget()
#当然用户可以设置更多的tab窗口。必须使用全局变量g.变量名
#重复建立新tab窗会出错，所以我们先检测是否None,不是就先做删除旧tab窗口。


if g.tab5!=None:
    g.tabControl.forget(g.tab5)
    g.tab5=None

#用户自建新画面
g.tab5 = tk.Frame(g.tabControl)
g.tabControl.add(g.tab5, text='策略回测') 
g.tabControl.select(g.tab5)

#回测面板
def hc(frame)    :
    Label(frame, text=' ').grid(row=0, column=0)
    label1 = Label(frame, width=10, text='开始日期: ',ancho=S)
    label1.grid(row=0, column=1)
    #输入框 (Entry)
    g.hcdate_s = StringVar()
    entrydates = Entry(frame, width=10, textvariable=g.hcdate_s)
    entrydates.grid(row=0, column=2)
    g.hcdate_s.set(g.sday)
    Label(frame , text=' ').grid(row=0, column=3)
    label2 = Label(frame ,width=10, text='结束日期: ')
    label2.grid(row=0, column=4)
    #输入框 (Entry)
    g.hcdate_e = StringVar()
    entrydatee = Entry(frame, width=10,textvariable=g.hcdate_e)
    g.hcdate_e.set(g.eday)
    entrydatee.grid(row=0, column=5)
    Label(frame , text=' ').grid(row=0, column=6)
    label3 = Label(frame ,width=10, text='初始资金(元):')
    label3.grid(row=0, column=7)
    #输入框 (Entry)
    g.hczj = StringVar()
    g.hczj.set(g.money)    
    entryzj = Entry(frame,width=12, textvariable=g.hczj)
    entryzj.grid(row=0, column=8)
    Label(frame , text=' ').grid(row=0, column=6)
    label4 = Label(frame ,width=12, text='止损幅度(%):')
    label4.grid(row=0, column=9)
    #输入框 (Entry)
    g.hczs = StringVar()
    g.hczs.set(g.stop_loss_range)    
    entryzs = Entry(frame,width=10, textvariable=g.hczs)
    entryzs.grid(row=0, column=10)
    Label(frame , text=' ').grid(row=0, column=11)
    label4 = Label(frame ,width=12, text='股票代码:')
    label4.grid(row=0, column=12)
    #输入框 (Entry)
    g.hcstock = StringVar()
    g.hcstock.set('000001')    
    entryst = Entry(frame,width=10, textvariable=g.hcstock)
    entryst.grid(row=0, column=13)
    Label(frame , text=' ').grid(row=0, column=14)
    def stt():
        if g.UserCanvas!=None:
            g.UserPlot.cla() 
            g.UserPlot.close()
            g.UserCanvas._tkcanvas.pack_forget() 
            g.UserCanvas=None
        if g.UserPlot !=None:
            g.UserPlot.pack_forget()         
    #按钮  (Button)
    getname = tk.Button(frame , text='清除画面' ,command=stt)
    getname.grid(row=0, column=15)

frmt=tk.Frame(g.tab5)
myhc=hc(frmt)
frmt.pack(side=tk.TOP,fill=tk.Y)

#创建frame容器
frmA = ttk.LabelFrame(g.tab5, text='回测输出画板')
frmA.rowconfigure(0,weight=1)
frmA.columnconfigure(0,weight=1)
frmA.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
frmL = tk.Frame(frmA,width =  g.winW-600, \
                  height = 800,relief=tk.SUNKEN)
frmR = tk.Frame(frmA,width = 600, \
                  height = 800,relief=tk.SUNKEN)
g.UserFrame=frmL

#窗口布局
frmL.grid(row = 0, column = 0,sticky=tk.NSEW)
frmR.grid(row = 0, column = 1,sticky=tk.NSEW)
myedit3=htk.useredit(frmR)

