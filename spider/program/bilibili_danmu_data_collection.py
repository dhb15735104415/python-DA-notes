#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 7:58
# @Author  : duanhaobin
# @File    : bilibili_danmu_data_collection.py
# @Software: PyCharm
# @desc:   Bilibili弹幕采集


import re
import csv
import requests
import pymongo
from bs4 import BeautifulSoup


def get_url(u_start, h_dic, c_dic):
    '''
    视频页面url获取
    :param u_start: 起始网址
    :param h_dic:headers
    :param c_dic:cookies
    :return:视频页面list
    '''
    r = requests.get(url=u_start, headers=h_dic, cookies=c_dic)
    soup = BeautifulSoup(r.text, 'lxml')
    lilst = soup.find('ul', class_="video-list clearfix").findAll('li')
    resultlst = []
    for li in lilst:
        resultlst.append('https:' + li.a['href'])
    return resultlst


def get_datas(ui, h_dic, c_dic, table):
    '''
    获取弹幕信息并储存至MongoDB中
    :param ui: 视频页面url
    :param h_dic: headers
    :param c_dic: cookies
    :param table: MongoDB集合对象
    :return:插入MongoDB成功的数据数量
    '''
    r1 = requests.get(url=ui, headers=h_dic, cookies=c_dic)
    soup1 = BeautifulSoup(r1.text, 'lxml')
    video_name = soup1.find('div', id="viewbox_report").h1['title']
    video_publish_date = re.search(r'20.+\d', soup1.find('div', class_="video-data").text).group()

    cid = re.search(r'"cid":(\d*),', r1.text).group(1)  # 获取弹幕cid
    cid_url = 'https://comment.bilibili.com/%s.xml' % cid  # 弹幕信息网址

    r2 = requests.get(url=cid_url, headers=h_dic, cookies=c_dic)
    r2.encoding = r2.apparent_encoding  # 解决乱码
    dm_lst = re.findall(r'<d.*?/d>', r2.text)  # 非贪婪匹配 结果才是lst,否则只是一大串字符串
    n = 0
    for dm in dm_lst:
        dic = {}
        dic['视频名称'] = video_name
        dic['视频发布时间'] = video_publish_date
        dic['cid'] = cid
        dic['弹幕内容'] = re.search(r'>(.*)<', dm).group(1)
        dic['其他'] = re.search(r'p="(.*)">', dm).group(1)
        table.insert_one(dic)  # 数据入库
        n += 1
    return n


def export_csv(table):
    '''
    导出至csv文件
    :param table:MongoDB集合对象
    :return:
    '''
    with open(f"Blibili弹幕数据.csv", "w", newline='', encoding='utf-8') as csvfileWriter:
        writer = csv.writer(csvfileWriter)
        # 先写列名
        # 写第一行，字段名
        fieldList = [
            "_id",
            "视频名称",
            "视频发布时间",
            "弹幕内容",
            "其他",
        ]
        writer.writerow(fieldList)

        allRecordRes = table.find()
        # 写入多行数据
        for record in allRecordRes:
            recordValueLst = []
            for field in fieldList:
                if field not in record:
                    recordValueLst.append("None")
                else:
                    recordValueLst.append(record[field])
            try:
                writer.writerow(recordValueLst)
            except Exception as e:
                print(f"write csv exception. e = {e}")

if __name__ == "__main__":
    h_dic = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}
    cookies = "LIVE_BUVID=AUTO6715442489583521; buvid3=34BDF70F-7215-4D7B-93ED-F373F6680C6A10386infoc; " \
              "stardustvideo=1; CURRENT_FNVAL=16; rpdid=|(J~kkul||lm0J'ull~k|)Ru~; " \
              "_uuid=7FA25C3A-7240-ADBA-AFFC-8378D535BD0B69091infoc; CURRENT_QUALITY=80; sid=5jnq7h1u; " \
              "im_notify_type_273918449=0; UM_distinctid=16cf5287da13d1-04b273b52042f6-34564b7b-144000-16cf5287da33c4" \
              "; pgv_pvi=6949402624; laboratory=1-1; DedeUserID=273918449; DedeUserID__ckMd5=68b43467c23cadf3; " \
              "SESSDATA=6770af0a%2C1576917515%2C8586d4b1; bili_jct=df0e7523289c0f6a3da9e60fc4cb03cd; finger=edc6ecda; " \
              "arrange=matrix; INTVER=1; bp_t_offset_273918449=326325099687937398 "
    c_dic = {}
    for c in cookies.split('; '):
        c_dic[c.split("=")[0]] = c.split("=")[1]

    u = 'https://search.bilibili.com/all?keyword=%E4%BB%BB%E6%AD%A3%E9%9D%9E&from_source=nav_search'
    urls = get_url(u, h_dic, c_dic)

    # 导入mongodb
    myclient = pymongo.MongoClient('mongodb://localhost:27017')
    db = myclient['Bilibili数据库']
    dm_collection = db['danmu数据']
    count = 0
    errorlst = []
    for ui in urls[:3]:
        try:
            count += get_datas(ui, h_dic, c_dic, dm_collection)
            print("采集Bilibili弹幕数据成功，共采集%i条数据" % count)
        except Exception as e:
            errorlst.append(ui)
            print("采集Bilibili弹幕数据异常，数据网址为：", ui)
            print('异常为:', e)

    # 将MongoDB中的数据导出并保存成csv文件
    export_csv(dm_collection)
