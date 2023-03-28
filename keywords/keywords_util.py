#
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: keywords_util.py
# @Author: chenhuaishu
# @Time: 2022/10/25 16:14
# 存储所有的变量信息
import pandas
import pymysql

from setting import DIR_NAME

global_variables = {}

# 存储api的信息
apis = {}

# 获取所有变量的值
def get_global_variables():
    res = pandas.read_excel(DIR_NAME+'/data/mtxshop_keywords.xlsx',
                      sheet_name='全局变量',
                      keep_default_na=False,
                      engine='openpyxl')
    # 获取行
    row_count = res.shape[0]
    for row in range(row_count):
        key = res.iloc[row, 0]  # 变量
        value = res.iloc[row, 1] # 值
        global_variables[key] = value  # 存储到全局变量

# 获取api的存储信息
def get_apis_info():
    res = pandas.read_excel(DIR_NAME+'/data/mtxshop_keywords.xlsx',
                      sheet_name='单接口',
                      keep_default_na=False,
                      engine='openpyxl')
    row_count = res.shape[0]
    col_count = res.columns.size
    for row in range(row_count):
        # api的名字获取
        api_name = res.iloc[row, 0]
        # 定义列表
        api_info_list = []
        for col in range(1, col_count):
            text = res.iloc[row, col]
            api_info_list.append(text)
        # api_name为键，将api的url，method，headers，和参数为元素的列表作为值存储到apis中
        apis[api_name] = api_info_list

# 获取所有要执行的测试用例
def get_all_cases():
    res = pandas.read_excel(DIR_NAME + '/data/mtxshop_keywords.xlsx',
                            sheet_name='测试用例集合',
                            keep_default_na=False,
                            engine='openpyxl')
    # 获取行
    row_count = res.shape[0]
    case_list = []
    for row in range(row_count):
        if res.iloc[row, 1].lower() == 'y':
            case_list.append(res.iloc[row,0])

    return case_list

# 获取测试用例中每个接口的信息，保存到一个字典中
def get_cases_info(casename):
    '''

    :param casename: 测试用例的名字--sheet页的名字
    :return: {’casename':[[接口1的信息-url，method,headers,参数，响应提取，状态码断言，，],[接口2的信息……]]
    '''
    res = pandas.read_excel(DIR_NAME + '/data/mtxshop_keywords.xlsx',
                            sheet_name=casename,
                            keep_default_na=False,
                            engine='openpyxl')
    # 获取行
    row_count = res.shape[0]
    col_count = res.columns.size
    # 返回测试用例信息,字典
    cases_info = {}
    # 存储需要调用的接口的所有信息
    steps = []
    for row in range(row_count):
        api_name = res.iloc[row, 0]
        api_infos = apis[api_name]
        for col in range(1, col_count):
            api_infos.append(res.iloc[row, col])   # api_infos 包含请求和响应的所有信息

        steps.append(api_infos)
    cases_info[casename] = steps
    return cases_info

# 封装数据库
class DB():
    def __init__(self):
        # 连接数据库 配置文件的内容
        self.db = pymysql.connect(
            # 数据库的信息-全局变量sheet页中-global_variables-{"dbip":xxx,"dbport":xx,...}
            host=global_variables['dbip'],
            port=global_variables['dbport'],
            user=global_variables['dbusername'],
            # 存储excel里面的key是dbpwd
            password=global_variables['dbpwd'],
            charset='utf8mb4',
            # 返回的数据类型-字典
            cursorclass=pymysql.cursors.DictCursor
        )
    # 查询 返回数据
    def select(self,sql):
        '''

        :param sql: 原生的查询语句
        :return:
        '''
        # 创建游标
        cursor = self.db.cursor()
        cursor.execute(sql)  # 执行sql
        data = cursor.fetchall()  # 获取查询得到的所有数据
        self.db.commit()  # 一次连接多次查询时会有问题
        cursor.close()
        return data

    # 增加 删除 修改
    def update(self,sql):
        '''

        :param sql: 原生的sql(修改，删除，增加语句)
        :return:
        '''
        cursor = self.db.cursor()
        cursor.execute(sql)  # 执行sql
        self.db.commit()  # 但凡有更新语句都是要提交
        cursor.close()
    def close(self):
        '''
        对数据库进行关闭
        :return:
        '''
        if self.db != None:
            self.db.close()

if __name__ == '__main__':
    get_apis_info()   # 构造apis变量的函数，给apis提供接口的数据
    data = get_cases_info('立即购买-数量为空')
    print(data)
    # get_global_variables()
    # print(global_variables)
    all_cases = get_all_cases()
    print(all_cases)

