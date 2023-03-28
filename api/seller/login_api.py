from api.base_api import SellerBaseApi
from common.client import RequestsClient
from common.encry_decry import md5

# 卖家登录接口api
class SellerLoginApi(SellerBaseApi):
    def __init__(self):
        # super().__init__()   同等功能
        SellerBaseApi.__init__(self)
        self.url = self.host + '/seller/login'
        self.method = 'get'
        self.params = {
            'username': 'shamoseller',
            # 密码通过md5加密
            'password': md5('123456'),
            'captcha': '1512',
            'uuid': 'qwert'
        }


if __name__ == '__main__':
    resp = SellerLoginApi().send()
    print(resp.text)
