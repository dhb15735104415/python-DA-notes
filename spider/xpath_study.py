#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 23:27
# @Author  : duanhaobin
# @File    : xpath_study.py
# @Software: PyCharm
# @desc: Xpath学习

'''
    一、概念
        Xpath即为XML路径语言（XML Path Language），它是一种用来确定XML文档中某部分位置的语言
        Xpath也可以用于定位html的标签
        Xpath就像是一个地址，可以找到网页代码里你需要的数据

        xpath就是在定位html的标签位置
    二、基本语法
        /	从根节点选取
        //	从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置
        @	选取属性
        *通配符
            *：匹配任何元素节点
            @*：匹配任何属性
            //*：选择文档中的所有元素节点
            //ul/*：选择ul元素中的所有子节点
            //a[@*]：选择所有带属性的a节点
    三、使用
        完整路径：是从根节点开始，不常用  eg: /html/body/div[2]/div[2]/div[2]/ul/li[1]/img
        相对路径：一般会使用class或者id定位   eg: //ul[@class="toturial-list video-list"]/li/img
                                        eg: //*[@id="wrapper"]/h1/span
    四、BeautifulSoup如何调用xpath解析器
        BeautifulSoup支持Python标准库中的HTML解析器,还支持一些第三方的解析器,其中一个是 lxml
        BeautifulSoup支持多种解析器
        eg: BeautifulSouo(markup,'lxml')
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
soup = BeautifulSoup(html_text, "lxml")
print(type(soup))  # <class 'bs4.BeautifulSoup'>  BeautifulSoup对象
print(soup)

