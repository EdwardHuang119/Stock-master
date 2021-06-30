# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import Frame
from tkinter.messagebox import *
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from tkinter.filedialog import *
import threading
from threading import Timer
import string
import HP_global as g
from HP_formula import *

#用户输出信息
def tprint(txt):
    if g.ttmsg != None :
        g.ttmsg.insert(tk.END, txt)
        g.ttmsg.see(END)

#用户输出信息,带颜色
def ttprint(txt,color):
    if g.ttmsg != None :
        g.ttmsg.insert(tk.END, txt,color)
        g.ttmsg.see(END)


#用户代码编辑类
class useredit(Frame):# 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.filename=''
        self.Init()

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

    def runuc(self):
        try:
            msg = self.textPad.get(1.0,tk.END)
            print('开始运行用户代码。\n')
            tprint('开始运行用户代码。\n')
            exec(msg)
        except Exception as e:
            ttprint('用户代码出错:'+str(e)+'\n','red')
            print('用户代码出错:'+str(e)+'\n')
            showinfo(title='用户代码出错', message=str(e))

    
    def saveas(self):
        #global filename
        f = asksaveasfilename(initialfile = 'newfile',defaultextension ='.py')
        self.filename = f
        fh = open(f,'w',encoding='utf-8',errors='ignore')
        msg = self.textPad.get(1.0,tk.END)
        fh.write(msg)
        fh.close()
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
        self.toolbarName = ('新策略','打开','保存','另存','Undo','Redo','Cut','Copy','Paste','SelectAll','运行策略')
        self.toolbarCommand = (self.newfile,self.openfile,self.savefile,self.saveas,self.undo,self.redo,self.cut,self.copy,self.paste,self.selectall,self.runuc)
        def addButton(name,command):
            for (toolname ,toolcom) in zip(name,command):
                shortButton = tk.Button(self.toolbar,text=toolname,relief='groove',command=toolcom)
                shortButton.pack(side=LEFT,padx=2,pady=5)
        addButton(self.toolbarName,self.toolbarCommand) #调用添加按钮的函数
        self.toolbar.pack(side=tk.TOP,fill=tk.X)
        
       # 创建弹出菜单
        self.menubar=tk.Menu(self)
        self.toolbarName2 = ('新策略','打开','保存','另存','Undo','Redo','Cut','Copy','Paste','SelectAll','运行策略')
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
        self.textPad.pack(expand=YES,fill=BOTH)
        self.textPad.focus_set()
        self.textPad.bind("<Button-3>",pop)
        self.scroll = tk.Scrollbar(self.textPad)
        self.textPad.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.textPad.yview)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
#        global zhs
#        zhs=0
#        timer_interval = 10
#
#        def getline():
#            global t,row,zhs
#            msg = self.textPad.get(1.0,tk.END)
#            if len(msg)>0 :
#                row,col = self.textPad.index(tk.INSERT).split('.')
#                lineNum = '行:  ' +row+'   '+'列:  '+col
#            var.set(lineNum)
#            timer_interval = 3
#            t = Timer(timer_interval,getline)
#            t.start()
#
#        t = Timer(timer_interval,getline)
#        t.start()
        var = tk.StringVar()
        self.status = Label(self.root,anchor=tk.E,height=1,text='Ln',relief=tk.FLAT,takefocus=False,textvariable=var,padx=2)
        self.status.pack(fill=tk.X)


