# -*- coding: utf-8 -*-
"""
#功能：Python小白用tkinter做可视化开发工具
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标,小白量化
#开始设计日期: 2019-03-01
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2019年3月1日
#主程序：HP_main.py
"""
import sys  
import os
import time
import threading
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import  tkinter  as  tk   #导入Tkinter
import  tkinter.ttk  as  ttk   #导入Tkinter.ttk
import  tkinter.tix  as  tix   #导入Tkinter.tix
from tkinter.tix import Tk, ScrolledText
from tkinter.tix import *
from tkinter import Frame,messagebox
import PIL
import HP_global as g 
#from HP_set import *
from threading import Timer
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from tkinter import scrolledtext  #装载scrolledtext模块
from tkinter.messagebox import *
from tkinter.filedialog import *
from HP_formula import *    #使用HP_formula公式基本函数库

from PIL import Image, ImageTk, ImageDraw, ImageFont,ImageGrab

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class ScrolledText(scrolledtext.ScrolledText):
    def __init__(self, master=None, **kw):
        scrolledtext.ScrolledText.__init__(self, master, **kw)

#多线程启动函数
def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    #t.setDaemon(True)
    # 启动
    t.start()


def RGB(color):
    r=eval('0x'+color[1:3])
    g=eval('0x'+color[3:5])
    b=eval('0x'+color[5:7])
    return r,g,b
    
def drawFont (im,x,y,txt,size=30,r=255,g=255,b=255): #显示汉字
    #im图像对象,坐标(x,y),txt文字,size字体大小;颜色r,j,b=0-255
    font = ImageFont.truetype("simfang.ttf", size)
	#font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simfang.ttf", 40)    
    draw = ImageDraw.Draw(im)
    draw.ink = r + 256*g + 256*256*b
    draw.text((x, y), txt, font=font)

def drawFont2 (im,x,y,txt,size=30,r=255,g=255,b=255): #显示汉字
    #im图像对象,坐标(x,y),txt文字,size字体大小;颜色r,j,b=0-255
    font = ImageFont.truetype("SIMLI.TTF", size)
	#font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simfang.ttf", 40)    
    draw = ImageDraw.Draw(im)
    draw.ink = r + 256*g + 256*256*b
    draw.text((x, y), txt, font=font)

def drawFont3(im,x,y,txt,size=30,r=255,g=255,b=255): #显示汉字
    #im图像对象,坐标(x,y),txt文字,size字体大小;颜色r,j,b=0-255
    font = ImageFont.truetype("STXINGKA.TTF", size)
	#font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simfang.ttf", 40)    
    draw = ImageDraw.Draw(im)
    draw.ink = r + 256*g + 256*256*b
    draw.text((x, y), txt, font=font)


#移动窗口到屏幕中央       
def setCenter(root,w,h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int( (ws/2) - (w/2) )
    y = int( (hs/2) - (h/2) )
    root.geometry('{}x{}+{}+{}'.format(w, h, x, y))

#移动窗口到屏幕坐标x,y       
def setPlace(root,x, y,w,h):
    root.geometry('{}x{}+{}+{}'.format(w, h, x, y))

#显示窗口ico图标
def showIco(root,Ico):
    root.iconbitmap(Ico)    

#是否禁止修改窗口大小
def reSizable(root,x,y):
    root.resizable(x, y)   #是否禁止修改窗口大小

def resize(w, h, w_box, h_box, pil_image):  
  ''' 
  对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例 
  '''  
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
  f2 = 1.0*h_box/h  
  factor = min([f1, f2])  
  #print(f1, f2, factor) # test  
  # use best down-sizing filter  
  width = int(w*factor)  
  height = int(h*factor)  
  return pil_image.resize((width, height), Image.ANTIALIAS)      
        
    
def imgresize(w, h, w_box, h_box, pil_image):  
  ''' 
  resize a pil_image object so it will fit into 
  a box of size w_box times h_box, but retain aspect ratio 
  对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例 
  '''  
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
  f2 = 1.0*h_box/h
#  factor = min([f1, f2])  
  #print(f1, f2, factor) # test  
  # use best down-sizing filter  
#  width = int(w*factor)  
#  height = int(h*factor)  
  width = int(w*f1)  
  height = int(h*f2)  
  return pil_image.resize((width, height), PIL.Image.ANTIALIAS)  

# 主窗
class MainWindow(tix.Tk):
    def __init__(self, title='主窗口',x=0,y=0,w=800, h=600,picture='',zoom=True,center=True,bg=''):
        super().__init__()
        self.width=w
        self.height=h
        self.x=x
        self.y=y
        self.title(title)
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        self.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False
        self.iconbitmap('ico/APS0.ico')   
        self.bind("<Configure>", self.Callback)  #Motion事件表示当鼠标进入组件时，就会响应这个事件
        self.attributes('-topmost', 0)
        self.picture=picture
        self.bg=bg
        self.pil_image=None
        self.pil_image2=None
        self.zoom=zoom
        self.tk_image=None
        self.backimg=None
        self.uinit=None
        self.udestroy=None
        self.refresh()
        if center==True:
            self.SetCenter()
            self.update()
        self.protocol("WM_DELETE_WINDOW", self.callback_quit)

    def userfun(self):
        if self.uinit !=None:
            self.uinit()

    def userfun2(self):
        if self.udestroy !=None:
            self.udestroy()

    def refresh(self):
        if self.picture!='':
            self.pil_image=PIL.Image.open(self.picture)
            self.pil_image2=self.pil_image
            if self.zoom:
                w2, h2 = self.pil_image.size  
                self.pil_image2=imgresize(w2,h2,self.width,self.height, self.pil_image)
            self.tk_image =PIL.ImageTk.PhotoImage(self.pil_image2)
            self.backimg=tk.Label(self,image=self.tk_image)
            self.backimg.place(x=0, y=0, relwidth=1, relheight=1,bordermode=tk.OUTSIDE)
        elif self.bg!='':
            self.backimg=tk.Label(self,bg=self.bg)
            self.backimg.place(x=0, y=0, relwidth=1, relheight=1,bordermode=tk.OUTSIDE)
    
    def save(self,filename = 'temp.png',wr=16,hr=46):
        '''
        save(filename = 'temp.png',wr=16,hr=46)
        wr宽度修正
        hr高度修正,工具栏和状态栏影响高度
        '''
        im = PIL.ImageGrab.grab((self.x,self.y,self.x+self.width+wr,self.y+self.height+hr))
        im.save(filename)
        im=im.resize((32,32))
        im.save('temp32.png')
        im.close()
        
    def Destroy(self):
        #销毁应用程序窗口
        self.userfun2()
        self.destroy()   

    def Overturn(self):
        self.update_idletasks()
        self.overrideredirect(self.flag)
        self.flag=not self.flag #switch

    def size(self,w,h):
        self.width=w
        self.height=h       
        self.geometry('{}x{}'.format(self.width,self.height))  #改变窗口大小

    #移动窗口到屏幕中央       
    def SetCenter(self):
        #print('SetCenter')
        ws = self.winfo_screenwidth()  #获取屏幕宽度
        hs = self.winfo_screenheight() #获取屏幕高度
        self.width=self.winfo_width()   #获取窗口宽度（单位：像素）
        self.height=self.winfo_height()  #获取窗口高度（单位：像素）
        self.x = int( (ws/2) - (self.width/2) )
        self.y = int( (hs/2) - (self.height/2) )
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

    def OnTop(self):
        self.attributes('-topmost', 1)
        self.attributes('-topmost', 0)

    def AlwaysOnTop(self):
        self.attributes('-topmost', 1)
    
    #----------------------------------------------------------------------    
    def hide(self):
        """"""
        self.root.withdraw()
    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()

    #移动窗口到屏幕坐标x,y
    def setPlace(self,x, y,w=0,h=0):
        if (w==0  or  h==0):
            w = self.winfo_width()   #获取窗口宽度（单位：像素）
            h = self.winfo_height()  #获取窗口高度（单位：像素）
        self.width=w
        self.height=h
        self.x=x
        self.y=y        
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
    
    
    
    def Callback(self, event):
        self.width=self.winfo_width()   #获取窗口宽度（单位：像素）
        self.height=self.winfo_height()  #获取窗口高度（单位：像素）
        self.x=self.winfo_x()  #获取窗口x坐标（单位：像素）
        self.y=self.winfo_y()  #获取窗口y坐标（单位：像素）
        if self.picture!='':
            if self.zoom:
                #self.pil_image=PIL.Image.open(self.picture)
                w2, h2 = self.pil_image.size  
                self.pil_image2=imgresize(w2,h2,self.width,self.height, self.pil_image)
                self.tk_image = PIL.ImageTk.PhotoImage(self.pil_image2)
                self.backimg['image']=self.tk_image
            self.backimg.place(x=0, y=0, relwidth=1, relheight=1,bordermode=tk.OUTSIDE)

    def callback_quit(self):
        #messagebox.showwarning('提示','程序结束')
        ans=messagebox.askyesno('提示', '要程序结束吗?') #确定/取消，返回值True/False
        if ans==True:
            self.Destroy()  


#=================================================================== 
class Form:
    def __init__(self, root, title='新Form',x=0,y=0,w=300, h=200,picture='',zoom=True,center=True):
        self.width=w
        self.height=h
        self.x=x
        self.y=y
        self.top = tk.Toplevel(root, width=w, height=h)
        self.top.title(title)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False
        self.top.iconbitmap('ico/APS0.ico')   
        self.top.bind("<Configure>", self.Callback)  #Motion事件表示当鼠标进入组件时，就会响应这个事件
        self.top.attributes('-topmost', 0)
        self.picture=picture
        self.pil_image=None
        self.pil_image2=None
        self.zoom=zoom
        self.tk_image=None
        self.backimg=None
        self.refresh()
        if center:
            self.SetCenter()


    def refresh(self):
        if self.picture!='':
            self.pil_image=PIL.Image.open(self.picture)
            self.pil_image2=self.pil_image
            if self.zoom:
                w2, h2 = self.pil_image.size  
                self.pil_image2=imgresize(w2,h2,self.width,self.height, self.pil_image)
            self.tk_image = PIL.ImageTk.PhotoImage(self.pil_image2)
            self.backimg=tk.Label(self.top,image=self.tk_image)
            self.backimg.place(x=0, y=0, relwidth=1, relheight=1,bordermode=tk.OUTSIDE)
    
    def save(self,filename = 'temp.png',wr=16,hr=46):
        '''
        save(filename = 'temp.png',wr=16,hr=46)
        wr宽度修正
        hr高度修正,工具栏和状态栏影响高度
        '''
        im = PIL.ImageGrab.grab((self.x,self.y,self.x+self.width+wr,self.y+self.height+hr))
        im.save(filename)
        im=im.resize((32,32))
        im.save('temp32.png')
        im.close()
        
        

    
    def Destroy(self):
        #销毁应用程序窗口
        self.top.destroy()   

    def Overturn(self):
        self.top.update_idletasks()
        self.top.overrideredirect(self.flag)
        self.top.flag=not self.flag #switch

    #移动窗口到屏幕中央       
    def SetCenter(self):
        ws = g.root.winfo_screenwidth()  #获取屏幕宽度
        hs = g.root.winfo_screenheight() #获取屏幕高度
        self.width=self.top.winfo_width()   #获取窗口宽度（单位：像素）
        self.height=self.top.winfo_height()  #获取窗口高度（单位：像素）
        self.x = int( (ws/2) - (self.width/2) )
        self.y = int( (hs/2) - (self.height/2) )
        self.top.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

    def OnTop(self):
        self.top.attributes('-topmost', 1)
        self.top.attributes('-topmost', 0)

    def AlwaysOnTop(self):
        self.top.attributes('-topmost', 1)
    
    #移动窗口到屏幕坐标x,y       
    def SetPlace(self,x, y,w,h):
        self.width=w
        self.height=h
        self.x=x
        self.y=y        
        self.top.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
    
    def Callback(self, event):
        self.width=self.top.winfo_width()   #获取窗口宽度（单位：像素）
        self.height=self.top.winfo_height()  #获取窗口高度（单位：像素）
        self.x=self.top.winfo_x()  #获取窗口x坐标（单位：像素）
        self.y=self.top.winfo_y()  #获取窗口y坐标（单位：像素）
        if self.picture!='':
            if self.zoom:
                #self.pil_image=PIL.Image.open(self.picture)
                w2, h2 = self.pil_image.size  
                self.pil_image2=imgresize(w2,h2,self.width,self.height, self.pil_image)
                self.tk_image = PIL.ImageTk.PhotoImage(self.pil_image2)
                self.backimg['image']=self.tk_image
            self.backimg.place(x=0, y=0, relwidth=1, relheight=1,bordermode=tk.OUTSIDE)
        #self.save()
        #print("当前位置：", self.x, self.y)
        #print("窗口大小：", self.width, self.height)
#------------------------------------------------------------------------------------

#定义我的窗口基类
class myWindow:
    def __init__(self, root, myTitle,w=300, h=200):
        self.width=w
        self.height=h
        self.top = tk.Toplevel(root, width=w, height=h)
        self.top.title(myTitle)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False

    def destroy(self):
        #销毁应用程序窗口
        self.top.destroy()   

    def overturn(self):
        self.top.update_idletasks()
        self.top.overrideredirect(self.flag)
        self.flag=not self.flag #switch

    #移动窗口到屏幕中央       
    def setCenter(self,w,h):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int( (ws/2) - (w/2) )
        y = int( (hs/2) - (h/2) )
        self.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    
    #移动窗口到屏幕坐标x,y       
    def setPlace(self,x, y,w,h):
        self.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    
    
    #显示窗口ico图标
    def showIco(self,Ico):
        self.iconbitmap(Ico)    
    
    #是否禁止修改窗口大小
    def reSizable(self,x,y):
        self.resizable(x, y)   #是否禁止修改窗口大小




###############
#     1       #
###############
#     2       #
###############
class view2(Frame): # 继承Frame类  
    def __init__(self, root=None):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.m=2
        self.v=[]
        self.v1=tk.Frame(self)
        self.v2=tk.Frame(self)
        self.v1.pack(side=tk.TOP, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)
        
    def hpack(self):
        self.pack(fill=tk.BOTH, expand=tk.YES)

################
#      #       #
#   1  #   2   #
#      #       #
################
class view2b(Frame): # 继承Frame类  
    def __init__(self, root=None,width=0):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.width=width
        self.m=2
        self.v=[]
        if self.width==0:
            self.v1=tk.Frame(self)
        else:
            self.v1=tk.Frame(self,width=self.width)
        self.v2=tk.Frame(self)
        if self.width==0:
            self.v1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        else:
            self.v1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
            
        self.v2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)

    def hpack(self):
        self.pack(fill=tk.BOTH, expand=tk.YES)

