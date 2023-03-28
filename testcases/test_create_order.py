# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: test_create_order.py
# @Author: chenhuaishu
# @Time: 2022/10/24 22:01
import jsonpath
import pytest

from api.buy.buy_now import BuyNowApi
from api.buy.creatorder_api import CreatOrderApi
from common.dbutil import DB


class TestCreateOrder():
    # 数据库连接
    def setup_class(self):
        self.db = DB('test')
    # 数据库关闭
    def teardown_class(self):
        self.db.close()
    def test_create_order(self):
        # 立即登录接口
        BuyNowApi().send()
        # 创建登录接口
        createorderapi = CreatOrderApi()
        resp = createorderapi.send()
        # 断言
        pytest.assume(resp.text)
        pytest.assume(resp.status_code)
        # 断言：从响应中提取trade_sn 查询数据库，看是否能返回数据
        trade_sn = createorderapi.extract_expr('$.trade_sn')
        # 数据库查询
        # db = DB('test')
        sql = 'select * from mtxshop_trade.es_order where trade_sn ={};'.format(trade_sn)
        data = self.db.select(sql)
        pytest.assume(len(data) == 1)
        # db.close()
