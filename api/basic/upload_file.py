# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: upload_file.py
# @Author: chenhuaishu
# @Time: 2022/10/24 23:49
from api.base_api import BasicBaseApi
from setting import DIR_NAME


class UploadFileApi(BasicBaseApi):
    def __init__(self, filename):
        super().__init__()
        self.url = self.host +'/uploaders'
        self.method = 'post'
        self.params = {
        "scene":'goods'
        }
        self.files = {
            'file': ('1.png', open(DIR_NAME+'/data/'+filename, 'rb'), 'image/png')
        }
if __name__ == '__main__':
    UploadFileApi('1.png').send()
