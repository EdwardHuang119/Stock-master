# -*- coding: utf-8 -*-
"""
#功能：通通股票分析软件框架主程序界面
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
"""

from PIL import Image, ImageTk
import webbrowser
import os
from HP_VIEW.HP_view import * #菜单栏对应的各个子页面
from HP_VIEW.HP_global import *
from HP_VIEW.HP_set import *


   
class MainPage(object):  
    def __init__(self, master=None):  
        HP_init()
#        if G_os==1:
#            exec('import win32api')
        self.root = master #定义内部变量root  
        G_root=self.root
        self.w = G_winW
        self.h = G_winH
        self.root.title(G_title)  
        self.staIco = G_ico
        self.root.geometry('%dx%d' % (self.w, self.h)) #设置窗口大小  
        #plotCreat(self.root)
        self.createUI()
        self.center()
        self.loop()


    # 生成界面
    def createUI(self):
        self.createICO()
        self.createMenu()
        self.createPage()  


    def loop(self):
        self.root.resizable(True, True)   #禁止修改窗口大小
        self.center()                       #窗口居中
        self.root.mainloop()
    
    def _quit(self):
        #结束事件主循环，并销毁应用程序窗口
        self.root.quit()
        self.root.destroy()     

    def center(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = int( (ws/2) - (self.w/2) )
        y = int( (hs/2) - (self.h/2) )
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))
        self.root.iconbitmap(self.staIco)
    
    
    # 创建菜单
    def createMenu(self):
        '''只支持两层嵌套'''
        menus = ['用户功能','公式分析', '量化研究','智能学习', '历史回测', '网络爬虫','系统设置','帮助']
        items = [['用户注册','退出系统'],['编辑公式','运行公式'],
                 [],[],[],[],[],[]]
        callbacks = [[ self.web2, self._quit ],[self.webbrowser2,None],
                     [],
                     [],[],[],[],[]]
        icos = [[self.img1, self.img2],[None,None],
                [],
                [],[],[],[],[]]
        
        menubar = Menu(self.root)
        for i,x in enumerate(menus):
            m = Menu(menubar, tearoff=0)
            for item, callback, ico in zip(items[i], callbacks[i], icos[i]):

                if isinstance(item, list):
                    sm = Menu(menubar, tearoff=0)
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
            menubar.add_cascade(label=x, menu=m)
        self.root.config(menu=menubar)
    
    
        # 生成所有需要的图标
    def createICO(self):
        self.img1 =ImageTk.PhotoImage(Image.open('./t1.jpg'))
        self.img2 =ImageTk.PhotoImage(Image.open('./t2.jpg'))
        self.img3 =ImageTk.PhotoImage(Image.open('./t3.jpg'))
        self.img4 =ImageTk.PhotoImage(Image.open('./t4.jpg'))


    def web2(self):
        webbrowser.open("https://www.joinquant.com/user/login/index")
    
    def webbrowser(self):
        webbrowser.open("https://www.joinquant.com")
        #os.system('"C:/Program Files/Internet Explorer/iexplore.exe" http://www.baidu.com')

    def webbrowser2(self):
        webbrowser.open("https://www.joinquant.com/community/algorithm")

    def webbrowser3(self):
        webbrowser.open("https://www.joinquant.com/help/api/help?name=factor")

    def webbrowser4(self):
        webbrowser.open("https://www.joinquant.com/algorithm/live/shoplist")

    def webbrowser5(self):
        webbrowser.open("https://www.joinquant.com/algorithm/live/shoplist?f=home&m=memu")

    def webbrowser6(self):
        webbrowser.open("https://www.joinquant.com/data/dict/technicalanalysis")

    def webbrowser7(self):
        webbrowser.open("https://www.joinquant.com/help/api/help?name=JQData")        
  
    def webbrowser8(self):
        webbrowser.open("https://www.joinquant.com/default/index/jqclient?f=home&m=memu")
        
    def webbrowser9(self):
        webbrowser.open("https://www.joinquant.com/algorithm/live/shareList?f=home&m=memu")

    def webbrowser10(self):
        webbrowser.open("https://www.joinquant.com/algorithm/index/edit?algorithmId=e3a1f2b2d0824923375953d13bcf95ab&isNew=1&type=&f=&baseCapital=100000&startTime=2016-06-01&endTime=2016-12-31")        

    def webbrowser11(self):
        webbrowser.open("https://www.joinquant.com/help/api/help?name=factor_values")

    def webbrowser12(self):
        webbrowser.open("https://www.joinquant.com/algorithm/live/shoplist?f=home&m=memu")

    def createPage(self):  
        self.mainPage = MainFrame(self.root)  
        self.mainPage.pack(fill=X) #默认显示数据录入界面  
        self.plotPage = plotFrame3(self.root)  
        self.plotPage.pack()
        self.mainPage.canvas=self.plotPage.canvas
        
   
    def MainFrame(self):  
        self.mainPage.pack(fill=X)
        self.plotPage.canvas._tkcanvas.pack(fill=X)
        self.plotPage.pack(fill=X)


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