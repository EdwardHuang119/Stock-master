# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import time
import gzip
import random
import hashlib
import jieba
import jieba.posseg as pseg
import requests
import threading
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from threading import Timer
import HP_tk as htk
import HP_global as g 

global ttmsg,ttrobot,fanyi
ttmsg=None

#判断是否是英文句子
def isenglish(ss):
    result=True
    for c in ss.lower():
        if c in "abcdefghijklmnopqrstuvwxyz,.' !?":
            continue 
        result=False
        break
    return result
        
#返回文件的全路径
def pp(ppath):
	import os
	return os.path.join(os.getcwd(),os.path.dirname(__file__),ppath)

#知识库类
class zhishiku():
	def __init__(self, q ):	#a是答案（必须是1给）, q是问题（1个或多个）
		self.q = [q]
		self.a = ""
		self.sim = 0
		self.q_vec = []
		self.q_word = []
	def __str__(self):
		return 'q=' + str(self.q) + '\na=' + str(self.a)  + '\nq_word=' + str(self.q_word) + '\nq_vec=' + str(self.q_vec)
		#return 'a=' + str(self.a) + '\nq=' + str(self.q)

#问答类
class FAQrobot():
	def __init__(self, zhishitxt = 'FAQ.txt', lastTxtLen =10, usedVec = False):
		#usedVec 如果是True 在初始化时会解析词向量，加快计算句子相似度的速度
		global ttmsg,ttrobot,fanyi
		self.lastTxt = []	#记录之前输入的问句，方便调试
		self.lastTxtLen = lastTxtLen	#lastTxt数组的长度上限
		self.zhishitxt = zhishitxt
		self.posWeight = {"Ag":1,#形语素
				"a":0.5,#形容词
				"ad":0.5,#副形词
				"an":1,#名形词
				"b":1,#区别词
				"c":0.2,#连词
				"dg":0.5,#副语素
				"d":0.5,#副词
				"e":0.5,#叹词
				"f":0.5,#方位词
				"g":0.5,#语素
				"h":0.5,#前接成分
				"i":0.5,#成语
				"j":0.5,#简称略语
				"k":0.5,#后接成分
				"l":0.5,#习用语
				"m":0.5,#数词
				"Ng":1,#名语素
				"n":1,#名词
				"nr":1,#人名
				"ns":1,#地名
				"nt":1,#机构团体
				"nz":1,#其他专名
				"o":0.5,#拟声词
				"p":0.3,#介词
				"q":0.5,#量词
				"r":0.2,#代词
				"s":1,#处所词
				"tg":0.5,#时语素
				"t":0.5,#时间词
				"u":0.5,#助词
				"vg":0.5,#动语素
				"v":1,#动词
				"vd":1,#副动词
				"vn":1,#名动词
				"w":0.01,#标点符号
				"x":0.5,#非语素字
				"y":0.5,#语气词
				"z":0.5,#状态词
				"un":0.3 } #未知词
		self.usedVec = usedVec
		self.reload()
        
	def reload(self):
		print('知识库开始载入。。。')
		self.zhishiku = []

		with open(pp(self.zhishitxt),encoding='utf-8') as f:
			txt = f.readlines()
			#print(txt)
			abovetxt = 0	#上一行的种类： 0空白/注释  1答案   2问题
			i=0
			for t in txt:	#读取FAQ文本文件
				t1=t
				t=t.strip()
				
				#print(i,len(t),t)
				i=i+1
				if t[:1] == '#' or t == '' or len(t)<2:
					abovetxt = 0
				elif abovetxt !=2:
					if t[:4] == '【问题】':						#输入第一个问题
						self.zhishiku.append(zhishiku(t[4:]))
						abovetxt = 2
					else:										#输入答案文本（非第一行的）
						#self.zhishiku[-1].a += '\n' + t1
						self.zhishiku[-1].a += t1                        
						abovetxt = 1
				else :
					if t[:4] == '【问题】':						#输入问题（非第一行的）
						self.zhishiku[-1].q.append(t[4:])
						abovetxt = 2
					else:										#输入答案文本
						self.zhishiku[-1].a += t1
						abovetxt = 1
		
		for t in self.zhishiku:
			for question in t.q:
				t.q_word.append(set(jieba.cut(question)))

		print('知识库载入完毕！')
		#g.ttext=g.ttext+'知识库载入完毕！\n'
        
	def printKu(self):
		for t in self.zhishiku:
			print(t, '\n')

	def intolastTxt(self, intxt):
		self.lastTxt.append(intxt)
		if len(self.lastTxt) > self.lastTxtLen:
			self.lastTxt.pop(0)
	
	#找出知识库里的和输入句子相似度最高的句子
	def maxSimTxt(self, intxt, simCondision=0.1, simType='simple'):	#simType=simple, simple_POS, vec
		self.intolastTxt(intxt)
		for t in self.zhishiku:
			simList=[]
			questionMaxSim=0
			if simType=='simple':
				for question in t.q_word:
					simValue = self.juziSim_simple(intxt, question)
					if questionMaxSim < simValue : questionMaxSim = simValue  
			t.sim = questionMaxSim
		maxSim = max(self.zhishiku, key = lambda x : x.sim)

		if maxSim.sim < simCondision:
			#return( '抱歉，我没有理解您的意思。')
			return( '')
		else:
			return maxSim.a
	
	#simple: 简单的对比相同词汇数量，得到句子相似度
	def juziSim_simple(self, intxt,questionWordset):	#juziIn输入的句子，juziLi句子库里的句子
		intxtSet = set(  jieba.cut(intxt)) 
		if not len(intxtSet):
			return 0
		simWeight = 0
		for t in intxtSet:
			if t in questionWordset:
				simWeight += 1
		return simWeight/len(intxtSet)

	def answer(self, intxt, simType='simple'):	#simType=simple, simple_POS, vec, all
		if intxt == '-zsk':		#'-zsk'  显示当前所有知识库
			self.printKu()
			return ''
		elif intxt == '-reload':		#-reload 重新载入QA知识库
			self.reload()
			return 'reload完毕'
		elif intxt[:3] == '-s ':	#-s -1 查看上一个问句的结果和中间参数
			return 'pass,   error'
		else:
			if intxt[:3] == '-q ':	#-q -1 重复提问，把当一个问句当做输入
				tmp = intxt.split(' ')
				try:
					intxt = self.lastTxt[int(tmp[-1])]
				except (IndexError,ValueError) as e:
					print(e)
					addlog(time.strftime('%F %R') + '\n输入：' + intxt + '\n' + str(e) + '\n\n')
					return ''
			if not intxt:
				return ''
			outtxt = self.maxSimTxt(intxt, simType='simple') 
			return outtxt

