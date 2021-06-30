# -*- coding: utf-8 -*-
"""
#功能：通通量化投资开发环境全局变量
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标
#开始设计日期: 2018-07-08
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2018年12月16日
#主程序：HP_main.py
"""

#运行系统环境设置
#G_os=1 windows,=2 linux, =3 mac oS
global os   #操作系统
global pyver  #Python版本

#软件名称设置
global name  #软件名称
global title #软件标题
global developer #软件开发者
global ver   #软件版本号

#软件数据目录
global datapath  #数据目录
global prgpath  #软件目录

#软件平台设置信息 
global winW  #默认主窗口宽度
global winH  #默认主窗口高度
global root   #窗口根句柄
global ico   #软件图标

#用户信息
global user  #用户名
global login  #用户登录标记

#绘图设置
global cns  #颜色表
global hcolor  #颜色表
global hcursor #鼠标模式集
global ubg #背景色
global ufg #前景色
global utg #文字颜色
global uvg #成交量颜色

#通通框架控件名称
global mainform  #主窗口
global tabControl #主窗口tabControl
global tab1  #tab1控件名
global tab2
global tab3
global tab4
global tab5
global tab6
global tab7
global tab8
global tab9
global tab10
global tab11
global tab12
global tab13
global tab14
global tab15
global tab16
global tab17
global tab18
global tab19
global tab20
global ttmsg  ##信息输出窗 
global mymsg  ##信息输入窗 
global status #主窗口状态栏
global toolsbar #工具栏(横向）
global toolsbar2 #工具栏（纵向）
global mainmenu #主菜单

global names
global date_s
global date_e
global stock_i
global book_s
global tabs
global tabn
global stock_names
global zxg
global zxg2
global zxg3
global zxg4
global zxg5
global zxg6
global zxg7
global zxg8
global zxg9
global blockname
global bkdf
global pys
global hqlink

global UserView
global UserF10View
global inText
global outText
###########################################
#软件指标回测参数
global gtype   #画面模式,暂用于显示指标图形个数
global stype   #股票数据类型
global gmarket #股票市场,0深圳,1上海
global stock   #当前股票代码
global index   #是否指数
global formula #当前用户指标
global df      #当前股票代码数据
global vdate_s
global vdate_e
global vbook
global vstock
global vtitle 
global sday    #分析开始日期
global eday    #分析结束日期
global MA1     #价格平均线周期
global MA2     #价格平均线周期
global MA3     #价格平均线周期
global MA4     #价格平均线周期
global MA5     #价格平均线周期
global MA6     #价格平均线周期
global MAV1     #成交量平均线周期
global MAV2     #成交量平均线周期
global money   #当前用户资金
global stamp_duty   #印花税 0.1%
global trading_Commission    #交易佣金0.05%
global stop_loss_on #允许止损
global stop_loss_max #止损3次,就停止交易
global stop_loss_range   #止损幅度
global hcdate_s #回测窗输入开始日期
global hcdate_e #回测窗输入结束日期
global hczj  #回测窗输入的起始资金
global hczs  #回测窗输入的止损幅度
global hczy  #回测窗输入的止盈幅度
global hczz  #回测窗输入的追涨幅度
global hcts  #回测窗输入的停损此数
global hcstock #回测窗输入的股票代码
global mstock #分时图股票代码
global mds #分时开始日期
global mde #分时开始日期
global ec #英汉字典
global hca,hcb,hcc,hcd,hce,hcf
global cw #财务字典
global hctitle #回测标题
#####################################################

global canvas  #绘图canvas
global figure  #绘图figure
global plot    #绘图plot
global frame
global plotPage
global UserFrame
global UserFig
global UserPlot
global date_tickers
global Usercanvas
global ttree
global scrollBarA 
global scrollBarB 
global ttext
global ttmsg
global mymsg

global ttrobot
global fanyi


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