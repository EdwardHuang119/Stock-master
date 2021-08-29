import  tkinter  as  tk   #导入Tkinter
#from mttkinter import mtTkinter as tk
import  tkinter.ttk  as  ttk   #导入Tkinter.ttk
import  tkinter.tix  as  tix   #导入Tkinter.tix
from tkinter.filedialog import *
from tkinter.messagebox import *
import HP_tk as htk   #导入htk
from  HP_robot import *
from  HP_edit import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
import pickle
import sys
import os
import HP_global as g   #建立全局数据域g
import HP_set   #全局数据域g中变量初始化
#import HP_robot as hrt
import webbrowser
import string
import  HP_view as hpv
import threading
import HP_tdx as htdx
import HP_data as hp
import datetime as dt
from HP_formula import *
import requests
from HP_cl import * #中文常量
from PIL import Image, ImageTk, ImageDraw, ImageFont


global svr_ip       #行情服务ip
global svr_port      #行情服务端口
svr_ip='40.73.76.10'
svr_port=7709


global timer_interval
timer_interval=1  #时钟
global shpy,szpy
global shpyzd,szpyzd
global hq

hq=None
g.hqlink=False
g.login=False

#用户输出信息
#用户输出信息
def tprint(txt):
    g.ttmsg.insert(tk.END, txt)
    g.ttmsg.see(tk.END)

#用户输出信息,带颜色
def ttprint(txt,color):
    if g.ttmsg != None :
        g.ttmsg.insert(tk.END, txt,color)
        g.ttmsg.see(tk.END)

global tk_image,pil_image,logolabel
def logo(root=g.root):
    global tk_image,pil_image,logolabel
    pil_image =Image.open('img/bj.jpg')
    #获取图像的原始大小  
    w, h = pil_image.size  
    w2=w+1
    h2=h+10        
    pil_image = htk.resize(w, h, w2 , h2, pil_image)  
    r2,g2,b2=htk.RGB(g.cns['gold'])
    htk.drawFont2(pil_image,10,10,"小白量化投资分析系统",size=40,r=r2,g=g2,b=b2)
    r2,g2,b2=htk.RGB(g.cns['gold'])
    htk.drawFont2(pil_image,80,50,"--大众化基于人工智能的量化投资系统",size=26,r=r2,g=g2,b=b2)
    htk.drawFont3(pil_image,10,70,"超越!",size=80,r=255,g=0,b=0)
    htk.drawFont3(pil_image,110,150,"是我们的每一步！",size=54,r=255,g=255,b=0)
    htk.drawFont(pil_image,150,240,"设 计： 何 战 军",size=30,r=0,g=0,b=0)
    htk.drawFont(pil_image,140,230,"设 计： 何 战 军",size=30,r=255,g=255,b=255)
    tk_image = ImageTk.PhotoImage(pil_image)  
    w1 = htk.myWindow2(g.root,g.title,w2,h2)  #创建弹出窗口
    w1.overturn() #隐藏窗口边框
    label=tk.Label(w1.top,image=tk_image)
    label.place(x=0, y=0, relwidth=1, relheight=1,bordermode=tk.OUTSIDE)
    htk.setCenter(w1.top,tk_image.width()+4,tk_image.height()+4)
    htk.reSizable(w1.top,False, False)
    logolabel = tk.StringVar()  
    logolabel.set('正在加载数据...')
    tk.Label(w1.top, text = '',textvariable=logolabel,width=43,\
          font = 'Helvetica -18 bold',bg=g.cns['darkblue'],fg='white').place(x=26, y=310)

    def fun_timer():
        global timer
        w1.destroy()  
        timer.cancel()   
    timer = threading.Timer(18, fun_timer)
    timer.start()


#获取网页或网页文件的内容 
def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def runpy():
    filename = askopenfilename(defaultextension='.py')
    msg=''
    if filename == '':
        filename = ''
    else:
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        msg=msg+f.read()
        f.close()

    try:
        print('开始运行用户代码。\n')
        tprint('开始运行用户代码。\n')
        exec(msg)
    except Exception as e:
        #print(type(e))
        #ttprint('用户代码出错:'+str(e)+'\n','red')
        print('用户代码出错:'+str(e)+'\n')
        showinfo(title='用户代码出错', message=str(e))
        

g.title='小白量化投资分析系统(QQ:2775205)'

#建立主窗口
root=htk.MainWindow(title=g.title,x=100,y=200,w=1200, h=700)
g.root=root
root.iconbitmap('ico/xb.ico')  #设置应用程序图标
root.SetCenter()  #移动到屏幕中央
#htk.thread_it(logo())  ##用多线程启动定时器



#建立菜单
menus = [['文件',['执行程序','-','新建','打开','运行','-','保存','另存为']],\
         ['编辑',['撤销','重做','-','剪切','复制','粘贴','清除','-','全选']],\
         ['显示',['绘图','表格']],\
         ['程序',['运行','编译']],\
         ['项目',['工程设置','系统设置']],\
         ['数据',['连接行情服务器','断开行情服务器','下载股票代码表','下载财务数据',\
                '下载板块数据']],\
         ['帮助',['关于软件','退出']]]


mainmenu=htk.windowMenu(root,menus) #窗口菜单
g.mainmenu=mainmenu
png= ImageTk.PhotoImage(Image.open('ico/16x16/3.ICO'))
#mainmenu.set('文件','打开',image=png)
mainmenu.set('文件','执行程序',command=runpy)

#建立工具栏
toolsbar=htk.ToolsBar(root,5,bg='#1E488F') #创建工具栏
toolsbar.pack(side=tk.TOP, fill=tk.X)   #把工具栏放到窗口顶部
png0= ImageTk.PhotoImage(Image.open('ico/program.ico'))
png1= ImageTk.PhotoImage(Image.open('ico/Table.ico'))
png2= ImageTk.PhotoImage(Image.open('ico/GRAPH01.ICO'))
png3= ImageTk.PhotoImage(Image.open('ico/FOLDER06.ICO'))
png4= ImageTk.PhotoImage(Image.open('ico/GRAPH07.ICO'))
#改变工具栏的图标
toolsbar.config(0,image=png0)
toolsbar.config(1,image=png1)
toolsbar.config(2,image=png2)
toolsbar.config(3,image=png3)
toolsbar.config(4,image=png4)

#建立状态栏
status=htk.StatusBar(root)    #建立状态栏
status.pack(side=tk.BOTTOM, fill=tk.X) #把状态栏放到窗口底部
status.clear()
status.text(0,'状态栏') #在状态栏1输出信息
status.text(1,'超越自我！') #在状态栏2输出信息
status.text(2,'超越！是我们的每一步！')
status.text(3,'版权所有')
status.text(4,'侵权必究')
status.text(5,'设计:小白')
status.config(1,color='red') #改变状态栏2信息颜色
status.config(3,color='green') #改变状态栏2信息颜色
status.config(4,color='blue') #改变状态栏2信息颜色
#status.config(5,width=5)   #改变状态栏6的宽度
g.status=status

