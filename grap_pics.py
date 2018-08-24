# -*- coding: utf-8 -*
import numpy as np
import pandas as pd
import pymysql
import urllib
import urllib2
import os
import re
import oss2



config_oss2={
    'AccessKeyId': 'LTAIgZxQ3TtshmAB',
    'AccessKeySecret': '0F6juS5boKfbARqiJR6kBfRPHKBYTf',
     # 公网地址，用于本地测试
     #'Endpoint': 'http://oss-cn-beijing.aliyuncs.com',
     #'Host': 'http://x-pic.oss-cn-beijing.aliyuncs.com/',
     # 内网地址，用于服务器上运行
     'Endpoint': 'http://oss-cn-beijing-internal.aliyuncs.com',
     'Host': 'http://x-pic.oss-cn-beijing-internal.aliyuncs.com/',
    'BucketName': 'x-pic'
}


# 链接OSS 认证
auth = oss2.Auth(config_oss2['AccessKeyId'], config_oss2['AccessKeySecret'])
bucket = oss2.Bucket(auth, config_oss2['Endpoint'], config_oss2['BucketName'], connect_timeout=30)

bucket_info = bucket.get_bucket_info()


# 链接数据库
def getconnect():
    # '''数据库地址'''
    host = "rm-2zehra4b3vu4i4x31i.mysql.rds.aliyuncs.com"
    # 数据库名称
    db = "dev_mapping"
    # 登录用户名
    user = "read_only"
    # 登陆密码
    password = "jdfsoIfou234A"
    # 链接数据库 并制定编码 charset='utf-8')
    conn = pymysql.connect(host, user, password, db, port=3306, charset='utf8')
    return conn

# 获得图片链接，并返回目录层级名称
def get_url():
    conn = getconnect()
    cursor = conn.cursor()
    pattern = re.compile('^http')  # 正则制定pic_url 为http开头
    sql = '''select sight_id,country_code,city_code,pic_url from cm_sight_qyer limit 20'''  # sql 为查询sight_id 和 pic_url
    cursor.execute(sql)
    results = cursor.fetchall()
    list = results

    for row in results:
        try:
            sight_id = row[0]
            country_code = row[1]
            city_code = row[2]
            pic_url = row[3]
            # 模式匹配出http: 开头的链接
            if (pattern.match(pic_url) != None):
                get_image(sight_id, country_code, city_code, pic_url)
            else:
                print("")
        except:
            continue
    cursor.close

# 爬取图片 进行判断后存储到相应目录
def get_image(sight_id, country_code, city_code, pic_url):

    # 取模
    m = int(sight_id) % 9
    # 构建请求
    request = urllib2.Request(pic_url)
    # 获取服务器相应
    response = urllib2.urlopen(request)


    image = response.read()
    # 通过 国家/城市/取模 来构建目录
    path = 'qyer/%s/%s/%s/' % (country_code, city_code, str(m))
    # 判断目录是否已存在
    flag = os.path.exists(path)
    # 如果存在 那么进入到最底目录 存储文件
    if (flag):
        # 切换目录
        os.chdir(path)
        # 写文件
        with open("%s.jpg" % sight_id, "wb") as fp:
            fp.write(image)
    # 如果不存在则递归创建目录 并存储文件
    else:
        # 递归创建目录
        os.makedirs(path)
        # 切换目录
        os.chdir(path)
        # 写文件
        with open("%s.jpg" % sight_id, 'wb') as fp:
            fp.write(image)
    os.chdir("../../../../")

'''对马蜂窝图片数据字符串进行处理'''
def select_mo():



    conn = getconnect()
    cursor = conn.cursor()
    sql = '''select sight_id,images from cm_sight_mafengwo_etl limit 3'''  # sql 为查询sight_id 和 pic_url
    cursor.execute(sql)
    # 存储数据，然后关闭链接再对数据进行操作
    result = cursor.fetchall()


    for row in result:
        sight_id = row[0]

        # 首先将字符串去除两边[] 然后按照逗号进行切割 存储为列表
        # 取模啊
        m = int(sight_id) % 100
        list = row[1].strip("[]").split(",")
        # 遍历列表，然后对每一个URL进行爬取
        str = ""
        for img in list:
            url = img.strip("\"")
            # 获取URL在列表中的索引 然后拼接sight_id 作为文件名称
            num= list.index(img)
            request = urllib2.Request(url)
            # 获取服务器相应
            response = urllib2.urlopen(request)
            image = response.read()
            # 定义图片存储路径
            path = 'mafengwo/%s/%s/%s_%d.jpg' % (m,sight_id,sight_id, num)
            bucket.put_object(path,image)
            # 拼接字符串
            str = str+","+'%s_%d.jpg'%(sight_id,num)
            img_str = str.strip(",")
        print(img_str)
        sql = '''update cm_sight_mafengwo_etl set hbc_pics = '%s' where sight_id = %s'''%(img_str,sight_id)
        cursor.execute(sql)
        conn.commit()
    # 关闭游标 释放链接
    conn.close()
    cursor.close()


select_mo()





