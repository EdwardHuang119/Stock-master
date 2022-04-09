#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO 使用from...import从pyecharts.charts中导入Bar模块
from pyecharts.charts import Bar
# TODO 使用from...import从pyecharts中导入options模块并简写为opts
from pyecharts import options as opts

# # 将公司的名字存入变量名为"name"的列表中
# name = ["ibm","microsoft","pwc","citi","amazon","apple","ey","walmart","siemens","google"]
# # 按照公司名字的顺序，依次将公司的人数存入变量名为"employee"的列表中
# employee = [274047,116196,111372,101482,93247,90095,158363,120753,87381,75109]
# # TODO 创建Bar对象，并赋值给bar
# bar = Bar()
# # TODO 传入参数xaxis_data=name使用add_xaxis()设置x轴为公司名称
# # TODO 传入参数xaxis_data=name使用add_xaxis()设置x轴为公司名称
# bar.add_xaxis(xaxis_data = name)
# # TODO 传入参数y_axis=employee使用add_yaxis()设置y轴，series_name设置为空
# bar.add_yaxis(series_name = '',y_axis = employee)
# # TODO 使用render()绘制柱状图保存到"/Users/company_size.html"
# bar.render("/Users/Mac/PycharmProjects/Stock-master/Yequ/data visualization/practisedata/company_size.html")


# 设置列表
months = ["1月","2月","3月","4月","5月","6月","7月", "8月", "9月", "10月", "11月", "12月"]
choc_sales=[2045,2580,2789,3455,3256,3678,5340,6078,6460,6475,7431,8038]
gum_sales=[1234,1467,1754,2354,2897,3487,4340,4379,4460,5075,5431,6038]
walnut_sales=["-", "-", "-","-", "-", "-",6340,5579,4460,4075,3431,3038]

# TODO 创建Bar对象，赋值给变量bar
bar=Bar()

# TODO 使用add_xaxis()函数，添加参数xaxis_data，将参数值设置为months
bar.add_xaxis(months)

# 使用add_yaxis()函数
# 将图例设置为“巧克力”
# y轴数值设置为列表choc_sales
# 添加参数stack，将值设置为sales
# 添加参数label_opts，将其值设置为标签配置项opts.LabelOpts()，参数position，设置为"inside"
bar.add_yaxis(
    series_name="巧克力",
    y_axis=choc_sales,
    stack="sales",
    label_opts=opts.LabelOpts(position="inside")
    )

# 使用add_yaxis()函数
# 将图例设置为“口香糖”
# y轴数值设置为列表gum_sales
# 添加参数stack，将值设置为sales
# 添加参数label_opts，将其值设置为标签配置项opts.LabelOpts()，参数position，设置为"inside"
bar.add_yaxis(
    series_name="口香糖",
    y_axis=gum_sales,
    stack="sales",
    label_opts=opts.LabelOpts(position="inside")
    )

# TODO 使用add_yaxis()函数
# 将图例设置为“核桃”
# y轴数值设置为列表walnut_sales
# 添加参数stack，将值设置为sales
# 添加参数label_opts，将其值设置为标签配置项opts.LabelOpts()，参数position，设置为"inside"
bar.add_yaxis("核桃",walnut_sales,stack="sales",label_opts=opts.LabelOpts(position="inside"))

# TODO 使用reversal_axis()，让图片xy轴翻转
bar.reversal_axis()

# 使用全局配置项，设置标题为"2020全年商品销售额变化"
bar.set_global_opts(
    title_opts=opts.TitleOpts(title="2020全年商品销售额变化")
    )

# 使用render函数将堆积柱状图保存在指定路径
bar.render("/Users/Mac/PycharmProjects/Stock-master/Yequ/data visualization/practisedata/bar_stack.html")