def hq1():
    global hq
    g.status.text(2,'正在连接行情服务器...')
    hq=htdx.TdxInit(ip='180.153.18.171',port=7709)  ##初始化通达信
    if hq==None:
        g.status.text(2,'行情服务器连接失败!')
    else:
        g.status.text(2,'行情服务器连接成功!')

def hq2():
    global hq
    if hq==None:
        g.status.text(2,'没有连接行情服务器。')
    else:
        hq=htdx.disconnect()  ##断开通达信行情服务器
        hq=None
        g.status.text(2,'已经断开行情服务器。')

def hq3():
    global hq
    if hq!=None:
        g.status.text(2,'正在下载代码表...请等待，如强制退出，将无法启动软件。')
        htdx.shcode()
        htdx.szcode()
        g.status.text(2,'代码表下载完成。')
    else:
        g.status.text(2,'没有连接行情服务器。')

def hq4():
    global hq
    if hq==None:
        g.status.text(2,'没有连接行情服务器。')
    else:
        g.status.text(2,'正在下载财务报表...请等待，如强制退出，将无法启动软件。')
        htdx.get_szcw()
        htdx.get_shcw()
        g.status.text(2,'财务报表下载完成。')

def hq5():
    global hq
    if hq==None:
        g.status.text(2,'没有连接行情服务器。')
    else:
        g.status.text(2,'正在下载板块数据...请等待，如强制退出，将无法启动软件。')
        df=htdx.get_block("block.dat")
        df=htdx.get_block("block_zs.dat")
        df=htdx.get_block("block_fg.dat")
        df=htdx.get_block("block_gn.dat")
        g.status.text(2,'板块数据下载完成。')

        
mainmenu.set('数据','连接行情服务器',command=hq1)
mainmenu.set('数据','断开行情服务器',command=hq2)
mainmenu.set('数据','下载股票代码表',command=hq3)
mainmenu.set('数据','下载财务数据',command=hq4)
mainmenu.set('数据','下载板块数据',command=hq5)


frame = tk.Frame(toolsbar, bg='#1E488F')
lb1=tk.Label(frame, text=' ',bg='#1E488F').grid(row=0, column=0)
lb2 = tk.Label(frame, width=10, text='开始日期: ',ancho=tk.S,\
               bg='#1E488F',fg='white')
lb2.grid(row=0, column=1)
#输入框 (Entry)
date_s = tk.StringVar()
g.date_s=date_s
entrydates = tk.Entry(frame, width=10, textvariable=date_s)
entrydates.grid(row=0, column=2)
date_s.set(g.sday)
lb3=tk.Label(frame , text=' ',bg='#1E488F').grid(row=0, column=3)
lb4 = tk.Label(frame ,width=10, text='结束日期: ',bg='#1E488F',\
                   fg='white')
lb4.grid(row=0, column=4)
#输入框 (Entry)
date_e = tk.StringVar()
g.date_e=date_e
entrydatee = tk.Entry(frame, width=10,textvariable=date_e)
nowdt=dt.datetime.now()   #获取今天日期
g.eday=nowdt.strftime('%Y-%m-%d')   #将日期格式转字串格式
date_e.set(g.eday)
entrydatee.grid(row=0, column=5)
lb5=tk.Label(frame , text=' ',bg='#1E488F').grid(row=0, column=6)
lb6 = tk.Label(frame ,width=10, text='股票代码:',bg='#1E488F',\
               fg='white')
lb6.grid(row=0, column=7)
#输入框 (Entry)
stock = tk.StringVar()
g.stock_i=stock
stock.set(g.stock)    
entrystock = tk.Entry(frame,width=10, textvariable=stock)
entrystock.grid(row=0, column=8)

global dsq       #定时器状态
global dsqsj     #定时期时间
global timer2  #定时器2
dsqsj=20    #秒

def dsjs():
    if g.tabs==6:
         try:
            filename= '../../../Downloads/xb2e/view/分时图.py'
            g.status.text(2,'查看'+g.stock+' '+g.stock_names[g.stock]+' 分时图！')
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            msg=f.read()
            f.close()
            exec(msg)
            g.tabs=6
         except Exception as e:
            g.status.text(1,'')
            g.status.text(2,'用户代码出错:'+str(e))
            ttprint('用户代码出错:'+str(e)+'\n','red')

#确定按钮
def rtnkey(event=None):
    global dsq       #定时器状态
    global dsqsj     #定时期时间
    global timer2  #定时器2
    xx=g.tabControl.select()
    yy=g.tabControl.index(xx)
    zz=g.tabControl.tab(yy)['text']
    if zz in g.tabn:
        g.tabs=g.tabn.index(zz)+1
    else:
        g.tabs=3
    cmd=stock.get()
    cmd=cmd.strip()
    cmd=cmd.upper()
    if cmd=='FST':
        g.tabs=6
        stock.set(g.stock)
    elif cmd=='RXT':
        g.tabs=3
        stock.set(g.stock)
    elif cmd=='F10':
        g.tabs=7
        stock.set(g.stock)        
    
    stockn=stock.get()
    stockn=stockn.strip()
    stockn=stockn.zfill(6)
    stock.set(stockn)
    g.stock=stockn
    if g.tabs<=5:
         try:
            filename= '../../../Downloads/xb2e/view/日线图.py'
            g.status.text(2,'查看'+g.stock+' '+g.stock_names[g.stock]+' 日线图！')
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            msg=f.read()
            f.close()
            exec(msg)
         except Exception as e:
            g.status.text(1,'')
            g.status.text(2,'用户代码出错:'+str(e))
            ttprint('用户代码出错:'+str(e)+'\n','red')
    elif g.tabs==6:
         dsjs()

    elif g.tabs==7:
        try:
            filename= '../../../Downloads/xb2e/view/F10窗口.py'
            g.status.text(2,'查看'+g.stock+' '+g.stock_names[g.stock]+'  F10信息！')
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            msg=f.read()
            f.close()
            exec(msg)
        except Exception as e:
            g.status.text(1,'')
            g.status.text(2,'用户代码出错:'+str(e))
            ttprint('用户代码出错:'+str(e)+'\n','red')        
    elif g.tabs==8:
        try:
            filename= '../../../Downloads/xb2e/view/三画面.py'
            g.status.text(2,'查看'+g.stock+' '+g.stock_names[g.stock]+'  三画面！')
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            msg=f.read()
            f.close()
            exec(msg)
        except Exception as e:
            g.status.text(1,'')
            g.status.text(2,'用户代码出错:'+str(e))
            ttprint('用户代码出错:'+str(e)+'\n','red')       
    elif g.tabs==9:
        try:
            filename= '../../../Downloads/xb2e/view/四画面.py'
            g.status.text(2,'查看'+g.stock+' '+g.stock_names[g.stock]+'  四画面！')
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            msg=f.read()
            f.close()
            exec(msg)
        except Exception as e:
            g.status.text(1,'')
            g.status.text(2,'用户代码出错:'+str(e))
            ttprint('用户代码出错:'+str(e)+'\n','red')  

            