#图灵聊天机器人
def tuling_robot(chedan):
    tuling_data = {
            "key": "4c0206d1ed6444bf8ea970074ee0729d",
            "info": chedan,
            "userid": "18578755056"
    }
    tuling_api_url = 'http://www.tuling123.com/openapi/api'
    t = requests.post(tuling_api_url, data=tuling_data)
    return(eval(t.text)["text"])

#茉莉聊天机器人
def moli_robot(chedan):
    moli_data = {
        "question": chedan,
        "api_key": "685b5f0616a5b96b93dc98eea923f42d",
        "api_secret": "se3r9w2wbjdu"
    }
    moli_api_url = 'http://i.itpk.cn/api.php'
    m = requests.post(moli_api_url, data=moli_data)
    if m=='NULL' or m.text=='NUL' or len(m.text)<1:
        m.text='发呆中~~~'
    return( m.text)

#问答及机器人初始化
def robot_init():
    global ttmsg,ttrobot,fanyi
    fanyi = YouDaoFanyi()
    ttrobot = FAQrobot('FAQ.txt', usedVec = False)

#多线程启动函数
def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    #t.setDaemon(True) 
    # 启动
    t.start()

def robot_init2():
    thread_it(robot_init2)
    
#运行用户代码
def EXEC(st):
    try:
        exec(st)
        return('命令运行完成。')   
    except Exception as e:
        return('用户命令出错:'+str(e))
    return('命令运行完成。')   


#小白聊天机器人
def tt_robot(xxx,ai='通通'):
    global ttmsg,ttrobot,fanyi
    en=0
    huida=''
    xx=xxx.strip()
    if len(xx)>0:
        if xx[0:1]=='@':
            huida='茉莉：'+moli_robot(xx[1:])
            return(huida)
        if xx[0:1]=='*':
            huida=ai+'：'+tuling_robot(xx[1:])
            return(huida)       
        if xx[0:1]=='?':
            huida='计算结果：'+str(eval(xx[1:]))
            return(huida)       
        if xx[0:1]=='>':
            xx2=xx[1:]
            xx2=xx2.strip()
            thread_it(EXEC,xx2)    
            
    if xxx.upper()=='RELOAD':
        robot = FAQrobot('FAQ.txt', usedVec = False)
        xxx=''
        huida=''
        return(huida)            
    if isenglish(xxx) and len(xxx)>4:
        result = fanyi.crawl(xxx)
        xxx=result
        en=1

    if xxx[:2].strip()=='翻译':
        xxx1=xxx[2:]
        if len(xxx1)<2:
            return(huida)  
        result = fanyi.crawl(xxx1)
        huida='翻译：'+result
        xxx=result
        return(huida)   
		         
    huida=ttrobot.answer(xxx,'simple')
    if en==1 and len(huida)>1:
        huida= fanyi.crawl(huida)
    if len(huida)<2:
        huida=tuling_robot(xxx)
        #print('回复：'+huida+'\n')
    
    return(huida)
    
