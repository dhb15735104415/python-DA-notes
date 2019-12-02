#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 15:13
# @Author  : duanhaobin
# @File    : qunaer_data_collection.py
# @Software: PyCharm
# @desc:    去哪儿网景点数据采集


import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_urls(city, n):
    '''
    分页url获取
    :param city:城市代号 eg:cs299914-beijing
    :param n:页面参数
    :return:url列表
    '''
    urllst = []
    for i in range(n):
        urllst.append('https://travel.qunar.com/p-%s-jingdian-1-%i' % (city, i + 1))
    return urllst


def get_datas(ui, d_h, d_c):
    '''
    采集旅游景点信息
    :param ui:分页url
    :param d_h:user-agent
    :param d_c:cookies
    :return:旅游经典信息，列表字典
    '''
    r = requests.get(url=ui, headers=d_h, cookies=d_c)
    soupi = BeautifulSoup(r.text, 'lxml')
    lilst = soupi.find('ul', class_="list_item clrfix").findAll('li')
    datalst = []
    for li in lilst:
        dic = {}
        dic['景点名称'] = li.find('a').span.text
        dic['简介'] = li.find('div', class_='desbox').text
        dic['旅行攻略篇数'] = li.find('div', class_='strategy_sum').text
        dic['点评数量'] = li.find('div', class_='comment_sum').text
        dic['评分(百分制)'] = li.find('span', class_='total_star').span['style']
        dic['排名'] = li.find('span', class_='ranking_sum').text
        dic['驴友推荐程度'] = li.find('div', class_='txtbox clrfix').find('span').text
        datalst.append(dic)
    return datalst


if __name__ == '__main__':
    urls = get_urls('cs299914-beijing', 1)
    dict_h = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/70.0.3538.25 Safari/537.36'}
    cookies = 'QN1=dXrgj13kuLeQIh+dBqZGAg==; QN205=organic; QN277=organic; _i=ueHd8gLHAWo9VZUA4D7odm4ZkIkX; ' \
              'QN269=3A46D2A0AB8911E9A7B6FA163EEA7E2C; fid=a4e95ad5-bc7c-41cd-ad00-2c3ddc036237; QN99=5216; ' \
              'QN300=organic; QN25=ccf68b91-17fa-4dc2-8335-f82109cb0a0a-9f992f90; QN42=rfaj8762; _q=U.jfqioqd2588; ' \
              '_t=26363951; csrfToken=7CntzUibiGhgvxasWNejDqQoJKhBnKdL; _s=s_VRU2WEALP45TZGGYITKSAZEWSM; ' \
              '_v=bo-V3bK-4yKdFC35VgY7etfnifooVtlnCcIcPTh4AxmvUW0eK33sRRwILEb0lARt4cVqd1NQVj8rioipiJM4sPHPbeekPjBgbb0XUa10jZ2e8ii_AqsmAK5RVQVaMR2i-FIhMFxU9NQHc2vxgAClFNp9NJ3buVvfKAlCrjkqbgVe; _vi=gWTXF-LzZN8ZjSNIBVCBCBVKa63b5yx8Twx226XHJiR-es5naeBoc9P2MknD0RxDcyOL0fVXeryPmlKDVeMJfBSmsAH1-StzNMC0gXcIOCns9R1nEIc8ffFqWDZOa7LDqBcIOsznai-ULonsEPYnaXS6ZQUtrOj1md-byyVb9nxS; QN44=jfqioqd2588; Hm_lvt_c56a2b5278263aa647778d304009eafc=1575270586,1575270667,1575270685; QN48=tc_138c0ad474f1ef13_16ec5733801_32f7; viewdist=299878-7|299914-7; uld=1-299914-7-1575271331|1-299878-7-1575271082; Hm_lpvt_c56a2b5278263aa647778d304009eafc=1575271333; QN271=791cfde6-8f40-496c-b977-d9a9788be9b8; QN267=088717026749eb529a '
    dict_c = {}
    for c in cookies.split('; '):
        dict_c[c.split('=')[0]] = c.split('=')[1]

    datalst = []
    errolst = []
    for ui in urls:
        try:
            datalst.extend(get_datas(ui, dict_h, dict_c))
            print('旅游景点数据采集成功，总共采集%i条数据' % len(datalst))
        except:
            errolst.append(ui)
            print('旅游景点数据采集失败，失败%i条数据，网址为：%s' % (len(errolst), ui))

    print(datalst)
    datadf = pd.DataFrame(datalst)
        # 数据清洗
    datadf['点评数量'] = datadf['点评数量'].astype('int')
    datadf['旅行攻略篇数'] = datadf['旅行攻略篇数'].astype('int')
    datadf['评分(百分制)'] = datadf['评分(百分制)'].str.split(':').str[-1].str.replace('%', '').astype('int')
    datadf['多少比例驴友来过'] = datadf['驴友推荐程度'].str.split('%').str[0].astype('float')/100

    print(datadf)