#绑定回车键
entrystock.bind('<Key-Return>', rtnkey)   
lb7=tk.Label(frame, text=' ',bg='#1E488F').grid(row=0, column=9)
#按钮  (Button)
getname = tk.Button(frame , width=5,text='确认' ,command=rtnkey)
getname.grid(row=0, column=10)
lb9=tk.Label(frame , text=' ',bg='#1E488F').grid(row=0, column=11)
lb10 = tk.Label(frame,width=5,text='指标:',bg='#1E488F',fg='white')
lb10.grid(row=0, column=12)
#增加 Combobox
book = tk.StringVar()
g.book_s=book
bookChosen = ttk.Combobox(frame, width=10, textvariable=book)
bookChosen['values'] = ('HPCPX','KDJ', 'MACD','RSI','OBV','BOLL',\
          '自定义','HPYYX')
bookChosen.grid(row=0, column=13)
bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标
bookChosen.config(state='readonly')  #设为只读模式
frame.grid(row=0, column=6, padx=1, pady=1, sticky=tk.E)
g.vbook=book 


# 建立 tixballoon
b = tix.Balloon(root, statusbar=status.l[2])

b.bind_widget(toolsbar.t[0], balloonmsg='工作台',
              statusmsg='按下这个按钮,切换到工作台画面。')
b.bind_widget(toolsbar.t[1], balloonmsg='报价分析',
              statusmsg='按下这个按钮,切换到报价分析画面。')
b.bind_widget(toolsbar.t[2], balloonmsg='技术分析',
              statusmsg='按下这个按钮,切换到技术分析画面。')

b.bind_widget(toolsbar.t[3], balloonmsg='装载插件',
              statusmsg='按下这个按钮,装入用户插件程序。')

b.bind_widget(toolsbar.t[4], balloonmsg='执行策略',
              statusmsg='按下这个按钮,执行代码编辑器中。')

b.bind_widget(status.l[0], balloonmsg='状态栏')
b.bind_widget(status.l[1], balloonmsg='时间')
b.bind_widget(status.l[2], balloonmsg='输出信息栏')

m1 = tk.PanedWindow(root,showhandle=True, sashrelief=tk.SUNKEN,sashwidth=1,width=200)  #默认是左右分布的
m1.pack(fill=tk.BOTH, expand=1)
#左画面设计
ttabControl = ttk.Notebook(m1)          # Create Tab Control
ttab1 = ttk.Frame(ttabControl)            # Add a third tab
ttabControl.add(ttab1, text='系统插件')      # Make second tab visible
ttab2 = ttk.Frame(ttabControl)            # Create a tab 
ttabControl.add(ttab2, text='用户代码')      # Add the tab
ttab3 = ttk.Frame(ttabControl)            # Add a second tab
ttabControl.add(ttab3, text='小白帮助')      # Make second tab visible
m1.add(ttabControl)
m1.paneconfig(ttabControl,width=200)

t6 = htk.Tree(ttab1,width=200)
path= 'view'
t6.load_path(path)
t6.pack(expand = 1, fill = tk.BOTH)

t7 = htk.Tree(ttab2,width=200)
path= 'user'
t7.load_path(path)
t7.pack(expand = 1, fill = tk.BOTH)

t8 = htk.Tree(ttab3,width=200)
path= 'guide'
t8.load_path(path)
t8.pack(expand = 1, fill = tk.BOTH)


#右画面设计
m2 = tk.PanedWindow(orient=tk.VERTICAL, showhandle=True, sashrelief=tk.SUNKEN,height=500)
m1.add(m2)

tabControl = ttk.Notebook(m2)  #创建Notebook
tab1 = tk.Frame(tabControl,bg='blue')  #增加新选项卡tab1
tabControl.add(tab1, text='工作台')  #把新选项卡增加到Notebook
tab2 = tk.Frame(tabControl,bg='yellow') #增加新选项卡tab3
tabControl.add(tab2, text='行情报价')  #把新选项卡增加到Notebook
tab3 = tk.Frame(tabControl,bg='green')  #增加新选项卡tab3
tabControl.add(tab3, text='日线图')  #把新选项卡增加到Notebook
tab4 = tk.Frame(tabControl,bg='red')  #增加新选项卡tab3
tabControl.add(tab4, text='编写代码')  #把新选项卡增加到Notebook
tab5 = tk.Frame(tabControl)  #增加新选项卡tab3
tabControl.add(tab5, text='策略回测')  #把新选项卡增加到Notebook


tabControl.pack(expand=1, fill="both")  #使用pack方法显示
tabControl.select(tab1) #选择tab1
g.tabs=1
g.tabControl=tabControl
g.tab1=tab1
g.tab2=tab2
g.tab3=tab3
g.tab4=tab4
g.tab5=tab5


#-----------------
#小白培训视频第6讲知识点
#可调边布局,划分2部分
p1 = tk.PanedWindow(tab1,orient=tk.VERTICAL,showhandle=True, \
                    sashrelief=tk.SUNKEN,sashwidth=1)  #默认是左右分布的
p1.pack(fill=tk.BOTH, expand=1)
f1=tk.Frame(p1,bg='blue',height=360)
p1.add(f1)
p1.paneconfig(f1,height=360)
myedit=htk.useredit(f1)
myedit.pack()

#logolabel.set('正在加载知识库...')
robot_init()  #聊天机器人初始化



#T3是右下画面
f2=tk.Frame(m2,bg='yellow',heigh=200)
p1.add(f2)
umess=htk.useredit2(f2,fontsize=12) #信息输出框
p1.paneconfig(f2,heigh=200)
htk.ttmsg=umess.textPad   #绑定信息输出变量，

label3 = tk.Label(umess.statusbar ,width=5, text='AI对话:')
label3.pack(side=tk.LEFT)
us=tk.StringVar(value='')
us2=tk.Entry(umess.statusbar,width=90, textvariable=us)
us2.pack(side=tk.LEFT)
g.ttmsg=htk.ttmsg
myedit.outmess=g.ttmsg   #设置代码输出信息框

#发送信息
def sendmessage(event=None): 
    ai=' Py小灵通'
    msgcontent = '\n 我: ' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n ' 
    umess.tcprint( msgcontent, 'green') 
    xx=us.get()
    umess.tcprint( xx, 'black')
    us.set('')
    txt=tt_robot(xx)
    if txt=='亲爱的，当天请求次数已用完。':
        txt=moli_robot(xx)
    if len(txt.strip())<1:
        htk.ttmsg.see(END)
        return
    msgcontent = '\n'+ai+': ' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n ' 
    umess.tcprint( msgcontent, 'purple') 
    umess.tcprint( txt,'blue')
    htk.ttmsg.see(END)

btn=tk.Button(umess.statusbar , width=5,text='确认' ,command=sendmessage)
btn.pack(side=tk.LEFT)
#绑定回车键
us2.bind('<Key-Return>',  sendmessage)   

def ld():
    webbrowser.open("https://blog.csdn.net/hepu8")
def ld2():
    webbrowser.open("https://item.taobao.com/item.htm?spm=a1z10.1-c.w4004-3329876017.6.27b72b14j99nH5&id=528594825831")