################
#      #       #
#   1  #   2   #
#      #       #
################
class view2c(Frame): # 继承Frame类  
    def __init__(self, root=None,width=300):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.width=width
        self.m=2
        self.v=[]
        self.v1=tk.Frame(self,relief=tk.SUNKEN,bg='blue')
        self.v2=tk.Frame(self,relief=tk.SUNKEN,bg='green',width = self.width)
        self.v1.grid(row = 0, column = 0,sticky=tk.NSEW,columnspan=3)
        self.v2.grid(row = 0, column = 4,sticky=tk.NSEW,columnspan=1)
        self.v.append(self.v1)
        self.v.append(self.v2)

    def hpack(self):
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.pack(fill=tk.BOTH, expand=tk.YES)
        
################
#      #       #
#   1  #   2   #
#      #       #
################
class view2d(Frame): # 继承Frame类  
    def __init__(self, root=None,scale=0.5):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.scale=scale
        #self.hpack()
        self.width=800   #获取窗口宽度（单位：像素）
        self.height=600  #获取窗口高度（单位：像素）
        self.width1=int(self.width*self.scale)
        self.width2=int(self.width*(1-self.scale))
        self.m=2
        self.v=[]
        self.v1=tk.Frame(self,relief=tk.SUNKEN,bg='blue',width =self.width1 )
        self.v2=tk.Frame(self,relief=tk.SUNKEN,bg='green',width=self.width2 )
        self.v1.pack(side=tk.LEFT,fill=tk.Y, expand=tk.YES)
        self.v2.pack(side=tk.RIGHT,fill=tk.Y, expand=tk.YES)
#        self.v1.grid(row = 0, column = 0,sticky=tk.NSEW,columnspan=1)
#        self.v2.grid(row = 0, column = 1,sticky=tk.NSEW,columnspan=2)
        self.v.append(self.v1)
        self.v.append(self.v2)
        self.bind("<Configure>", self.Callback)  #Motion事件表示当鼠标进入组件时，就会响应这个事件

    def hpack(self):
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.pack(fill=tk.BOTH, expand=tk.YES)
        
    def Callback(self, event):
        self.width=self.winfo_width()   #获取窗口宽度（单位：像素）
        self.height=self.winfo_height()  #获取窗口高度（单位：像素）
        self.width1=int(self.width*self.scale)
        self.width2=int(self.width*(1-self.scale))
        self.v1['width']=self.width1
        self.v2['width']=self.width2
        self.v1.pack(side=tk.LEFT,fill=tk.Y, expand=tk.YES)
        self.v2.pack(side=tk.RIGHT,fill=tk.Y, expand=tk.YES)
        self.root.update()
        
        
        
###############
#  1  #   2   #
###############
#     3       #
###############
class view3(Frame): # 继承Frame类  
    def __init__(self, root=None):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.m=3
        self.v=[]
        self.vm=tk.Frame(self)
        self.v1=tk.Frame(self.vm)
        self.v2=tk.Frame(self.vm)
        self.v3=tk.Frame(self)
        
        self.vm.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.v3.pack(side=tk.BOTTOM,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)        
        self.v1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v2.pack(side=tk.RIGHT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)
        self.v.append(self.v3)

###############
#     1       #
###############
#   2  #  3  #
##############
class view3b(Frame): # 继承Frame类  
    def __init__(self, root=None):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.m=3
        self.v=[]
        self.v1=tk.Frame(self)
        self.vm=tk.Frame(self)
        self.v2=tk.Frame(self.vm)
        self.v3=tk.Frame(self.vm)
        self.v1.pack(side=tk.TOP, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.vm.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.v2.pack(side=tk.LEFT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v3.pack(side=tk.RIGHT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)
        self.v.append(self.v3)

###############
#  1  #   2   #
###############
#  3  #   4   #
###############
class view4(Frame): # 继承Frame类  
    def __init__(self, root=None):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.m=4
        self.v=[]
        self.vm1=tk.Frame(self)
        self.vm2=tk.Frame(self)
        self.v1=tk.Frame(self.vm1)
        self.v2=tk.Frame(self.vm1)
        self.v3=tk.Frame(self.vm2)
        self.v4=tk.Frame(self.vm2)
        
        self.vm1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.vm2.pack(side=tk.BOTTOM,expand=1,fill=tk.BOTH)        
        self.v1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v2.pack(side=tk.RIGHT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v3.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v4.pack(side=tk.RIGHT,expand=1,fill=tk.BOTH,ipady=1,pady=1,ipadx=1,padx=1)
        self.v.append(self.v1)
        self.v.append(self.v2)
        self.v.append(self.v3)
        self.v.append(self.v4)

#=================================================================== 
#状态栏
class StatusBar(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='0000').place(x=0, y=0, relwidth=1,bordermode=tk.OUTSIDE)
        self.m=6  #有6个子栏
        self.l=[]
        self.l1 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.CENTER,width=7,text='状态栏',justify=tk.CENTER)
        self.l1.pack(side=tk.LEFT,padx=1,pady=1)
        self.l.append(self.l1)
        self.l2 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,width=20,text='2')
        self.l2.pack(side=tk.LEFT,padx=1,pady=1)
        self.l.append(self.l2)
        self.l3 = tk.Label(self, bd=1, anchor=tk.W,relief=tk.SUNKEN,text='3')
        self.l3.pack(side=tk.LEFT,fill=tk.X)
        self.l.append(self.l3)
        self.l4 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,width=10,text='6')
        self.l4.pack(side=tk.RIGHT,padx=1,pady=1)
        self.l5 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,width=10,text='5')
        self.l5.pack(side=tk.RIGHT,padx=1,pady=1)
        self.l6 = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,width=10,text='4')
        self.l6.pack(side=tk.RIGHT,padx=2,pady=1)
        self.l.append(self.l6)
        self.l.append(self.l5)
        self.l.append(self.l4)
    
    def text(self,i,t): #输出文字信息
        self.l[i].config(text=t)
        self.l[i].update_idletasks()
        
    def config(self,i,**kargs):  #配置长度 和 颜色
        for x,y in kargs.items():
            if x=='text':
                self.l[i].config(text=y)
            if x=='color':
                self.l[i].config(fg=y)        
            if x=='width':
                self.l[i].config(width=y)        

    def clear(self):  #清除所有信息
        for i in range(0,self.m):
            self.l[i].config(text='')
            self.l[i].update_idletasks()


    def set(self,i, format, *args):   #输出格式信息
        self.l[i].config(text=format % args)
        self.l[i].update_idletasks()

#=================================================================== 
#工具栏（横向）
class ToolsBar(tk.Frame):
    def __init__(self, root,n=3,**kw):
        tk.Frame.__init__(self, root,**kw)
        self.png= PIL.ImageTk.PhotoImage(PIL.Image.open('../../../Downloads/xb2e/ico/python.ico'))
        self.m=n  #有10个子栏
        if self.m>20:
            self.m=20
        if self.m<0:
            self.m=1
            
        self.t=[]
        self.t1 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t2 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t3 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t4 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t5 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t6 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t7 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t8 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t9 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t10 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t11 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t12 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t13 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t14 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t15 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t16 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t17 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t18 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t19 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t20 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')


        
        self.t.append(self.t1)
        self.t.append(self.t2)
        self.t.append(self.t3)    
        self.t.append(self.t4)
        self.t.append(self.t5)
        self.t.append(self.t6)    
        self.t.append(self.t7)
        self.t.append(self.t8)
        self.t.append(self.t9)    
        self.t.append(self.t10)
        self.t.append(self.t11)
        self.t.append(self.t12)
        self.t.append(self.t13)    
        self.t.append(self.t14)
        self.t.append(self.t15)
        self.t.append(self.t16)    
        self.t.append(self.t17)
        self.t.append(self.t18)
        self.t.append(self.t19)    
        self.t.append(self.t20)        
        for i in range(self.m):
            self.t[i].grid(row=0, column=i, padx=1, pady=1, sticky=tk.E)

    def config(self,i,**kargs):  #配置长度 和 颜色
        for x,y in kargs.items():
            if x=='image':
                self.t[i].config(image=y)
            if x=='command':
                self.t[i].config(command=y)
            if x=='color':
                self.t[i].config(fg=y)        
            if x=='width':
                self.t[i].config(width=y)   
#=================================================================== 
#工具栏(纵向)
class ToolsBar2(tk.Frame):
    def __init__(self, root,n=3,**kw):
        tk.Frame.__init__(self, root,**kw)
        #tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,text='0000').place(x=0, y=0, relwidth=1,bordermode=tk.OUTSIDE)
        self.png= PIL.ImageTk.PhotoImage(Image.open('../../../Downloads/xb2e/ico/python.ico'))
        self.m=n  #有10个子栏
        if self.m>20:
            self.m=20
        if self.m<0:
            self.m=1
            
        self.t=[]
        self.t1 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t2 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t3 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t4 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t5 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t6 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t7 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t8 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t9 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t10 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t11 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t12 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t13 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t14 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t15 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t16 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t17 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t18 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t19 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')
        self.t20 = ttk.Button(self, width=20, image=self.png, command=None,cursor='hand2')


        
        self.t.append(self.t1)
        self.t.append(self.t2)
        self.t.append(self.t3)    
        self.t.append(self.t4)
        self.t.append(self.t5)
        self.t.append(self.t6)    
        self.t.append(self.t7)
        self.t.append(self.t8)
        self.t.append(self.t9)    
        self.t.append(self.t10)
        self.t.append(self.t11)
        self.t.append(self.t12)
        self.t.append(self.t13)    
        self.t.append(self.t14)
        self.t.append(self.t15)
        self.t.append(self.t16)    
        self.t.append(self.t17)
        self.t.append(self.t18)
        self.t.append(self.t19)    
        self.t.append(self.t20)        
        for i in range(self.m):
            self.t[i].grid(row=i, column=0, padx=1, pady=1, sticky=tk.E)

    def config(self,i,**kargs):  #配置长度 和 颜色
        for x,y in kargs.items():
            if x=='image':
                self.t[i].config(image=y)
            if x=='command':
                self.t[i].config(command=y)
            if x=='color':
                self.t[i].config(fg=y)        
            if x=='width':
                self.t[i].config(width=y)   


