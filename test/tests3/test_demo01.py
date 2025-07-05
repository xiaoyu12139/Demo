import allure
import pytest
import logging

log = logging.getLogger()

@allure.epic('用户模块')
@allure.feature('登录功能')
@allure.story('用户输入密码登录')
@allure.title('登录成功测试')
# @pytest.mark.usefixtures('click_login_bt')
def test_login_success():
    log.info("login success")
    assert True, '登录成功'

@allure.epic('用户模块')
@allure.feature('登录功能')
@allure.story('用户输入密码登录')
@allure.title('登录失败测试')
# @pytest.mark.usefixtures('click_login_bt')
def test_login_fail():
    log.info("login fail")
    assert True, '登录失败'