bb1= tk.Button(umess.statusbar, text="我的博客", cursor='hand2',
                     command=ld,bg='#0000AA',fg='yellow') #带参数函数)
bb1.pack(side=tk.RIGHT,padx=10,pady=4)

#bb2= tk.Button(umess.statusbar, text="我的淘宝", cursor='hand2',
#                     command=ld2,bg='#FFA0A0',fg='blue') #带参数函数)
#bb2.pack(side=tk.LEFT,padx=4,pady=4)


code='''import HP_global as g
#用户输出信息
def tprint(txt):
    g.ttmsg.insert(tk.END, txt)
    g.ttmsg.see(tk.END)
tprint('人生苦短!学习小白量化!')

#框架中[增强插件]在view目录中
#框架中[用户程序]在user目录中
#框架中[小白帮助]在guide目录中
#股票代码框输入:fst分时图  rxt日线图  f10 F10信息

#购买<零基础搭建量化投资系统>正版书,送小白量化软件源代码。
#独狼荷蒲qq:2775205
#通通python量化群:524949939
#电话微信:18578755056
#微信公众号：独狼股票分析
'''

code=code+'\n#服务器ip: %s , 服务器port : %d'%(svr_ip,svr_port)

myedit.textPad.delete(1.0,tk.END)  #清空代码框
myedit.textPad.insert(tk.END,code) #代码框插入字符串

def treepop6(event):
    item = t6.tree.selection()[0]
    i2=t6.tree.parent(item)
    s2=""
    while i2!="":
        s2=t6.tree.item(i2, "text")+'\\'+s2
        i2=t6.tree.parent(i2)
    txt2=s2+t6.tree.item(item, "text")
    if txt2[-4:]=='.txt' or txt2[-3:]=='.py':
        myedit.loadfile(txt2)
    tabControl.select(tab1) #选择tab1

t6.usepop=treepop6




def treepop6(event):
    item = t6.tree.selection()[0]
    i2=t6.tree.parent(item)
    s2=""
    while i2!="":
        s2=t6.tree.item(i2, "text")+'\\'+s2
        i2=t6.tree.parent(i2)
    txt2=s2+t6.tree.item(item, "text")
    if txt2[-4:]=='.txt' or txt2[-3:]=='.py':
        myedit.loadfile(txt2)
    tabControl.select(g.tab1) #选择tab1

t6.usepop=treepop6


def treepop7(event):
    item = t7.tree.selection()[0]
    i2=t7.tree.parent(item)
    s2=""
    while i2!="":
        s2=t7.tree.item(i2, "text")+'\\'+s2
        i2=t7.tree.parent(i2)
    txt2=s2+t7.tree.item(item, "text")
    if txt2[-4:]=='.txt' or txt2[-3:]=='.py':
        myedit.loadfile(txt2)
    tabControl.select(g.tab1) #选择tab1

t7.usepop=treepop7


def treepop8(event):
    item = t8.tree.selection()[0]
    i2=t8.tree.parent(item)
    s2=""
    while i2!="":
        s2=t8.tree.item(i2, "text")+'\\'+s2
        i2=t8.tree.parent(i2)
    txt2=s2+t8.tree.item(item, "text")
    if txt2[-4:]=='.txt' or txt2[-3:]=='.py':
        myedit.loadfile(txt2)
    tabControl.select(tab1) #选择tab1

t8.usepop=treepop8

#[['文件',['执行','-','新建','打开','运行','-','保存','另存为']],\
#['编辑',['撤销','重做','-','剪切','复制','粘贴','清除','-','全选']],\
def newf():
    myedit.newfile()
mainmenu.set('文件','新建',command=newf)
def openfile():
    myedit.openfile()
mainmenu.set('文件','打开',command=openfile)
def savefile():
    myedit.savefile()
mainmenu.set('文件','保存',command=savefile)
def saveas():
    myedit.saveas()
mainmenu.set('文件','另存为',command=saveas)
def runuc():
    myedit.runnc()
mainmenu.set('文件','运行',command=saveas)


#--------------------------------------------------
global mytab1,mytab2,mytab3,mytab4,mytab5,mytab6
mytabControl=htk.Notebook2(tab2,anchor=tk.SW)
mytab1 = tk.Frame(mytabControl,bg='red')  #增加新选项卡
mytabControl.add(mytab1,text='上海指数板块')
mytab2 = tk.Frame(mytabControl,bg='red')  #增加新选项卡
mytabControl.add(mytab2,text='上海证券')

mytab3 = tk.Frame(mytabControl,bg='blue')  #增加新选项卡
mytabControl.add(mytab3,text='深圳指数板块')
mytab4 = tk.Frame(mytabControl,bg='blue')  #增加新选项卡
mytabControl.add(mytab4,text='深圳证券')
mytab5 = tk.Frame(mytabControl,bg='yellow')  #增加新选项卡
mytabControl.add(mytab5,text='自选股')
mytab6 = tk.Frame(mytabControl,bg='yellow')  #增加新选项卡
mytabControl.add(mytab6,text='板块')
v1=tk.Frame(mytab6,width = 300)
v1.pack(side=tk.LEFT,fill=tk.Y)
v2=tk.Frame(mytab6,bg='yellow')
v2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

fsize=12
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


global tb,tb2,tb3,tb4,tb5,tb6
tb = htk.Table(mytab1)   #创建表格控件
tb.pack(expand = 1, fill = tk.BOTH)
tb2 = htk.Table(mytab2)   #创建表格控件
tb2.pack(expand = 1, fill = tk.BOTH)
tb3= htk.Table(mytab3)   #创建表格控件
tb3.pack(expand = 1, fill = tk.BOTH)
tb4 = htk.Table(mytab4)   #创建表格控件
tb4.pack(expand = 1, fill = tk.BOTH)

tb6 = htk.Table(v2)   #创建表格控件
tb6.pack(expand = 1, fill = tk.BOTH)


def get_shcode(t=''):
    base=pd.read_csv('./data/sh.csv' , encoding= 'gbk')
    base= base.drop('Unnamed: 0', axis=1)
    if t!='':
        base=base[base['type']==t]    
        base=base.reset_index(drop=True)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

def get_szcode(t=''):
    base=pd.read_csv('./data/sz.csv' , encoding= 'gbk')
    base= base.drop('Unnamed: 0', axis=1)
    if t!='':
        base=base[base['type']==t]
        base=base.reset_index(drop=True)
    base.code=['0'*(6-len(x)) + x for x in base.code.astype(str)]
    return base

global mydf2
if os.path.isfile('../../../Downloads/xb2e/data/zxg.dat'):
    #获取自选股文件
    f = open('../../../Downloads/xb2e/data/zxg.dat', 'rb')
    g.zxg=pickle.load(f)
    f.close()  


    
def main_init():
    global tb,tb2,tb3,tb4,tb5,tb6
    global mydf2,hq
    global svr_ip       #行情服务ip
    global svr_port      #行情服务端口

