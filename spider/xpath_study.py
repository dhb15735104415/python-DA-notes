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

'''
    网页标签解析步骤记录
'''
html_text = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" hb="test"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

'''
    1.用BeautifulSoup解析网页代码 文档树格式化输出
'''
soup = BeautifulSoup(html_text, "lxml")
print(type(soup))  # <class 'bs4.BeautifulSoup'>  BeautifulSoup对象
print(soup)  # 平铺输出
print('--------------------分割线------------------------')
# soup.prettify()  以Unicode编码输出,每个XML/HTML标签都独占一行
print(soup.prettify())

'''
    2.HTML的3个基本要素识别：标签、属性、元素
'''
# 1) 标签  soup.标签名
# 首先要知道有这样找到标签的方法 后续主要用.find() / .find_all()来寻找
print(soup.title)  # <title>The Dormouse's story</title>

# 2) 属性
'''
    soup.标签名.attrs  返回属性，对象类型为字典  如果存在多个同名标签，则返回第一个找到的标签属性
    soup.标签名['属性名'] 返回该标签的某属性  类似字典的读取操作
'''
print(soup.p.attrs)  # {'class': ['title'], 'hb': 'test'}
print(soup.p.attrs['hb'])  # test

# 3) 元素
'''
    soup.标签名.text 直接输出字符串str
    soup.标签名.text 与 soup.标签名.string → 选择前者
    后者在tag 包含了多个子节点时，.string 方法无法确定应该调用哪个子节点的内容, .输出结果有可能是 None
'''
html_text2 = '''<html>
<td>some text</td> 
<td></td>
<td><p>more text</p></td>
<td>even <p>more text</p></td>
</html>'''
soup2 = BeautifulSoup(html_text2, 'lxml')
tds = soup2.findAll('td')
print('tds----', tds)  # tds---- [<td>some text</td>, <td></td>, <td><p>more text</p></td>, <td>even <p>more text</p></td>]

# 先用soup.标签名.text
for td1 in tds:
    print(td1.text)
'''
    结果为:
    some text

    more text
    even more text
'''
# 先用soup.标签名.string
for td2 in tds:
    print(td2.string)
'''
    结果为:
    some text
    None
    more text
    None
'''
