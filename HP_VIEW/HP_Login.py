# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架登陆窗口
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2018年9月14日
#主程序：HP_main.py
修改位置：  18行，78行，79行
"""


# from jqdatasdk import *   #聚宽数据包，不用可注释掉

from PIL import Image, ImageTk
from HP_VIEW.HP_global import *
from HP_VIEW.HP_set import *
from HP_VIEW.HP_MainPage import *

class LoginPage(object):  
    def __init__(self, master=None):  
        HP_init()
        exec(G_tk)
        exec(G_tk1)
        self.w = 300
        self.h = 180
        self.root = master #定义内部变量root  
        self.staIco = g.ico
        self.root.geometry('%dx%d' % (self.w, self.h )) #设置窗口大小  
        self.username = StringVar()  
        self.password = StringVar()  
        self.createPage()  
        self.loop()

  
    def loop(self):
        self.root.resizable(False, False)   #禁止修改窗口大小
        self.center()                       #窗口居中
        self.root.mainloop()
    
    def _quit(self):
        #结束事件主循环，并销毁应用程序窗口
        self.root.quit()
        self.root.destroy()     

    def center(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        #print(ws,hs)
        x = int( (ws/2) - (self.w/2) )
        y = int( (hs/2) - (self.h/2) )
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))
        self.root.iconbitmap(self.staIco)
        
  
    def createPage(self):  
        self.page = Frame(self.root) #创建Frame  
        self.page.pack()  
        Label(self.page).grid(row=0, stick=W)  
        Label(self.page, text = '聚宽账户: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        self.username.set(g.user)
        Label(self.page, text = '聚宽密码: ').grid(row=2, stick=W, pady=10)  
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)  
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10)  
        Button(self.page, text='退出', command=self._quit).grid(row=3, column=1, stick=E)  
 
    
    def loginCheck(self):  
        name = self.username.get()  
        secret = self.password.get()  
        try:
            # x=auth(name,secret)   #聚宽用户认证,不需要可注释掉，把下一句注释去掉。
            x='Good'
        except:
            x="error"
        #x='test'
        if x!='error' or x=='' :
            self.page.destroy()  
            G_login=True
            MainPage(self.root)  
        else:  
            showinfo(title='错误', message='账号或密码错误！')
            G_login=False


#####################################################
################独狼荷蒲软件版权声明###################
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