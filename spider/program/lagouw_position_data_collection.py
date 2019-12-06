#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 9:10
# @Author  : duanhaobin
# @File    : lagouw_position_data_collection.py
# @Software: PyCharm
# @desc:   拉勾网职位信息采集并储存到MongoDB
# 注意设置延时
# time模块
# random模块
# 页面数据采集 - 配合正则解析标签

import time
import random
import pymongo
import re
from selenium import webdriver
import warnings
warnings.filterwarnings('ignore')
    # 不发出警告


def login(u, username_str, password_str):
    '''
    登陆拉勾网
    :param u:拉勾网网址
    :param username: 用户名
    :param password: 密码
    :return: None
    '''
    browser.get(u)
    browser.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[1]/a').click()
        # 点击北京站
    browser.find_element_by_xpath('//*[@id="lg_tbar"]/div/div[2]/ul/li[3]/a').click()
        # 点击登陆

    username = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div['
                                             '1]/form/div[1]/div/input')
    password = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div['
                                             '1]/form/div[2]/div/input')
    username.clear()
    password.clear()
    username.send_keys(username_str)
    password.send_keys(password_str)
        # 设置密码
    browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]').clear()
        # 点击登陆  有验证码 目前技术有限，需手动操作
    print('登陆成功，返回目前网址：', browser.current_url)


def get_urls(n):
    '''
    数据挖掘职位 分页url采集
    :param n:页面参数
    :return:url列表
    '''
    url = 'https://www.lagou.com/zhaopin/shujuwajue/%i/?filterOption=3&sid=c11a75d485ee4db48f7258cda0aee2dc'
    urllist = []
    for i in range(1, n+1):
        urllist.append(url % i)
    return urllist


def get_datas(u, table):
    '''
    职位信息采集
    :param u: 分页url
    :param table: MongoDB集合对象
    :return: 返回采集数据成功条数
    '''
    browser.get(u)
    ul = browser.find_element_by_xpath('//*[@id="s_position_list"]/ul')
    lilist =ul.find_elements_by_tag_name('li')
    n = 0
    for li in lilist:
        dic = {}
        dic['职位名称'] = li.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3').text
        dic['地区'] = li.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/span/em').text
        dic['发布时间'] = li.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/span').text
        dic['公司名称'] = li.find_element_by_class_name('company_name').text
        infor1 = li.find_element_by_class_name('li_b_l').text
        infor1 = re.split(r'[ /]', infor1)
        dic['薪资'] = infor1[0]
        dic['经验要求'] = infor1[1]
        dic['学历要求'] = infor1[-1]
        infor2 = li.find_element_by_class_name('industry').text.split(' / ')
        dic['行业'] = infor2[0]
        dic['融资情况'] = infor2[1]
        dic['公司规模'] = infor2[2]
        dic['技术标签'] = li.find_element_by_class_name('list_item_bot').find_element_by_class_name('li_b_l').text
        dic['文化/福利'] = li.find_element_by_class_name('list_item_bot').find_element_by_class_name('li_b_r').text
        table.insert_one(dic)
        n += 1
    return n

if __name__ == '__main__':
    chrome_driver = 'F:\GoogleWebDriver\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=chrome_driver)
    url = 'https://www.lagou.com'
    login(url, 'xxxxx', 'xxxx')
    urllst = get_urls(9)
    myclient = pymongo.MongoClient('mongodb://localhost:27017')
    db = myclient['拉勾网信息']
    collection_table = db['职位信息数据']
    count = 0
    errorlst = []
    flag = False
    for ui in urllst:
        try:
            count += get_datas(ui, collection_table)
            sleeptime = random.randint(1, 5)  # 设置睡眠时长 1-5s
            time.sleep(sleeptime)
            print('拉勾网职位信息数据采集成功,采集%i条数据' % count)
        except:
            errorlst.append(ui)
            flag = True
            print('拉勾网职位信息数据采集失败,失败网址为:', ui)
    if flag:
        print('发现数据采集失败,采集错误网址有:', errorlst)


