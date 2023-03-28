# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: test_buynow.py
# @Author: chenhuaishu
# @Time: 2022/10/24 16:40
import jsonpath
import pytest

from api.base_api import BuyerBaseApi
from api.buy.buy_now import BuyNowApi
from api.buy.login_api import BuyerLoginApi
from common.file_load import read_yml, read_excel

data = read_yml('/data/buynow.yml')['buynow']
# data = read_excel('/data/buyer.xlsx','立即购买')
class TestBuyNow:
    # def setup_class(self): # 该级别只会调用一次
        # 依赖登录接口
        # buyerapi = BuyerLoginApi()
        # 发起请求
        # resp = buyerapi.send()
        # 生成token
        # BuyerBaseApi.buyer_token = jsonpath.jsonpath(resp.json(), '$.access_token')[0]
    # 登录接口调用多次，可以用setup_method
    @pytest.mark.parametrize('casename,params_name,status_assert,business_assert',data)
    def test_buynow(self,casename,params_name,status_assert,business_assert):
        buynowapi = BuyNowApi()
        # 修改立即购买的参数
        buynowapi.params = params_name
        resp = buynowapi.send()
        print(resp.status_code)
        print(resp.text)
        # 断言
        pytest.assume(resp.status_code == status_assert)
        if resp.status_code != 200:
            # 对响应体做断言
           pytest.assume(jsonpath.jsonpath(resp.json(), '$.message')[0] == business_assert)