#    logolabel.set('正在连接行情服务器...')
    hq=htdx.TdxInit(ip=svr_ip,port=svr_port)  ##初始化通达信
    sh1=get_shcode('指数板块')
    sh1=sh1.round(2)  #改变符点数小数点后2位
    tb.load_df(sh1) #把变量df的数据显示到表格中
    tb.brush()  #用2种底色交替显示表格
    sh2=get_shcode('证券')
    sh2=sh2.round(2)  #改变符点数小数点后2位
    gp=sh2
    tb2.load_df(sh2) #把变量df的数据显示到表格中
    tb2.brush()  #用2种底色交替显示表格

    sz1=get_szcode('指数板块')
    sz1=sz1.round(2)  #改变符点数小数点后2位
    tb3.load_df(sz1) #把变量df的数据显示到表格中
    tb3.brush()  #用2种底色交替显示表格
    sz2=get_szcode('证券')
    sz2=sz2.round(2)  #改变符点数小数点后2位
    gp=gp.append(sz2,ignore_index=True)
    tb4.load_df(sz2) #把变量df的数据显示到表格中
    tb4.brush()  #用2种底色交替显示表格
    #print(gp)
    g.stock_names={}
    codes2=list(gp.code)
    names2=list(gp.name)
    i=0
    for i in range(len(codes2)):
        g.stock_names.update({codes2[i]:names2[i]})
    cd=get_szcode()
    cd2=get_shcode()
    cd=cd.append(cd2)
    cd=cd.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    #cd.to_csv('./data/codes.csv' , encoding= 'gbk')
    cds={}
    for i in range(len(cd)):
        cds[(cd.market[i],cd.code[i])]=cd.name[i]
    g.names=cds
    df=htdx.get_hq2(g.zxg)
    
    df['zd']=df['price']-df['last_close']  #涨跌
    df['zdf1']=df['zd']*100/df['last_close']  #涨跌幅
    df['vol']=df['vol']/10000
    df=df.round(2)  #改变符点数小数点后2位
    df['zdf']=df['zdf1'].astype(str)+'%'
    df['code2']=['0'*(6-len(x)) + x for x in df.code.astype(str)]
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=cds[(df.loc[i,'market'],df.loc[i,'code2'])]
    df.to_csv('./data/hq.csv' , encoding= 'gbk')    
    df=df[['code','name','zdf','price','zd','bid1','ask1','vol',\
           'high','open','low','last_close','market']]
    df.rename(columns={'code':'代码', 'name':'名称','zdf':'涨幅',\
                       'price':'现价','zd':'涨跌','bid1':'买价',\
                       'ask1':'卖价','vol':'总量(万)','open':'今开',\
                       'high':'最高','low':'最低','last_close':'昨收'},\
                        inplace = True)

    tb5 = htk.Table(mytab5)   #创建表格控件
    tb5.pack(expand = 1, fill = tk.BOTH)
    
    tb5.load_df(df) #把变量df的数据显示到表格中
    tb5.brush()  #用2种底色交替显示表格
    
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

main_init()
#htk.thread_it(main_init())

def selectbk1(event):
    global tb6
    ss=lba.get(lba.curselection())
    df=g.bkdf[0]
    df=df[df.blockname==ss]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
    df=df[['code_index','blockname','code','name']]
    df.rename(columns={'code_index':'序号', 'blockname':'板块名称',\
                       'code':'代码','name':'名称'},\
                        inplace = True)    
    tb6.clear()    
    tb6.load_df(df) #把变量df的数据显示到表格中
    tb6.brush()  #用2种底色交替显示表格    

lba.bind('<Double-Button-1>',selectbk1)

def selectbk2(event):
    global tb6
    ss=lba2.get(lba2.curselection())
    df=g.bkdf[1]
    df=df[df.blockname==ss]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
    df=df[['code_index','blockname','code','name']]
    df.rename(columns={'code_index':'序号', 'blockname':'板块名称',\
                       'code':'代码','name':'名称'},\
                        inplace = True)        
    tb6.clear()    
    tb6.load_df(df) #把变量df的数据显示到表格中
    tb6.brush()  #用2种底色交替显示表格    
lba2.bind('<Double-Button-1>',selectbk2)

def selectbk3(event):
    global tb6
    ss=lba3.get(lba3.curselection())
    df=g.bkdf[2]
    df=df[df.blockname==ss]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
    df=df[['code_index','blockname','code','name']]
    df.rename(columns={'code_index':'序号', 'blockname':'板块名称',\
                       'code':'代码','name':'名称'},\
                        inplace = True)    
    tb6.clear()    
    tb6.load_df(df) #把变量df的数据显示到表格中
    tb6.brush()  #用2种底色交替显示表格    
lba3.bind('<Double-Button-1>',selectbk3)

def selectbk4(event):
    global tb6
    ss=lba4.get(lba4.curselection())
    df=g.bkdf[3]
    df=df[df.blockname==ss]
    df=df.reset_index(level=None, drop=True ,col_level=0, col_fill='')
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=g.names[(htdx.get_market(df.loc[i,'code']),df.loc[i,'code'])]
    df=df[['code_index','blockname','code','name']]
    df.rename(columns={'code_index':'序号', 'blockname':'板块名称',\
                       'code':'代码','name':'名称'},\
                        inplace = True)    
    tb6.clear()    
    tb6.load_df(df) #把变量df的数据显示到表格中
    tb6.brush()  #用2种底色交替显示表格    
lba4.bind('<Double-Button-1>',selectbk4)



#上海股票行情
def rxt():
    ds=date_s.get()
    de=date_e.get()
    g.gtype=g.vbook.get()
    g.sday=ds.strip()
    g.eday=de.strip()
    item =tb2.tree.selection()[0]
    aa=tb2.tree.item(item, "values")
    bb=list(aa)        
    if bb[0][0:1]=='6' or bb[0][0:1]=='5':
        g.stock=bb[0] 
        g.gmarket=1
        stock.set(g.stock)
        g.vtitle=bb[1]
        #print(bb[0])
    
        df3=htdx.get_k_data2(g.stock,g.sday,g.eday)
        if g.tab3!=None:
            g.tabControl.forget(g.tab3)
            g.tab3=None
        
        #用户自建新画面
        g.tab3 = tk.Frame(g.tabControl)
        g.tabControl.add(g.tab3, text='日线图') 
        g.tabControl.select(g.tab3)
        axview3x(g.tab3,df3,t=g.stock+' '+g.stock_names[g.stock],n=2,f1='VOL',f2=g.gtype)
        g.tabControl.select(g.tab3)
        g.tabs=3
        
    
def fst():
    ds=date_s.get()
    de=date_e.get()
    item = tb2.tree.selection()[0]        
    aa=tb2.tree.item(item, "values")
    bb=list(aa)
    if bb[0][0:1]=='6':
        g.stock=bb[0]
        g.mstock=bb[0]
        g.vtitle=bb[1]
        g.gmarket=1
        stock.set(g.stock)
        try:
            filename= '../../../Downloads/xb2e/view/分时图.py'
            g.status.text(2,'查看'+bb[0]+'分时图！')
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            msg=f.read()
            f.close()
            exec(msg)
        except Exception as e:
            g.status.text(1,'')
            g.status.text(2,'用户代码出错:'+str(e))
            tprint('用户代码出错:'+str(e)+'\n','red')

