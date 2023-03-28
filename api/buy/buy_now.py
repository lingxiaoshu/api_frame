import jsonpath

from api.base_api import BuyerBaseApi
from api.buy.login_api import BuyerLoginApi
from common.client import RequestsClient


# 立即购买api
class BuyNowApi(BuyerBaseApi):
    def __init__(self):
        super().__init__()
        self.url = self.host + '/trade/carts/buy'
        self.params = {
        'sku_id':"26923",
        'num':"1"
        }
        self.method = 'post'

if __name__ == '__main__':
    buyerapi = BuyerLoginApi()
    # 发起请求
    resp = buyerapi.send()
    BuyerBaseApi.buyer_token = jsonpath.jsonpath(resp.json(),'$.access_token')[0]
    resp = BuyNowApi().send()
    print(resp.status_code)
