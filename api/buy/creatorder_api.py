# PyCharm
# -*- coding: utf-8 -*-
# ---
# @Soft: apiframework
# @File: creatorder_api.py
# @Author: chenhuaishu
# @Time: 2022/10/24 16:17
import jsonpath

from api.base_api import BuyerBaseApi
from api.buy.buy_now import BuyNowApi
from api.buy.login_api import BuyerLoginApi
from common.client import RequestsClient


# 创建订单api
class CreatOrderApi(BuyerBaseApi):
    def __init__(self):
        super().__init__()
        self.url = self.host + '/trade/create'
        self.params = {
        'client': 'PC',  # 字符串类型
        'way': 'BUY_NOW'
        }
        self.method = 'post'

if __name__ == '__main__':
    buyerapi = BuyerLoginApi()
    # 发起请求
    resp = buyerapi.send()
    RequestsClient.access_token = jsonpath.jsonpath(resp.json(),'$.access_token')[0]
    resp = BuyNowApi().send()
    print(resp.status_code)
    print(resp.text)
    resp = CreatOrderApi().send()
    print(resp.status_code)
    print(resp.text)
