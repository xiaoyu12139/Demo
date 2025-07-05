import logging
import os
import shutil
import pytest
import allure

log = logging.getLogger()

def pytest_configure(config):
    print("=== pytest_configure hook is running! ===")
    logging.basicConfig(
        filename='pytest.log',  # 日志文件名称
        level=logging.INFO,  # 设置日志级别为 INFO
        format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
        filemode='a'  # 追加模式，'a' 表示追加
    )

def pytest_unconfigure(config):
    logging.info("pytest_unconfigure")
    print("=== pytest_unconfigure hook is running! ===")

def pytest_sessionstart(session):
    logging.info("pytest_sessionstart")
    results_dir = "allure-results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
        os.mkdir(results_dir)

@pytest.fixture(autouse=False, scope="session")
def myconfig(pytestconfig):
    markers = pytestconfig.getini('markers')
    # print(f"markers: {markers}")
    logging.info(f"markers: {markers}")

@pytest.fixture(autouse=False, scope='function')
def fixture01():
    print("\nfixture01 setup")
    yield 8
    print("\nfixture01 teardown")

@pytest.fixture(scope='function', params=[1,2,3,4,5])
def fixture02(request):
    logging.info("fixture02")
    return request.param


@allure.step('输入用户名')
@pytest.fixture(scope='function')
def enter_user():
    log.info('enter_user')

@allure.step('输入密码')
@pytest.fixture(scope='function')
def enter_password():
    log.info('enter_password')

@allure.step('点击登录按钮')
@pytest.fixture(scope='function')
# @pytest.mark.usefixtures('enter_user', 'enter_password')
def click_login_bt():
    log.info('click_login_bt')