#------------------------------------------------------------------------------------
class WinTools(Form):
    def __init__(self, root, title='横向工具栏WindowToolsBar',x=0, y=0,n=3):
        self.n=n
        self.width=100
        self.height=0
        self.x=0
        self.y=0
        self.top = tk.Toplevel(root, width=self.width, height=self.height)
        self.top.title(title)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False
        self.top.iconbitmap('ico/APS0.ico')   
        self.top.bind("<Configure>", self.Callback)  #Motion事件表示当鼠标进入组件时，就会响应这个事件
        self.top.attributes('-topmost', 0)
        self.init()
        
    def init(self) :
        self.tools=ToolsBar(self.top,self.n)
        self.tools.pack()
        self.top.attributes("-toolwindow", 1)
               
#=================================================================== 
class Tk(tix.Tk):
    def __init__(self, root=None, title='主窗口',w=300, h=200,picture='',zoom=True):
        self.width=w
        self.height=h
        self.x=0
        self.y=0
        self.root=root
        if self.root==None:
            self.root = tk.Tk()
            self.top=self.root
            g.root=self.root
        self.top.title(title)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False
        self.top.iconbitmap('ico/APS0.ico')   
        self.top.bind("<Configure>", self.Callback)  #Motion事件表示当鼠标进入组件时，就会响应这个事件
        self.top.attributes('-topmost', 0)
        self.picture=picture
        self.pil_image=None
        self.pil_image2=None
        self.zoom=zoom
        self.tk_image=None
        self.backimg=None
        self.SetCenter()
        self.refresh()
        #return self.root

    def refresh(self):
        if self.picture!='':
            self.pil_image=PIL.Image.open(self.picture)
            self.pil_image2=self.pil_image
            if self.zoom:
                w2, h2 = self.pil_image.size  
                self.pil_image2=imgresize(w2,h2,self.width,self.height, self.pil_image)
            self.tk_image = PIL.ImageTk.PhotoImage(self.pil_image2)
            self.backimg=tk.Label(self.top,image=self.tk_image)
            self.backimg.place(x=0, y=0, relwidth=1, relheight=1,bordermode=tk.OUTSIDE)
        
    def Destroy(self):
        #销毁应用程序窗口
        self.top.destroy()   

    def Overturn(self):
        self.top.update_idletasks()
        self.top.overrideredirect(self.flag)
        self.top.flag=not self.flag #switch

    #移动窗口到屏幕中央       
    def SetCenter(self):
        ws = g.root.winfo_screenwidth()  #获取屏幕宽度
        hs = g.root.winfo_screenheight() #获取屏幕高度
        self.width=self.top.winfo_width()   #获取窗口宽度（单位：像素）
        self.height=self.top.winfo_height()  #获取窗口高度（单位：像素）
        self.x = int( (ws/2) - (self.width/2) )
        self.y = int( (hs/2) - (self.height/2) )
        self.top.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

    def OnTop(self):
        self.top.attributes('-topmost', 1)
        self.top.attributes('-topmost', 0)

    def AlwaysOnTop(self):
        self.top.attributes('-topmost', 1)
    
    #移动窗口到屏幕坐标x,y       
    def SetPlace(self,x, y,w,h):
        self.width=w
        self.height=h
        self.x=x
        self.y=y        
        self.top.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
    
    def Callback(self, event):
        self.width=self.top.winfo_width()   #获取窗口宽度（单位：像素）
        self.height=self.top.winfo_height()  #获取窗口高度（单位：像素）
        self.x=self.top.winfo_x()  #获取窗口x坐标（单位：像素）
        self.y=self.top.winfo_y()  #获取窗口y坐标（单位：像素）
        if self.picture!='':
            if self.zoom:
                #self.pil_image=PIL.Image.open(self.picture)
                w2, h2 = self.pil_image.size  
                self.pil_image2=imgresize(w2,h2,self.width,self.height, self.pil_image)
                self.tk_image = PIL.ImageTk.PhotoImage(self.pil_image2)
                self.backimg['image']=self.tk_image
            self.backimg.place(x=0, y=0, relwidth=1, relheight=1,bordermode=tk.OUTSIDE)
        #print("当前位置：", self.x, self.y)
        #print("窗口大小：", self.width, self.height)
#------------------------------------------------------------------------------------
class WinTools(Form):
    def __init__(self, root, title='横向工具栏WindowToolsBar',x=0, y=0,n=3):
        self.n=n
        self.width=100
        self.height=0
        self.x=0
        self.y=0
        self.top = tk.Toplevel(root, width=self.width, height=self.height)
        self.top.title(title)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False
        self.top.iconbitmap('ico/APS0.ico')   
        self.top.bind("<Configure>", self.Callback)  #Motion事件表示当鼠标进入组件时，就会响应这个事件
        self.top.attributes('-topmost', 0)
        self.init()
        
    def init(self) :
        self.tools=ToolsBar(self.top,self.n)
        self.tools.pack()
        self.top.attributes("-toolwindow", 1)

#------------------------------------------------------------------------------------
class WinTools2(Form): #纵向工具栏WindowToolsBar
    def __init__(self, root, title='',x=0, y=0,n=3):
        self.n=n
        self.width=100
        self.height=0
        self.x=0
        self.y=0
        self.top = tk.Toplevel(root, width=self.width, height=self.height)
        self.top.title(title)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False
        self.top.iconbitmap('ico/APS0.ico')   
        self.top.bind("<Configure>", self.Callback)  #Motion事件表示当鼠标进入组件时，就会响应这个事件
        self.top.attributes('-topmost', 0)
        self.init()
        
    def init(self) :
        self.tools=ToolsBar2(self.top,self.n)
        self.tools.pack()
        #self.top.overrideredirect(True)
        self.top.attributes("-toolwindow", 1)
        

#------------------------------------------------------------------------------------
###############
#             #
#     1       #
#             #
###############
class view1(Frame): # 继承Frame类  
    def __init__(self, root=None):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.m=1
        self.v=[]
        self.v1=tk.Frame(self)
        self.v.append(self.v1)
        self.hpack()
    
    def hpack(self):
        #self.v1.pack(side=tk.TOP, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.v1.pack(fill=tk.BOTH, expand=tk.YES)


#------------------------------------------------------------------------------------
###############
#             #
#     1       #
#             #
###############

class View(Frame): # 继承Frame类  
    def __init__(self, root=None, **options):  
        Frame.__init__(self, root, **options)  
        self.root = root #定义内部变量root  
        #self.hpack()

    def ReSize(self):
        pass

    def hpack(self):
        #self.pack(side=tk.TOP, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)
        self.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.YES)
         
#------------------------------------------------------------------------------------
################
#      #       #
#   1  #   2   #
#      #       #
################
class View2(Frame): # 继承Frame类  
    def __init__(self, root=None,scale=0.5):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.scale=scale
        #self.hpack()
        self.width=800   #获取窗口宽度（单位：像素）
        self.height=600  #获取窗口高度（单位：像素）
        self.width1=int(self.width*self.scale)
        self.width2=int(self.width*(1-self.scale))
        self.m=2
        self.v=[]
        self.v1=tk.Frame(self,relief=tk.SUNKEN,bg='blue',width =self.width1 )
        self.v2=tk.Frame(self,relief=tk.SUNKEN,bg='green',width=self.width2 )
        self.v1.pack(side=tk.LEFT,fill=tk.Y, expand=tk.YES)
        self.v2.pack(side=tk.RIGHT,fill=tk.Y, expand=tk.YES)
#        self.v1.grid(row = 0, column = 0,sticky=tk.NSEW,columnspan=1)
#        self.v2.grid(row = 0, column = 1,sticky=tk.NSEW,columnspan=2)
        self.v.append(self.v1)
        self.v.append(self.v2)
        self.bind("<Configure>", self.Callback)  #Motion事件表示当鼠标进入组件时，就会响应这个事件

    def hpack(self):
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.pack(fill=tk.BOTH, expand=tk.YES)
        
    def Callback(self, event):
        self.width=self.winfo_width()   #获取窗口宽度（单位：像素）
        self.height=self.winfo_height()  #获取窗口高度（单位：像素）
        self.width1=int(self.width*self.scale)
        self.width2=int(self.width*(1-self.scale))
        self.v1['width']=self.width1
        self.v2['width']=self.width2
        self.v1.pack(side=tk.LEFT,fill=tk.Y, expand=tk.YES)
        self.v2.pack(side=tk.RIGHT,fill=tk.Y, expand=tk.YES)
        self.root.update()
        

class Notebook2(tk.Frame): # 继承Frame类的Notebook类
    def __init__(self, master=None,m=0,anchor=tk.NW, size=9,width=10,**kw):  
        tk.Frame.__init__(self, master,**kw)  
        self.root = master #定义内部变量root
        self.m=m
        self.width=width
        self.size=size
        self.anchor=anchor
        self.s1=tk.TOP
        self.s2=tk.BOTTOM
        if (self.anchor in [tk.SW,tk.S,tk.SE]):
            self.s1=tk.BOTTOM
            self.s2=tk.TOP
        self.t=[]
        self.v=[]
        self.view=None
        self.pack(side=self.s2, fill=tk.BOTH, expand=1,ipady=1,pady=1,ipadx=1,padx=1)

        self.tab()


    def add(self,tab=None,text=''):
        if (tab!=None):
            self.m=self.m+1
            def handler (self=self, i=self.m-1 ):
                self.select(i)
            
            if (self.anchor in [tk.NW,tk.N,tk.SW,tk.S]):
                self.button = tk.Button(self.tab, width=self.width,text=text, cursor='hand2',
                                        anchor=tk.S,
                                        font=('Helvetica', '%d'%self.size),
                                        command=handler)
                self.t.append(self.button)
                self.button.pack(side=tk.LEFT)
                self.v.append(tab)
                if (self.m==1):
                    self.select(0)


            if (self.anchor in [tk.NE,tk.SE]):
                self.button = tk.Button(self.tab, width=self.width,text=text, cursor='hand2',
                                        anchor=tk.S,
                                        font=('Helvetica','%d'%self.size),
                                        command=handler)
                self.t.append(self.button)
                self.button.pack(side=tk.RIGHT)
                self.v.append(tab)
                if (self.m==1):
                    self.select(0)


    def tab(self):
        self.tab=tk.Frame(self)
        if (self.anchor in [tk.N,tk.S]):
            self.tab.pack(side=self.s1)
        if (self.anchor in [tk.NW,tk.NE,tk.SW,tk.SE]):
            self.tab.pack(side=self.s1,fill=tk.X)

        
        for i in range(self.m):
            def handler (self=self, i=i ):
                self.select(i)
            self.button = tk.Button(self.tab, width=self.width,text='Tab%d'%i, cursor='hand2',
                                    anchor=tk.S,
                                    font=('Helvetica','%d'%self.size),
                                    command=handler)
            self.t.append(self.button)
            self.v.append(None)
            if (self.anchor in [tk.NW,tk.SW]) :
                self.button.pack(side=tk.LEFT)
            else:
                self.button.pack(side=tk.RIGHT)
            
        self.update()

         
    def frame(self):
        self.frame=tk.Frame(self,bd=2,
                            borderwidth=2,  #边框宽度
                            padx=1,  #部件x方向间距
                            pady=1, #部件y方向间距
                            )
        self.frame.pack(side=self.s2,fill=tk.BOTH, expand=1)         


    def select(self,x):
        #print(x)
        if (self.view!=None):
            self.view.pack_forget()
        for i in range(self.m):
            self.t[i]['relief']=tk.RIDGE
            self.t[i]['anchor']=tk.S
            self.t[i]['bg']="#F0F0ED"
            
        self.t[x]['anchor']=tk.N
        self.t[x]['bg']='white'
        self.view=self.v[x]
        if (self.view!=None):
            self.view.pack(fill=tk.BOTH, expand=1)   


    def modify(self,x,tab=None,text=''):
        if (x>self.m-1):
            return
        if (tab!=None):
            self.v[x]=tab
        if (text!=''):
            self.t[x]['text']=text
