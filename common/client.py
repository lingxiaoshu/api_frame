
'''
封装请求的对象
'''
import jsonpath
import requests

from common.encry_decry import md5
from common.logger import GetLogger


class RequestsClient:
    # 这个类会作为所有单接口测试的基类出现，因此在类中定义好接口需要的各个字段
    def __init__(self):
        # 创建logger日志对象
        self.logger = GetLogger.get_logger()
        # 创建session对象
        self.session = requests.session()
        self.host = None
        self.url = None
        self.headers = None
        self.method = None
        self.params = None
        self.data = None
        self.json = None
        self.files = None
        self.resp = None

    # 对于请求中存在很多不确定的参数，因此采用可变参数进行传递
    # 如果init里面定义了一些属性，子类可以进行继承+重新进行传递，如果init里面没有定义的属性，可以通过send（）中
    # **kwargs参数进行传递
    def send(self, **kwargs):
        '''
        kwargs 字典
        **kwargs 解包 -> 关键字传参进行传递
        发起请求
        :return:
        '''
        if kwargs.get('url') == None:
            kwargs['url'] = self.url
        if kwargs.get('method') == None:
            kwargs['method'] = self.method
        if kwargs.get('headers') == None:
            kwargs['headers'] = self.headers
        if kwargs.get('params') == None:
            kwargs['params'] = self.params
        if kwargs.get('data') == None:
            kwargs['data'] = self.data
        if kwargs.get('json') == None:
            kwargs['json'] = self.json
        if kwargs.get('files') == None:
            kwargs['files'] = self.files
        # 日志 查看接口的各个值
        for item in kwargs.items():
            self.logger.info('接口信息是：{}'.format(item))
        self.logger.info('准备开始发起请求')
        # 发送请求，获取响应数据
        self.resp = self.session.request(**kwargs)
        self.logger.info('接口响应状态码是：{}'.format(self.resp.status_code))
        self.logger.info('接口响应内容是：{}'.format(self.resp.text))
        return self.resp
    def extract_expr(self, jsonpath_express, index=0):
        '''

        :param index: 代表想要获取目标结果中的第几个数据。index=0，默认获取第一个数据
        index=1,2……正常索引值的获取
        index=-1   获取所有的数据
        :return:
        '''
        if self.resp != None and self.resp != '':
            if index >= 0:
                extract_data = jsonpath.jsonpath(self.resp.json(), jsonpath_express)[index]
                self.logger.info('接口的提取出来的响应内容是:{}'.format(extract_data))
                return extract_data
            elif index == -1:
                extract_data = jsonpath.jsonpath(self.resp.json(), jsonpath_express)
                self.logger.info('接口的提取出来的响应内容是:{}'.format(extract_data))
                return extract_data

if __name__ == '__main__':
    # 卖家登录
    url = 'http://www.mtxshop.com:7003/seller/login'
    params = {
        'username': 'shamoseller',
        # 密码通过md5加密
        'password': md5('123456'),
        'captcha': '1512',
        'uuid': 'qwert'
    }
    kwargs = {
        'url':url,
        'method':'get',
        'params':params
    }
    client = RequestsClient()
    resp = client.send(**kwargs)
    print(f'响应内容{resp.json()}')
    print(f'响应状态码{resp.status_code}')