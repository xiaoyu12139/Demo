import pytest

def setup_module():
    print('setup_module\n')

def setup_function():
    print("setup function\n")

def teardown_function():
    print("teardown function\n")

def test_demo03():
    print('demo03')
    assert True

def test_demo04():
    print('demo04')
    with pytest.raises(TypeError):
        a = 1 / 0

def test_demo05():
    print('demo05')
    assert 0.2 + 0.1 == pytest.approx(0.3), '比较错误'

def test_demo06():
    print('demo06')
    assert 0.2 + 0.1 == 0.3, '比较错误'