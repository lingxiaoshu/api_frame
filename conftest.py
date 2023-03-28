import jsonpath
import pytest

from api.base_api import BuyerBaseApi, SellerBaseApi
from api.buy.login_api import BuyerLoginApi
from api.seller.login_api import SellerLoginApi


# hook函数
def pytest_collection_modifyitems(items):
    # item表示每个测试用例，解决测试用例中名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")

'''
fixture 函数可以实现setup的功能，在测试用例之前执行内容，类似初始化
功能更强大，可以任意命名
@pytest.fixture(scope="",autouse=False)
autouse=False:不自动引用
session：pytest发起请求到结束，只会执行一次（命令行发起pytest请求）
function：函数级别的测试用例和方法级别的测试用例执行一次
class：引用fixture函数的class类，就会执行一次
module:引用fixture函数的python文件，就会执行一次

引用：把fixture装饰的函数的名字当做参数传递到测试用例中调用即可
'''
@pytest.fixture(scope='function',autouse=True)
def buyer_login():
    # 依赖登录接口
    buyerapi = BuyerLoginApi()
    # 发起请求
    resp = buyerapi.send()
    # 生成token
    BuyerBaseApi.buyer_token = jsonpath.jsonpath(resp.json(), '$.access_token')[0]
    # print("========buyer_login======")

@pytest.fixture(scope='function',autouse=True)
def seller_login():
    # 登录接口
    sellerloginapi = SellerLoginApi()
    sellerloginapi.send()
    # 数据提取
    SellerBaseApi.seller_token = sellerloginapi.extract_expr('$.access_token')