#------上面是class Notebook2定义


#定义我的窗口基类
class myWindow2:
    def __init__(self, root, myTitle,w=300, h=200):
        self.width=w
        self.height=h
        self.top = Toplevel(root, width=w, height=h)
        self.top.title(myTitle)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False

    def destroy(self):
        #销毁应用程序窗口
        self.top.destroy()   

    def overturn(self):
        self.top.update_idletasks()
        self.top.overrideredirect(self.flag)
        self.flag=not self.flag #switch



class PopMenu:  #通用弹出菜单
    def __init__(self ,root):
        self.root=root
        self.menu=None
        #self.usermenu=None
        self.selectall=None
        self.init()
        self.root.bind("<Button-3>", self.popup)  #把弹出菜单绑定到所需的控件上。
        self.root.bind('<F5>', lambda event: self.root.update)
        
        for i in 'c', 'C':
            self.root.bind('<Control-%s>' % i,                       
                        lambda event: self.root.event_generate('<<Copy>>'))
        for i in 'v', 'V':
            self.root.bind('<Control-%s>' % i,                       
                        lambda event: self.root.event_generate('<<Paste>>'))
        for i in 'x', 'X':
            self.root.bind('<Control-%s>' % i,
                        lambda event: self.root.event_generate('<<Cut>>'))
        for i in 'z', 'Z':
            self.root.bind('<Control-%s>' % i,
                        lambda event: self.root.event_generate('<<Undo>>'))
        for i in 'y', 'Y':
            self.root.bind('<Control-%s>' % i,
                        lambda event: self.root.event_generate('<<Redo>>'))
        
    def init(self):
        # 建立一个弹出菜单
        self.menu = tk.Menu(self.root, tearoff=False)  #创建弹出菜单
        self.menu.add_command(label="弹出菜单",  command=None)
        self.menu.add_separator()  #增加filemenu的分割线
        self.menu.add_command(label="取消 Undo", accelerator='Ctrl+Z', command=self.undo)
        self.menu.add_command(label="恢复 Redo", accelerator='Ctrl+Y', command=self.redo)
        self.menu.add_command(label="复制 Copy", accelerator='Ctrl+C', command=self.copy)
        self.menu.add_command(label="粘贴 Paste", accelerator='Ctrl+V', command=self.paste) 
        self.menu.add_command(label="剪切 Cut", accelerator='Ctrl+X', command=self.cut)
        self.menu.add_separator()  #增加filemenu的分割线
        self.menu.add_command(label="刷新 Refresh", command=self.update)
        self.menu.add_command(label="关闭弹出菜单", command=None)

    
    def popup(self,event): #弹出菜单操作函数
        self.menu.post(event.x_root, event.y_root)
        
    def cut(self):
        self.root.event_generate('<<Cut>>')
    
    def copy(self):
        self.root.event_generate('<<Copy>>')
    
    def paste(self):
        self.root.event_generate('<<Paste>>')
    
    def redo(self):
        self.root.event_generate('<<Redo>>')
    
    def undo(self):
        self.root.event_generate('<<Undo>>')
    
    def update(self):
        self.root.update()

          
#------------------------------------------------------------------------------------
#用户代码编辑类
class useredit(Frame):# 继承Frame类  
    def __init__(self, root=None):  
        Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.filename=''
        self.outmess=g.ttmsg
        self.myconsole=console()
        self.Init()


    def loadfile(self,file):
        global cve
        filename =file
        if filename == '':
            filename = None
        else:
            self.filename = filename
            self.userpath=os.path.abspath(os.path.dirname(self.filename)+os.path.sep+".")
            self.textPad.delete(1.0,tk.END)#delete all
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            s=f.read()
            s=s.replace('\t','    ')
            self.textPad.insert(1.0,s)
            f.close()

    #用户输出信息
    def tprint(self, txt):
        if txt != "" :
            self.outmess.insert(tk.END, txt)
            self.outmess.see(tk.END)
    
    #用户输出信息,带颜色
    def tcprint(self,txt,color):
        if txt != "" :
           self.outmess.tag_config(color, foreground=Tkcolor(color))   
           self.outmess.insert(tk.END, txt,color)
           self.outmess.see(tk.END)
           
    def openfile(self):
        #global filename
        self.filename = askopenfilename(defaultextension='.py')
        if self.filename == '':
            self.filename = None
        else:
            #root.title('通通量化软件编辑器--'+os.path.basename(filename))
            self.textPad.delete(1.0,tk.END)#delete all
            f = open(self.filename,'r',encoding='utf-8',errors='ignore')
            self.textPad.insert(1.0,f.read())
            f.close()

    def openfile2(self):
        filename = 'usercode2.txt'
        if filename == '':
            filename = None
        else:
            #root.title('通通量化软件编辑器--'+os.path.basename(filename))
            self.textPad.delete(1.0,tk.END)#delete all
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            self.textPad.insert(1.0,f.read())
            f.close()
    
    def newfile(self):
        #root.title('new file')
        self.filename = None
        self.textPad.delete(1.0,tk.END)
    
    def savefile(self):
        #global filename
        try:
            f = open(self.filename,'w',encoding='utf-8',errors='ignore')
            msg = self.textPad.get(1.0,tk.END)
            f.write(msg)
            f.close()
        except:
            self.saveas()

    def runuc2(self):
        try:
            msg = self.textPad.get(1.0,tk.END)
            print('开始运行用户代码。\n')
            tprint('开始运行用户代码。\n')
            exec(msg)
        except Exception as e:
            ttprint('\n用户代码出错:'+str(e)+'\n','red')
            print('\n用户代码出错:'+str(e)+'\n')
            showinfo(title='用户代码出错', message=str(e))

    def runuc(self):
        global input
        self.myconsole.SwitchOut()  #接管print()函数， 开关方法
        self.myconsole.sysinput=input
        input=self.myconsole.MyInput
        try:
            msg = self.textPad.get(1.0,tk.END)
            #print('开始运行用户代码。\n')
            self.tcprint('\n\n#开始运行用户代码。\n','blue')
            mg=globals()
            ml=locals()
            #thread_it(EXEC,msg) 
            exec(msg,mg,ml)
            #exec(msg)
        except Exception as e:
            self.tcprint('\n#用户代码出错:'+str(e)+'\n','red')
            #print('用户代码出错:'+str(e)+'\n')
            showinfo(title='用户代码出错', message=str(e))
        self.myconsole.SwitchOut()  #接管print()函数， 开关方法
        self.tcprint('\n\'\'\'\n','blue')
        s=self.myconsole.str
        self.tcprint(s,'gray')
        self.tcprint('\n\'\'\'\n','blue')
        self.myconsole.clear()
        input=self.myconsole.sysinput
    
    def saveas(self):
        #global filename
        try:
            f = asksaveasfilename(initialfile = 'newfile',defaultextension ='.py')
            self.filename = f
            fh = open(f,'w',encoding='utf-8',errors='ignore')
            msg = self.textPad.get(1.0,tk.END)
            fh.write(msg)
            fh.close()
        except Exception as e:
            ttprint('\n用户代码出错:'+str(e)+'\n','red')
            print('\n用户代码出错:'+str(e)+'\n')
            showinfo(title='用户代码出错', message=str(e))
        #root.title('FileName:'+os.path.basename(f))
    
    def cut(self):
        self.textPad.event_generate('<<Cut>>')
    
    def copy(self):
        self.textPad.event_generate('<<Copy>>')
    
    def paste(self):
        self.textPad.event_generate('<<Paste>>')
    
    def redo(self):
        self.textPad.event_generate('<<Redo>>')
    
    def undo(self):
        self.textPad.event_generate('<<Undo>>')
    
    def selectall(self):
        self.textPad.tag_add('sel',1.0,tk.END)
    
    def search(self):
        topsearch=tk.Toplevel(self)
        topsearch.geometry('300x30+200+250')
        labell=tk.Label(topsearch,text='find')
        labell.grid(row=0,column=0,padx=5)
        entry1=tk.Entry(topsearch,width=28)
        entry1.grid(row=0,column=1,padx=5)
        button1=tk.Button(topsearch,text='find')
        button1.grid(row=0,column=2)
    
    #用户类初始化
    def Init(self):
        #按钮
        self.toolbar = tk.Frame(self.root,height=20)
        self.toolbarName = ('新文件','打开','保存','另存','Undo','Redo','Cut','Copy','Paste','SelectAll','运行程序')
        self.toolbarCommand = (self.newfile,self.openfile,self.savefile,self.saveas,self.undo,self.redo,self.cut,self.copy,self.paste,self.selectall,self.runuc)
        def addButton(name,command):
            for (toolname ,toolcom) in zip(name,command):
                shortButton = tk.Button(self.toolbar,text=toolname,relief='groove',command=toolcom)
                shortButton.pack(side=tk.LEFT,padx=2,pady=5)
        addButton(self.toolbarName,self.toolbarCommand) #调用添加按钮的函数
        self.toolbar.pack(side=tk.TOP,fill=tk.X)
        
       # 创建弹出菜单
        self.menubar=tk.Menu(self)
        self.toolbarName2 = ('新文件','打开','保存','另存','Undo','Redo','Cut','Copy','Paste','SelectAll','运行程序')
        self.toolbarCommand2 = (self.newfile,self.openfile,self.savefile,self.saveas,self.undo,self.redo,self.cut,self.copy,self.paste,self.selectall,self.runuc)
        def addPopButton(name,command):
            for (toolname ,toolcom) in zip(name,command):
                self.menubar.add_command(label=toolname,command=toolcom)
    
        def pop(event):
            # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
            self.menubar.post(event.x_root,event.y_root)
    
        addPopButton(self.toolbarName2,self.toolbarCommand2) #创建弹出菜单
        self.textPad = tk.Text(self.root,undo=True,bg='#FFF8DC')
        self.textPad.insert(1.0,' \n')
        self.textPad.pack(expand=tk.YES,fill=tk.BOTH)
        self.textPad.focus_set()
        self.textPad.bind("<Button-3>",pop)
        self.scroll = tk.Scrollbar(self.textPad)
        self.textPad.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.textPad.yview)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        var = tk.StringVar()
        self.status = tk.Label(self.root,anchor=tk.E,height=1,text='Ln',relief=tk.FLAT,takefocus=False,textvariable=var,padx=2)
        self.status.pack(fill=tk.X)

class windowMenu2:
    def __init__(self, root, menus=['文件','编辑','工具','帮助'],items=[['文件'],['编辑'],['工具'],['帮助']]):
        self.root=root
        self.menus=menus
        self.items=items
        self.menubar = tk.Menu(self.root)
        self.menu = self.menubar
        for i,x in enumerate(self.menus):
            m = tk.Menu(self.menubar, tearoff=0)
            for item in self.items[i]:
                if isinstance(item, list):
                    sm = tk.Menu(self.menubar, tearoff=0)
                    for subitem in item[1:]:
                        if subitem == '-':
                            sm.add_separator()
                        else:
                            sm.add_command(label=subitem, command=None, image=None, compound='left')
                    m.add_cascade(label=item[0], menu=sm)
                elif item == '-':
                    m.add_separator()
                else:
                    m.add_command(label=item, command=None, image=None, compound='left')
            self.menubar.add_cascade(label=x, menu=m)
        self.root.config(menu=self.menubar)

