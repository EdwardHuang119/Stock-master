 # -*- coding: utf-8 -*-
"""
#功能：小白可视化开发环境全局变量
#版本：Ver1.00
#设计人：独狼荷蒲
#电话:18578755056
#QQ：2775205
#百度：荷蒲指标,小白量化
#开始设计日期: 2019-03-01
#公众号:独狼股票分析
#使用者请同意最后<版权声明>
#最后修改日期:2019年03月01日
#主程序：HP_main.py
"""

import platform
import HP_global as g
import time

##数据主目录
g.datapath='\\xbdata'
g.prgpath='\\xb'

#软件名称
g.root=None
g.name='小白证券分析研究平台'
g.title='小白证券分析研究平台(QUANTAXIS版) 设计:荷蒲 QQ:2775205'
g.name='小白证券分析研究平台'
#g.title='小白证券分析研究平台(1.00版) 设计:荷蒲 QQ:2775205'
g.ico='tt.ico'
g.winW=1200
g.winH=800
g.ver=1.01
g.user='18578755056'
g.login=False
g.os=1
g.hqlink=False

#白底色
g.ubg='w'
g.ufg='b'
g.utg='b'
g.uvg='#1E90FF'

##黑底色
g.ubg='#07000d'
g.ufg='w'
g.utg='w'
g.uvg='#FFD700'

g.pyver=int(platform.python_version()[0:1])

#小白框架控件
g.mainform=None
g.frame=None
g.canvas=None
g.figure=None
g.plot=None
g.frame=None
g.tabControl=None
g.tab1=None  #工作台
g.tab2=None  #行情报价
g.tab3=None  #日线图
g.tab4=None  #编写代码
g.tab5=None  #策略回测
g.tab6=None  #分时图
g.tab7=None  #F10
g.tab8=None  #板块
g.tab9=None  #选股
g.tab10=None
g.tab11=None
g.tab12=None
g.tab13=None
g.tab14=None
g.tab15=None
g.tab16=None
g.tab17=None
g.tab18=None
g.tab19=None
g.tab20=None
g.plotPage=None
g.ttree=None
g.scrollBarA =None
g.scrollBarB =None
g.mainmenu=None

g.date_s =None
g.date_e =None
g.stock_i =None
g.book_s =None
g.tabs=None
g.tabn=['工作台','行情报价','日线图','编写代码','策略回测','分时图','F10信息','三画面','四画面']
g.stock_names={}
g.zxg=[[1,'000001'],[0,'399001'],[0,'000776'],[1,'600030']]
g.zxg2=[]
g.zxg3=[]
g.zxg4=[]
g.zxg5=[]
g.zxg6=[]
g.zxg7=[]
g.zxg8=[]
g.zxg9=[]
g.names={}
g.blockname=[]
g.bkdf=[]
g.pys={}

g.UserView=None
g.UserF10View=None
g.inText=None
g.outText=None
#小白框架控件回测
g.UserFrame=None
g.UserFig=None
g.UserPlot=None
g.UserCanvas=None
g.date_tickers=None
#小白框架控件AI输出信息
g.ttext=''
g.ttmsg=None
g.mymsg=None
g.status=None

###########################################
#软件参数
#stype=0 通通本地数据，ts=1,qa=2,jq=3
g.stype=2  #股票数据类型
g.gtype=3  #指标线数量
g.stock='000001' #股票代码 
g.gmarket=0
g.df=None #默认df
g.sday='2018-10-01'
g.eday=time.strftime('%Y-%m-%d',time.localtime(time.time()))
g.index=False
g.formula='PXCPX'
g.MA1=5
g.MA2=10
g.MA3=20
g.MA4=60
g.MA5=120
g.MA6=240
g.MAV1=5
g.MAV2=10
g.money=1000000.00
g.stamp_duty=0.001   #印花税 0.1%
g.trading_Commission=0.0005    #交易佣金0.05%
g.stop_loss_on=True #允许止损
g.stop_loss_max=50 #止损3次,就停止交易
g.stop_loss_range=0.05   #止损幅度

#g.hcdate_s='2019-01-01'
#g.hcdate_e='2020-01-15'
#g.hczj=1000000.00
#g.hczs=0.05 
#g.hczy=0.05 
#g.hczz=0.05 
#g.hcts=3
g.hcstock='000001'
g.mstock='600030'
g.mds='2019-07-10 09:30:00'
g.mde=time.strftime('%Y-%m-%d',time.localtime(time.time()))+' 15:30:00'
g.hctitle=''
g.vstock=g.stock
g.vtitle=''

