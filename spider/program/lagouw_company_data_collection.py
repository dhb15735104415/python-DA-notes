#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 14:53
# @Author  : duanhaobin
# @File    : lagouw_company_data_collection.py
# @Software: PyCharm
# @desc:    拉勾网招聘公司信息采集
# 循环li标签时的同时如何用xpath来定位标签
# 如何通过设置交互实现 - 翻页处理

import time
import random
import re
import pymongo
import time
from selenium import webdriver
import warnings
warnings.filterwarnings('ignore')
    # 不发出警告

def login(url, username_str, password_str):
    '''
    登陆
    :param url: 拉勾网网址
    :param username_str: 用户名
    :param password_str: 密码
    :return: 返回当前url
    '''
    browser.get(url)
    browser.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[1]/a').click()
    browser.find_element_by_xpath('//*[@id="lg_tbar"]/div/div[1]/ul/li[3]/a').click()
        # 点击公司标签 进入公司页面
    sleeptime = random.randint(1, 2)
    time.sleep(sleeptime)
    browser.find_element_by_xpath('//*[@id="lg_tbar"]/div/div[2]/ul/li[3]/a').click()
    username = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div['
                                             '1]/form/div[1]/div/input')
    password = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div['
                                             '1]/form/div[2]/div/input')
    username.clear()
    password.clear()
    username.send_keys(username_str)
    password.send_keys(password_str)

    browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]').click()
        # 登陆
    print('登陆成功，返回目前网址：', browser.current_url)
    return browser.current_url


def get_datas(u, table, page_n):
    '''
    访问页面 + 采集公司信息
    :param u:数据页面网址
    :param table:MongoDB集合对象
    :param page_n:分页参数
    :return:采集数据条数
    '''
    browser.get(u)
    for page in range(page_n):
        ul = browser.find_element_by_xpath('//*[@id="company_list"]/ul')
        lilist = ul.find_elements_by_tag_name('li')
        for i in range(len(lilist)):
            dic = {}
            dic['公司名称'] = lilist[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%i]/div[1]/h3' % (i+1)).text
            infor1 = lilist[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%i]/div[1]/h4[1]' % (i+1)).text
            infor1 = re.split(r'/', infor1)
            dic['行业'] = infor1[0]
            dic['融资情况'] = infor1[1]
            dic['公司规模'] = infor1[2]
            dic['公司愿景'] = browser.find_element_by_xpath('//*[@id="company_list"]/ul/li[%i]/div[1]/h4[2]' % (i+1)).text
            infor2 = browser.find_element_by_xpath('//*[@id="company_list"]/ul/li[%i]/div[2]' % (i+1)).text
            infor2 = re.split(r'\n.*\n', infor2)
            dic['面试评价数量'] = infor2[0]
            dic['在招职位数量'] = infor2[1]
            dic['简历处理率'] = infor2[2].split('%')[0]
            table.insert_one(dic)
            n += 1
        browser.find_element_by_class_name('pager_container').find_element_by_class_name('pager_next ').click()
            # 点击下一页
        sleeptime = random.randint(1, 5)
        time.sleep(sleeptime)
            # 适当停留
        print('成功采集%i条数据,休眠%i秒' % (n, sleeptime))


if __name__ == '__main__':
    chrome_driver = 'F:\GoogleWebDriver\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=chrome_driver)
    url = login('https://www.lagou.com', 'xxxxx', 'xxxxx')

    myclient = pymongo.MongoClient('mongodb://localhost:27017')
    db = myclient['拉勾网信息']
    collection_table = db['公司职位信息']
    try:
        get_datas(url, collection_table, 10)
    except:
        print('数据采集异常')