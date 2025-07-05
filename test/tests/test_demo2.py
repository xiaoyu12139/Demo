import logging

import pytest

@pytest.mark.skip
def test_demo01():
    print("demo01")
    # print(f"fixture01:{fixture01}")

@pytest.mark.smoke
@pytest.mark.usefixtures('fixture01')
def test_demo02():
    logging.info("demo02")

@pytest.mark.skip
class TestDemo3(object):

    def test_demo03(self):
        print("demo03")

    def test_demo04(self):
        print("demo04")








