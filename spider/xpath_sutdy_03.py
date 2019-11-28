#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 11:29
# @Author  : duanhaobin
# @File    : xpath_sutdy_03.py
# @Software: PyCharm
# @desc:    遍历文档树学习

from bs4 import BeautifulSoup

html_text = """<html>
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;and they lived at the bottom of a well.
</p>
<p class="story2">...</p>
</body>
</html>
"""

soup = BeautifulSoup(html_text, 'lxml')
'''
    先明确节点关系：
    子（Children）：一个Tag可能包含多个字符串或其它的Tag,这些都是这个Tag的子节点
    父（Parent）：每个tag或字符串都有父节点
    兄弟（Sibling）：同一个元素的子节点可以成为兄弟节点
'''

'''
    1. 子节点
    .contents    将tag的子节点以列表的方式输出
    .children    生成器,可以对tag的子节点进行循环
    .descendants 对所有tag的子孙节点进行递归循环。包括子节点，及子节点的子节点（子孙节点）
'''

# contents
body_c = soup.body.contents  # 获取body的子节点
print(type(body_c))  # <class 'list'>
print(body_c)

# children  # 获取body子节点的生成器,可以对tag的进行循环
body_ch = soup.body.children
print(type(body_ch))  # <class 'list_iterator'>
print(body_ch)  # <list_iterator object at 0x000001FDD9AC82E8>

for i in body_ch:
    print(i, end='-------')

'''
结果如下，a标签不是子节点，而是孙节点：
(有一个空格,控制台不显示,故特此批注)
-------<p class="title"><b>The Dormouse's story</b></p>-------    (有一个空格,控制台不显示,故特此批注)
-------<p class="story">Once upon a time there were three little sisters; and their names were
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.
</p>-------  (有一个空格,控制台不显示,故特此批注)
-------<p class="story2">...</p>-------   (有一个空格,控制台不显示,故特此批注)
-------
'''

# descendants  descendants 属性可以对所有tag的子孙节点进行递归循环 包括子节点，及子节点的子节点（子孙节点）

body_de = soup.body.descendants
print(type(body_de))  # <class 'generator'>
print(body_de)  # <generator object Tag.descendants at 0x000002112BE2D4F8>
for j in body_de:
    print(j, end='~~~~')

'''
结果为:
~~~~<p class="title"><b>The Dormouse's story</b></p>~~~~<b>The Dormouse's story</b>~~~~The Dormouse's story~~~~
~~~~<p class="story">Once upon a time there were three little sisters; and their names were
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.
</p>~~~~Once upon a time there were three little sisters; and their names were
~~~~<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>~~~~Elsie~~~~,
~~~~<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>~~~~Lacie~~~~ and
~~~~<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>~~~~Tillie~~~~;and they lived at the bottom of a well.
~~~~
~~~~<p class="story2">...</p>~~~~...~~~~
~~~~

观察输出结果：
    descendants属性既包含了子节点也包含了孙节点，并且按顺寻平铺输出
'''


'''
    2. 父节点
    .parent  获取某个元素的父节点
    .parents 递归得到元素的所有父辈节点
'''
# parent  获取某个元素的父节点
parent_t = soup.title.parent  # 获取title标签的父节点  head
print(type(parent_t))  # <class 'bs4.element.Tag'>
print(parent_t)  # <head><title>The Dormouse's story</title></head>
print('---------------------分割线------------------------')
# parents  递归得到元素的所有父辈节点
parents_t = soup.title.parents
print(type(parents_t))  # <class 'generator'>  结果是一个生成器
print(parents_t)  # <generator object PageElement.parents at 0x00000249D795CE58>
print(list(parents_t))

# for k in parents_t:
#     print(k)

'''
结果解析如下，会输出两个<html>节点的内容，是因为parents是所有元素的父辈节点内容，也包含了<head>标签的父节点:
[<head><title>The Dormouse's story</title></head>(第一个), <html>
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.
</p>
<p class="story2">...</p>
</body>
</html>(第二个), <html>
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.
</p>
<p class="story2">...</p>
</body>
</html> (第三个)
]
'''
