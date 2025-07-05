import logging

import allure
import pytest


# @pytest.mark.parametrize(
#     "num",
#     [1,2,3,4,5])
# def test_demo10(num: int):
#     logging.info("test demo 10")
#     logging.info(num)
#

@allure.epic('项目')
@allure.feature('模块')
@allure.title('用例名称')
@allure.description('用例描述')
@allure.severity(allure.severity_level.NORMAL)
@allure.step('步骤1')
def test_demo20(fixture02):
    logging.info("test demo 20")
    logging.info(fixture02)

# @pytest.mark.parametrize(
#     "num",
#     [1,2,3,4,5])
# def test_demo30(fixture02, num):
#     logging.info("test_demo30")
#     logging.info(f'fixture02: {fixture02}')
#     logging.info(f'num: {num}')