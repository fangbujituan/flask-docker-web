"""
pytest配置模块 - 全局测试配置

这个文件是pytest的配置文件，pytest会自动发现并加载此文件。
它包含全局的fixtures、hooks和配置设置。
"""

import pytest
import sys
import os
from datetime import datetime


# 添加项目路径到Python路径，以便导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)  # 添加当前目录
sys.path.insert(0, os.path.join(current_dir, "demo"))  # 添加demo目录
sys.path.insert(0, os.path.join(current_dir, "fixtures"))  # 添加fixtures目录


def pytest_configure(config):
    """
    pytest配置钩子 - 在测试开始前执行
    """
    print("\n" + "=" * 60)
    print("开始运行pytest测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")


def pytest_unconfigure(config):
    """
    pytest卸载钩子 - 在测试结束后执行
    """
    print("\n" + "=" * 60)
    print("pytest测试完成")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")


def pytest_collection_modifyitems(config, items):
    """
    修改测试集合钩子 - 修改收集到的测试项
    """
    # 可以在这里添加测试项的自定义排序或标记
    for item in items:
        # 为包含特定关键词的测试添加标记
        if "error" in item.nodeid:
            item.add_marker(pytest.mark.error_handling)
        if "fixture" in item.nodeid:
            item.add_marker(pytest.mark.fixture_test)


def pytest_addoption(parser):
    """
    添加命令行选项钩子
    """
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="运行包括慢速测试在内的所有测试"
    )
    parser.addoption(
        "--integration",
        action="store_true", 
        default=False,
        help="运行集成测试"
    )


def pytest_runtest_setup(item):
    """
    测试运行设置钩子 - 在每个测试运行前执行
    """
    # 检查是否跳过慢速测试
    if "slow" in item.keywords and not item.config.getoption("--slow"):
        pytest.skip("需要 --slow 选项来运行慢速测试")


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """
    会话级别的fixture - 在整个测试会话期间执行一次
    """
    print("设置测试环境...")
    # 这里可以设置测试环境，如创建临时目录、初始化数据库等
    
    yield  # 测试运行在此处
    
    print("清理测试环境...")


@pytest.fixture(scope="module")
def module_level_resource():
    """
    模块级别的fixture - 在每个测试模块期间执行一次
    """
    print("初始化模块级别资源...")
    resource = {"module_resource": True}
    
    yield resource
    
    print("清理模块级别资源...")
    resource.clear()

# 添加一些基本的fixtures
@pytest.fixture
def calculator():
    """计算器fixture"""
    from demo.calculator import Calculator
    return Calculator()

@pytest.fixture
def user_manager():
    """用户管理器fixture"""
    from demo.user_manager import UserManager
    manager = UserManager()
    # 预先添加一些测试用户
    manager.register("alice", "alice@example.com", "pass123")
    manager.register("bob", "bob@example.com", "pass456")
    manager.register("charlie", "charlie@example.com", "pass789")
    return manager