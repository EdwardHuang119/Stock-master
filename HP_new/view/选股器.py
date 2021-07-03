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


if g.tab9!=None:
    g.tabControl.forget(g.tab9)
    g.tab9=None

#用户自建新画面
g.tab9 = tk.Frame(g.tabControl)
g.tabControl.add(g.tab9, text='选股器') 
g.tabControl.select(g.tab9)

bkml='bk'  #板块路径
if os.path.exists(bkml)==False:
    os.makedirs(bkml)  #建立文件夹

global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6,bkv7
global lba,lba2,lba3,lba4,lba5
global usrbk,usrbk2
global fsize,v2,v4
fsize=11
usrbk=''
usrbk2=''
v1=tk.Frame(g.tab9,width = 200)
v1.pack(side=tk.LEFT,fill=tk.Y)
v2=tk.LabelFrame(g.tab9, text="板块内股票(0)",font = 'Helvetica %d'%fsize,width = 100)
v2.pack(side=tk.LEFT, fill=tk.BOTH)
v3=tk.LabelFrame(g.tab9, text="运算",font = 'Helvetica %d'%fsize,width = 100)
v3.pack(side=tk.LEFT, fill=tk.Y)
v4=tk.LabelFrame(g.tab9, text="股票池(0)",font = 'Helvetica %d'%fsize,width = 100)
v4.pack(side=tk.LEFT, fill=tk.Y)

v5=tk.LabelFrame(g.tab9, text="条件选股",font = 'Helvetica %d'%fsize,width = 100)
v5.pack(side=tk.LEFT, fill=tk.Y)


v1a=tk.LabelFrame(v1, text="板块1",font = 'Helvetica %d'%fsize)
v1a.pack(side=tk.TOP)
scrollbara=tk.Scrollbar(v1a)
scrollbara.pack(side=tk.RIGHT,fill=tk.Y)
bkv1=tk.StringVar()
lba=tk.Listbox(v1a,selectmode=tk.BROWSE,yscrollcommand=scrollbara.set,
              font = 'Helvetica %d'%fsize,listvariable=bkv1,height=4)
lba.pack(expand=tk.YES,fill=tk.X,padx=5,pady=5)
scrollbara.config(command=lba.yview)

bkv2=tk.StringVar()
v2a=tk.LabelFrame(v1, text="板块2",font = 'Helvetica %d'%fsize)
v2a.pack(side=tk.TOP)
scrollbara2=tk.Scrollbar(v2a)
scrollbara2.pack(side=tk.RIGHT,fill=tk.Y)
lba2=tk.Listbox(v2a,selectmode=tk.BROWSE,yscrollcommand=scrollbara2.set,
              font = 'Helvetica %d'%fsize,listvariable=bkv2,height=4)
lba2.pack(expand=tk.YES,fill=tk.X,padx=5,pady=5)
scrollbara2.config(command=lba2.yview)

bkv3=tk.StringVar()
v3a=tk.LabelFrame(v1, text="板块3",font = 'Helvetica %d'%fsize)
v3a.pack(side=tk.TOP)
scrollbara3=tk.Scrollbar(v3a)
scrollbara3.pack(side=tk.RIGHT,fill=tk.Y)
lba3=tk.Listbox(v3a,selectmode=tk.BROWSE,yscrollcommand=scrollbara3.set,
              font = 'Helvetica %d'%fsize,listvariable=bkv3,height=4)
lba3.pack(expand=tk.YES,fill=tk.X,padx=5,pady=5)
scrollbara3.config(command=lba3.yview)

bkv4=tk.StringVar()
v4a=tk.LabelFrame(v1, text="板块4",font = 'Helvetica %d'%fsize)
v4a.pack(side=tk.TOP)
scrollbara4=tk.Scrollbar(v4a)
scrollbara4.pack(side=tk.RIGHT,fill=tk.Y)
lba4=tk.Listbox(v4a,selectmode=tk.BROWSE,yscrollcommand=scrollbara4.set,
              font = 'Helvetica %d'%fsize,listvariable=bkv4,height=4)
lba4.pack(expand=tk.YES,fill=tk.X,padx=5,pady=5)
scrollbara4.config(command=lba4.yview)

bkv5=tk.StringVar()
v5a=tk.LabelFrame(v1, text="自选板块",font = 'Helvetica %d'%fsize)
v5a.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
scrollbara5=tk.Scrollbar(v5a)
scrollbara5.pack(side=tk.RIGHT,fill=tk.Y)
lba5=tk.Listbox(v5a,selectmode=tk.BROWSE,yscrollcommand=scrollbara5.set,
              font = 'Helvetica %d'%fsize,listvariable=bkv5,height=4)
