#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 8:28
# @Author  : duanhaobin
# @File    : douban_img_data_collection.py
# @Software: PyCharm
# @desc:   豆瓣图片收集并保存到本地电脑
#          爬虫逻辑：【分页网页url采集】-【数据采集】-【保存图片】
import requests
from bs4 import BeautifulSoup


def get_urls(n):
    '''
    分页网页url采集函数
    :param n: 页面参数
    :return: url列表
    '''
    urllst = []
    for i in range(n):
        urllst.append(
            'https://movie.douban.com/subject/25887288/photos?type=R&start=%i&sortby=like&size=a&subtype=a' % (i * 30))
    return urllst


def get_pics(ui, d_h, d_c):
    '''
    采集豆瓣电影图片函数
    :param ui:分页url
    :param d_h:user_agent
    :param d_c:cookies
    :return:图片dic,包括图片id和图片src
    '''
    r = requests.get(url=ui, headers=d_h, cookies=d_c)
    soupi = BeautifulSoup(r.text, 'lxml')
    picdatas = soupi.find('ul', class_="poster-col3 clearfix").findAll('li')
    piclst = []
    for pic in picdatas:
        dic = {}
        dic['picid'] = pic['data-id']
        dic['picsrc'] = pic.find('img')['src']
        piclst.append(dic)
    return piclst


def save_img(prcdic):
    '''
    图片保存函数
    :param prcdic: 图片存储的字典，包括图片id和图片src
    :return: None
    '''
    img = requests.get(url=prcdic['picsrc'])
    with open('p' + prcdic['picid'] + '.jpg', 'ab') as f:
        # 写入文件
        f.write(img.content)
        f.close()


if __name__ == '__main__':
    import os

    os.chdir('C:/Users/HBlock/Desktop/图片/python/pics')  # 设置图片存储路径
    dict_h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36'}
    cookies = 'viewed="33440205"; bid=FkeG50F4XvY; gr_user_id=6015c5ac-82f6-4b50-bb85-3c5575d26897; __utmc=30149280; ' \
              '_vwo_uuid_v2=DF10E7B10E49A5D9F60728C833D04996C|bbcdcfe17d39131c077d26d2ed9db281; ' \
              'dbcl2="169993529:e2JKdBZQZgI"; ck=jwLe; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16999; ' \
              'll="108288"; __utmc=223695111; ct=y; ' \
              '__gads=ID=9763ab6fce682839:T=1575072304:S=ALNI_Mb4Quhrbq68h-ZPDrYlrczybvM-wA; ' \
              '_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1575247297%2C%22https%3A%2F%2Fbook.douban.com%2Ftag%2F%25E7' \
              '%2594%25B5%25E5%25BD%25B1%3Fstart%3D80%26type%3DT%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,' \
              '6.0; __utma=30149280.625182603.1574410772.1575201612.1575247297.10; __utmb=30149280.0.10.1575247297; ' \
              '__utmz=30149280.1575247297.10.2.utmcsr=book.douban.com|utmccn=(' \
              'referral)|utmcmd=referral|utmcct=/tag/%E7%94%B5%E5%BD%B1; ' \
              '__utma=223695111.1686897134.1574410852.1574410852.1575247297.2; __utmb=223695111.0.10.1575247297; ' \
              '__utmz=223695111.1575247297.2.2.utmcsr=book.douban.com|utmccn=(' \
              'referral)|utmcmd=referral|utmcct=/tag/%E7%94%B5%E5%BD%B1; __yadk_uid=a923JVEOAd9DFPJhdyBR1SIdjEK3nWAx; ' \
              '_pk_id.100001.4cf6=d3373bb311cddf39.1574410852.2.1575247374.1574410852. '
    dict_c = {}
    for c in cookies.split('; '):
        dict_c[c.split('=')[0]] = c.split('=')[1]
    srclst = []
    for ui in get_urls(5):
        # 获取图片src
        try:
            piclst = get_pics(ui, dict_h, dict_c)
            srclst.extend(piclst)
            print('图片src获取成功，总共获取%i条' % len(srclst))
        except:
            continue
    n = 0
    m = 0
    for src in srclst:
        try:
            save_img(src)
            n += 1
            print('图片保存成功，总共保存%i张' % n)
        except:
            m += 1
            print('图片保存失败，失败%i张，失败地址为%s' % (m, src))
