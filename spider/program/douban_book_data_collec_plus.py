#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/11/30 10:01
# @Author  : duanhaobin
# @File    : douban_book_data_collec_plus.py
# @Software: PyCharm
# @desc:豆瓣图书数据采集练习
#       爬虫逻辑：【分页网页url采集】-【数据采集】

import time
import requests
from bs4 import BeautifulSoup


def get_urls(n):
    '''
    分页网页url构造
    :param n: 页数
    :return: 分页网页url列表
    '''
    urllst = []
    for i in range(n):
        urllst.append('https://book.douban.com/tag/%%E7%%94%%B5%%E5%%BD%%B1?start=%i&type=T' % (n * 20))
    return urllst


def get_datas(ui, d_h, d_c):
    r = requests.get(url=ui, headers=d_h, cookies=d_c)
    soup = BeautifulSoup(r.text, 'lxml')
    lilst = soup.find('ul', class_='subject-list').findAll('li')
    resultlst = []
    for li in lilst:
        dic = {}
        dic['书名'] = li.find('h2').find('a')['title']
        dic['其他'] = li.find('div', class_='pub').text.replace(' ', '').replace('\n', '')
        dic['评价'] = li.find('div', class_="star clearfix").text.replace(' ', '').replace('\n', '')
        dic['简介'] = li.find('p').text.replace(' ', '').replace('\n', '')
        resultlst.append(dic)
    return resultlst


if __name__ == '__main__':
    dict_h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36'}
    dict_c = {}
    cookies = 'viewed="33440205"; bid=FkeG50F4XvY; gr_user_id=6015c5ac-82f6-4b50-bb85-3c5575d26897; __utmc=30149280; ' \
              '__utmz=30149280.1574410772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ' \
              '__utmz=81379588.1574410772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=81379588; ' \
              '_vwo_uuid_v2=DF10E7B10E49A5D9F60728C833D04996C|bbcdcfe17d39131c077d26d2ed9db281; ' \
              'dbcl2="169993529:e2JKdBZQZgI"; ck=jwLe; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16999; ' \
              'll="108288"; __yadk_uid=xoYMePLedf9yf3sEbLPkosdMuq2B4fvU; ct=y; ' \
              '__gads=ID=9763ab6fce682839:T=1575072304:S=ALNI_Mb4Quhrbq68h-ZPDrYlrczybvM-wA; ap_v=0,' \
              '6.0; _pk_id.100001.3ac3=06e6cfa033259840.1574410772.8.1575197031.1575072892.; _pk_ses.100001.3ac3=*; ' \
              '__utma=30149280.625182603.1574410772.1575072306.1575197031.8; __utmt_douban=1; ' \
              '__utmb=30149280.1.10.1575197031; __utma=81379588.1008532201.1574410772.1575072306.1575197031.8; ' \
              '__utmt=1; __utmb=81379588.1.10.1575197031 '
    for c in cookies.split('; '):
        dict_c[c.split('=')[0]] = c.split('=')[1]
    urllst = get_urls(2)
    datalst = []
    errorlst = []
    for ui in urllst:
        try:
            datalst.extend(get_datas(ui, dict_h, dict_c))
            print('采集网页信息成功，总共采集%i条数据' % len(datalst))
        except:
            errorlst.extend(get_datas(ui, dict_h, dict_c))
            print('采集网页信息失败，网址为：', ui)

    print(datalst)