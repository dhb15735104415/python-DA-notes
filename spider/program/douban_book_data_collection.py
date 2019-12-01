# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/29 18:09
# @Author  : duanhaobin
# @File    : douban_book_data_collection.py
# @Software: PyCharm
# @desc:   豆瓣图书数据采集练习
#          爬虫逻辑：【分页网页url采集】-【数据信息网页url采集】-【数据采集】

import requests
import time
from bs4 import BeautifulSoup


def get_urls(n):
    '''
    分页网页url采集函数
    :param n:页面参数
    :return:url列表
    '''
    urlslst = []
    for i in range(n):
        urlslst.append('https://book.douban.com/tag/%%E7%%94%%B5%%E5%%BD%%B1?start=%i&type=T' % (i * 20))
    return urlslst


def get_dataurls(ui, d_h, d_c):
    '''
    数据信息网页url采集 函数
    :param ui:分页网址
    :param d_h:user_agent
    :param d_c:cookies信息
    :return:数据信息网页url列表
    '''
    # 访问网页
    r = requests.get(url=ui, headers=d_h, cookies=d_c)
    #  解析网页
    soup = BeautifulSoup(r.text, 'lxml')
    # 找到所有li标签
    lis = soup.find('ul', class_='subject-list').findAll('li')
    li_lst = []
    for li in lis:
        # 构建链接列表
        li_lst.append(li.find('a')['href'])
    return li_lst


def get_data(ui, d_h, d_c):
    '''
    数据采集函数
    :param ui:书名url
    :param d_h:user_agent
    :param d_c:cookies
    :return:数据字典
    '''
    print('进入get_data,ui:', ui)
    r2 = requests.get(url=ui, headers=dict_h, cookies=dict_c)
    soup = BeautifulSoup(r2.text, 'lxml')
    dic = {}
    dic['书名'] = soup.find('div', id='wrapper').find('h1').text.replace('\n', '')
    dic['评分'] = soup.find('div', class_='rating_self clearfix').find('strong').text.replace(' ', '')
    dic['评价人数'] = soup.find('div', class_='rating_sum').find('a').find('span').text
    infors = soup.find('div', id="info").text.replace(' ', '').split('\n')
    for i in infors:
        if ':' in i:
            dic[i.split(':')[0]] = i.split(':')[1]
        else:
            continue
    return dic


if __name__ == "__main__":
    begin_t = time.time()
    # 获取分页网址
    urllst1 = get_urls(2)
    # 拼接user_agent
    dict_h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36'}
    cookies = 'viewed="33440205"; bid=FkeG50F4XvY; gr_user_id=6015c5ac-82f6-4b50-bb85-3c5575d26897; __utmc=30149280; ' \
              '__utmz=30149280.1574410772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ' \
              '__utmz=81379588.1574410772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=81379588; ' \
              '_vwo_uuid_v2=DF10E7B10E49A5D9F60728C833D04996C|bbcdcfe17d39131c077d26d2ed9db281; ' \
              'dbcl2="169993529:e2JKdBZQZgI"; ck=jwLe; __gads=Test; push_noty_num=0; push_doumail_num=0; ' \
              '__utmv=30149280.16999; ll="108288"; __yadk_uid=xoYMePLedf9yf3sEbLPkosdMuq2B4fvU; ap_v=0,' \
              '6.0; _pk_ses.100001.3ac3=*; __utma=30149280.625182603.1574410772.1575012018.1575022271.5; ' \
              '__utma=81379588.1008532201.1574410772.1575012018.1575022271.5; ' \
              '_pk_id.100001.3ac3=06e6cfa033259840.1574410772.5.1575022338.1575012051.; __utmb=30149280.2.10.1575022271; ' \
              '__utmb=81379588.2.10.1575022271 '

    dict_c = {}
    # 拼接cookies
    for i in cookies.split('; '):
        dict_c[i.split('=')[0]] = i.split('=')[1]

    urllst2 = []
    # 获取数据信息页面网址urllst2
    for u in urllst1:
        try:
            urllst2.extend(get_dataurls(u, dict_h, dict_c))
            print('数据信息网页获取成功,总共获取%i条网页' % len(urllst2))
        except:
            print('数据信息网页获取失败,失败网页：', u)

    successlst = []
    errolst = []
    # 采集需求数据
    for ui in urllst2:
        try:
            successlst.append(get_data(ui, dict_h, dict_c))
            print('数据采集成功，总共%i条数据' % len(successlst))
        except:
            errolst.append(ui)
            print('数据采集失败，失败网址为:', errolst)

    end_t = time.time()
    print(successlst)
    print('数据采集结束，共耗时:%ss' %(str(end_t - begin_t)))
