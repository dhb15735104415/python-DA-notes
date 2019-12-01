#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/11/23 3:00
# @Author  : duanhaobin
# @File    : xpath_study_02.py
# @Software: PyCharm
# @desc: 主要学习搜索文档树

from bs4 import BeautifulSoup
'''
    核心方法：find() 和 find_all()
'''
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
    1.find(name , attrs, ...) 
    寻找标签，可以通过属性寻找
    注意：由于class在Python中是内置语句，所以class的属性应该加下划线：class_
    可以通过.text直接输出元素    
'''
print(soup.find('head'))  # <head><title>The Dormouse's story</title></head>

print(soup.find('a', id='link2'))  # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

print(soup.find('p', class_='story'))
'''
    结果为；
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
    <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.
    </p>
'''
# .text直接输出元素
print(soup.find('p', class_='story').text)  # 保留原格式输出 包括换行等
'''
    Once upon a time there were three little sisters; and their names were
    Elsie,
    Lacie and
    Tillie;and they lived at the bottom of a well.
'''

print('-------------------findAll 开始----------------------------------')

'''
    2.find_all( name , attrs , ...)
    寻找所有tag子节点标签
    可以寻找多个标签  
'''
a_tags = soup.findAll('a', class_='sister')
print(a_tags)
for i in a_tags:
    print(i)

print('-----------------ap  开始----------------------')
ap_tags = soup.findAll(['a', 'p'])  # 寻找多个标签(a , p 标签)，按网页代码顺序输出
print(ap_tags)
print('------------------ap 遍历------------------------')
for i in ap_tags:
    print(i)

'''
    结果为：  为啥输了两遍a标签? 因为第二个<p>标签子节点都是<a>,find_all()找出全部符合条件的
    <p class="title"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
    <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.
    </p>
    <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
    <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
    <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
    <p class="story2">...</p>
'''