#有道翻译    
class YouDaoFanyi(object):
    def crawl(self,word):
        url= "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        data={}
        head={}
        ctime=int(time.time()*1000)
        r=str(ctime + random.randint(1,10))
        s='fanyideskweb'
        d='aNPG!!u6sesA>hBAW1@(-'
        data['i']=word
        data['from']='AUTO'
        data['to']='AUTO'
        data['smartresult']='dict'
        data['client']='fanyideskweb'
        data['salt']=r
        data['sign']=hashlib.md5((s + word + r + d).encode('utf-8')).hexdigest()
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_CLICKBUTTION'
        data['typoResult'] = 'false'
        head['Accept'] = 'application/json, text/javascript, */*; q=0.01'  
        head['Accept-Encoding'] = 'gzip, deflate'  
        head['Accept-Language'] = 'zh-CN,zh;q=0.9'  
        head['Connection'] = 'Keep-Alive'  
        head['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'  
        head['Cookie'] = 'OUTFOX_SEARCH_USER_ID=-1645744815@10.169.0.84; JSESSIONID=aaa9_E-sQ3CQWaPTofjew; OUTFOX_SEARCH_USER_ID_NCOO=2007801178.0378454; fanyi-ad-id=39535; fanyi-ad-closed=1; ___rl__test__cookies=' + str(ctime)  
        head['Host'] = 'fanyi.youdao.com'  
        head['Origin'] = 'http://fanyi.youdao.com'  
        head['Referer'] = 'http://fanyi.youdao.com/'  
        head[ 'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'  
        head['X-Requested-With'] = 'XMLHttpRequest'     
        data = urllib.parse.urlencode(data).encode('utf-8')
        req=urllib.request.Request(url,data,head)
        response = urllib.request.urlopen(req)  
        with gzip.open(response, 'rb') as f:  
            html = f.read()  
        target=json.loads(html)
        result = target['translateResult'][0][0]['tgt']  
        return result


#聊天机器人窗口
def mytalk(root):
    filename=''
    
    #创建几个frame作为容器
    frame_top   = Frame(root,width=1100, height=500, bg='white') 
    frame_center2  = Frame(root,width=1100, height=30)
    frame_center  = Frame(root,width=1100, height=120, bg='#FFF8DC')
    frame_bottom  = Frame(root,width=1180, height=30) 
    
    ##创建需要的几个元素
    text_msg2 = Text(frame_top,bg='#FFFFFF')
    g.ttmsg=text_msg2
    scroll = Scrollbar(text_msg2)
    text_msg2.config(yscrollcommand=scroll.set)
    scroll.config(command=text_msg2.yview)
    scroll.pack(side=RIGHT,fill=Y)
    
    #创建一个绿色的tag
    text_msg2.tag_config('green', foreground='#008B00')   
    text_msg2.tag_config('red', foreground='#FF0000')
    text_msg2.tag_config('blue', foreground='#0000FF')
    text_msg2.tag_config('gold', foreground='#FFD700')  
                         
    def tb1():
        text_msg2.delete(1.0,END)

    def tb2():
        text_msg.delete(1.0,END)

    def tb3():
        text_msg.delete(1.0,END)
        text_msg.insert(END, '? ') 

    def tb4():
        text_msg.delete(1.0,END)
        text_msg.insert(END, '> ') 

    def tb5():
        text_msg.delete(1.0,END)
        text_msg.insert(END, '* ') 

    def tb6():
        text_msg.delete(1.0,END)
        text_msg.insert(END, '@ ') 
    
    #发送信息
    def sendmessage(ai='通通'): 
        msgcontent = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n ' 
        text_msg2.insert(END, msgcontent, 'green') 
        xx=text_msg.get('0.0', END)
        text_msg2.insert(END, xx)
        text_msg.delete('0.0', END)
        txt=tt_robot(xx)
        if len(txt.strip())<1:
            text_msg2.see(END)
            return
        msgcontent = ai+':' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n ' 
        text_msg2.insert(END, msgcontent, 'green') 
        text_msg2.insert(END,txt+'\n','blue')
        text_msg2.see(END)
        
    #按钮
    toolbar = Frame(frame_center2,height=20)
    toolbarName = ('清空信息窗','清空输入框','计算','呼叫通通','呼叫茉莉')
    toolbarCommand = (tb1,tb2,tb3,tb5,tb6)
    #toolbarName = ('清空信息窗','清空输入框')
    #toolbarCommand = (tb1,tb2)    
    def addButton(name,command):
        for (toolname ,toolcom) in zip(name,command):
            shortButton = Button(toolbar,text=toolname,relief='groove',command=toolcom)
            shortButton.pack(side=LEFT,padx=2,pady=5)

    
    addButton(toolbarName,toolbarCommand) #调用添加按钮的函数
                       
    
    text_msg   = Text(frame_center,bg='#FFF8DC',width=20,height=10)
    g.mymsg=text_msg
    button_sendmsg   = Button(frame_bottom, text='发送', command=lambda :thread_it(sendmessage))
    
    #使用grid设置各个容器位置
    frame_top.pack(expand=YES,fill=BOTH,side=TOP)
    frame_center2.pack(fill=X)
    frame_center.pack(fill=X)
    frame_bottom.pack(fill=X,side=BOTTOM)    
    
    text_msg2.pack(expand=YES,fill=BOTH)
    toolbar.pack(side=LEFT) 
    text_msg.pack(fill=X)
    button_sendmsg.pack(side=LEFT) 

#用户输出信息
def tprint(txt):
    global ttmsg
    ttmsg.insert(END, txt)
    ttmsg.see(END)

#用户输出信息,带颜色
def ttprint(txt,color):
    global ttmsg
    ttmsg.insert(END, txt,color)
    ttmsg.see(END)

##聊天机器人类
#class talkman(tmsg):
#    def __init__(self, root=None):  
#        global ttmsg
#        filename=''
#    
#
#    
#    ##创建需要的几个元素
#    text_msg2 = ttmsg
#    
#    #创建一个绿色的tag
#    text_msg2.tag_config('green', foreground='#008B00')   
#    text_msg2.tag_config('red', foreground='#FF0000')
#    text_msg2.tag_config('blue', foreground='#0000FF')
#    text_msg2.tag_config('gold', foreground='#FFD700')  
#                         
#    def tb1():
#        text_msg2.delete(1.0,END)
#
#    def tb2():
#        text_msg.delete(1.0,END)
#
#    def tb3():
#        text_msg.delete(1.0,END)
#        text_msg.insert(END, '? ') 
#
#    def tb4():
#        text_msg.delete(1.0,END)
#        text_msg.insert(END, '> ') 
#
#    def tb5():
#        text_msg.delete(1.0,END)
#        text_msg.insert(END, '* ') 
#
#    def tb6():
#        text_msg.delete(1.0,END)
#        text_msg.insert(END, '@ ') 
#    
#    #发送信息
#    def sendmessage(ai='通通'): 
#        msgcontent = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n ' 
#        text_msg2.insert(END, msgcontent, 'green') 
#        xx=text_msg.get('0.0', END)
#        text_msg2.insert(END, xx)
#        text_msg.delete('0.0', END)
#        txt=tt_robot(xx)
#        if len(txt.strip())<1:
#            text_msg2.see(END)
#            return
#        msgcontent = ai+':' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n ' 
#        text_msg2.insert(END, msgcontent, 'green') 
#        text_msg2.insert(END,txt+'\n','blue')
#        text_msg2.see(END)
#        
#    #按钮
#    toolbar = Frame(frame_center2,height=20)
#    toolbarName = ('清空信息窗','清空输入框','计算','呼叫通通','呼叫茉莉')
#    toolbarCommand = (tb1,tb2,tb3,tb5,tb6)
#    #toolbarName = ('清空信息窗','清空输入框')
#    #toolbarCommand = (tb1,tb2)    
#    def addButton(name,command):
#        for (toolname ,toolcom) in zip(name,command):
#            shortButton = Button(toolbar,text=toolname,relief='groove',command=toolcom)
#            shortButton.pack(side=LEFT,padx=2,pady=5)
#
#    
#    addButton(toolbarName,toolbarCommand) #调用添加按钮的函数
#                       
#    
#    text_msg   = Text(frame_center,bg='#FFF8DC',width=20,height=10)
#    g.mymsg=text_msg
#    button_sendmsg   = Button(frame_bottom, text='发送', command=lambda :thread_it(sendmessage))
#    
#    #使用grid设置各个容器位置
#    frame_top.pack(expand=YES,fill=BOTH,side=TOP)
#    frame_center2.pack(fill=X)
#    frame_center.pack(fill=X)
#    frame_bottom.pack(fill=X,side=BOTTOM)    
#    
#    text_msg2.pack(expand=YES,fill=BOTH)
#    toolbar.pack(side=LEFT) 
#    text_msg.pack(fill=X)
#    button_sendmsg.pack(side=LEFT) 