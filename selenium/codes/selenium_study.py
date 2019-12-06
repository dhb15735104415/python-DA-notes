#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 10:58
# @Author  : duanhaobin
# @File    : selenium_study.py
# @Software: PyCharm
# @desc:   Selenium基本语法练习


from selenium import webdriver

chrome_driver = 'F:\GoogleWebDriver\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver)
# 启动webDriver

# 访问具体网址 get()
browser.get("https://book.douban.com")

# current_url 返回网页网址
print(browser.current_url)

# get_cookies() 返回cookies
print(browser.get_cookies())

'''
    定位元素
        定位单个元素
            find_element_by_id()  常用  返回匹配id属性名的第一个元素。如果没有元素具有匹配的类属性名，则会报错NoSuchElementException
            find_element_by_name()
            find_element_by_xpath()  常用
            find_element_by_link_text()
            find_element_by_partial_link_text()
            find_element_by_tag_name()  常用  返回带有给定tag name的第一个元素...
            find_element_by_class_name()  常用  返回匹配class属性名的第一个元素 ...
            find_element_by_css_selector()
        定位一组元素，返回1个list（类似bs里的find_all()）
            find_elements_by_name()  常用
            find_elements_by_xpath()  常用
            find_elements_by_link_text()
            find_elements_by_partial_link_text()
            find_elements_by_tag_name()  常用  通过标签的共同特征寻找
            find_elements_by_class_name()  常用  通过属性的共同特征寻找
            find_elements_by_css_selector()
'''

# find_element_by_xpath() 通过xpath定位单个元素
book_href = browser.find_element_by_xpath(
    '//*[@id="content"]/div/div[1]/div[1]/div[2]/div/div/ul[2]/li[1]/div[1]/a').click()

# find_element_by_id() 通过id定位单个元素
div_id = browser.find_element_by_id('content')

# find_element_by_tag_name()
tag_name = browser.find_element_by_tag_name('h1')
print(tag_name.text)  # 兔子洞女孩

# find_elements_by_tag_name() 获取多个元素
tag_name_h2 = browser.find_elements_by_tag_name('h2')
for tag_h2 in tag_name_h2:
    print(tag_h2.text)

# 通过单个元素定位 + 循环迭代xpath获取一组元素
h2lst = []

for i in range(1, 2):
    xpathi = '//*[@id="content"]/div/div[1]/div[3]/h2[%i]' % i
    h2 = browser.find_element_by_xpath(xpathi).text
    print(h2)
    h2lst.append(h2)
print(h2lst)

'''
    定位元素后有哪些操作
        .size：返回元素尺寸
        .text ：返回元素文本
        .get_attribute(name)：获得属性值
        .find_....：继续识别
        .click()：点击按钮
'''

info_id = browser.find_element_by_id('info')
print(info_id.size)  # {'height': 208, 'width': 180}
print(info_id.find_element_by_tag_name('a').get_attribute('href'))  # https://book.douban.com/author/275618


'''
    实现网页的账号登陆
'''
print(browser.current_url)
# 找到登陆链接，并点击登陆
login_href = browser.find_element_by_xpath('//*[@id="db-global-nav"]/div/div[1]/a').click()
# 选择账号密码登陆
login_input = browser.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click()

# 找到账号密码 input标签
username = browser.find_element_by_id('username')
password = browser.find_element_by_id('password')

# 清空页面字符 并设置相关数值
username.clear()
password.clear()
username.send_keys('************')
password.send_keys('************')

# 找到登陆按钮 并点击
login_button = browser.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()
print(browser.current_url)

# 退出登陆
login_out = browser.find_element_by_xpath('//*[@id="db-global-nav"]/div/div[1]/ul/li[2]/div/table/tbody/tr[5]/td/a').click()
print(browser.current_url)