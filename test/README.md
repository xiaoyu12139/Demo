> 2025-4-23

夹具：

* auto=true，scope="function"则所有的测试函数与类的所有测试方法都会自动调用
* auto=true, scope="class"则所有的测试函数与类会自动调用，类只调用一次
* auto=true, scope="moudle"则每个模块调用一次
* auto=true, scope="session"则启动时调用一次

config.py用于配置共享夹具

setup_xx, teardown_xx: 其中xx为(function,method,class,moudle) ，配置在config.py中不生效，必须在所需要用的模块中定义，所导入到需要用的模块

读取pytest.ini的文件可以使用内置夹具pytestconfig.getini(“配置名”)

print不会打印，因为pytest将输出重定向了，使用logging可打印

夹具中的params，在夹具中使用request.param返回，然后在测试函数中显示调用即可拿到这个param

在pytest_configure中使用logging打印失败的原因是，执行这个钩子函数时，logging还未配置好，使用print即可打印，在pytest_configure中进行logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")配置后调用logging可打印成功

**钩子函数** 和 **夹具** 中的 `print` 行为差异主要与 **日志捕获**（log capturing）功能和 `pytest` 的输出处理机制有关。`pytest` 默认会捕获标准输出（如 `print` 输出），并将其包含在测试报告中，但它会限制 **测试函数中的 `print` 输出**，而允许钩子函数中的 `print` 输出显示在控制台。

`pytest_configure` 会在 `pytest` 测试框架初始化时调用，通常是在 `pytest` 解析完配置文件（如 `pytest.ini`）和命令行选项之后，但在这时，`pytest` 还没有开始加载你的代码文件或模块。

常见的钩子函数：configure,unconfigure,sessionstart,sessionfinish

pytest_runtest_protocol(item, nextitem)

pytest_runtest_call(item)

pytest_runtest_logreport(report)

pytest_deselected(items)

pytest_collection_modifyitems(items)

生成allure报告：pip install allure-pytest, 运行参数--alluredir=allure-results，查看allure serve allure-results

allure generate allure-results --clean输出报告到指定目录

> 2025-4-24

allure常用注解：

* @allure.epic项目
* @allure.featrue功能
* @allure.title用例名称
* @allure.description用例描述
* @aluure.severity优先级
* @allure.step步骤

页面介绍：

* 类别：是用于帮助测试人员分析失败的用例，将失败用例按照失败原因（AssertionError、TimeoutError 等）**分类归因**；帮助排查错误。默认显示显示失败或异常用例。通过categories.json定制规则
* Suites，测试套件：显示所有测试套件下的所有测试用例
* Overview：图表和统计视图，展示通过率/趋势等信息
* 测试套：测试脚本集合，可以是一整个类、一个模块或一组测试；通常逻辑上是一组相关测试。每个 `.py` 文件或测试类构成一个“套件”
* 功能：对应系统的业务功能，比如“用户登录”、“商品下单”，feature（用户模块）对应业务模块，store（登录功能）对应具体子模块。
* 测试用例：一个具体的测试函数
* 包：Python 的模块/包目录；也可以指测试文件所属的包路径。目录或模块（如 `tests/login/test_x.py`）控制项目代码组织 / import 路径

Package（包） → Feature（功能） → Suite（测试套） → Test Case（测试用例）

```sql
用户模块 (Epic)
├── 用户登录功能 (Feature)
    ├── 使用账号密码登录 (Story)
    │   ├── 测试账号密码登录成功(title)
    │   └── 测试账号密码错误登录失败(title)
    └── 使用验证码登录 (Story)
        └── 验证码正确登录成功(title)
```

step的两种写法：

* with allure.step("登录用户"):
          user_token = login("vip_user", "123456")
* @allure.step("登录操作：用户名={username}，密码={password}")
  def do_login(username, password):
      return login(username, password)

在步骤中控制夹具调用顺序，使用嵌套或者在一个夹具内调用执行步骤，但这样可能会导致step只显示最后调用的一个

除非在一个夹具内使用with的方法实现step

还或者在测试函数中，显示调用夹具

#### 自动发邮件

```
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
```

server发送后需要显示调用server.quit()否则会报错

使用zipfile包压缩报告，然后发送

使用qq邮箱发送：qq邮箱中设置打开stmp服务，获取授权码

```
auth_code = 'tpgmgswayrxqebji'
sender = "2267592072@qq.com"
receiver = ["zhouji0726@163.com"]  # 可写多个
smtp_server = "smtp.qq.com"
smtp_port = 465
```
