# api_frame
### 基于python+request+pytest+Excel+parametrize+logging+allure+Jenkins的接口自动化框架的搭建

#### 1.分层思想：将具有单独功能的内容抽离出来，然后封装在一起，在进行层层调用。优点：

		·完全解耦
    
		·针对具体层具体修改和debug
    
	·发起请求层：请求头、请求参数、请求url
  
	·测试用例层：pytest框架，参数化、断言、测试报告
 
#### 2.开始创建项目apiframework：

	**api**：对业务的接口发起请求
	**common**:封装请求对象和一些常用的方法,封装请求的客户端
	**data**：放一些参数化的数据
	**reports**：生成的测试报告（文件夹） 
	**logs**：存放生成的日志（文件夹） 
    先在common中增加logger日志；
    在common/client.py中增加logger日志的信息，首先在init中增加self.logger这个属性，然后在核心代码处添加logger日志的信息：logger日志一般都会增加在底层文件中
	**testcases**：存放测试用例（包）
		假设运行100条用例，用时5min，token有效时间4分钟，此时需要选择方法级别的setup
	  token需要生成几次，需要根据token有效期决定登录接口调用几次
	  conftest.py中增加fixture函数，调用登录接口并生成token，可以节省工作量

#### 3.对请求对象进行封装
  common/client.py
  当买家和卖家host和请求头相同，可以做进一步的api抽离，在base_api.py中，因为卖家和买家都需要依赖登录接口，且token的值不同，所以在该文件的两个基类中各创建卖家和买家的token

#### 4.测试报告----allure报告

  1）配置java环境
  
  2）allure配置环境变量
  
  3）安装allure-pytest
  
  4）在代码中增加内容
  
    ·pytest运行测试用例时增加参数
    pytest -sv .\testcases\test_buynow.py --alluredir ./reports/report --clean-alluredir
    --- 测试用例运行后生成json文件
    需要通过allure服务将json文件生成html文件：
    allure generate ./reports/report -o ./reports/html --clean
    ·开启allure服务
    
#### 5.将pytest参数放入一个配置文件（pytest.ini, 名字固定）中进行管理，存放参数配置信息

#### 6.将配置信息写入python代码中：
·在当前项目下创建主文件，运行主文件即可

#### 7.生成项目对应用到的模块
	·安装pipreqs    pip install pipreqs
	·在当前工程目录生成文件requirements.txt
		pipreqs . --encoding=utf-8 --force
	·使用requirements.txt安装依赖的方式（便于其他人直接下载）
		pip install -r requirements.txt
	
#### 8.数据库封装
	对响应内容中的trade_sn字段提取，查询数据数据库，看trade_sn是否存在，对数据库进行封装 common/dbutil.py
	
#### 9.提取数据
  很多接口会需要提取响应中的部分内容，可以在底层文件（client.py）中的RequestsClient新增对响应值提取的方法
