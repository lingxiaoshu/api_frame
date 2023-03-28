# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: base_api.py
# @Author: chenhuaishu
# @Time: 2022/10/24 16:24
import requests

from common.client import RequestsClient
from common.file_load import read_yml


class BuyerBaseApi(RequestsClient):
    buyer_token = None
    def __init__(self):
        RequestsClient.__init__(self)
        # self.host = 'http://www.mtxshop.com:7002'
        self.host = read_yml('/config/mtx_host.yml')['buyerhost']
        self.headers = {
            'Authorization': BuyerBaseApi.buyer_token  # access_token需要从登录接口中提取
        }
class SellerBaseApi(RequestsClient):
    seller_token = None
    def __init__(self):
        RequestsClient.__init__(self)
        # self.host = 'http://www.mtxshop.com:7003'
        self.host = read_yml('/config/mtx_host.yml')['sellerhost']
        self.headers = {
            'Authorization': SellerBaseApi.seller_token  # access_token需要从登录接口中提取
        }

class BasicBaseApi(RequestsClient):
    def __init__(self):
        RequestsClient.__init__(self)
        # self.host = 'http://www.mtxshop.com:7000'
        self.host = read_yml('/config/mtx_host.yml')['basichost']
