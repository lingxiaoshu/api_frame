import jsonpath
import requests

from api.base_api import BuyerBaseApi
from common.client import RequestsClient
from common.encry_decry import md5

class BuyerLoginApi(BuyerBaseApi):
    def __init__(self):
        # 继承父类，重新改写
        super().__init__()
        self.url = self.host + '/passport/login'
        # 请求参数,构造成字典的形式

        self.params = {
            'username': 'yaoyao',
            # 密码通过md5加密
            'password': md5('yaoyao123456'),
            'captcha': '1512',
            'uuid': 'qwert'
        }
        self.method = 'post'

if __name__ == '__main__':
    # 创建登录对象
    buyerapi = BuyerLoginApi()
    # 发起请求
    resp = buyerapi.send()
    print(f'响应内容{resp.json()}')
    print(f'响应状态码{resp.status_code}')