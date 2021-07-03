# -*- coding: utf-8 -*-
import time
import threading, time
import pandas as pd
import numpy as np
import tkinter as tk  #装载tkinter模块,用于Python3
from tkinter import ttk  #装载tkinter.ttk模块,用于Python3
import  HP_tk  as  htk   #导入htk
from tkinter import scrolledtext  #装载scrolledtext模块
from PIL import Image, ImageTk, ImageDraw, ImageFont
import sys
sys.path.append("..")
import HP_tk  as  htk   #导入ht
import HP_tdx as htdx
import HP_global as g


if g.tab7!=None:
    g.tabControl.forget(g.tab7)
    g.tab7=None

#用户自建新画面
g.tab7 = tk.Frame(g.tabControl)
g.tabControl.add(g.tab7, text='F10信息') 
mk=htdx.get_market(g.stock)

class UserF10(tk.Frame): # 继承Frame类  
    def __init__(self, master=None,stock=''):  
        tk.Frame.__init__(self, master)  
        self.stock=stock
        if self.stock=='':
            self.stock=g.stock
        self.root = master #定义内部变量root  
        self.button2=None
        self.r=1
        self.c=8
        self.b=[]
        self.F10text=scrolledtext.ScrolledText(self,undo=True,bg='#FFF8DC')
        self.F10text.pack(side=tk.TOP, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.init()
        self.pack(fill=tk.BOTH, expand=1,)

    def bt(self,n=0):
        import HP_tdx as htdx
        mk=htdx.get_market(self.stock)
        df=htdx.get_company_info_category(mk,self.stock)
        self.F10text.delete(2.0,tk.END)
        self.F10text.insert(tk.INSERT,'\n\n')        
        t=htdx.get_F10(self.stock,df.name[n])
        self.F10text.insert(tk.INSERT,t)

    def bt2(self):
        stockn=g.stock_i.get()
        stockn=stockn.strip()
        stockn=stockn.zfill(6)
        self.stock=stockn
        g.stock=stockn
        self.init()
        g.status.text(2,'查看'+self.stock+'  F10信息！')
        self.bt(n=0)

    def init(self):
        import HP_tdx as htdx
        mk=htdx.get_market(self.stock)
        df=htdx.get_company_info_category(mk,self.stock)
        fr=tk.Frame(self.F10text)
        k=0
        for i in range(self.r):
            for j in range(self.c):
                def kk(self=self, k=k):
                    self.bt(k)

                self.button = tk.Button(fr,text=df.name[k],command=kk,cursor='hand2')
                self.b.append(self.button)
                self.button.grid(row=i, column=j, padx=1, pady=1, sticky=tk.E)
                k+=1
        self.button2 = tk.Button(fr,text='切换股票',command=self.bt2,cursor='hand2')  
        self.button2.grid(row=0, column=self.c+1, padx=1, pady=1, sticky=tk.E)              
        fr.pack(side=tk.TOP)
        self.F10text.window_create(tk.INSERT,window=fr)
        self.F10text.insert(tk.INSERT,'\n\n')
        t=htdx.get_F10(self.stock,df.name[0])
        self.F10text.insert(tk.INSERT,t)
    
g.UserF10View=UserF10(g.tab7)
g.UserF10View.pack(fill=tk.BOTH, expand=1)
g.tabControl.select(g.tab7)
g.tabs=7




