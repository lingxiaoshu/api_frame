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

from api.base_api import SellerBaseApi
from api.buy.buy_now import BuyNowApi
from api.buy.creatorder_api import CreatOrderApi
from api.seller.add_goods import AddGoods
from api.seller.login_api import SellerLoginApi
from common.dbutil import DB


class TestAddGoods():
    # 数据库连接
    def setup_class(self):
        self.db = DB('test')
    # 数据库关闭
    def teardown_class(self):
        self.db.close()
    def test_add_goods(self):
        addgoods = AddGoods()
        resp = addgoods.send()
        # 状态码断言
        pytest.assume(resp.status_code == 200)
        if resp.status_code == 200:
            # 响应值的提取
            goods_id = addgoods.extract_expr('$.goods_id')
            # print(type(goods_id))
            # 查库
            sql = "select * from mtxshop_goods.es_goods where goods_id ={};".format(goods_id)
            data = self.db.select(sql)
            # 数据库断言
            pytest.assume(len(data) == 1)
