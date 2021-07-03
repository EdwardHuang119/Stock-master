# -*- coding: utf-8 -*-
# 显示2个K线图的模板
import  tkinter  as  tk   #导入Tkinter
import  tkinter.ttk  as  ttk   #导入Tkinter.ttk
import  tkinter.tix  as  tix   #导入Tkinter.tix
import time
import pandas as pd
import numpy as np
import HP_global as g 
import HP_data as hp
from HP_view import * #菜单栏对应的各个子页面 
import HP_tdx as htdx

'''
查询公司信息目录
    name    filename   start  length
0   最新提示  000776.txt       0   13477
1   公司概况  000776.txt   13477   18703
2   财务分析  000776.txt   32180   28283
3   股东研究  000776.txt   60463   16935
4   股本结构  000776.txt   77398    3437
5   资本运作  000776.txt   80835   18565
6   业内点评  000776.txt   99400   34554
7   行业分析  000776.txt  133954   38922
8   公司大事  000776.txt  172876   63519
9   港澳特色  000776.txt  236395   17899
10  经营分析  000776.txt  254294   20236
11  主力追踪  000776.txt  274530   14745
12  分红扩股  000776.txt  289275  139365
13  高层治理  000776.txt  428640   36667
14  龙虎榜单  000776.txt  600079    7961
15  关联个股  000776.txt  465307  134772
'''


txt=htdx.get_F10(g.mstock,'股东研究')
tprint(txt)     