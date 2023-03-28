# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: test_run.py
# @Author: chenhuaishu
# @Time: 2022/10/25 17:01
import allure
import pytest

from common.client import RequestsClient
from keywords.keywords_run import run
from keywords.keywords_util import get_apis_info, get_global_variables, get_all_cases

client = RequestsClient()
# 获取所有api信息
get_apis_info()
# 获取所有的变量信息
get_global_variables()
# 获取所有的测试用例
all_cases = get_all_cases()

@allure.title('{casename}')
@pytest.mark.parametrize('casename', all_cases)
def test_run(casename):
    # 调用核心的run方法
    run(client, casename)
