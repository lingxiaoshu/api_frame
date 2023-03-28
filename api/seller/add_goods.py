# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: add_goods.py
# @Author: chenhuaishu
# @Time: 2022/10/24 23:25
from api.base_api import SellerBaseApi


class AddGoods(SellerBaseApi):
    def __init__(self):
        super().__init__()
        self.url = self.host + '/seller/goods'
        self.method = 'post'
        # 请求参数的类型是json
        self.json = {
              "brand_id": "",
              "category_id": 88,
              "category_name": "",
              "goods_name": "彩虹豆测试88",
              "sn": "342435",
              "price": "101",
              "mktprice": "100",
              "cost": "60",
              "weight": "1",
              "goods_gallery_list": [
                {
                  "img_id": -1,
                  "original": "http://www.mtxshop.com:7000/statics/attachment/goods/2021/6/20/11/19099180.png",
                  "sort": 0
                }
              ],
              "quantity": 9999999,
              "goods_transfee_charge": 1,
              "has_changed": 0,
              "market_enable": 1,
              "template_id": 0,
              "exchange": {
                "category_id": "",
                "enable_exchange": 0,
                "exchange_money": 0,
                "exchange_point": 0
              },
              "shop_cat_id": 0,
              "meta_description": "",
              "meta_keywords": "",
              "page_title": "",
              "goods_params_list": [],
              "sku_list": [],
              "intro": ""
            }
