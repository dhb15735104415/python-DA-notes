#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 10:00
# @Author  : duanhaobin
# @File    : test_driver.py
# @Software: PyCharm
# @desc:   测试google webdriver是否安装好

from selenium import webdriver

chrome_driver = 'F:\GoogleWebDriver\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver)
    # 启动webDriver