lba5.pack(expand=tk.YES,fill=tk.BOTH,padx=5,pady=5)
scrollbara5.config(command=lba5.yview)

bkv6=tk.StringVar()
scrollbara6=tk.Scrollbar(v2)
scrollbara6.pack(side=tk.RIGHT,fill=tk.Y)
lba6=tk.Listbox(v2,selectmode=tk.BROWSE,yscrollcommand=scrollbara6.set,
              font = 'Helvetica %d'%fsize,listvariable=bkv6)
lba6.pack(expand=tk.YES,fill=tk.BOTH,padx=5,pady=5)
scrollbara6.config(command=lba6.yview)


bkv7=tk.StringVar()
scrollbara7=tk.Scrollbar(v4)
scrollbara7.pack(side=tk.RIGHT,fill=tk.Y)
lba7=tk.Listbox(v4,selectmode=tk.BROWSE,yscrollcommand=scrollbara7.set,
              font = 'Helvetica %d'%fsize,listvariable=bkv7)
lba7.pack(expand=tk.YES,fill=tk.BOTH,padx=5,pady=5)
scrollbara7.config(command=lba7.yview)


bk=htdx.get_block2("block.dat")
g.bkdf.append(bk)
bk2=list(bk['blockname'])
bk3=set(bk2)
bk2=list(bk3)
g.blockname.append(bk2)
bkv1.set(bk2)
bk=htdx.get_block2("block_zs.dat")
g.bkdf.append(bk)
bk2=list(bk['blockname'])
bk3=set(bk2)
bk2=list(bk3)
g.blockname.append(bk2)
bkv2.set(bk2)
bk=htdx.get_block2("block_fg.dat")
g.bkdf.append(bk)
bk2=list(bk['blockname'])
bk3=set(bk2)
bk2=list(bk3)
g.blockname.append(bk2)
bkv3.set(bk2)
bk=htdx.get_block2("block_gn.dat")
g.bkdf.append(bk)
bk2=list(bk['blockname'])
bk3=set(bk2)
bk2=list(bk3)
g.blockname.append(bk2)
bkv4.set(bk2)

global bk4,bk5
bk4=os.listdir('bk')
bk5=[]
for x in bk4:
    y=x.split('.')
    bk5.append(y[0])
bkv5.set(bk5)

def selectbk1(event):
    global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6,bkv7
    import HP_tdx as htdx
    global tb6,usrbk,v2
    ss=lba.get(lba.curselection())
    df=g.bkdf[0]
    df=df[df.blockname==ss]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    df['name']=''
    mybk=[]
    usrbk=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
        mybk.append(df.loc[i,'code']+'  '+df.loc[i,'name'])
        usrbk+=df.loc[i,'code']+' '
    bkv6.set(mybk) 
    v2['text']="板块内股票(%d)"%len(df)

lba.bind('<Double-Button-1>',selectbk1)

def selectbk2(event):
    global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6
    import HP_tdx as htdx
    global tb6,usrbk,v2,lba2
    ss=lba2.get(lba2.curselection())
    df=g.bkdf[1]
    df=df[df.blockname==ss]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    df['name']=''
    mybk=[]
    usrbk=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
        mybk.append(df.loc[i,'code']+'  '+df.loc[i,'name'])
        usrbk+=df.loc[i,'code']+' '
    bkv6.set(mybk)
    v2['text']="板块内股票(%d)"%len(df)    
    
lba2.bind('<Double-Button-1>',selectbk2)

def selectbk3(event):
    global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6
    import HP_tdx as htdx
    global tb6,usrbk,v2
    ss=lba3.get(lba3.curselection())
    df=g.bkdf[2]
    df=df[df.blockname==ss]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    df['name']=''
    mybk=[]
    usrbk=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
        mybk.append(df.loc[i,'code']+'  '+df.loc[i,'name'])
        usrbk+=df.loc[i,'code']+' '       
    bkv6.set(mybk)
    v2['text']="板块内股票(%d)"%len(df)    

lba3.bind('<Double-Button-1>',selectbk3)

def selectbk4(event):
    global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6
    import HP_tdx as htdx
    global tb6,usrbk,v2
    ss=lba4.get(lba4.curselection())
    df=g.bkdf[3]
    df=df[df.blockname==ss]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    df['name']=''
    mybk=[]
    usrbk=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
        mybk.append(df.loc[i,'code']+'  '+df.loc[i,'name'])
        usrbk+=df.loc[i,'code']+' '
    bkv6.set(mybk) 
    v2['text']="板块内股票(%d)"%len(df)
  
lba4.bind('<Double-Button-1>',selectbk4)


