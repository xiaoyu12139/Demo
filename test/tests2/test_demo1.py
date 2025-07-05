import allure

@allure.epic('项目0')
@allure.feature('模块2')
def test_demo1_0():
    assert False

@allure.feature('模块2')
def test_demo1_1():
    assert True