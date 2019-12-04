#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/12/4 20:12
# @Author  : duanhaobin
# @File    : mongodb_study.py
# @Software: PyCharm
# @desc:    使用Python操作mongodb

import pymongo
import pandas as pd

'''
    1、创建MongoClient对象 连接mongodb
'''
# 创建MongoClient对象 连接mongodb
myclien = pymongo.MongoClient('mongodb://localhost:27017')
print(myclien)  # MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)

# 查看现有数据库 list_database_names()
print(myclien.list_database_names())  # ['admin', 'config', 'local', 'study', 'test01']

# 读取数据库
db_study = myclien['study']
print(db_study)  # Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True),
# 'study')

'''
    2、查询集合、文档
'''
# 查看某数据库下现有的集合 .list_collection_names()  如‘study'数据库下的集合
collections_lst = db_study.list_collection_names()
print(collections_lst)  # ['table01', 'table02']

# 查看数据库下的文档  不是collections_lst['table01']
collection_table01 = db_study['table01']
print(collection_table01)

# 查询单条数据find_one()
print(collection_table01.find_one())  # {'_id': ObjectId('5de75da9b042c61a788126f3'), 'a': 'aaaa'}

# 查询所有的数据find() 返回的是Cursor对象
data_all = collection_table01.find()
print(data_all)  # <pymongo.cursor.Cursor object at 0x00000223C420B668>
print(list(data_all))  # [{'_id': ObjectId('5de75da9b042c61a788126f3'), 'a': 'aaaa'}, {'_id': ObjectId(
# '5de75e6bb042c61a788126f4'), 'b': 1212.0, 'one': 11.0}]

# 插入单个文档 insert_one(dict)
# collection_table01.insert_one({'c': 'cccc'})
data_all = collection_table01.find()
print(list(data_all))  # [{'_id': ObjectId('5de75da9b042c61a788126f3'), 'a': 'aaaa'}, {'_id': ObjectId(
# '5de75e6bb042c61a788126f4'), 'b': 1212.0, 'one': 11.0}, {'_id': ObjectId('5de7a6e67d4016ee844780fa'), 'c': 'cccc'}]

# 插入多个文档 insert_many(字典列表)
dict_lst = [
    {'d': 'dddd'},
    {'e': 'eeee'},
    {'f': 'ffff'}
]
collection_table01.insert_many(dict_lst)
print(list(collection_table01.find()))  # [{'_id': ObjectId('5de75da9b042c61a788126f3'), 'a': 'aaaa'}, {'_id':
# ObjectId('5de75e6bb042c61a788126f4'), 'b': 1212.0, 'one': 11.0}, {'_id': ObjectId('5de7a6e67d4016ee844780fa'),
# 'c': 'cccc'}, {'_id': ObjectId('5de7a7e749f413f7c3230640'), 'd': 'dddd'}, {'_id': ObjectId(
# '5de7a7e749f413f7c3230641'), 'e': 'eeee'}, {'_id': ObjectId('5de7a7e749f413f7c3230642'), 'f': 'ffff'}]

# 删除单个文档 delete_one()
collection_table01.delete_one({'b': 1212.0})

# 删除多条数据 delete_many()  无参则表示删除所有数据 慎用！！！
collection_table01.delete_many({'f': 'ffff'})

# 删除集合 drop()  慎用！！！  在实际业务中删出表操作需要确定清楚
# collection_table01.drop()

'''
    3、pandas如何配合mongo：
'''
# 1) 通过查询的方式，将数据存成dataframe
data_all = collection_table01.find()
datadf = pd.DataFrame(list(data_all))
print(datadf)
# 2) dataframe通过.to_dict()方法输出字典列表，再通过insert_many()导入数据库
lst = datadf.to_dict(orient='records')  # 将datadf转成字典列表
collection_table03 = db_study['table03']  # 创建table03集合(表)
collection_table03.insert_many(lst)  # 新集合中,会有很多NaN的数据
'''
    从Robo3T中拷贝的数据，print(datadf)这里本身就包含了NaN数据，所以在往新集合里插入新数据时，会按照datadf的数据来插入
    /* 1 */
    {
        "_id" : ObjectId("5de75da9b042c61a788126f3"),
        "a" : "aaaa",
        "c" : NaN,
        "d" : NaN,
        "e" : NaN,
        "one" : NaN
    }
    
    /* 2 */
    {
        "_id" : ObjectId("5de7a6e67d4016ee844780fa"),
        "a" : NaN,
        "c" : "cccc",
        "d" : NaN,
        "e" : NaN,
        "one" : NaN
    }
    
    /* 3 */
    {
        "_id" : ObjectId("5de7a7e749f413f7c3230640"),
        "a" : NaN,
        "c" : NaN,
        "d" : "dddd",
        "e" : NaN,
        "one" : NaN
    }


'''

# 3) 数据修改、处理、分析，都在pandas中执行

# 4) 数据爬取过程中，以字典方式存储每一条数据，可以直接通过insert_one()插入数据库中
