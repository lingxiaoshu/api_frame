# !/usr/bin python3
# encoding: utf-8 -*-
# @author: 夭夭
# @Time: 2021-07-18 13:39
# @Copyright：北京码同学网络科技有限公司
import re
# 调用requests核心库，发起请求，获取响应,断言
from common import encry_decry
from keywords.keywords_util import get_cases_info, global_variables, DB
import pytest

def run(client,casename):
    '''

    :param client: client = RequestsClient()的对象
    :param casename: 测试用例的名字
    :return:
    '''
    cases_info = get_cases_info(casename) # {casename:[[接口1的信息],[接口2的信息]]}
    steps = cases_info[casename]
    for step in steps:
        # url 0, method 1,headers 索引值2，请求参数 索引值3，
        # 响应提取 4，状态码断言 5，响应断言 6，数据库断言  7，用例参数 8
        # 字符串转换成字典的方法：'{"params":{\n"sku_id":891,\n"num":2\n}}'
        # 1.eval():可以将类似字典的字符串转换成字典 2.json.loads() 把json字符串转换成字典
        # eval()特点: 转换空字符串会报错，所以判空
        ####请求参数的处理#######
        # 1.url地址 ${变量} 变量替换
        url = step[0]
        client.url = regex_sub(url) # url做变量替换
        # 2.method
        method=step[1]
        client.method = method
        # 3.headers
        headers = step[2]
        if headers != '':
            # 先变量替换 然后做eval转换
            # 正则表达式是对字符串做处理
            client.headers = eval(regex_sub(headers))
        # 4.请求参数
        # 优先级处理: 如果测试用例有用例参数就用用例参数，否则就用默认参数
        if step[8] != '': # 用例参数有值
            params = regex_sub(step[8])  # 变量替换
        else:# 用api里面默认的参数
            params = regex_sub(step[3])  # 变量替换
        # md5函数加密替换
        params = regex_func(params)
        # 把字符串转换成字典
        params = eval(params)
        # 判断请求参数是什么类型：查询参数，data表单，file，json呢
        if 'params'in params:
            client.params = params['params'] # 查询参数
        if 'data' in params:
            client.data = params['data']
        if 'json' in params:
            client.json = params['json']
        if 'files' in params:
            client.data = params['files']
        ##########发起请求
        resp=client.send()
        ######## 获取响应了，断言处理
        # 响应提取 4，状态码断言 5，响应断言 6，数据库断言  7，
        # 5.数据提取
        extract_data = step[4]
        if extract_data !='': # '{"buyerToken":"$.access_token"\n}'
            extract_data = eval(extract_data)  # 字符串转字典
            for item in extract_data.items():# item 是(key,value)
                key = item[0]  # 数据提取赋值的变量
                jsonpath_value = item[1]   # jsonpath的表达式
                # 解析jsonpath表达式
                value = client.extract_expr(jsonpath_value)
                # 把响应数据里面提取出的变量和值存储到全局变量global_variables
                global_variables[key]=value
        # 6.状态码断言
        expect_status_code = step[5]
        if expect_status_code != '':
            # 断言  pytest.assume(表达式)
            pytest.assume(resp.status_code==expect_status_code)
        # 7.响应断言 # '{"actual":"$.message", "expect":"购买数量不能为空"}'
        expect_body_assert = step[6]
        if expect_body_assert != '':
            expect_body_assert=eval(expect_body_assert)
            jsonpath_value = expect_body_assert['actual']  # jsonpath表达式
            # 解析jsonpath表达式
            actual_value = client.extract_expr(jsonpath_value)
            expect_value = expect_body_assert["expect"]
            pytest.assume(actual_value==expect_value)
        # 8.数据库断言  实际值(sql查询结果)==预期(响应结果提取)
        # excel里面数据书写
        # '{
        # "sql":"SELECT uname,nickname FROM mtxshop_member.es_member where uname=\'yaoyao\';",
        # \n"actual":"uname,nickname",
        # \n"expect":{\n"uname":"$.username",\n"nickname":"$.nickname"\n}\n}'
        db_assert = step[7]
        if db_assert != '':
            db_assert = eval(db_assert)
            sql = db_assert['sql']
            actual = db_assert['actual'] # "uname,nickname"
            expect = db_assert['expect']
            # 创建数据库对象-选择关键字自己封装的数据库库
            db = DB()
            result = db.select(sql)[0]   # {'uname': 'yaoyao', 'nickname': 'yaoyao'}
            actual_li = actual.split(',')  # ['uname','nickname']
            for actual_key in actual_li:
                # 获取result数据库里面的值
                actual_value = result.get(actual_key)
                # 响应里面的预期的表达式
                expect_jsonpath = expect.get(actual_key)
                expect_value = client.extract_expr(expect_jsonpath)
                # 断言
                pytest.assume(actual_value==expect_value)





