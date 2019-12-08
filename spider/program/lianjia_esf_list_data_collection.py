#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/8 15:33
# @Author  : duanhaobin
# @File    : lianjia_esf_list_data_collection.py
# @Software: PyCharm
# @desc:    ljia网站esf列表数据采集及清洗练习

import re
import requests
import time
import random
import pymongo
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
    # 不发出警告


def get_data(u, h_dic, table):
    '''
    数据采集及入库
    :param u:房源列表信息网址
    :param h_dic:user_agent
    :param table:MongoDB集合对象
    :return:
    '''
    r = requests.get(url=u, headers=h_dic)
    soup = BeautifulSoup(r.text, 'lxml')
    lilist = soup.find('ul', class_='sellListContent').findAll('li')
    n = 0
    for li in lilist:
        dic = {}
        dic['标题'] = li.find('div', class_='title').find('a').text
        dic['总价'] = li.find('div', class_='totalPrice').find('span').text
        dic['单价'] = li.find('div', class_='unitPrice').text
        dic['链接'] = li.find('a')['href']
        positionInfo = re.split(r'([ -]+)', li.find('div', class_='positionInfo').text)
        dic['小区'] = positionInfo[0]
        dic['地段'] = positionInfo[2]
        houseInfo = re.split(r'([|]+)', li.find('div', class_='houseInfo').text)
        dic['户型'] = houseInfo[0].replace(' ', '')
        dic['面积'] = houseInfo[2].replace(' ', '')
        dic['朝向'] = houseInfo[4].replace(' ', '')
        dic['装修情况'] = houseInfo[6].replace(' ', '')
        dic['楼层情况'] = houseInfo[8].replace(' ', '')
        dic['始建年限'] = houseInfo[10]
        dic['楼型'] = houseInfo[12].replace(' ', '')
        followInfo = li.find('div', class_='followInfo').text
        dic['关注人数'] = re.search(r'([\d]+)', followInfo).group(1)
        dic['发布时间'] = re.search(r' /(.+)发布', followInfo).group(1).replace(' ', '')
        table.insert_one(dic)
        n += 1
    return n

def data_cleaning(table,table_new):
    '''
    从数据库中读取数据并清洗
    :param table: 旧表
    :param table_new: 新表
    :return:
    '''
    n = 0
    datalst = table.find()
    for d in datalst:
        del d['_id']
        d['关注人数'] = int(d['关注人数'])
        d['总价_万'] = float(d['总价'])
        del d['总价']
        d['单价_元'] = float(re.search(r'([\d.]+)', d['单价']).group(1))
        del d['单价']
        d['面积'] = float(re.search(r'([\d.]+)', d['面积']).group(1))
        year_data = d['始建年限']
        year_matchob = re.search(r'(\d{4})', d['始建年限'])
        if year_data and year_matchob:
            d['年份'] = int(year_matchob.group())
            del d['始建年限']
        lc_info = d['楼层情况']
        tmp_lc = re.search(r'(\D+)层', lc_info)
        if tmp_lc:
            d['楼层'] = tmp_lc.group(1)
        tmp_lc_number = re.search(r'(\d+)层', lc_info)
        if tmp_lc_number:
            d['层数'] = int(tmp_lc_number.group(1))
        del d['楼层情况']
        table_new.insert_one(d)
        n += 1
    return n


if __name__ == '__main__':
    city_url = 'https://bj.lianjia.com/ershoufang/'
    urllst = [city_url + 'pg%i/' % (i + 1) for i in range(20)]
        # 采集20页

    myclient = pymongo.MongoClient('mongodb://localhost:27017')
    db = myclient['链家esf数据01']
    table_collection = db['esf_list_data01']
    table_collection.delete_many({})
    h_dic = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}
    errorlst = []
    count = 0
    for u in urllst:
        time.sleep(random.random())  # 随机等待0-1秒
        try:
            count += get_data(u, h_dic, table_collection)
        except Exception as e:
            errorlst.append(u)
            print(f"采集数据异常. e = {e}", errorlst)
        else:
            print(f'数据采集成功,总共采集{count}条数据')
    print('开始数据清洗......')
    table_collection_new = db['esf_list_data01_new']
    table_collection_new.delete_many({})

    success_count = 0
    try:
        success_count = data_cleaning(table_collection, table_collection_new)
    except Exception as e:
        print(f'清洗数据异常, e = {e}')
    else:
        print(f'清洗数据成功,共清洗{success_count}条数据')