def F10():
    item = tb2.tree.selection()[0]        
    aa=tb2.tree.item(item, "values")
    bb=list(aa)
    g.stock=bb[0]
    g.mstock=bb[0]
    g.vtitle=bb[1]
    g.gmarket=1
    stock.set(g.stock)
    try:
        filename= '../../../Downloads/xb2e/view/F10窗口.py'
        g.status.text(2,'查看'+bb[0]+'  F10信息！')
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        msg=f.read()
        f.close()
        exec(msg)
    except Exception as e:
        g.status.text(1,'')
        g.status.text(2,'用户代码出错:'+str(e))
        tprint('用户代码出错:'+str(e)+'\n','red')

def zxg():
    global tb1,tb2,tb3,tb4,tb5
    item = tb2.tree.selection()[0]        
    aa=tb2.tree.item(item, "values")
    bb=list(aa)
    g.stock=bb[0]
    g.mstock=bb[0]
    g.vtitle=bb[1]
    g.gmarket=1
    g.zxg.append([g.gmarket,g.stock])
    cd=get_szcode()
    cd2=get_shcode()
    cd=cd.append(cd2)
    cd=cd.reset_index(level=None, drop=True ,col_level=0, col_fill='')    
    cds={}
    for i in range(len(cd)):
        cds[(cd.market[i],cd.code[i])]=cd.name[i]
    g.names=cds
    df=htdx.get_hq2(g.zxg)
    df=htdx.get_hq2(g.zxg)
    df['zd']=df['price']-df['last_close']  #涨跌
    df['zdf1']=df['zd']*100/df['last_close']  #涨跌幅
    df['vol']=df['vol']/10000
    df=df.round(2)  #改变符点数小数点后2位
    df['zdf']=df['zdf1'].astype(str)+'%'
    df['code2']=['0'*(6-len(x)) + x for x in df.code.astype(str)]
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=cds[(df.loc[i,'market'],df.loc[i,'code2'])]
    df.to_csv('./data/hq.csv' , encoding= 'gbk')    
    df=df[['code','name','zdf','price','zd','bid1','ask1','vol',\
           'high','open','low','last_close','market']]
    df.rename(columns={'code':'代码', 'name':'名称','zdf':'涨幅',\
                       'price':'现价','zd':'涨跌','bid1':'买价',\
                       'ask1':'卖价','vol':'总量(万)','open':'今开',\
                       'high':'最高','low':'最低','last_close':'昨收',\
                       'market':'市场'},\
                        inplace = True)

    tb5.clear()    
    tb5.load_df(df) #把变量df的数据显示到表格中
    tb5.brush()  #用2种底色交替显示表格    
            
# 创建弹出菜单
menubar=tk.Menu(tb.tree)
toolbarName2 = ('日线图','分时图','F10信息','加入自选股')
toolbarCommand2 = (rxt,fst,F10,zxg)
def addPopButton(name,command):
    for (toolname ,toolcom) in zip(name,command):
        menubar.add_command(label=toolname,command=toolcom)

def pop(event):
    # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
    menubar.post(event.x_root,event.y_root)

addPopButton(toolbarName2,toolbarCommand2) #创建弹出菜单
tb2.tree.bind("<Button-3>",pop)

#深圳股票行情
def rxt2():
    ds=date_s.get()
    de=date_e.get()
    g.gtype=g.vbook.get()
    g.sday=ds.strip()
    g.eday=de.strip()
    item =tb4.tree.selection()[0]
    aa=tb4.tree.item(item, "values")
    bb=list(aa)        
    #if bb[0][0:1]=='0' or bb[0][0:1]=='3':
    g.stock=bb[0] 
    g.vtitle=bb[1]
    stock.set(g.stock)
    g.gmarket=0
    df3=htdx.get_k_data2(g.stock,g.sday,g.eday)
    if g.tab3!=None:
        g.tabControl.forget(g.tab3)
        g.tab3=None
    
    #用户自建新画面
    g.tab3 = tk.Frame(g.tabControl)
    g.tabControl.add(g.tab3, text='日线图') 
    g.tabControl.select(g.tab3)
    axview3x(g.tab3,df3,t=g.stock+' '+g.stock_names[g.stock],n=2,f1='VOL',f2=g.gtype)
    g.tabControl.select(g.tab3)
    g.tabs=3
        
    
def fst2():
    ds=date_s.get()
    de=date_e.get()
    item = tb4.tree.selection()[0]        
    aa=tb4.tree.item(item, "values")
    bb=list(aa)
    #if bb[0][0:1]=='0' or bb[0][0:1]=='3':
    g.stock=bb[0]
    g.mstock=bb[0]
    g.vtitle=bb[1]
    stock.set(g.stock)
    g.gmarket=0
    try:
        filename= '../../../Downloads/xb2e/view/分时图.py'
        g.status.text(2,'查看'+bb[0]+'分时图！')
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        msg=f.read()
        f.close()
        exec(msg)
    except Exception as e:
        g.status.text(1,'')
        g.status.text(2,'用户代码出错:'+str(e))
        tprint('用户代码出错:'+str(e)+'\n','red')

def F10b():
    item = tb4.tree.selection()[0]        
    aa=tb4.tree.item(item, "values")
    bb=list(aa)

    g.stock=bb[0]
    g.mstock=bb[0]
    g.vtitle=bb[1]
    g.gmarket=1
    stock.set(g.stock)
    try:
        filename= '../../../Downloads/xb2e/view/F10窗口.py'
        g.status.text(2,'查看'+bb[0]+'  F10信息！')
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        msg=f.read()
        f.close()
        exec(msg)
    except Exception as e:
        g.status.text(1,'')
        g.status.text(2,'用户代码出错:'+str(e))
        tprint('用户代码出错:'+str(e)+'\n','red')


def zxg2():
    global tb1,tb2,tb3,tb4,tb5
    item = tb4.tree.selection()[0]        
    aa=tb4.tree.item(item, "values")
    bb=list(aa)
    g.stock=bb[0]
    g.mstock=bb[0]
    g.vtitle=bb[1]
    g.gmarket=0
    g.zxg.append([g.gmarket,g.stock])
    cd=get_szcode()
    cd2=get_shcode()
    cd=cd.append(cd2)
    cd=cd.reset_index(level=None, drop=True ,col_level=0, col_fill='')    
    cds={}
    for i in range(len(cd)):
        cds[(cd.market[i],cd.code[i])]=cd.name[i]
    g.names=cds
    df=htdx.get_hq2(g.zxg)
    df=htdx.get_hq2(g.zxg)
    df['zd']=df['price']-df['last_close']  #涨跌
    df['zdf1']=df['zd']*100/df['last_close']  #涨跌幅
    df['vol']=df['vol']/10000
    df=df.round(2)  #改变符点数小数点后2位
    df['zdf']=df['zdf1'].astype(str)+'%'
    df['code2']=['0'*(6-len(x)) + x for x in df.code.astype(str)]
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=cds[(df.loc[i,'market'],df.loc[i,'code2'])]
    df.to_csv('./data/hq.csv' , encoding= 'gbk')    
    df=df[['code','name','zdf','price','zd','bid1','ask1','vol',\
           'high','open','low','last_close','market']]
    df.rename(columns={'code':'代码', 'name':'名称','zdf':'涨幅',\
                       'price':'现价','zd':'涨跌','bid1':'买价',\
                       'ask1':'卖价','vol':'总量(万)','open':'今开',\
                       'high':'最高','low':'最低','last_close':'昨收',\
                       'market':'市场'},\
                        inplace = True)

    tb5.clear()    
    tb5.load_df(df) #把变量df的数据显示到表格中
    tb5.brush()  #用2种底色交替显示表格    



