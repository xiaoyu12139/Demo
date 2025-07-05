import os
import sys

import pytest
import qqemail


if __name__ == '__main__':
    # pytest.main(['-s','test_demo.py'])
    # pytest.main(['-s','test_demo.py::test_demo01'])
    # pytest.main(['--collect-only'])
    # pytest.main(['-s'])
    # pytest.main(['--capture=no', 'tests'])
    # pytest.main(['--capture=no', 'tests/test_demo2.py'])
    # pytest.main(['tests1/test_demo.py'])
    pytest.main(['tests3'])
    # pytest.main()

    # 发送报告
    os.system('allure generate allure-results -o allure-report --clean')
    zippath = qqemail.zip_report()
    qqemail.send_email_with_qq(zippath)