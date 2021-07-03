# -*- coding: utf-8 -*-
# 选股器面板
import time
import tkinter as tk
import  tkinter.ttk  as  ttk   #导入Tkinter.ttk
import  tkinter.tix  as  tix   #导入Tkinter.tix
import  HP_tk  as  htk   #导入htk
import HP_global as g 
import HP_data as hp
from HP_view import * #菜单栏对应的各个子页面 
import HP_tdx as htdx
from tkinter import messagebox, filedialog, simpledialog, colorchooser
import pandas as pd
import os

#系统设定了g.tab1--g.tab9,系统只是用了g.tab1--g.tab6
#控件结构 g.root -〉 g.tabControl  -〉g.tab1
#增加tab，用add()
#删除tab,用forget()
#当然用户可以设置更多的tab窗口。必须使用全局变量g.变量名
#重复建立新tab窗会出错，所以我们先检测是否None,不是就先做删除旧tab窗口。


if g.tab11!=None:
    g.tabControl.forget(g.tab11)
    g.tab11=None

#用户自建新画面
g.tab11 = tk.Frame(g.tabControl)
g.tabControl.add(g.tab11, text='公式转换') 
g.tabControl.select(g.tab11)


global fsize,v1,v2,v3
global text1,text2
fsize=11
v1=tk.LabelFrame(g.tab11, text="指标公式",font = 'Helvetica %d'%fsize,width = 400)
v1.pack(side=tk.LEFT, fill=tk.Y)

v2=tk.LabelFrame(g.tab11, text="转换参数",font = 'Helvetica %d'%fsize,width = 100)
v2.pack(side=tk.LEFT, fill=tk.Y)

v3=tk.LabelFrame(g.tab11, text="Python代码",font = 'Helvetica %d'%fsize,width = 400)
v3.pack(side=tk.LEFT, fill=tk.BOTH)

text1 = tk.Text(v1,width=60 )

text1.pack(expand=tk.YES,fill=tk.BOTH)
pop1=htk.PopMenu(text1)

gs='''#KDJ指标
RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
K:SMA(RSV,M1,1);
D:SMA(K,M2,1);
J:3*K-2*D;
'''
text1.insert(1.0,gs)

global gsn,gsna,gscs
label1 = tk.Label(v2, width=10, text='公式名称:',ancho=tk.S)
label1.pack(side=tk.TOP,padx=10,pady=4)
gsn = tk.StringVar()
gsn.set('KDJ')
gsn2 = tk.Entry(v2, width=10, textvariable=gsn)
gsn2.pack(side=tk.TOP,padx=10,pady=4)

label1a = tk.Label(v2, width=10, text='公式参数:',ancho=tk.S)
label1a.pack(side=tk.TOP,padx=10,pady=4)
gsna = tk.StringVar()
gsna.set('N=9,M1=3,M2=3')
gsn2a = tk.Entry(v2, width=10, textvariable=gsna)
gsn2a.pack(side=tk.TOP,padx=10,pady=4)

gscs=tk.IntVar()
gscs.set(0)
check1 = tk.Checkbutton(v2, text="转换函数", variable=gscs)   
check1.pack(side=tk.TOP,padx=10,pady=4)

def getbk6():
    global v1,v2,v3
    global text1,text2
    global gsn,gsna,gscs
    gs3=[]
    if gscs.get()==0:
        gsx=gsna.get()
        gsx=gsx.strip()
        gsx=gsx.upper()
        if len(gsx)>3:
            gsx2=gsx.split(',')
            for s in gsx2:
                gs3.append(s)
        gs= text1.get(1.0,tk.END)
        gs=gs.upper()
        gs2=gs.split('\n')     #分解为行列表
        ovar=''
        for s in gs2:
            s=s.replace(':=','=')
            if s.find(':')>0:
                if len(ovar)>0:
                    ovar=ovar+','+s[0:s.find(':')]
                else:
                    ovar=s[0:s.find(':')]
                s=s.replace(':','=')
            s=s.strip() 
            if (len(s))>0:
                if s[-1]==';':
                    s=s[0:len(s)-1]
            gs3.append(s)
        gs4="\n".join(gs3)
        gs4=gs4+'\n#return '+ovar
        text2.delete(1.0,tk.END)#delete all
        text2.insert(1.0,gs4)
    else:
        gsx3=gsn.get()
        gsx3=gsx3.strip()
        gsx3=gsx3.upper()
        if len(gsx3)<1:
            gsx3='UFN'
        ss='def '+gsx3
        gsx=gsna.get()
        gsx=gsx.strip()
        gsx=gsx.upper()
        if len(gsx)>3:
            ss=ss+'('+gsx+'):'
        else:
            ss=ss+'():'
        gs3.append(ss)
        gs= text1.get(1.0,tk.END)
        gs=gs.upper()
        gs2=gs.split('\n')     #分解为行列表
        ovar=''
        for s in gs2:
            s=s.replace(':=','=')
            if s.find(':')>0:
                if len(ovar)>0:
                    ovar=ovar+','+s[0:s.find(':')]
                else:
                    ovar=s[0:s.find(':')]
                s=s.replace(':','=')
            s=s.strip() 
            if (len(s))>0:
                if s[-1]==';':
                    s=s[0:len(s)-1]
            s='    '+s
            gs3.append(s)
        gs4="\n".join(gs3)
        gs4=gs4+'\n    return '+ovar
        text2.delete(1.0,tk.END)#delete all
        text2.insert(1.0,gs4)

bb1= tk.Button(v2, text="开始转换", cursor='hand2',\
                     command=getbk6) #带参数函数)
bb1.pack(side=tk.TOP,padx=10,pady=4)

text2 = tk.Text(v3,width=60)

text2.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
pop2=htk.PopMenu(text2)