# 创建弹出菜单
menubar2=tk.Menu(tb4.tree)
toolbarName3 = ('日线图','分时图','F10信息','加入自选股')
toolbarCommand3 = (rxt2,fst2,F10b,zxg2)
def addPopButton3(name,command):
    for (toolname ,toolcom) in zip(name,command):
        menubar2.add_command(label=toolname,command=toolcom)

def pop3(event):
    # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
    menubar2.post(event.x_root,event.y_root)

addPopButton3(toolbarName3,toolbarCommand3) #创建弹出菜单
tb4.tree.bind("<Button-3>",pop3)

def rxt5():
    ds=date_s.get()
    de=date_e.get()
    g.gtype=g.vbook.get()
    g.sday=ds.strip()
    g.eday=de.strip()
    item =tb5.tree.selection()[0]
    aa=tb5.tree.item(item, "values")
    bb=list(aa)        
    g.stock=bb[0] 
    g.gmarket=int(bb[12])
    stock.set(g.stock)
    g.vtitle=bb[1]
    df3=htdx.get_k_data2(g.stock,g.sday,g.eday)
    if g.tab3!=None:
        g.tabControl.forget(g.tab3)
        g.tab3=None
    
    #用户自建新画面
    g.tab3 = tk.Frame(g.tabControl)
    g.tabControl.add(g.tab3, text='日线图') 
    g.tabControl.select(g.tab3)
    hpv.axview3x(g.tab3,df3,t=g.stock+' '+g.stock_names[g.stock],n=2,f1='VOL',f2=g.gtype)
    g.tabControl.select(g.tab3)
    g.tabs=3
    
    
def fst5():
#    ds=date_s.get()
#    de=date_e.get()
    item = tb5.tree.selection()[0]        
    aa=tb5.tree.item(item, "values")
    bb=list(aa)
    g.stock=bb[0]
    g.mstock=bb[0]
    g.vtitle=bb[1]
    g.gmarket=int(bb[12])
    stock.set(g.stock)
    try:
        filename= '../../../Downloads/xb2e/view/分时图.py'
        g.status.text(2,'查看'+bb[0]+'分时图！')
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        msg=f.read()
        f.close()
        exec(msg)
    except Exception as e:
        g.status.text(1,'')
        g.status.text(2,'用户代码出错:'+str(e))
        tprint('用户代码出错:'+str(e)+'\n','red')

def F105():
    item = tb5.tree.selection()[0]        
    aa=tb5.tree.item(item, "values")
    bb=list(aa)
    g.stock=bb[0]
    g.mstock=bb[0]
    g.vtitle=bb[1]
    g.gmarket=int(bb[12])
    stock.set(g.stock)
    try:
        filename= '../../../Downloads/xb2e/view/F10窗口.py'
        g.status.text(2,'查看'+bb[0]+'  F10信息！')
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        msg=f.read()
        f.close()
        exec(msg)
    except Exception as e:
        g.status.text(1,'')
        g.status.text(2,'用户代码出错:'+str(e))
        tprint('用户代码出错:'+str(e)+'\n','red')
        
def zxg5():
    global tb1,tb2,tb3,tb4,tb5
    item = tb5.tree.selection()[0]        
    aa=tb5.tree.item(item, "values")
    bb=list(aa)
    g.stock=bb[0]
    g.mstock=bb[0]
    g.vtitle=bb[1]
    g.gmarket=int(bb[12])
    g.zxg.remove([g.gmarket,g.stock])
    cd=get_szcode()
    cd2=get_shcode()
    cd=cd.append(cd2)
    cd=cd.reset_index(level=None, drop=True ,col_level=0, col_fill='')    
    cds={}
    for i in range(len(cd)):
        cds[(cd.market[i],cd.code[i])]=cd.name[i]
    g.names=cds
    df=htdx.get_hq2(g.zxg)
    df=htdx.get_hq2(g.zxg)
    df['zd']=df['price']-df['last_close']  #涨跌
    df['zdf1']=df['zd']*100/df['last_close']  #涨跌幅
    df['vol']=df['vol']/10000
    df=df.round(2)  #改变符点数小数点后2位
    df['zdf']=df['zdf1'].astype(str)+'%'
    df['code2']=['0'*(6-len(x)) + x for x in df.code.astype(str)]
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=cds[(df.loc[i,'market'],df.loc[i,'code2'])]
    df.to_csv('./data/hq.csv' , encoding= 'gbk')    
    df=df[['code','name','zdf','price','zd','bid1','ask1','vol',\
           'high','open','low','last_close','market']]
    df.rename(columns={'code':'代码', 'name':'名称','zdf':'涨幅',\
                       'price':'现价','zd':'涨跌','bid1':'买价',\
                       'ask1':'卖价','vol':'总量(万)','open':'今开',\
                       'high':'最高','low':'最低','last_close':'昨收',\
                       'market':'市场'},\
                        inplace = True)

    tb5.clear()    
    tb5.load_df(df) #把变量df的数据显示到表格中
    tb5.brush()  #用2种底色交替显示表格    
# 创建弹出菜单
menubar5=tk.Menu(tb5.tree)
toolbarName5 = ('日线图','分时图','F10信息','删除自选股')
toolbarCommand5 = (rxt5,fst5,F105,zxg5)
def addPopButton5(name,command):
    for (toolname ,toolcom) in zip(name,command):
        menubar5.add_command(label=toolname,command=toolcom)

def pop5(event):
    # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
    menubar5.post(event.x_root,event.y_root)

addPopButton5(toolbarName5,toolbarCommand5) #创建弹出菜单
tb5.tree.bind("<Button-3>",pop5)

#-----------------------------------
#表格6
def rxt6():
    ds=date_s.get()
    de=date_e.get()
    g.gtype=g.vbook.get()
    g.sday=ds.strip()
    g.eday=de.strip()
    item =tb6.tree.selection()[0]
    aa=tb6.tree.item(item, "values")
    bb=list(aa)        
    g.stock=bb[2] 
    g.vtitle=bb[3]
    stock.set(g.stock)
    g.gmarket=htdx.get_market(g.stock)
    df3=htdx.get_k_data2(g.stock,g.sday,g.eday)
    if g.tab3!=None:
        g.tabControl.forget(g.tab3)
        g.tab3=None
    
    #用户自建新画面
    g.tab3 = tk.Frame(g.tabControl)
    g.tabControl.add(g.tab3, text='日线图') 
    g.tabControl.select(g.tab3)
    axview3x(g.tab3,df3,t=g.stock+' '+g.stock_names[g.stock],n=2,f1='VOL',f2=g.gtype)
    g.tabControl.select(g.tab3)
    g.tabs=3
        
    
