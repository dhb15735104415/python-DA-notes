#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 8:31
# @Author  : duanhaobin
# @File    : lianj_esf_info_data_collection.py
# @Software: PyCharm
# @desc:   lianj esf详细信息数据采集(动态代理ip)及清洗

import re
import requests
import pymongo
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings('ignore')


def get_urls(table):
    datalst = table.find()
    return [i['链接'] for i in datalst]


def get_proxies(p_User, p_Pass, p_Host, p_Port):
    '''
    生成动态代理ip
    :param p_User:设置代理隧道验证信息
    :param p_Pass:设置代理隧道验证信息
    :param p_Host:设置代理服务器
    :param p_Port:设置代理服务器
    :return:ip列表
    '''
    proxyMeta = f"http://{p_User}:{p_Pass}@{p_Host}:{p_Port}"
    ips = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    return ips


def test_ips():
    ips = get_proxies('H4K7A67RE7V39C1D', '2D53906310122580', 'http-dyn.abuyun.com', '9020')
    url = 'https://bj.lianjia.com/ershoufang/101105294964.html'
    result = requests.get(url=url, headers=h_dic, proxies=ips)

    print(result)


def get_datas(u, h_dic, ips, table):
    '''
    房源详细信息采集及数据入库
    :param u:
    :param h_dic:
    :param ips:
    :param table:
    :return:
    '''
    r = requests.get(url=u, headers=h_dic)
    soup = BeautifulSoup(r.text, 'lxml')
    dic = {}
    dic['总价_万'] = soup.find('span', class_='total').text
    dic['单价_元'] = soup.find('span', class_='unitPriceValue').text
    dic['年份/楼型'] = soup.find('div', class_='area').find('div', class_='subInfo').text
    dic['小区名称'] = soup.find('div', class_='communityName').find('a').text
    dic['所在区域'] = re.sub(r'\xa0', ' ', soup.find('span', class_='info').text)
    base_lst = soup.find('div', class_='base').find('div', class_='content').find('ul').findAll('li')
    for li in base_lst:
        # 采集基本属性
        base_info = re.split(r'<.+?>', str(li))
        dic[base_info[2]] = base_info[3]

    trans_lst = soup.find('div', class_='transaction').find('div', class_='content').find('ul').findAll('li')
    for li in trans_lst:
        # 采集交易属性
        trans_info = re.split(r'<.+?>', str(li))
        dic[trans_info[2]] = re.sub(r'[ \n]+', '', trans_info[4])
    position = re.search(r"resblockPosition:'([.\d]+),([\d.]+)'", r.text)
    dic['lng'] = position.group(1)  # 经度
    dic['lat'] = position.group(2)  # 纬度
    # 经纬度  坐标拾取器大致识别,然后再根据坐标去页面查找
    table.insert_one(dic)


def data_cleaning(table_old, table_new):
    '''
    房源数据清洗
    :param table_old:源数据MongoDB集合对象
    :param table_new:清洗后新数据MongoDB集合对象
    :return:清洗成功数量
    '''
    datalst = table_old.find()
    n = 0
    for d in datalst:
        del d['_id']
        d['总价_万'] = float(d['总价_万'])
        d['单价_元'] = float(re.search(r'([\d.]+)', d['单价_元']).group(1))
        d['lng'] = float(d['lng'])
        d['lat'] = float(d['lat'])
        d['建筑面积'] = float(re.search(r'([.\d]+)', d['建筑面积']).group(1))
        mod_area1 = re.search(r'([.\d]+)', d['套内面积'])
        if mod_area1:
            d['套内面积'] = mod_area1.group(1)
        else:
            del d['套内面积']
        d['产权年限'] = int(re.search(r'([\d]+)', d['产权年限']).group(1))
        lc_info = re.search(r'([\D]+)层', d['所在楼层'])
        if lc_info:
            d['楼层'] = lc_info.group(1) + '层'
        lc_number = re.search(r'(\d+)', d['所在楼层'])
        if lc_number:
            d['总层数'] = int(lc_number.group(1))
        del d['所在楼层']
        table_new.insert_one(d)
        n += 1
    return n


if __name__ == '__main__':

    h_dic = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}
    myclient = pymongo.MongoClient('mongodb://localhost:27017')
    db = myclient['链家esf数据01']
    table_collection_orgin = db['esf_list_data01_new']  # 源数据MongoDB集合对象
    table_collection = db['esf_infor_data']  # 采集详细房源数据MongoDB集合对象
    table_collection.delete_many({})
    table_collection_new = db['esf_infor_data_clean']  # 清洗详细房源数据MongoDB集合对象

    urllst = get_urls(table_collection_orgin)

    ips = get_proxies('H4K7A67RE7V39C1D', '2D53906310122580', 'http-dyn.abuyun.com', '9020')
    n = 0
    errorlst = []
    for u in urllst:
        try:
            get_datas(u, h_dic, ips, table_collection)
            n += 1
        except Exception as e:
            errorlst.append(u)
            print(f'数据采集异常,e = {e}', errorlst)
        else:
            print(f'数据采集成功,共采集{n}条数据')
    success_count = 0
    try:
        success_count = data_cleaning(table_collection, table_collection_new)
    except Exception as e:
        print(f'清洗数据异常,e:{e}')
    else:
        print(f'清洗数据结束,总共清洗{success_count}条数据')

    # test_ips()  测试动态代理
