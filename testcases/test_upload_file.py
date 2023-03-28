# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: test_upload_file.py
# @Author: chenhuaishu
# @Time: 2022/10/25 0:06
import pytest

from api.basic.upload_file import UploadFileApi


class TestUploadFile:
    def test_upload_file(self):
        filename = '1.png'
        upload_file = UploadFileApi(filename)
        resp = upload_file.send()
        pytest.assume(resp.status_code == 200)
        # 数据提取
        if resp.status_code == 200:
            ext = upload_file.extract_expr('$.ext')
            pytest.assume(ext == filename.split('.')[-1])