class windowMenu3:
    def __init__(self, root, menus=None,items=None,cmds=None,icos=None):
        self.root=root
        self.menus=menus
        self.items=items
        self.menubar = tk.Menu(self.root)
        self.menu = self.menubar
        for i,x in enumerate(self.menus):
            m = tk.Menu(self.menubar, tearoff=0)
            for item, callback, ico in zip(items[i], cmds[i], icos[i]):
                if isinstance(item, list):
                    sm = tk.Menu(self.menubar, tearoff=0)
                    for subitem, subcallback, subico in zip(item[1:], callback, ico):
                        if subitem == '-':
                            sm.add_separator()
                        else:
                            sm.add_command(label=subitem, command=subcallback, image=subico, compound='left')
                    m.add_cascade(label=item[0], menu=sm)
                elif item == '-':
                    m.add_separator()
                else:
                    m.add_command(label=item, command=callback, image=ico, compound='left')
            self.menubar.add_cascade(label=x, menu=m)
        self.root.config(menu=self.menubar)

##--------------------------------------------------------------------
def Tkcolor(colorname):
    cns = {
    'aliceblue':            '#F0F8FF',
    'antiquewhite':         '#FAEBD7',
    'aqua':                 '#00FFFF',
    'aquamarine':           '#7FFFD4',
    'azure':                '#F0FFFF',
    'beige':                '#F5F5DC',
    'bisque':               '#FFE4C4',
    'black':                '#000000',
    'blanchedalmond':       '#FFEBCD',
    'blue':                 '#0000FF',
    'blueviolet':           '#8A2BE2',
    'brown':                '#A52A2A',
    'burlywood':            '#DEB887',
    'cadetblue':            '#5F9EA0',
    'chartreuse':           '#7FFF00',
    'chocolate':            '#D2691E',
    'coral':                '#FF7F50',
    'cornflowerblue':       '#6495ED',
    'cornsilk':             '#FFF8DC',
    'crimson':              '#DC143C',
    'cyan':                 '#00FFFF',
    'darkblue':             '#00008B',
    'darkcyan':             '#008B8B',
    'darkgoldenrod':        '#B8860B',
    'darkgray':             '#A9A9A9',
    'darkgreen':            '#006400',
    'darkkhaki':            '#BDB76B',
    'darkmagenta':          '#8B008B',
    'darkolivegreen':       '#556B2F',
    'darkorange':           '#FF8C00',
    'darkorchid':           '#9932CC',
    'darkred':              '#8B0000',
    'darksalmon':           '#E9967A',
    'darkseagreen':         '#8FBC8F',
    'darkslateblue':        '#483D8B',
    'darkslategray':        '#2F4F4F',
    'darkturquoise':        '#00CED1',
    'darkviolet':           '#9400D3',
    'deeppink':             '#FF1493',
    'deepskyblue':          '#00BFFF',
    'dimgray':              '#696969',
    'dodgerblue':           '#1E90FF',
    'firebrick':            '#B22222',
    'floralwhite':          '#FFFAF0',
    'forestgreen':          '#228B22',
    'fuchsia':              '#FF00FF',
    'gainsboro':            '#DCDCDC',
    'ghostwhite':           '#F8F8FF',
    'gold':                 '#FFD700',
    'goldenrod':            '#DAA520',
    'gray':                 '#808080',
    'green':                '#008000',
    'greenyellow':          '#ADFF2F',
    'honeydew':             '#F0FFF0',
    'hotpink':              '#FF69B4',
    'indianred':            '#CD5C5C',
    'indigo':               '#4B0082',
    'ivory':                '#FFFFF0',
    'khaki':                '#F0E68C',
    'lavender':             '#E6E6FA',
    'lavenderblush':        '#FFF0F5',
    'lawngreen':            '#7CFC00',
    'lemonchiffon':         '#FFFACD',
    'lightblue':            '#ADD8E6',
    'lightcoral':           '#F08080',
    'lightcyan':            '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgreen':           '#90EE90',
    'lightgray':            '#D3D3D3',
    'lightpink':            '#FFB6C1',
    'lightsalmon':          '#FFA07A',
    'lightseagreen':        '#20B2AA',
    'lightskyblue':         '#87CEFA',
    'lightslategray':       '#778899',
    'lightsteelblue':       '#B0C4DE',
    'lightyellow':          '#FFFFE0',
    'lime':                 '#00FF00',
    'limegreen':            '#32CD32',
    'linen':                '#FAF0E6',
    'magenta':              '#FF00FF',
    'maroon':               '#800000',
    'mediumaquamarine':     '#66CDAA',
    'mediumblue':           '#0000CD',
    'mediumorchid':         '#BA55D3',
    'mediumpurple':         '#9370DB',
    'mediumseagreen':       '#3CB371',
    'mediumslateblue':      '#7B68EE',
    'mediumspringgreen':    '#00FA9A',
    'mediumturquoise':      '#48D1CC',
    'mediumvioletred':      '#C71585',
    'midnightblue':         '#191970',
    'mintcream':            '#F5FFFA',
    'mistyrose':            '#FFE4E1',
    'moccasin':             '#FFE4B5',
    'navajowhite':          '#FFDEAD',
    'navy':                 '#000080',
    'oldlace':              '#FDF5E6',
    'olive':                '#808000',
    'olivedrab':            '#6B8E23',
    'orange':               '#FFA500',
    'orangered':            '#FF4500',
    'orchid':               '#DA70D6',
    'palegoldenrod':        '#EEE8AA',
    'palegreen':            '#98FB98',
    'paleturquoise':        '#AFEEEE',
    'palevioletred':        '#DB7093',
    'papayawhip':           '#FFEFD5',
    'peachpuff':            '#FFDAB9',
    'peru':                 '#CD853F',
    'pink':                 '#FFC0CB',
    'plum':                 '#DDA0DD',
    'powderblue':           '#B0E0E6',
    'purple':               '#800080',
    'red':                  '#FF0000',
    'rosybrown':            '#BC8F8F',
    'royalblue':            '#4169E1',
    'saddlebrown':          '#8B4513',
    'salmon':               '#FA8072',
    'sandybrown':           '#FAA460',
    'seagreen':             '#2E8B57',
    'seashell':             '#FFF5EE',
    'sienna':               '#A0522D',
    'silver':               '#C0C0C0',
    'skyblue':              '#87CEEB',
    'slateblue':            '#6A5ACD',
    'slategray':            '#708090',
    'snow':                 '#FFFAFA',
    'springgreen':          '#00FF7F',
    'steelblue':            '#4682B4',
    'tan':                  '#D2B48C',
    'teal':                 '#008080',
    'thistle':              '#D8BFD8',
    'tomato':               '#FF6347',
    'turquoise':            '#40E0D0',
    'violet':               '#EE82EE',
    'wheat':                '#F5DEB3',
    'white':                '#FFFFFF',
    'whitesmoke':           '#F5F5F5',
    'yellow':               '#FFFF00',
    'yellowgreen':          '#9ACD32'}
    return cns[colorname]

#运行用户代码
def EXEC(st):
    try:
        st=exec_s+st
        #print(st)
        g=globals()
        l=locals()
        exec(st,g,l)
        return('命令运行完成。')   
    except Exception as e:
        return('用户命令出错:'+str(e))
    return('命令运行完成。')   