#--------------
g.ec = {
'open':'开盘',
'Open': '开盘',
'close':'收盘',
'Close':'收盘',
'low':'最低',
'Low':'最低',
'high':'最高',
'High':'最高',
'volume':'成交量',
'Volume':'成交量',
'money':'成交额',
'Money':'成交额',
'date':'日期',
'Date':'日期',}
#--------------
g.cw={
'market':  '市场',
'code':  '代码',
'liutongguben':   '流通股本',
'province' :  '领域',
'industry' :  '行业',
'updated_date' :  '更新日期',
'ipo_date' :   'ipo日期',
'zongguben': '总股本',
'guojiagu': '国家股',
'faqirenfarengu' : '法企人法人股',
'farengu' : '法人股',
'bgu':   'B股',
'hgu' :  'H股',
'zhigonggu': '职工股',
'zongzichan' :  '总资产',
'liudongzichan' : '流动资产',
'gudingzichan' : '固定资产',
'wuxingzichan' : '无形资产',
'gudongrenshu' : '股东人数',
'liudongfuzhai' : '流动负债',
'changqifuzhai' : '长期负债',
'zibengongjijin': '资本公积金',
'jingzichan' :  '净资产',
'zhuyingshouru' : '主营收入',
'zhuyinglirun' :  '主营利润',
'yingshouzhangkuan' : '应手帐款',
'yingyelirun':  '营业利润',
'touzishouyu' : '投资收益',
'jingyingxianjinliu' :'经营现金流',
'zongxianjinliu' :'总现金流',
'cunhuo' : '存货',
'lirunzonghe': '利润总和',
'shuihoulirun': '税后利润',
'jinglirun' : '净利润',
'weifenpeilirun': '未分配利润',
'meigujingzichan': '每股净资产',
'baoliu2' : '保留2'}
#--------------
g.hcursor=[
'num_glyphs',
'X_cursor',
'arrow',
'based_arrow_down',
'based_arrow_up',
'boat',
'bogosity',
'bottom_left_corner',
'bottom_right_corner',
'bottom_side',
'bottom_tee',
'box_spiral',
'center_ptr',
'circle',
'clock',
'coffee_mug',
'cross',
'cross_reverse',
'crosshair',
'diamond_cross',
'dot',
'dotbox',
'double_arrow',
'draft_large',
'draft_small',
'draped_box',
'exchange',
'fleur',
'gobbler',
'gumby',
'hand1',
'hand2',
'heart',
'icon',
'iron_cross',
'left_ptr',
'left_side',
'left_tee',
'leftbutton',
'll_angle',
'lr_angle',
'man',
'middlebutton',
'mouse',
'pencil',
'pirate',
'plus',
'question_arrow',
'right_ptr',
'right_side',
'right_tee',
'rightbutton',
'rtl_logo',
'sailboat',
'sb_down_arrow',
'sb_h_double_arrow',
'sb_left_arrow',
'sb_right_arrow',
'sb_up_arrow',
'sb_v_double_arrow',
'shuttle',
'sizing',
'spider',
'spraycan',
'star',
'target',
'tcross',
'top_left_arrow',
'top_left_corner',
'top_right_corner',
'top_side',
'top_tee',
'trek',
'ul_angle',
'umbrella',
'ur_angle',
'watch',
'xterm']

#########################
g.cns = {
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

g.hcolor=g.cns

########################################
#操作系统类型
def UseOS( ):
    sysstr = platform.system()
    if(sysstr =="Windows" or sysstr =="windows"):
        return 1
    elif(sysstr == "Linux"):
        return 2
    else:
        return 3


def HP_init():
    #软件名称
    g.pyver=int(platform.python_version()[0:1])
    g.os=UseOS( )


#通用平均线计算        
def G_MA(Series,n):
    g.pyver=int(platform.python_version()[0:1])
    g.ma=None
    if g.pyver==2:
        g.MAstr='pd.rolling_mean(Series,n)'
        g.ma=eval(MAstr)
    else :
        g.MAstr='Series.rolling(window=n,center=False).mean()'
        g.ma=eval(MAstr)
    return g.ma

#####################################################
################独狼荷蒲软件版权声明###################
'''
独狼荷蒲软件(或小白软件)版权声明
1、独狼荷蒲软件(或小白软件)均为软件作者设计,或开源软件改进而来，仅供学习和研究使用，不得用于任何商业用途。
2、用户必须明白，请用户在使用前必须详细阅读并遵守软件作者的“使用许可协议”。
3、作者不承担用户因使用这些软件对自己和他人造成任何形式的损失或伤害。
4、作者拥有核心算法的版权，未经明确许可，任何人不得非法复制；不得盗版。作者对其自行开发的或和他人共同开发的所有内容，
    包括设计、布局结构、服务等拥有全部知识产权。没有作者的明确许可，任何人不得作全部或部分复制或仿造。

独狼荷蒲软件
QQ: 2775205
Tel: 18578755056
公众号:独狼股票分析
'''