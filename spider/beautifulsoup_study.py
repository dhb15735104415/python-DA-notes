#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 19:51
# @Author  : duanhaobin
# @File    : beautifulsoup_study.py
# @Software: PyCharm
# @desc: BeautifulSoup基本语法学习

'''
什么是BeautifulSoup
    Beautiful Soup 是一个可以从HTML或XML文件中提取数据的Python库.它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式
'''
from bs4 import BeautifulSoup

html_text = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
# 用BeautifulSoup解析网页代码
soup = BeautifulSoup(html_text, features="lxml")
print(type(soup))  # <class 'bs4.BeautifulSoup'>  BeautifulSoup对象
print(soup)
# 输出网页的文本内容
print(soup.text)

# 输出title标签
print(soup.title)  # <title>The Dormouse's story</title>

# 输出title标签的名字
print(soup.title.name)  # title

# 输出p标签
print(soup.p)  # <p class="title"><b>The Dormouse's story</b></p>

# 输出p标签中class的内容
print(soup.p['class'])  # ['title']

# 输出第一个a标签
print(soup.find('a'))  # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

# 输出所有a标签
print(soup.findAll('a'))  # 输出结果为ResultSet，包含所有的a标签

print(type(soup.findAll('a')))  # <class 'bs4.element.ResultSet'>
'''
    A ResultSet is just a list that keeps track of the SoupStrainer that created it.
'''