#用户信息输出窗
class useredit2(tk.Frame):# 继承Frame类  
    def __init__(self, root=None,fontsize=12):  
        global userpath  #用户目录
        global prgpath  #软件目录
        tk.Frame.__init__(self, root)  
        self.root = root #定义内部变量root  
        self.filename=''
        self.textPad=None
        self.row=0
        self.col=0
        self.t=None
        self.fontsize=fontsize
        self.font='Fixdsys -%d'%self.fontsize
        self.fg='#000000'
        self.bg='#FFF8DC'
        self.row2=0
        self.col2=0
        self.inid=1
        self.inids=''
        self.inidl=0
        #self.myconsole=console()
        self.usercmd=''
        self.toolbar=None
        self.statusbar=None
        self.menubar=None
        self.timer_interval = 5
        prgpath=os.getcwd()
        self.userpath=prgpath
        self.prgpath=prgpath
        self.userdir=prgpath
        self.Init()
        
        self.init2()


    def init2(self):
        self.usercmd=''
        self.inid=1
        self.inids=''
        self.inidl=0
        self.inids='In [%d]: '%self.inid
        self.inidl=len(self.inids)
        self.tcprint('模拟','blue')
        self.tcprint('IPython  软件\n','red')
        self.tcprint('版本: '+sys.version,'blue')
        self.tcprint('\n'+self.inids,'darkblue')




    def runs(self,s):
        s1=s.strip() #删除字符串前后空格
        try:
            msg = self.usercmd+'\n'+s
            exec(msg,globals(),locals())
            #exec(msg,{},{})
            if s1[0:6]!='print(' and s1[0:5]!='help(' :
                self.usercmd=self.usercmd+'\n'+s       
        except Exception as e:
            self.tcprint('\n用户代码出错:'+str(e)+'\n','red')
            #print('用户代码出错: '+str(e)+'\n')
            #showinfo(title='用户代码出错', message=str(e))
        self.textPad.see(tk.END)

           

    def rtnkey(self,event=None):
        global input
        self.row2,self.col2 = self.textPad.index(tk.INSERT).split('.')
        ss=self.textPad.get (self.row2+'.0',self.row2+'.'+self.col2)
        if (len(ss)>self.inidl):
            ss1=ss[self.inidl:]
            self.myconsole.SwitchOut()  #接管print()函数， 开关方法
            self.myconsole.sysinput=input
            input=self.myconsole.MyInput
        
            #self.myconsole.SwitchOut()  #接管print()函数， 开关方法
            #input=self.myconsole.MyInput
            self.runs(ss1)
            self.myconsole.SwitchOut()  #接管print()函数， 开关方法
            s=self.myconsole.str
            s=s.strip() #删除字符串前后空格
            if s!='':
                self.tcprint('\n'+self.myconsole.str,'blue')
            self.myconsole.clear()
            input=self.myconsole.sysinput
            
            #self.myconsole.SwitchOut()  #接管print()函数， 开关方法

            self.inid=self.inid+1
            self.inids='In [%d]: '%self.inid
            self.inidl=len(self.inids)
            self.tcprint('\n'+self.inids,'darkblue')
            #print(locals())
            #lo=locals()
            #exec('print(locals())')
            #print(eval(ss1,{},locals()))
            self.textPad.see(tk.END)

                

    #用户输出信息
    def tprint(self, txt):
        if txt != "" :
            self.textPad.insert(tk.END, txt)
            self.textPad.see(tk.END)
    
    #用户输出信息,带颜色
    def tcprint(self,txt,color):
        if txt != "" :
           self.textPad.tag_config(color, foreground=Tkcolor(color))   
           self.textPad.insert(tk.END, txt,color)
           self.textPad.see(tk.END)


    def setfg(self):
        fgn,self.fg=colorchooser.askcolor(self.fg)
        self.textPad['fg']=self.fg

    def setbg(self):
        bgn,self.bg=colorchooser.askcolor(self.bg)
        self.textPad['bg']=self.bg


    def openfile(self):
        #global filename
        self.filename = askopenfilename(defaultextension='.py')
        if self.filename == '':
            self.filename = None
        else:
            self.userpath=os.path.abspath(os.path.dirname(self.filename)+os.path.sep+".")
            #root.title('通通量化软件编辑器--'+os.path.basename(filename))
            self.textPad.delete(1.0,tk.END)#delete all
            f = open(self.filename,'r',encoding='utf-8',errors='ignore')
            self.textPad.insert(1.0,f.read())
            f.close()

    def openfile2(self):
        filename = 'usercode2.txt'
        if filename == '':
            filename = None
        else:
            self.userpath=os.path.abspath(os.path.dirname(self.filename)+os.path.sep+".")
            #root.title('通通量化软件编辑器--'+os.path.basename(filename))
            self.textPad.delete(1.0,tk.END)#delete all
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            self.textPad.insert(1.0,f.read())
            f.close()
    
    def newfile(self):
        #root.title('new file')
        self.filename = None
        self.textPad.delete(1.0,tk.END)
        self.init2()
    
    def savefile(self):
        #global filename
        try:
            f = open(self.filename,'w',encoding='utf-8',errors='ignore')
            msg = self.textPad.get(1.0,tk.END)
            f.write(msg)
            f.close()
            self.userpath=os.path.abspath(os.path.dirname(self.filename)+os.path.sep+".")
        except:
            self.saveas()


    def runuc(self):
        self.myconsole.SwitchOut()  #接管print()函数， 开关方法
        input=self.myconsole.MyInput
        try:
            msg = self.textPad.get(1.0,tk.END)
            #print('开始运行用户代码。\n')
            self.tcprint('\n#开始运行用户代码。\n','blue')
            thread_it(EXEC,msg) 
            #exec(msg)
        except Exception as e:
            self.tcprint('\n#用户代码出错:'+str(e)+'\n','red')
            #print('用户代码出错:'+str(e)+'\n')
            showinfo(title='用户代码出错', message=str(e))
        self.myconsole.SwitchOut()  #接管print()函数， 开关方法
        self.tcprint('\n\'\'\'\n','blue')
        s=self.myconsole.str
        self.tcprint(s,'gray')
        self.tcprint('\n\'\'\'\n','blue')
        self.myconsole.clear()
        input=self.myconsole.sysinput

    def runuc2(self):
        try:
            f = open('temppy.py','w',encoding='utf-8',errors='ignore')
            msg = self.textPad.get(1.0,tk.END)
            f.write(msg)
            f.close()
            runpy='run_py.bat temppy.py'
            os.system(runpy)
        except Exception as e:
            pass

    def runuc3(self):
        thread_it(self.runuc2)
    
    def saveas(self):
        #global filename
        f = asksaveasfilename(initialfile = 'newfile',defaultextension ='.py')
        self.filename = f
        fh = open(f,'w',encoding='utf-8',errors='ignore')
        msg = self.textPad.get(1.0,tk.END)
        fh.write(msg)
        fh.close()
        self.userpath=os.path.abspath(os.path.dirname(self.filename)+os.path.sep+".")
        #root.title('FileName:'+os.path.basename(f))
    
    def cut(self):
        self.textPad.event_generate('<<Cut>>')
    
    def copy(self):
        self.textPad.event_generate('<<Copy>>')
    
    def paste(self):
        self.textPad.event_generate('<<Paste>>')
    
    def redo(self):
        self.textPad.edit_redo()
        #self.textPad.event_generate('<<Redo>>')
    
    def undo(self):
        self.textPad.edit_undo()
        #self.textPad.event_generate('<<Undo>>')
    
    def selectall(self):
        self.textPad.focus_set()
        self.textPad.see(1.0)
        self.textPad.tag_add('sel',1.0,tk.END)
    
    def search(self):
        topsearch=tk.Toplevel(self)
        topsearch.geometry('300x30+200+250')
        labell=tk.Label(topsearch,text='find')
        labell.grid(row=0,column=0,padx=5)
        entry1=tk.Entry(topsearch,width=28)
        entry1.grid(row=0,column=1,padx=5)
        button1=tk.Button(topsearch,text='find')
        button1.grid(row=0,column=2)


    def font2(self):
        if self.fontsize>8:
            self.fontsize=self.fontsize-1
            self.font='Fixdsys -%d'%self.fontsize
            self.textPad.config(font=self.font)
        

    def font3(self):
        if self.fontsize<80:
            self.fontsize=self.fontsize+1
            self.font='Fixdsys -%d'%self.fontsize
            self.textPad.config(font=self.font)

    
    #用户类初始化
    def Init(self):
        #按钮
        self.toolbar = tk.Frame(self.root,height=20)
        self.toolbarName =  ('清空窗口','打开','保存','另存','取消','重做','剪切','复制','粘贴','选择全部','外部运行','内部运行','字缩小','字放大','背景色','字体色')
        self.toolbarCommand = (self.newfile,self.openfile,self.savefile,self.saveas,self.undo,self.redo,self.cut,
                               self.copy,self.paste,self.selectall,self.runuc3,self.runuc,self.font2,self.font3,self.setbg,self.setfg)
        def addButton(name,command):
            for (toolname ,toolcom) in zip(name,command):
                shortButton = tk.Button(self.toolbar,text=toolname,relief='groove',command=toolcom)
                shortButton.pack(side=tk.LEFT,padx=2,pady=5)
        addButton(self.toolbarName,self.toolbarCommand) #调用添加按钮的函数
        self.toolbar.pack(side=tk.TOP,fill=tk.X)
        
        # 创建弹出菜单
        self.menubar=tk.Menu(self)
        self.toolbarName2 =  ('清空窗口','打开','保存','另存','取消','重做','剪切','复制','粘贴','选择全部','运行程序','字缩小','字放大')
        self.toolbarCommand2 = (self.newfile,self.openfile,self.savefile,self.saveas,self.undo,self.redo,self.cut,self.copy,self.paste,self.selectall,self.runuc,self.font2,self.font3)
        def addPopButton(name,command):
            for (toolname ,toolcom) in zip(name,command):
                self.menubar.add_command(label=toolname,command=toolcom)
    
        def pop(event):
            # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
            self.menubar.post(event.x_root,event.y_root)
    
        addPopButton(self.toolbarName2,self.toolbarCommand2) #创建弹出菜单
        self.textPad = tk.Text(self.root,undo=True,bg='#FFF8DC')
        #self.textPad.insert(1.0,' \n')
        self.textPad.pack(expand=tk.YES,fill=tk.BOTH)
        self.textPad.focus_set()
        self.textPad.bind("<Button-3>",pop)
        self.scroll = tk.Scrollbar(self.textPad)
        self.textPad.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.textPad.yview)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.zhs=0
        

        def getline():
            self.row,self.col = self.textPad.index(tk.INSERT).split('.')
            lineNum = '[行:  ' +self.row+'   '+'列:  '+self.col+' ]'
            self.var.set(lineNum)
            #text.delete(0.0, END)
            if int(self.row)>0:
                self.Zln=len(self.textPad.get('0.0',tk.END).split('\n'))
                #print(Zln)
                if self.zhs!=self.Zln   :
                    #G_zhs=self.Zln
                    self.zhs=self.Zln

                    self.textPad.see(tk.END)
            if self.timer_interval >0:
                self.t = Timer(self.timer_interval,getline)
                self.t.start()

        def getline2():
            if self.timer_interval >0:
                thread_it(getline)


        self.var = tk.StringVar()
        self.statusbar = tk.Frame(self.root,relief=tk.FLAT,padx=2)

        self.label=tk.Label(self.statusbar,anchor=tk.E,height=1,text='Ln',relief=tk.FLAT,takefocus=False,textvariable=self.var,padx=2)
        self.label.pack(side=tk.RIGHT)
        self.statusbar.pack(fill=tk.X)

        #绑定回车键
        self.textPad.bind('<Key-Return>', self.rtnkey) 
        self.font='Fixdsys -%d'%self.fontsize
        self.textPad.config(font=self.font)


    def Destroy(self):
        self.t.cancel() 


'''
菜单可以无限嵌套,但是菜单文字不能重名.
mm=mymenu.menuitem['编辑']
mi=mm.index('打开')
mm.entryconfig(mi, command=hello)
mm.entryconfig(mi, image=img1)
或
mymenu.set('编辑','打开',image=img1)
mymenu.set('编辑','另存为',image=img2,command=hello)
'''
class windowMenu:
    def __init__(self, root, menus=[['文件',[]],['编辑',[]],['工具',[]],['帮助',[]]]):
        self.root=root
        self.menus=[]
        self.items=[]
        self.menubar = tk.Menu(self.root)
        self.menus,self.items=self.menus_item(menus)
        self.menuitem={}
        for i,x in enumerate(self.menus):
            m = tk.Menu(self.menubar, tearoff=0)
            self.menuitem[x]=m
            for item in self.items[i]:
                if isinstance(item, list):
                    #print('list1')
                    #print(item,item[0],item[1:][0])
                    sm=self.additem(m,item)
                    m.add_cascade(label=item[0], menu=sm)
                    
                elif item == '-':
                    m.add_separator()
                else:
                    m.add_command(label=item, command=None, image=None, compound='left')
            self.menubar.add_cascade(label=x, menu=m)
        self.root.config(menu=self.menubar)

   
    def menus_item(self,itemlist):
        menus=[]
        items=[]
        for i in range(len(itemlist)):
            menus.append(itemlist[i][0:1][0])
            items.append(itemlist[i][1:][0])
        return menus,items


    def additem(self,menubar,item):
        #print('additem',item,len(item))
        menu=item[0]
        items=item[1:][0]
        #print(menu,items)
        m2 = tk.Menu(menubar, tearoff=0)
        self.menuitem[menu]=m2
        for item in items:
            if isinstance(item, list):
                #print('list2')
                #print(item,item[0],item[1:][0])
                sm=self.additem(m2,item)
                m2.add_cascade(label=menu, menu=sm)
            elif item == '-':
                m2.add_separator()
            else:
                m2.add_command(label=item, command=None, image=None, compound='left')
        return m2

    def additem2(self,menubar,item,menu):
        #print('additem')
        sm = tk.Menu(menubar, tearoff=0)
        self.menuitem[menu]=sm
        for subitem in item:
            if isinstance(subitem, list):
                print('列表2')
                a1,a2=self.menus_item(subitem)
                print(subitem,subitem[0],subitem[1:][0])
                print(a1,a2)
                for y in a2:
                    if isinstance(y, list):
                        ssm=self.additem(sm,y)
                        sm.add_cascade(label=y, menu=ssm)
                    if y == '-':
                        sm.add_separator()
                    else:
                        sm.add_command(label=y, command=None, image=None, compound='left')
            if subitem == '-':
                sm.add_separator()
            else:
                sm.add_command(label=subitem, command=None, image=None, compound='left')
        return sm

    def set(self,menu,item,**kw):
        mm=self.menuitem[menu]
        mi=mm.index(item)
        mm.entryconfig(mi, **kw)
        
        
    