def selectbk5(event):
    global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6
    import HP_tdx as htdx
    global tb6,usrbk,v2
    ss=lba5.get(lba5.curselection())
    ss=ss.strip()
    file=r'bk/'+ss+'.csv'
    df=pd.read_csv(file, encoding= 'gbk')
    df.rename(columns={'code':'code2'},\
                        inplace = True)
    df['code']=['0'*(6-len(x)) + x for x in df.code2.astype(str)]
    df= df.drop('code2', axis=1)
    df['name']=''
    mybk=[]
    usrbk=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
        mybk.append(df.loc[i,'code']+'  '+df.loc[i,'name'])
        usrbk+=df.loc[i,'code']+' '
    bkv6.set(mybk) 
    v2['text']="板块内股票(%d)"%len(df)
  
lba5.bind('<Double-Button-1>',selectbk5)


def getbk6():
    global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6
    global usrbk,usrbk2,v2,v4
    if len(usrbk2)==0:
        usrbk2+=usrbk
    else:
        usrbk2+=' '
        usrbk2+=usrbk
    bkv7.set(usrbk2)  
    usrbk3=usrbk2.strip().split(' ')
    v4['text']='股票池(%d)'%len(usrbk3)
    
    
def btncmd():
    global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6
    global usrbk,usrbk2,v4
    usrbk3=usrbk2.strip().split(' ')
    a=set(usrbk3)
    usrbk3=list(a)
    usrbk2=''
    for s in usrbk3:
        usrbk2=usrbk2+s+' '
    usrbk2=usrbk2.strip()
    bkv7.set(usrbk2)  
    usrbk3=usrbk2.strip().split(' ')
    v4['text']='股票池(%d)'%len(usrbk3)
    

def btncmd2():
    global bkv1,bkv2,bkv3,bkv4,bkv5,bkv6
    global usrbk,usrbk2,v4
    usrbk2=''
    bkv7.set(usrbk2)  
    v4['text']='股票池(%d)'%0
    
def btncmd3():
    file =simpledialog. askstring ('保存自选板块', '请输入自选板块名称(不能用中文)', initialvalue=None, parent = None)
    df = pd.DataFrame(columns = ['code'])
    usrbk3=usrbk2.strip().split(' ')
    df['code']=usrbk3
    #print(df)
    df.to_csv('bk/'+file+'.csv' , encoding= 'gbk')
    bk4=os.listdir('bk')
    bk5=[]
    for x in bk4:
        y=x.split('.')
        bk5.append(y[0])
    bkv5.set(bk5)

    

bb1= tk.Button(v3, text="加入股票池", cursor='hand2',\
                     command=getbk6) #带参数函数)
bb1.pack(side=tk.TOP,padx=10,pady=4)

bb2= tk.Button(v3, text="去重复代码", cursor='hand2',\
                     command=btncmd) #带参数函数)
bb2.pack(side=tk.TOP,padx=10,pady=4)

bb3= tk.Button(v3, text="清空股票池", cursor='hand2',\
                     command=btncmd2) #带参数函数)
bb3.pack(side=tk.TOP,padx=10,pady=4)

bb4= tk.Button(v3, text="保存自选股", cursor='hand2',\
                     command=btncmd3) #带参数函数)
bb4.pack(side=tk.TOP,padx=10,pady=4)


book2 = tk.StringVar()
books = ttk.Combobox(v5, width=10, textvariable=book2)
t=list(g.cw.values())
books['values'] =t
books.current(2)  #设置初始显示值，值为元组['values']的下标
books.pack(side=tk.TOP,padx=10,pady=4)


bb5= tk.Button(v5, text="财务数据过滤", cursor='hand2',\
                     command=btncmd3) #带参数函数)
bb5.pack(side=tk.TOP,padx=10,pady=4)

label11 = tk.Label(v5, width=10, text='过滤范围:',ancho=tk.S)
label11.pack(side=tk.TOP,padx=10,pady=4)
glfw1 = tk.StringVar()
glfw1a = tk.Entry(v5, width=10, textvariable=glfw1)
glfw1a.pack(side=tk.TOP,padx=10,pady=4)
label12 = tk.Label(v5 ,width=10, text='至')
label12.pack(side=tk.TOP,padx=10,pady=4)
glfw2 = tk.StringVar()
glfw2a = tk.Entry(v5, width=10, textvariable=glfw2)
glfw2a.pack(side=tk.TOP,padx=10,pady=4)

bb5= tk.Button(v5, text="开始过滤", cursor='hand2',\
                     command=btncmd3) #带参数函数)
bb5.pack(side=tk.TOP,padx=10,pady=4)
