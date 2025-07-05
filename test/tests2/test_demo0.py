import allure

@allure.epic('项目0')
@allure.feature('模块1')
def test_demo0_0():
    assert True

@allure.feature('模块1')
def test_demo0_1():
    assert True

@allure.feature('模块1')
class TestDemo02(object):
    def test_demo0(self):
        assert True