#Table表格类
class Table(tk.Frame): # 继承Frame类的ttk.Treeview类
    def __init__(self, master=None,**kw):  
        tk.Frame.__init__(self, master,**kw)  
        self.root = master #定义内部变量root
        self.col = [1,2]
        self.table=ttk.Treeview(self,show="headings")
        self.tree=self.table
        self.table_root=None
        self.table.pack(fill=tk.BOTH, expand=tk.YES,side = tk.LEFT)
        #x滚动条
        self.xscroll = tk.Scrollbar(self.table, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(xscrollcommand = self.xscroll.set)
        self.xscroll.pack(side = tk.BOTTOM, fill = tk.X)
        #y滚动条
        self.yscrollbar = tk.Scrollbar(self.table, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand = self.yscrollbar.set)
        self.yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        #self.tree.bind("<Button-1>", self.popup)
        #self.pack(expand = 1, fill = tk.BOTH)

    def load_df(self,df):
        grid_df=df
        grid_ss=grid_df.columns
        grid_colimns=[]
        for s in grid_ss:
            grid_colimns.append(s)
    
        #Treeview组件，6列，显示表头，带垂直滚动条
        self.table.configure(columns=(grid_colimns),show="headings")
        
        for s in grid_colimns:
            #设置每列宽度和对齐方式
            #tree.column(s, anchor='center')
            self.table.column(s,width=len(s)*30,  anchor='center')
            #设置每列表头标题文本
            self.table.heading(s, text=s)
            
    
        #插入演示数据
        for i in range(len(grid_df)):
            v=[]
            for s in grid_ss:
                #v.append(grid_df.get_value(i, s))
                v.append(grid_df.at[i,s])
            self.table.insert('', i, values=v)

   
    def delete_table(self):
        items =self.table.get_children()
        [self.table.delete(item) for item in items]

    def clear(self):
        items =self.table.get_children()
        [self.table.delete(item) for item in items]

    def brush(self,c1='#FAFAFA',c2='#eeeeff'):
    
        items = self.table.get_children()
    
        for i in range(len(items)):
    
            if i%2==1:
                self.table.item(items[i], tags=('row1'))
            else:
                self.table.item(items[i], tags=('row2'))
    
        self.table.tag_configure('row1', background=c1)
        self.table.tag_configure('row2', background=c2)


#Tree类类
class Tree(tk.Frame): # 继承Frame类的ttk.Treeview类
    def __init__(self, master=None,**kw):  
        tk.Frame.__init__(self, master,**kw)  
        self.root = master #定义内部变量root
        self.index=None
        self.col = [1,2]
        self.tree=ttk.Treeview(self)
        self.usepop=None
        self.img= tk.PhotoImage(file="../../../Downloads/xb2e/x0.gif")
        self.img2= tk.PhotoImage(file="../../../Downloads/xb2e/x1.gif")
        self.img3= tk.PhotoImage(file="../../../Downloads/xb2e/x2.gif")
        self.img4= tk.PhotoImage(file="../../../Downloads/xb2e/x3.gif")
        self.tree.image=self.img 
        self.tree_root=None
        self.tree.pack(fill=tk.BOTH, expand=tk.YES,side = tk.LEFT)
        #x滚动条
        self.xscroll = tk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand = self.xscroll.set)
        self.xscroll.pack(side = tk.BOTTOM, fill = tk.X)
        #y滚动条
        self.yscrollbar = tk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand = self.yscrollbar.set)
        self.yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.tree.bind("<Double-Button-1>", self.popup)
        #self.pack(expand = 1, fill = tk.BOTH)

    
    def delete_tree(self):
        items =self.tree.get_children()
        [self.tree.delete(item) for item in items]



    #读取目录
    def load_path(self,path='.'):
        self.img= tk.PhotoImage(file="../../../Downloads/xb2e/open.gif")
        self.abspath = os.path.abspath(path)
        self.root_node = self.tree.insert('', 'end', text=self.abspath, open=True,image=self.img)
        self.process_directory(self.root_node, self.abspath)
        self.fix_last() 
        
    #遍历路径下的子目录
    def process_directory(self, parent, path):
        #遍历路径下的子目录
        for p in os.listdir(path):
            #构建路径

            abspath = os.path.join(path, p)
            #是否存在子目录
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False,image=self.img2)
            #time.sleep(0.01)
            #self.tree.update()
            if isdir:
                self.process_directory(oid, abspath)
          

    #用递归法遍历带子字典或列表的数据
    def process_dict(self,d, tr='',ii=0):
        i=ii
        imgx=self.img
        for k,v in d.items():
            i+=1
            if type(v) == list:
                if type(v[0]) == dict:
                    if i==1:
                        imgx=self.img
                    else :
                        imgx=self.img2
                    trr = self.tree.insert(tr, 'end', text=k, open=True,image=imgx)
                    for ls in v:
                        i+=1
                        self.process_dict(ls, trr,i)
                else:
                    if i==1:
                        imgx=self.img
                    else :
                        imgx=self.img2
                    self.tree.insert(tr, 'end', text=k, values= v,image=imgx)
            elif type(v) == dict:
                trr = self.tree.insert(tr, 'end', text=k, open = True,image=imgx)
                self.process_dict(v, trr,i)

    
    def load_dict(self,d):
        self.process_dict(d)
        self.fix_last() 
            
    def fix_last(self):
        children = self.tree.get_children()          # 返回了一大帮children
        idd=children[-1]
        children = self.tree.get_children(idd)          # 返回了一大帮children
        idd=children[-1]
        if idd !='I001':
            self.tree.item(idd,image=self.img3)

    def popup(self,event):
        "鼠标事件"
        if self.usepop !=None:
            self.usepop(event)
#=================================================================== 
#定义我的窗口基类
class myWindow:
    def __init__(self, root, myTitle,w=300, h=200):
        self.width=w
        self.height=h
        self.top = Toplevel(root, width=w, height=h)
        self.top.title(myTitle)
        self.top.attributes('-topmost', 1)
        self.flag=True
        self.transparent=False

    def destroy(self):
        #销毁应用程序窗口
        self.top.destroy()   

    def overturn(self):
        self.top.update_idletasks()
        self.top.overrideredirect(self.flag)
        self.flag=not self.flag #switch




