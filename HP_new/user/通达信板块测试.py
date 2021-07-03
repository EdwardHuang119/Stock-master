import HP_global as g   #建立全局数据域g
import HP_tdx as htdx   #导入通达信模块
#返回板块中所有股票
tdxapi=htdx.TdxInit()
bk=htdx.getblock2('沪深300')
print(bk)

#获取股票所属板块名
bk2=htdx.getblock3('600030')
print(bk2)
