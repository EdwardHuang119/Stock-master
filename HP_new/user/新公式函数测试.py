import matplotlib.pyplot as plt
import HP_global as g
import HP_tdx as htdx
from HP_sys import *
import tkinter as tk
import HP_global as g 
import HP_data as hp
import  HP_tdxgs as gs

global CW,BASE2,NAME,PY
global mydf,MYDF
global CLOSE,LOW,HIGH,OPEN,VOL,AMOUNT
global C,L,H,O,V,AMO,VOLUME
global PERIOD,DATE,TIME,YEAR,MONTH,WEEKDAY,DAY,HOUR,MINUTE
global CODE,MARKET,SETCODE
global MINDIFF,TQFLAG,USEDDATANUM,MULTIPLIER
global TOTALCAPITAL,CAPITAL,TYPE2


global CLOSE,LOW,HIGH,OPEN,VOL
global C,L,H,O,V
stockn='600030'
df3=gs.get_security_bars(nCategory=4,nMarket =-1,code=stockn, nStart=0, nCount=240)
CW=gs.CW()
BASE2=gs.BASE2()
NAME=gs.NAME()
PY=gs.PY()
mydf=MYDF=gs.MYDF()
CLOSE=C=gs.CLOSE()
LOW=L=gs.LOW()
HIGH=H=gs.HIGH()
OPEN=O=gs.OPEN()
VOL=V=VOLUME=gs.VOL()
AMOUNT=AMO=gs.AMO()
PERIOD=gs.PERIOD()
DATE=gs.DATE()
TIME=gs.TIME()
YEAR=gs.YEAR()
MONTH=gs.MONTH()
WEEKDAY=gs.WEEKDAY()
DAY=gs.DAY()
HOUR=gs.HOUR()
MINUTE=gs.MINUTE()
CODE=gs.CODE()
MARKET=gs.MARKET()
SETCODE=gs.SETCODE()
MINDIFF=gs.MINDIFF()
TQFLAG=gs.TQFLAG()
USEDDATANUM=gs.USEDDATANUM()
MULTIPLIER=gs.MULTIPLIER()
TOTALCAPITAL=gs.TOTALCAPITAL()
CAPITAL=gs.CAPITAL()
TYPE2=gs.TYPE2()
def FINANCE(n):
    import  HP_tdxgs as gs
    return gs.FINANCE(n)







print(CODE,NAME,CAPITAL,FINANCE(1))


