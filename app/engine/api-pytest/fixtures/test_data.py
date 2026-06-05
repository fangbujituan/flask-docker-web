"""
测试数据fixture - 提供测试用的共享数据

这个模块包含pytest fixtures，用于为测试提供共享的数据和资源。
"""

import pytest
from demo.calculator import Calculator
from demo.user_manager import UserManager, User


@pytest.fixture
def calculator() -> Calculator:
    """
    计算器fixture
    
    Returns:
        计算器实例
    """
    return Calculator()


@pytest.fixture
def user_manager() -> UserManager:
    """
    用户管理器fixture
    
    Returns:
        用户管理器实例
    """
    manager = UserManager()
    # 预先添加一些测试用户
    manager.register("alice", "alice@example.com", "pass123")
    manager.register("bob", "bob@example.com", "pass456")
    manager.register("charlie", "charlie@example.com", "pass789")
    return manager


@pytest.fixture
def sample_user() -> User:
    """
    示例用户fixture
    
    Returns:
        用户实例
    """
    return User("testuser", "test@example.com", "testpass123")


@pytest.fixture
def sample_numbers() -> list[float]:
    """
    示例数字列表fixture
    
    Returns:
        数字列表
    """
    return [1.0, 2.0, 3.0, 4.0, 5.0]


@pytest.fixture
def empty_list() -> list:
    """
    空列表fixture
    
    Returns:
        空列表
    """
    return []


@pytest.fixture
def test_cases() -> list[tuple]:
    """
    测试用例fixture - 提供多种测试场景
    
    Returns:
        测试用例列表，每个用例是(描述, 输入, 期望输出)
    """
    return [
        ("两个正数相加", (2, 3), 5),
        ("两个负数相加", (-2, -3), -5),
        ("正数和负数相加", (5, -3), 2),
        ("小数相加", (2.5, 3.5), 6.0),
        ("零值相加", (0, 10), 10),
        ("两个零相加", (0, 0), 0),
    ]