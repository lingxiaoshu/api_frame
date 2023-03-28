# 
# -*- coding: utf-8 -*-
# ---
# @Project: apiframework
# @Software: PyCharm
# @File: re_exercise.py
# @Author: chenhuaishu
# @Time: 2022/10/25 23:10
import re

from common import encry_decry

# 反射：字符串当做特殊的函数处理
# 判断文件中是否有对应的函数：hasattr(filename,字符串类型的函数的名字)
# 返回True，文件中存在函数，否则没有
result = hasattr(encry_decry,'md5')
print(result)

# 获取md5函数：将md5字符串转化为函数
# md5的函数对象 = getattr（文件名字，‘md5’）
# 调用：result = md5的函数对象（参数）
function_obj = getattr(encry_decry, 'md5')
print(function_obj)
result = function_obj('yaoyao123456')
print(result)