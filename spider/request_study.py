#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 19:36
# @Author  : duanhaobin
# @File    : except_handing_study.py
# @Software: PyCharm
# @desc:  request study

import requests

u1 = 'https://read.douban.com/column/32512170/'
'''
    一、基础
'''
r = requests.get(url=u1)
print(r)  # <Response [418]>
print(type(r))  # <class 'requests.models.Response'>

# r.status_code  响应状态码
print(r.status_code)  # 418

# r.headers 响应头
print(r.headers)
print(type(r.headers))  # <class 'requests.structures.CaseInsensitiveDict'>

# r.text  网页内容(源代码)  print(r.text) 会格式化输出源代码

# r.encoding 网页编码
print(r.encoding)

# r.apparent_encoding  真实编码
print(r.apparent_encoding)

# 解决乱码问题(编码问题导致)
r.encoding = r.apparent_encoding

print('........................分割线...............................')
'''
    二、设置登陆信息 cookie
'''
# 1、登陆网页

# 2、F12->Network->Doc->Headers->Requests Headers  刷新页面,选一个

# 3、将header中的“User-Agent”内容设置成字典
h = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
dic_h = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
# 4、将header中的“cookies”内容设置成字典
cookies = 'viewed="33440205"; bid=FkeG50F4XvY; gr_user_id=6015c5ac-82f6-4b50-bb85-3c5575d26897; gr_cs1_e310e4ac-fb0e-439f-a4b3-591776f557fd=user_id%3A0; ap_v=0,6.0; _pk_ses.100001.3ac3=*; __utmc=30149280; __utma=30149280.625182603.1574410772.1574410772.1574410772.1; __utmz=30149280.1574410772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_douban=1; __utma=81379588.1008532201.1574410772.1574410772.1574410772.1; __utmz=81379588.1574410772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=81379588; __utmt=1; _vwo_uuid_v2=DF10E7B10E49A5D9F60728C833D04996C|bbcdcfe17d39131c077d26d2ed9db281; dbcl2="169993529:e2JKdBZQZgI"; ck=jwLe; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=6d222c61-3adb-4db7-88d5-85ab1176dec9; gr_cs1_6d222c61-3adb-4db7-88d5-85ab1176dec9=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_6d222c61-3adb-4db7-88d5-85ab1176dec9=true; __gads=Test; push_noty_num=0; push_doumail_num=0; __utmt=1; __utmv=30149280.16999; ll="108288"; __yadk_uid=xoYMePLedf9yf3sEbLPkosdMuq2B4fvU; _pk_id.100001.3ac3=06e6cfa033259840.1574410772.1.1574410862.1574410772.; __utmb=30149280.10.9.1574410857781; __utmb=81379588.4.10.1574410772'
cooklst = cookies.split('; ')
print(cooklst)
dic_c = {}
for i in cooklst:
    dic_c[i.split('=')[0]] = i.split('=')[1]

print(dic_c)

# 5、request.get()访问中，加载User-Agent和cookies信息
u2 = 'https://book.douban.com/subject/33380549/?icn=index-latestbook-subject'
r2 = requests.get(url=u2, headers=dic_h, cookies=dic_c)
print(r2)   # <Response [200]>
print(r2.status_code)  # 200  登陆成功

'''
    三、一些注意点
    1.一般情况，一个机构/平台的网页，用一个headers登录信息足够
    2.对于复杂的网页，【分页网页】使用一个headers信息，【数据信息网页】使用一个headers信息
'''