#多线程启动函数
def thread_it2(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()

#运行用户代码
def EXEC2(st):
    try:
        tprint('开始运行用户代码。\n')
        exec(st)
        return('命令运行完成。')   
    except Exception as e:
        ttprint('用户代码出错:'+str(e)+'\n','red')
        print('用户代码出错:'+str(e)+'\n')
        showinfo(title='用户代码出错', message=str(e))
    return('命令运行完成。')   



def showdialog():
    '''各种窗口'''
    pass
    #res = messagebox.askokcancel(title='标题', message='提示信息。。。', default=messagebox.CANCEL) # default=messagebox.CANCEL，指定默认焦点位置，另 ABORT/RETRY/IGNORE/OK/CANCEL/YES/NO
    #res = messagebox.showinfo(title='标题', message='提示信息。。。')
    #res = messagebox.showwarning(title='标题', message='提示信息。。。')
    #res = messagebox.showerror(title='标题', message='提示信息。。。')
    #res = messagebox.askquestion(title='标题', message='提示信息。。。') 
    #res = messagebox.askyesno(title='标题', message='提示信息。。。')
    #res = messagebox.askyesnocancel(title='标题', message='提示信息。。。')
    #res = messagebox.askretrycancel(title='标题', message='提示信息。。。')
    #res = filedialog.askdirectory()
    #res = filedialog.askopenfile(filetypes=[('xml', '*.xml')])
    #res = filedialog.askopenfiles()
    #res = filedialog.askopenfilename()
    #res = filedialog.askopenfilenames()
    #res = filedialog.asksaveasfile()
    #res = filedialog.asksaveasfilename()
    #res = simpledialog.askinteger(title='整数', prompt='输入一个整数', initialvalue=100)
    #res = simpledialog.askfloat(titlee='实数', prompt='输入一个实数', minvalue=0, maxvalue=11)
    #res = simpledialog.askstring(title='字符串', prompt='输入一个字符串')
    #res = colorchooser.askcolor()
    #print(res)




#定义一个添加菜单的类，想加什么菜单直接调用即可,副作用是没法加分隔线
class menuNameAccCom:
    def __init__(self,menuname,menucom,menuacc):
        self.menuname=menuname
        self.menuacc=menuacc
        self.menucom=menucom

    def addmenu(self,wigetName):
        for (name,com,acc) in (zip(self.menuname,self.menucom,self.menuacc)):
            wigetName.add_command(label=name,accelerator=acc,command=com)





def myedit(root,filename=''):
    global textPad
    def openfile():
        #global filename
        filename = askopenfilename(defaultextension='.py')
        if filename == '':
            filename = None
        else:
            #root.title('通通量化软件编辑器--'+os.path.basename(filename))
            textPad.delete(1.0,tk.END)#delete all
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            textPad.insert(1.0,f.read())
            f.close()

    def openfile2():
        nonlocal filename
        filename = 'usercode2.txt'
        if filename == '':
            filename = None
        else:
            #root.title('通通量化软件编辑器--'+os.path.basename(filename))
            textPad.delete(1.0,tk.END)#delete all
            f = open(filename,'r',encoding='utf-8',errors='ignore')
            textPad.insert(1.0,f.read())
            f.close()
    
    def newfile():
        nonlocal filename
        #root.title('new file')
        filename = None
        textPad.delete(1.0,tk.END)
    
    def savefile():
        #global filename
        try:
            f = open(filename,'w',encoding='utf-8',errors='ignore')
            msg = textPad.get(1.0,tk.END)
            f.write(msg)
            f.close()
        except:
            saveas()
    

    def runuc():
        try:
            #f = open('usercode.py','w',encoding='utf-8',errors='ignore')
            msg = textPad.get(1.0,tk.END)
            #f.write(msg)
            #f.close()
            print('开始运行用户代码。\n')
            tprint('开始运行用户代码。\n')
            #import usercode
            #print(msg)
            exec(msg)
        except Exception as e:
            #print(type(e))
            ttprint('用户代码出错:'+str(e)+'\n','red')
            print('用户代码出错:'+str(e)+'\n')
            showinfo(title='用户代码出错', message=str(e))


    
    def saveas():
        #global filename
        f = asksaveasfilename(initialfile = 'newfile',defaultextension ='.py')
        filename = f
        fh = open(f,'w',encoding='utf-8',errors='ignore')
        msg = textPad.get(1.0,tk.END)
        fh.write(msg)
        fh.close()
        #root.title('FileName:'+os.path.basename(f))
    
    def cut():
        textPad.event_generate('<<Cut>>')
    
    def copy():
        textPad.event_generate('<<Copy>>')
    
    def paste():
        textPad.event_generate('<<Paste>>')
    
    def redo():
        textPad.event_generate('<<Redo>>')
    
    def undo():
        textPad.event_generate('<<Undo>>')
    
    def selectall():
        textPad.tag_add('sel',1.0,tk.END)
    
    def search():
        topsearch=Toplevel(root)
        topsearch.geometry('300x30+200+250')
        labell=Label(topsearch,text='find')
        labell.grid(row=0,column=0,padx=5)
        entry1=Entry(topsearch,width=28)
        entry1.grid(row=0,column=1,padx=5)
        button1=Button(topsearch,text='find')
        button1.grid(row=0,column=2)
    
    
#    root = Tk()
#    root.title('通通量化软件编辑器')
#    root.geometry('800x500+100+100')
    
#    menubar = Menu(root)
#    root.config(menu= menubar)
#    
#    #文件菜单
#    filemenu = Menu(menubar,tearoff=False)
#    filemenuName = ('New','Open','Save','Save as')
#    filemenuAcc = ('Ctrl+N','Ctrl+O','Ctrl+S','Ctrl+Shift+S')
#    filemenuCom = (newfile,openfile,savefile,saveas)
#    
#    filem = menuNameAccCom(filemenuName,filemenuCom,filemenuAcc)#调用添加菜单的类
#    filem.addmenu(filemenu)
#    menubar.add_cascade(label='File',menu=filemenu)
#    
#    #编辑菜单
#    editmenu = Menu(menubar,tearoff=False)
#    editmenuName = ('Undo','Redo','Cut','Copy','Paste','Select All')
#    editmenuAcc = ('Ctrl+Z','Ctrl+Y','Ctrl+X','Ctrl+C','Ctrl+V','Ctrl+A')
#    editmenuCom = (undo,redo,cut,copy,paste,selectall)
#    
#    editm = menuNameAccCom(editmenuName,editmenuCom,editmenuAcc)#调用添加菜单的类
#    editm.addmenu(editmenu)
#    menubar.add_cascade(label='Edit',menu=editmenu)
#    
#    findmenu = Menu(menubar,tearoff=False)
#    findmenu.add_command(label='Find',accelerator='Ctrl+F',command=search)
#    menubar.add_cascade(label='Find',menu=findmenu)
    
    #按钮
    toolbar = Frame(root,height=20)
    toolbarName = ('新策略','打开','保存','另存','Undo','Redo','Cut','Copy','Paste','SelectAll','运行策略')
    toolbarCommand = (newfile,openfile,savefile,saveas,undo,redo,cut,copy,paste,selectall,runuc)
    def addButton(name,command):
        for (toolname ,toolcom) in zip(name,command):
            shortButton = Button(toolbar,text=toolname,relief='groove',command=toolcom)
            shortButton.pack(side=tk.LEFT,padx=2,pady=5)

    
    addButton(toolbarName,toolbarCommand) #调用添加按钮的函数
    toolbar.pack(side=tk.TOP,fill=tk.X)
    

   # 创建弹出菜单
    menubar=Menu(root)
    toolbarName2 = ('新策略','打开','保存','另存','Undo','Redo','Cut','Copy','Paste','SelectAll','运行策略')
    toolbarCommand2 = (newfile,openfile,savefile,saveas,undo,redo,cut,copy,paste,selectall,runuc)
    def addPopButton(name,command):
        for (toolname ,toolcom) in zip(name,command):
            menubar.add_command(label=toolname,command=toolcom)


    def pop(event):
        # Menu 类里面有一个 post 方法，它接收两个参数，即 x 和y 坐标，它会在相应的位置弹出菜单。
        menubar.post(event.x_root,event.y_root)

    addPopButton(toolbarName2,toolbarCommand2) #创建弹出菜单
    
    textPad = Text(root,undo=True,bg='#FFF8DC')
    textPad.pack(anchor=tk.CENTER,expand=1,fill=tk.BOTH)
    textPad.focus_set()
    textPad.bind("<Button-3>",pop)
    scroll = Scrollbar(textPad)
    textPad.config(yscrollcommand=scroll.set)
    scroll.config(command=textPad.yview)
    scroll.pack(side=tk.RIGHT,fill=tk.Y)
    
#    global zhs
#    zhs=0
#    timer_interval = 2
#    def getline():
#        global t,row,zhs
#        msg = textPad.get(1.0,tk.END)
#        if len(msg)>0 :
#            row,col = textPad.index(INSERT).split('.')
#            lineNum = '行:  ' +row+'   '+'列:  '+col
#        var.set(lineNum)
#        timer_interval = 3
#        t = Timer(timer_interval,getline)
#        t.start()
#    t = Timer(timer_interval,getline)
#    t.start()

    var = StringVar()
    status = Label(root,anchor=tk.E,height=1,text='Ln',relief=tk.FLAT,takefocus=False,textvariable=var,padx=2)
    status.pack(side=tk.BOTTOM,fill=tk.X)


class useredit2(Frame):# 继承Frame类  
    def __init__(self, master=None):  
        Frame.__init__(self, master)  
        self.root = master #定义内部变量root  
        self.filename=''
        self.Init()
 
    def Init(self):
        myed2=myedit( self.root )