# 替换变量
# 1.检索那个位置用到了变量的引用2.替换变量:global_variables
def regex_sub(string):
    '''
${buyerHost}- buyerHost-global_variables对应的真实的值-替换${buyerHost}=http://www.mtxshop.com:7002
    :param string: '${buyerHost}/passport/login'
    :return:
    '''
    # re.findall(pattern,string)
    # pattern 正则表达式的规则  目标字符串
    # 在string这个字符串中进行检索，看是否有符合pattern正则表达式的部分，如果有就返回，没有即返回None
    # findall如果有值的话，返回的是[符合规则的值，xxx]
    # $ 以什么结尾是特殊的正则表达式，匹配的${} 这个$并没有特殊函数 \转义的意思
    # results = re.findall(r'\$\{(.+?)\}',"${{md5(yaoyao123456)}}")
    results = re.findall(r'\$\{([^\{].+?)\}', string)
    # print(results)
    for result in results:
        # buyerHost这个变量所代表的真实的值是什么？
        # global_variables里面去找
        value = global_variables[result]
        # print('value的值是{}'.format(value))
        # 做替换${buyerHost}-'http://www.mtxshop.com:7002'
        # pattern:这个规则可以把你想要替换掉的内容匹配出来
        string =re.sub(r'\$\{'+result+'\}',value,string)
    return string

# md5方法的替换
# 方法替换的前提：方法一定是提前定义好了，提取函数，然后动态调用函数.
def regex_func(func_str):
    '''
    ${{函数的名字(参数)}}
    思路:
    1.正则表达式检索哪个字符串用到了函数引用
    1.1 替换之前需要拿到函数的返回值, 调用的是哪个函数，传递的参数是什么
    1.2 函数的名字     参数
    1.3 找到底层定义的函数的名字 然后进行调用
    2.替换: ${{md5(yaoyao123456)}}替换成函数运行之后的结果
    func_str: "${{md5(yaoyao123456)}}"
    :return:
    '''
    results =re.findall(r'\$\{\{(.+?)\((.+?)\)\}\}',func_str)
    # print(results)  # [('md5', 'yaoyao123456')]
    for result in results:
        func_name = result[0]
        # print(func_name)
        param_name = result[1]
        # print(param_name)
        # 判断文件里面是否有func_name这个函数
        if hasattr(encry_decry,func_name):
            # 获取func_name这个函数的对象
            func_obj = getattr(encry_decry,func_name)
            # 函数的调用，并获取返回值
            value = func_obj(param_name)
            # 替换变量
            # ${{md5(yaoyao123456)}} 替换成value  "${{md5(yaoyao123456)}}"
            # ${{ +func_name + ( + param_name+ )}}
            # sub(pattern,字符串的替换数据,原来的字符串)
            func_str = re.sub(r'\$\{\{'+func_name+r'\('+param_name+r'\)\}\}',str(value),func_str)
    return func_str


if __name__ == '__main__':
    # re.findall(pattern,string)
    # pattern 正则表达式的规则  目标字符串
    # 在string这个字符串中进行检索，看是否有符合pattern正则表达式的部分，如果有就返回，没有即返回None
    # findall如果有值的话，返回的是[符合规则的值，xxx]
    # $ 以什么结尾是特殊的正则表达式，匹配的${} 这个$并没有特殊含义 \转义的意思
    # {n,m} {1,3} 匹配1次，2次或者3次
    # .任意字符  + 代表数量:至少有一个
    # ？禁止贪婪 正则匹配是默认贪婪的 只要符合条件的 都会匹配到
    # global_variables ={'buyerHost': 'http://www.mtxshop.com:7002',
    #   'sellerHost': 'http://www.mtxshop.com:7003',
    #                    'managerHost': 'http://www.mtxshop.com:7004',
    #                    'basicHost': 'http://www.mtxshop.com:7000', 'dbip': '121.42.15.146', 'dbport': 3306, 'dbusername': 'root', 'dbpwd': 'Testfan#123', '': ''}
    # md5函数的应用${{md5(1234556)}}
    # 匹配到变量的引用，而不是md5函数的引用，正则表达式不严谨，需要完善
    # results = re.findall(r'\$\{(.+?)\}',"${{md5(yaoyao123456)}}")
    # results = re.findall(r'\$\{([^\{].+?)\}',"${{md5(yaoyao123456)}}")
    # print(results)
    # for result in results:
    #     # buyerHost这个变量所代表的真实的值是什么？
    #     # global_variables里面去找
    #     value = global_variables[result]
    #     print('value的值是{}'.format(value))
    #     # 做替换${buyerHost}-'http://www.mtxshop.com:7002'
    #     # pattern:这个规则可以把你想要替换掉的内容匹配出来
    #     new_string =re.sub(r'\$\{'+result+'\}',value,'${buyerHost}/passport/login')
    #     print(new_string)
    #
    # url = regex_sub('${buyerHost}/passport/login')
    # print(url)
    results =re.findall(r'\$\{\{(.+?)\((.+?)\)\}\}',"${{md5(yaoyao123456)}}")
    print(results)  # [('md5', 'yaoyao123456')]
    for result in results:
        func_name = result[0]
        print(func_name)
        param_name = result[1]
        print(param_name)
        # 判断文件里面是否有func_name这个函数
        if hasattr(encry_decry,func_name):
            # 获取func_name这个函数的对象
            func_obj = getattr(encry_decry,func_name)
            # 函数的调用，并获取返回值
            value = func_obj(param_name)
            # 替换变量
            # ${{md5(yaoyao123456)}} 替换成value  "${{md5(yaoyao123456)}}"
            # ${{ +func_name + ( + param_name+ )}}
            # sub(pattern,字符串的替换数据,原来的字符串)
            s = re.sub(r'\$\{\{'+func_name+r'\('+param_name+r'\)\}\}',str(value),"${{md5(yaoyao123456)}}")
            print(s)



    # $ { { md5 ( yaoyao123456 ) } }
    # 正则：我是()   目标字符串：我是夭夭
    # 匹配结果 夭夭