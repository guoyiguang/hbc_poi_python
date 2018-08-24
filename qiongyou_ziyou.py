#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import re
import oss2






class Poi:
    #获取链接
    def getconnect(self):
        #数据库地址
        host = "rm-2zehra4b3vu4i4x31.mysql.rds.aliyuncs.com"
        #数据库名称
        db = "dev_mapping"
        #登录用户名
        user="read_only"
        #登陆密码
        password="jdfsoIfou234A"
        #链接数据库 并制定编码 charset='utf-8')
        conn = pymysql.connect(host,user,password,db,port=3306,charset='utf8')
        cursor = conn.cursor()
        return cursor,conn
    '''对于穷游的name字段进行过滤'''
    def select_qiongyou(self,cursor,conn):
        sql = '''select id,hbc_name_cn from cm_sight_qyer_etl'''
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            name_cn = row[1]
            try:
                flag = poi.isContainChinese(name_cn)
                if flag:
                    continue
                else:
                    print(name_cn)
                    # 将查询到的字段插入到n
                    sql_1 = '''update cm_sight_qyer_etl set hbc_name_en = '%s' where id = %s and hbc_name_en='' ''' %(name_cn,id)
                    sql_2 = '''update cm_sight_qyer_etl set hbc_name_cn='' where id = %s and hbc_name_en= hbc_name_cn'''%id
                    cursor.execute(sql_2)
                    conn.commit()
            except:
                continue
        cursor.close()
        conn.close()
    ''' 对于马蜂窝的name字段进行过滤'''
    def select_mafengwo(sel,poi):
        # 定义批处理，一次查询1000行
        maxsize = 1000
        # pattern = re.compile('^http')  # 正则制定pic_url 为http开头

            # 获取游标
        cur = 0
        cursor,conn= poi.getconnect()


        sql = '''select sight_id,hbc_name_cn from cm_sight_mafengwo_etl'''
        #cur = cur+1000
        cursor.execute(sql)
        # 存储数据，然后关闭链接再对数据进行操作
        result = cursor.fetchall()
        # 如果没有数据 则跳出循环

        count = 0
        # 关闭游标 释放链接

        for row in result:
            sight_id = row[0]
            name = row[1]
            try:
                flag = poi.isContainChinese(name) or len(name)==0
                print(flag)
                if flag:
                    count= count+1
                    continue
                else:
                    sql_1 = '''update cm_sight_mafengwo_etl set hbc_name_en = '%s',hbc_name_cn='' where sight_id = %s '''%(name,sight_id)
                    cursor.execute(sql_1)
                    conn.commit()
                    count = count + 1
                    #print(name,sight_id)
            except:
                continue

            print(count)

        conn.close()
        cursor.close()



    '''检验字符串是否含有中文字符'''
    def isContainChinese(self,str):
        for c in str:
            if('\u4e00' <= c <= '\u9fa5'):
                return True
        return False

    '''检验字符串是否全部为中文'''
    def isAllChinese(self,str):
        for c in str:
            if not('\u4e00' <= c <= ']u9fa5'):
                return False
        return True

if __name__ == "__main__":
    poi =Poi()
    # cursor,conn = poi.getconnect()
    # df = poi.select_qiongyou(cursor,conn)
    poi.select_mafengwo(poi)
    #poi.insert_poi(df)