#移动窗口到屏幕中央       
def setCenter(root,w,h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int( (ws/2) - (w/2) )
    y = int( (hs/2) - (h/2) )
    root.geometry('{}x{}+{}+{}'.format(w, h, x, y))

#移动窗口到屏幕坐标x,y       
def setPlace(root,x, y,w,h):
    root.geometry('{}x{}+{}+{}'.format(w, h, x, y))


#显示窗口ico图标
def showIco(root,Ico):
    root.iconbitmap(Ico)    

#是否禁止修改窗口大小
def reSizable(root,x,y):
    root.resizable(x, y)   #是否禁止修改窗口大小

      

#由于tkinter中没有ToolTip功能，所以自定义这个功能如下
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
 
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
 
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
 
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
             

#===================================================================          
def createToolTip( widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def deltreeitem(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)

def deltree(tree):
    g.scrollBarA.pack_forget() 
    g.scrollBarB.pack_forget() 
    tree.pack_forget()
    g.ttree=None
    g.scrollBarA =None
    g.scrollBarB =None

def creattree(w,df):
    grid_df=df
    grid_ss=grid_df.columns
    grid_colimns=[]
    for s in grid_ss:
        grid_colimns.append(s)
    
    #滚动条
    scrollBarA =tk.Scrollbar(w)
    g.scrollBarA=scrollBarA
    g.scrollBarA.pack(side=tk.RIGHT, fill=tk.Y)

    #Treeview组件，6列，显示表头，带垂直滚动条
    tree = ttk.Treeview(w,columns=(grid_colimns),
                      show="headings",
                      yscrollcommand=g.scrollBarA.set)
    
    for s in grid_colimns:
        #设置每列宽度和对齐方式
        #tree.column(s, anchor='center')
        tree.column(s,width=len(s)*30,  anchor='center')
        #设置每列表头标题文本
        tree.heading(s, text=s)
        
    g.scrollBarA.config(command=tree.yview)

    scrollBarB  = tk.Scrollbar(w,orient = HORIZONTAL)
    g.scrollBarB=scrollBarB
    g.scrollBarB.set(0.5,0.2)
    g.scrollBarB.pack(side=tk.TOP, fill=tk.X)
    g.scrollBarB.config(command=tree.xview)
    
    #定义并绑定Treeview组件的鼠标单击事件
    #插入演示数据
    for i in range(len(grid_df)):
        v=[]
        for s in grid_ss:
            #v.append(grid_df.get_value(i, s))
            v.append(grid_df.at[i,s])
        tree.insert('', i, values=v)

    tree.pack(fill=tk.BOTH,expand=tk.YES)


    def pop2():
        g.tabControl.select(g.ta3)
        de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        df1=hp.get_k_data(g.g.stock,ktype='D',start='2018-01-01',end=de,index=False,autype='qfq')
        df2=hp.tstojq(df1)
        if g.plotPage !=None:
            g.plotPage.canvas._tkcanvas.pack_forget() 
            g.plotPage.pack_forget() 
            g.plotPage=None

        g.plotPage = plotFrame(g.tab2,df2,g.stock,g.formula)  
        g.plotPage.pack(fill=X)

    
    # 创建菜单
    menubar=Menu(w)
    # 创建第四个菜单项，并 绑定事件
    menubar.add_command(label='历史行情',command=pop2)


    
    def onDBClick(event):
        item = tree.selection()[0]
        aa=tree.item(item, "values")
        #print("you clicked on  "+item, tree.item(item, "values"))
        bb=list(aa)
        #print(bb[0])
        g.g.stock=bb[0]


    tree.bind("<Button-1>", onDBClick)
    tree.bind("<Double-1>", onDBClick)



    return tree 

def mygrid(w,df):
    grid_df=df
    grid_ss=grid_df.columns
    grid_colimns=[]
    for s in grid_ss:
        grid_colimns.append(s)
    
    #滚动条
    scrollBarA =tk.Scrollbar(w)
    g.scrollBarA=scrollBarA
    g.scrollBarA.pack(side=tk.RIGHT, fill=tk.Y)

    #Treeview组件，6列，显示表头，带垂直滚动条
    tree = ttk.Treeview(w,columns=(grid_colimns),
                      show="headings",
                      yscrollcommand=g.scrollBarA.set)
    
    for s in grid_colimns:
        #设置每列宽度和对齐方式
        #tree.column(s, anchor='center')
        tree.column(s,width=len(s)*30,  anchor='center')
        #设置每列表头标题文本
        tree.heading(s, text=s)
        
    g.scrollBarA.config(command=tree.yview)

    scrollBarB  = tk.Scrollbar(w,orient = HORIZONTAL)
    g.scrollBarB=scrollBarB
    g.scrollBarB.set(0.5,0.2)
    g.scrollBarB.pack(side=tk.TOP, fill=tk.X)
    g.scrollBarB.config(command=tree.xview)
    
    #定义并绑定Treeview组件的鼠标单击事件

    #插入演示数据
    for i in range(len(grid_df)):
        v=[]
        for s in grid_ss:
            #v.append(grid_df.get_value(i, s))
            v.append(grid_df.at[i,s])
        tree.insert('', i, values=v)


    #tree.pack(fill=X,ipady=g.winH-200)
    tree.pack(fill=tk.BOTH,expand=tk.YES)
    
    def onDBClick(event):
        item = tree.selection()[0]
        aa=tree.item(item, "values")
        #print("you clicked on  "+item, tree.item(item, "values"))
        bb=list(aa)
        #print(bb[0])
        g.g.stock=bb[0]

        
        
        
    tree.bind("<Double-1>", onDBClick)
    
    def pop1():
        g.tabControl.select(g.tab2)
        de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        df1=hp.get_k_data(g.g.stock,ktype='D',start='2018-01-01',end=de,index=False,autype='qfq')
        df2=hp.tstojq(df1)
        if g.plotPage !=None:
            g.plotPage.canvas._tkcanvas.pack_forget() 
            g.plotPage.pack_forget() 
            g.plotPage=None

        g.plotPage = plotFrame(g.tab2,df2,g.g.stock,g.g.index)  
        g.plotPage.pack(fill=X)

        

    def topwin():
        author_ui = Toplevel()
        author_ui.title('子窗口测试')
        #author_ui.iconbitmap('icons/48x48.ico')
        author_ui.geometry('200x80')
        about_string = Label(author_ui, text = '这是一个测试！')
        confirmButton = Button(author_ui, text = '确定',
                               command = lambda: self.destroy_ui(author_ui))
        about_string.pack()
        confirmButton.pack()
    
    # 创建菜单
    menubar=Menu(w)
    # 创建第四个菜单项，并 绑定事件
    menubar.add_command(label='历史行情',command=pop1)
    #menubar.add_command(label='子窗口 ',command=topwin)
    
    def pop(event):
        # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
        menubar.post(event.x_root,event.y_root)
    
    # 鼠标右键是用的<Button-3>
    # 使用 Menu 类的 pop 方法来弹出菜单
    tree.bind("<Button-3>",pop)    
    return tree
    


class gridFramejq(Frame): # 继承Frame类  
    def __init__(self, root=None):  
        Frame.__init__(self, root)  
      
        self.root = root #定义内部变量root  
        self.parenta = root
        self.tree=None
        self.dd=1
        self.n=1
        self.bt='指数列表'
        self.timer=None
        #self.gn=StringVar()
        self.gn=None
        self.classA=None
        self.stocks=None
        self.itemName = StringVar()  
        self.createPage()  
   
    def rxt(self):
        ds='2018-01-01'
        de=time.strftime('%Y-%m-%d',time.localtime(time.time()))+' 15:01:00'
        g.gtype=g.vbook.get()
        g.sday=ds.strip()
        g.eday=de.strip()
        item = self.tree.selection()[0]
        aa=self.tree.item(item, "values")
        #print("you clicked on  "+item, tree.item(item, "values"))
        bb=list(aa)        
        g.stock=bb[0] 
        g.vtitle=bb[1]
        print(bb[0])
        if g.login:
            g.stock=jq.normalize_code(g.stock)
            df3 = jq.get_price(g.stock, start_date=g.sday, end_date=g.eday,frequency='daily') # 获得000001.XSHG的2015年01月的分钟数据, 只获取open+close字段
            df2=hp.jqtots(df3)
            df2.date=df2.date.astype('str')
            if g.tab3!=None:
                g.tabControl.forget(g.tab3)
                g.tab3=None
            
            #用户自建新画面
            g.tab3 = tk.Frame(g.tabControl)
            g.tabControl.add(g.tab3, text='日线图') 
            g.tabControl.select(g.tab3)
            axview3x(g.tab3,df2,t=g.stock,n=2,f1='VOL',f2=g.gtype)
            #df2.to_csv('temp/000001.csv' , encoding= 'gbk')
        else:
            print('未登陆，不能操作！')
            g.status.text(1,'查看日线数据') #在状态栏2输出信息
            g.status.text(2,'未登陆，不能操作！')
        self.tabControl.select(g.tab3)


    def fst(self):
        item = self.tree.selection()[0]        
        aa=self.tree.item(item, "values")
        bb=list(aa)
        print("you popmenu on  "+item, bb[0])
        g.stock=bb[0]
        #self.timer.cancel()
        g.mstock=bb[0]
        g.vtitle=bb[1]
        try:
            filename='view/聚宽分时图.py'
            g.status.text(1,'')
            g.status.text(2,'查看'+bb[0]+'分时图！')
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            msg=f.read()
            f.close()
            exec(msg)
        except Exception as e:
            g.status.text(1,'')
            g.status.text(2,'用户代码出错:'+str(e))
            ttprint('用户代码出错:'+str(e)+'\n','red')
            print('用户代码出错:'+str(e)+'\n')

       
    
    def createPage(self):  
        self.LBtext=StringVar()
        self.LBtext.set(self.bt)
        self.LB=Label(self, textvariable = self.LBtext,bg="blue",fg="white").pack(fill=X)  
        if g.login:
            df4=jq.get_all_securities(types=['index'], date=None)
            df4.insert(0,'jkname',df4.index)
            df4.to_csv('temp/index.csv' , encoding= 'gbk')
        else:
            print('读本地index数据！')
            df4=pd.read_csv('temp/index.csv' , encoding= 'gbk')
        
        #滚动条
        scrollBar =tk.Scrollbar(self)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        #Treeview组件，6列，显示表头，带垂直滚动条
        self.tree = ttk.Treeview(self,columns=('c1', 'c2', 'c3','c4', 'c5', 'c6'),
                          show="headings",
                          yscrollcommand=scrollBar.set)

        #设置每列宽度和对齐方式
        self.tree.column('c1',  anchor='center')
        self.tree.column('c2', width=100,  anchor='center')
        self.tree.column('c3',width=100,   anchor='center')
        self.tree.column('c4',width=100,   anchor='center')
        self.tree.column('c5', width=100,  anchor='center')
        self.tree.column('c6',  anchor='center')
        #设置每列表头标题文本
        self.tree.heading('c1', text='聚宽代码')
        self.tree.heading('c2', text='指数名称')
        self.tree.heading('c3', text='指数缩写')
        self.tree.heading('c4', text='开始日期')
        self.tree.heading('c5', text='结束日期')
        self.tree.heading('c6', text='数据类型')
        
        #Treeview组件与垂直滚动条结合
        scrollBar.config(command=self.tree.yview)
        #scrollBar.config(command=tree.xview)
        #定义并绑定Treeview组件的鼠标单击事件

        def fun_timer():
            #print('Hello Timer!')
            self.n=self.n+1
            self.LBtext.set(self.bt)
            
            flash()
            self.timer = threading.Timer(60, fun_timer)
            self.timer.start()

        def delButton(tree):
            x=tree.get_children()
            for item in x:
                tree.delete(item)
                
        def flash():
                #self.tree.pack_forget() 
                n1=[]
                o1=[]
                c1=[]
                h1=[]
                l1=[]
                v1=[]
                m1=[]
                self.df=pd.DataFrame({'name':[s for s in self.stocks]})  
                ds=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                for s in self.stocks:
                    w=jq.get_price(s,start_date=ds,end_date=de, frequency='daily') # 获取000001.XSHE的2015年的按天数据
                    n1.append(s)
                    o1.append(w['open'][0])
                    c1.append(w['close'][0])
                    h1.append(w['high'][0])
                    l1.append(w['low'][0])
                    v1.append(w['volume'][0])
                    m1.append(w['money'][0])
                    
            
                #df=pd.DataFrame({'name':[s for s in stocks]})  
                ZB = pd.Series(o1, name = 'open')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(c1, name = 'close')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(h1, name = 'high')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(l1, name = 'low')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(v1, name = 'volume')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(m1, name = 'money')  
                self.df = self.df.join(ZB)                                   
    
                delButton(self.tree)  
                #设置每列表头标题文本
                self.tree.heading('c1', text='聚宽代码')
                self.tree.heading('c2', text=g.ec['open'])
                self.tree.heading('c3', text=g.ec['close'])
                self.tree.heading('c4', text=g.ec['high'])
                self.tree.heading('c5', text=g.ec['low'])
                self.tree.heading('c6', text=g.ec['volume'])                  
                #插入演示数据
                for i in range(len(self.df)):
                    self.tree.insert('', i, values=[self.df.name[i],self.df.open[i],self.df.close[i],self.df.high[i],self.df.low[i],self.df.volume[i]])
                self.tree.pack(fill=X,ipady=g.winH-20) 
        


        def onDBClick(event):
            if g.login==False:
                return
            g.status.text(1,'正在获取数据...') #在状态栏2输出信息
            item = self.tree.selection()[0]
            if self.dd==1:
                aa=self.tree.item(item, "values")
                #print("you clicked on  "+item, tree.item(item, "values"))
                bb=list(aa)
                #print(bb[0])
                self.LBtext.set(bb[1]+'  '+bb[0])
                self.stocks = jq.get_index_stocks(bb[0])
                g.status.text(2,'查看'+bb[0]+'股票列表！')
                self.bt='指数'+bb[0]+'股票列表'
                #print(self.stocks)

                
                #self.tree.pack_forget() 
                n1=[]
                o1=[]
                c1=[]
                h1=[]
                l1=[]
                v1=[]
                m1=[]
                self.df=pd.DataFrame({'name':[s for s in self.stocks]})  
                ds=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                de=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                de=ds='2019-02-01'
                for s in self.stocks:
                    w1=jq.get_price(s,start_date=ds,end_date=de, frequency='daily') # 获取000001.XSHE的2015年的按天数据
                    w=hp.jqtots(w1)
                    #print(w)
                    n1.append(s)
                    o1.append(w.at[0,'open'])
                    c1.append(w.at[0,'close'])
                    h1.append(w.at[0,'high'])
                    l1.append(w.at[0,'low'])
                    v1.append(w.at[0,'volume'])
                    m1.append(w.at[0,'money'])
                    
            
                #df=pd.DataFrame({'name':[s for s in stocks]})  
                ZB = pd.Series(o1, name = 'open')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(c1, name = 'close')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(h1, name = 'high')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(l1, name = 'low')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(v1, name = 'volume')  
                self.df = self.df.join(ZB)  
                ZB = pd.Series(m1, name = 'money')  
                self.df = self.df.join(ZB)                                   
    
                delButton(self.tree)  
                #设置每列表头标题文本
                self.tree.heading('c1', text='聚宽代码')
                self.tree.heading('c2', text=g.ec['open'])
                self.tree.heading('c3', text=g.ec['close'])
                self.tree.heading('c4', text=g.ec['high'])
                self.tree.heading('c5', text=g.ec['low'])
                self.tree.heading('c6', text=g.ec['volume'])                   
                #插入演示数据
                for i in range(len(self.df)):
                    self.tree.insert('', i, values=[self.df.name[i],self.df.open[i],self.df.close[i],self.df.high[i],self.df.low[i],self.df.volume[i]])
                self.tree.pack(fill=X,ipady=g.winH-20) 
                self.dd=2
                g.status.text(1,'') #在状态栏2输出信息
            elif self.dd==2:
                aa=self.tree.item(item, "values")
                bb=list(aa)
                print("you clicked on  "+item, bb[0])
                
                g.stock=bb[0]
                self.timer.cancel()
                g.mstock=bb[0]
                
                try:
                    filename='view/聚宽分时图.py'
                    g.status.text(1,'')
                    g.status.text(2,'查看'+bb[0]+'分时图！')
                    f = open(filename,'r',encoding='utf-8',errors='ignore')
                    msg=f.read()
                    f.close()
                    exec(msg)
                except Exception as e:
                    g.status.text(1,'')
                    g.status.text(2,'用户代码出错:'+str(e))
                    ttprint('用户代码出错:'+str(e)+'\n','red')
                    print('用户代码出错:'+str(e)+'\n')
                
#                self.tree.pack_forget() 
#                self.pack_forget() 
#                self.gn.set(g.stock)
#                self.classA.st3()
#                self.parenta.mainPage.pack(fill=X) 
#                self.parenta.mainPage.st()
#                self.parenta.plotPage.canvas._tkcanvas.pack(fill=X)
#                self.parenta.plotPage.pack(fill=X)

                
                
                
            self.timer = threading.Timer(1, fun_timer)
            self.timer.start()
    

        self.tree.bind("<Double-1>", onDBClick)
        


        #插入演示数据
        for i in range(len(df4)):
            self.tree.insert('', i, values=[df4.jkname[i],df4.display_name[i],df4.name[i],df4.start_date[i],df4.end_date[i],df4.type[i]])

        self.tree.pack(fill=X,ipady=g.winH-20)
        # 创建弹出菜单
        self.menubar=tk.Menu(self)
        self.toolbarName2 = ('日线图','分时图')
        self.toolbarCommand2 = (self.rxt,self.fst)
        def addPopButton(name,command):
            for (toolname ,toolcom) in zip(name,command):
                self.menubar.add_command(label=toolname,command=toolcom)
    
        def pop(event):
            # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
            self.menubar.post(event.x_root,event.y_root)
    
        addPopButton(self.toolbarName2,self.toolbarCommand2) #创建弹出菜单
        self.tree.bind("<Button-3>",pop)


global myconsole,input
class console(object):  
  
    def __init__(self):  
        self.stdout=None
        self.sysinput=input
        self.buffer = []  
        self.str=''
        self.n=0
        self.switchOut=False
        self.switchIn=False
        self.status=False


    def write(self, *args, **kwargs):  
        self.buffer.append(args)  
        self.n+=1
        self.str=self.str+str(args[0])
    
    def flush(self):
        pass
    
    def clear(self):
        self.buffer = []  
        self.str=''
        self.n=0
    
    def MyInput(self,prompt=''):
        ss=simpledialog.askstring ("输入窗", prompt)
        return ss

    def SwitchOut(self,sw=None):
        if sw!=None:
            self.switchOut=sw
            
        if (self.switchOut==False):
            self.stdout = sys.stdout    
            sys.stdout = self
            input=self.MyInput
            self.switchOut=True
            self.status=True
            return None
        else:
            text_area=sys.stdout
            sys.stdout=self.stdout    
            self.switchOut=False
            self.status=False
            input=self.sysinput
            return text_area
      
global ttmsg

def ttprint(s1,s2):
    print(s1)
    g.ttmsg.insert(tk.END, s1)
    g.ttmsg.see(tk.END)


def tprint(s1):
    s1='\n'+s1
    print(s1)
    g.ttmsg.insert(tk.END, s1)
    g.ttmsg.see(tk.END)


      
'''
独狼荷蒲软件(或通通软件)版权声明
1、独狼荷蒲软件(或通通软件)均为软件作者设计,或开源软件改进而来，仅供学习和研究使用，不得用于任何商业用途。
2、用户必须明白，请用户在使用前必须详细阅读并遵守软件作者的“使用许可协议”。
3、作者不承担用户因使用这些软件对自己和他人造成任何形式的损失或伤害。
4、作者拥有核心算法的版权，未经明确许可，任何人不得非法复制；不得盗版。作者对其自行开发的或和他人共同开发的所有内容，
    包括设计、布局结构、服务等拥有全部知识产权。没有作者的明确许可，任何人不得作全部或部分复制或仿造。

独狼荷蒲软件
QQ: 2775205
Tel: 18578755056
公众号:独狼股票分析
'''