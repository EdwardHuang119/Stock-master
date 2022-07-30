#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 使用from...import从pyecharts.charts中导入Graph
from pyecharts.charts import Graph

# 存储基本新的列表info
info = [ {"id": "Jon", "name": "Jon"},
         {"id": "Jac", "name": "Jac"},
         {"id": "Ten", "name": "Ten"},
         {"id": "Bla", "name": "Bla"},
         {"id": "Ann", "name": "Ann"},
         {"id": "Ace", "name": "Ace"},
         {"id": "Tom", "name": "Tom"},
         {"id": "Gra", "name": "Gra"}]

# 存储合作关系的列表coo
coo =  [ {"source":"Jon", "target":"Tom"},
         {"source":"Jon", "target":"Gra"},
         {"source":"Jon", "target":"Ace"},
         {"source":"Jon", "target":"Tom"},
         {"source":"Jac", "target":"Ten"},
         {"source":"Jon", "target":"Jac"},
         {"source":"Jac", "target":"Bla"},
         {"source":"Jon", "target":"Ann"}]

# 使用Graph()函数创建对象赋值给graph
graph = Graph()

# TODO 调用add()函数，设置series_name为空
# 将info赋值给nodes，将coo赋值给links
graph.add(
    "",
    nodes=info,
    links=coo
)

# TODO 使用render()生成文件存储/Users/bing/graph.html
graph.render("/Users/Mac/PycharmProjects/Stock-master/Yequ/data visualization/practisedata/graph.html")