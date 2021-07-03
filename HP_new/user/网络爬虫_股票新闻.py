# -*- coding: utf-8 -*-
#网络爬虫演示
import  tkinter  as  tk   #导入Tkinter
import requests
#from bs4 import BeautifulSoup
import bs4
import HP_global as g

#用户输出信息
def tprint(txt):
    if g.outText==None:
        g.ttmsg.insert(tk.END, txt)
        g.ttmsg.see(tk.END)
    else:
        g.outText.insert(END, txt)
        g.outText.see(END)        


#获取网页或网页文件的内容
def getHTMLText(url):
    import requests
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

#获取新闻利好的演示
url2='http://stock.stockstar.com/list/4957.shtml'
htmla = getHTMLText(url2) 
soupa = bs4.BeautifulSoup(htmla, 'html.parser') 
info= soupa.find('div',attrs={'class':'listnews'})
#tprint(htmla)
a = info.find_all('a')
#print('\n股票新闻：')
mymess='\n股票新闻：\n'
for i in a:
    try:
        #href = i.attrs['href']
        #print(i.string)
        mymess=mymess+i.string+'\n'
    except:
        continue

tprint(mymess)