def fst6():
    ds=date_s.get()
    de=date_e.get()
    item = tb6.tree.selection()[0]        
    aa=tb6.tree.item(item, "values")
    bb=list(aa)
    g.stock=bb[2] 
    g.vtitle=bb[3]
    stock.set(g.stock)
    g.gmarket=htdx.get_market(g.stock)
    try:
        filename= '../../../Downloads/xb2e/view/分时图.py'
        g.status.text(2,'查看'+bb[0]+'分时图！')
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        msg=f.read()
        f.close()
        exec(msg)
    except Exception as e:
        g.status.text(1,'')
        g.status.text(2,'用户代码出错:'+str(e))
        tprint('用户代码出错:'+str(e)+'\n','red')

def F10b6():
    item = tb6.tree.selection()[0]        
    aa=tb6.tree.item(item, "values")
    bb=list(aa)

    g.stock=bb[2] 
    g.vtitle=bb[3]
    stock.set(g.stock)
    g.gmarket=htdx.get_market(g.stock)
    try:
        filename= '../../../Downloads/xb2e/view/F10窗口.py'
        g.status.text(2,'查看'+bb[0]+'  F10信息！')
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        msg=f.read()
        f.close()
        exec(msg)
    except Exception as e:
        g.status.text(1,'')
        g.status.text(2,'用户代码出错:'+str(e))
        tprint('用户代码出错:'+str(e)+'\n','red')


def zxg6():
    global tb1,tb2,tb3,tb4,tb5
    item = tb6.tree.selection()[0]        
    aa=tb6.tree.item(item, "values")
    bb=list(aa)
    g.stock=bb[2] 
    g.vtitle=bb[3]
    stock.set(g.stock)
    g.gmarket=htdx.get_market(g.stock)
    g.zxg.append([g.gmarket,g.stock])
    cd=get_szcode()
    cd2=get_shcode()
    cd=cd.append(cd2)
    cd=cd.reset_index(level=None, drop=True ,col_level=0, col_fill='')    
    cds={}
    for i in range(len(cd)):
        cds[(cd.market[i],cd.code[i])]=cd.name[i]
    g.names=cds
    df=htdx.get_hq2(g.zxg)
    df=htdx.get_hq2(g.zxg)
    df['zd']=df['price']-df['last_close']  #涨跌
    df['zdf1']=df['zd']*100/df['last_close']  #涨跌幅
    df['vol']=df['vol']/10000
    df=df.round(2)  #改变符点数小数点后2位
    df['zdf']=df['zdf1'].astype(str)+'%'
    df['code2']=['0'*(6-len(x)) + x for x in df.code.astype(str)]
    df['name']=''
    for i in range(len(df)):
        df.loc[i,'name']=cds[(df.loc[i,'market'],df.loc[i,'code2'])]
    df.to_csv('./data/hq.csv' , encoding= 'gbk')    
    df=df[['code','name','zdf','price','zd','bid1','ask1','vol',\
           'high','open','low','last_close','market']]
    df.rename(columns={'code':'代码', 'name':'名称','zdf':'涨幅',\
                       'price':'现价','zd':'涨跌','bid1':'买价',\
                       'ask1':'卖价','vol':'总量(万)','open':'今开',\
                       'high':'最高','low':'最低','last_close':'昨收',\
                       'market':'市场'},\
                        inplace = True)

    tb5.clear()    
    tb5.load_df(df) #把变量df的数据显示到表格中
    tb5.brush()  #用2种底色交替显示表格    



# 创建弹出菜单
menubar6=tk.Menu(tb6.tree)
toolbarName6= ('日线图','分时图','F10信息','加入自选股')
toolbarCommand6 = (rxt6,fst6,F10b6,zxg6)
def addPopButton6(name,command):
    for (toolname ,toolcom) in zip(name,command):
        menubar6.add_command(label=toolname,command=toolcom)

def pop6(event):
    # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
    menubar6.post(event.x_root,event.y_root)

addPopButton6(toolbarName6,toolbarCommand6) #创建弹出菜单
tb6.tree.bind("<Button-3>",pop6)

#-----------------
#小白培训视频第2讲知识点
##把window划分为4个子容器,在不同子容器中显示不同股票K线图
#v=hpv.view4(tab3)
#v.pack(fill=tk.BOTH, expand=1)
def jsfx():
    ds='2018-01-01'  #行情开始日期
    de=time.strftime('%Y-%m-%d',time.localtime(time.time()))  #行情结束日期
    df2a=htdx.get_k_data2(g.stock,ds,de)
    # 三指标图
    hpv.axview3x(tab3,df2a,g.stock+' '+g.stock_names[g.stock])


htk.thread_it(jsfx())

myedit2=htk.useredit(tab4)
myedit2.pack()

#------------------------------------------------------
#用户自建新画面
#g.tab5 = tk.Frame(g.tabControl)
#g.tabControl.add(g.tab5, text='策略回测') 
#g.tabControl.select(g.tab5)

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

#------------------------------------------------------

def bt1():
    tabControl.select(tab1)
    print(1)

def bt2():
    tabControl.select(tab2)
    print(2)

def bt3():
    tabControl.select(tab3)
    print(3)

def bt4():
    tabControl.select(tab4)
    print(4)

def bt5():
    tabControl.select(tab5)


toolsbar.config(0,command=bt1)
toolsbar.config(1,command=bt2)
toolsbar.config(2,command=bt3)
toolsbar.config(3,command=bt4)
toolsbar.config(4,command=bt5)


#g.ttmsg.delete(1.0,tk.END)  #清空信息框
#tprint('用户输出信息框\n')
#-----------------
def fun_timer2():
    global timer_interval
    global timer
    def fun_timer():
        global timer
        global timer_interval
        dt=time.strftime('  %Y-%m-%d  %H:%M:%S',time.localtime(time.time()))
        status.text(1,dt) #在状态栏2输出信息
        if timer_interval>0:
            timer = threading.Timer(timer_interval, fun_timer)
            timer.start()  
    if timer_interval>0:
        timer = threading.Timer(1, fun_timer)
        timer.start()

  
htk.thread_it(fun_timer2())  ##用多线程启动定时器

def udestroy():
    global timer
    timer.cancel()
    htdx.disconnect()
    #把结果保存到文件中
    f = open('../../../Downloads/xb2e/data/zxg.dat', 'wb')
    pt=pickle.dumps(g.zxg,0)
    f.write(pt)
    f.close()  

root.udestroy=udestroy


#try:
filename= '../../../Downloads/xb2e/view/F10窗口.py'
f = open(filename,'r',encoding='utf-8',errors='ignore')
msg=f.read()
f.close()
exec(msg)
#except Exception as e:
#    tprint('用户代码出错:'+str(e)+'\n')
g.tabControl.select(g.tab1)  #选择面板

root.mainloop()  	#进入Tkinter消息循环


