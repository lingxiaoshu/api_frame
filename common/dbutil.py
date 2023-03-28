# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: dbutil.py
# @Author: chenhuaishu
# @Time: 2022/10/24 22:09
import pymysql

from common.file_load import read_yml


class DB:
    def __init__(self, db_env):
        # 调用读取yml文件的方法，读取对应的配置文件
        self.dbinfo = read_yml('/config/db.yml')[db_env]
        # 连接数据库,配置文件的内容
        self.db = pymysql.connect(
            host=self.dbinfo['host'],
            port=self.dbinfo['port'],
            user=self.dbinfo['user'],
            password=self.dbinfo['pwd'],
            charset="utf8mb4",
            # 返回数据类型-字典
            cursorclass=pymysql.cursors.DictCursor
        )
    # 查询 返回数据
    def select(self, sql):
        # 创建游标
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()  # 获取查询得到的所有数据
        self.db.commit()   # 防止多次查询不会出现问题,原子性
        cursor.close()
        return data

    # 增加 删除 修改
    def update(self,sql):
        # 创建游标
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()   # 修改语句需要提交
        cursor.close()

    def close(self):
        '''
        对数据库进行关闭
        :param self:
        :return:
        '''
        if self.db != None:
            self.db.close()

if __name__ == '__main__':
    db = DB('test')
    sql = 'select * from mtxshop_trade.es_order where trade_sn =“20210711000005”;'
    data = db.select(sql)
    print(data)