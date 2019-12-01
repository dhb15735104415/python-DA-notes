#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 19:36
# @Author  : duanhaobin
# @File    : except_handing_study.py
# @Software: PyCharm
# @desc:   爬虫异常处理

'''
    1 什么时候会出现错误异常？
        连不上服务器
        远程的服务不存在
        BeautifulSoup解析网页标签时，由于数据源问题，无法准确识别
    2 处理方法
        try...except...语句
        目的是什么？
        报错情况下，爬虫继续进行
'''

import requests

h = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
dic_h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

cookies = 'viewed="33440205"; bid=FkeG50F4XvY; gr_user_id=6015c5ac-82f6-4b50-bb85-3c5575d26897; gr_cs1_e310e4ac-fb0e-439f-a4b3-591776f557fd=user_id%3A0; ap_v=0,6.0; _pk_ses.100001.3ac3=*; __utmc=30149280; __utma=30149280.625182603.1574410772.1574410772.1574410772.1; __utmz=30149280.1574410772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_douban=1; __utma=81379588.1008532201.1574410772.1574410772.1574410772.1; __utmz=81379588.1574410772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=81379588; __utmt=1; _vwo_uuid_v2=DF10E7B10E49A5D9F60728C833D04996C|bbcdcfe17d39131c077d26d2ed9db281; dbcl2="169993529:e2JKdBZQZgI"; ck=jwLe; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=6d222c61-3adb-4db7-88d5-85ab1176dec9; gr_cs1_6d222c61-3adb-4db7-88d5-85ab1176dec9=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_6d222c61-3adb-4db7-88d5-85ab1176dec9=true; __gads=Test; push_noty_num=0; push_doumail_num=0; __utmt=1; __utmv=30149280.16999; ll="108288"; __yadk_uid=xoYMePLedf9yf3sEbLPkosdMuq2B4fvU; _pk_id.100001.3ac3=06e6cfa033259840.1574410772.1.1574410862.1574410772.; __utmb=30149280.10.9.1574410857781; __utmb=81379588.4.10.1574410772'
cooklst = cookies.split('; ')
dic_c = {}
for i in cooklst:
    dic_c[i.split('=')[0]] = i.split('=')[1]

urllst = ['https://book.douban.com/subject/33380549/?icn=index-latestbook-subject',
          'https://book.douban.com/subject/33380549/?icn=index-latestbook-subject',
          'https://book.doubanss.com/subject/33380549/?icn=index-latestbook-subject',  # 故意设置错误url
          'https://book.douban.com/subject/33380549/?icn=index-latestbook-subject',
          'https://book.douban.com/subject/33380549/?icn=index-latestbook-subject', ]
success = 0
fail = 0
for u in urllst:
    try:
        r = requests.get(url=u, headers=dic_h, cookies=dic_c)
        success += 1
        print('本次访问成功,第%d次成功' % success)
    except:
        fail += 1
        print('本次访问失败,第%d次失败，错误网址为:%s' % (fail, u))
