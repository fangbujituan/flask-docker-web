"""
测试标记和装饰器示例

展示pytest的各种标记和装饰器用法。
"""

import pytest
import time


@pytest.mark.smoke
class TestSmokeTests:
    """冒烟测试 - 基本功能验证"""
    
    @pytest.mark.smoke
    def test_basic_addition(self):
        """基本加法测试"""
        assert 1 + 1 == 2
    
    @pytest.mark.smoke  
    def test_basic_subtraction(self):
        """基本减法测试"""
        assert 5 - 3 == 2


@pytest.mark.regression
class TestRegressionTests:
    """回归测试 - 验证已有功能"""
    
    @pytest.mark.regression
    def test_string_concatenation(self):
        """字符串拼接测试"""
        result = "Hello" + " " + "World"
        assert result == "Hello World"
    
    @pytest.mark.regression
    def test_list_operations(self):
        """列表操作测试"""
        my_list = [1, 2, 3]
        my_list.append(4)
        assert my_list == [1, 2, 3, 4]
        
        my_list.remove(2)
        assert my_list == [1, 3, 4]


@pytest.mark.skip(reason="功能尚未实现")
class TestSkippedTests:
    """跳过的测试 - 功能未实现或暂时不需要"""
    
    def test_unimplemented_feature(self):
        """未实现的功能测试"""
        assert False, "这个功能还没有实现"


@pytest.mark.skipif(1 == 1, reason="条件跳过的测试")
def test_conditional_skip():
    """条件跳过的测试"""
    assert False, "这个测试应该被跳过"


@pytest.mark.xfail(reason="已知问题，预期失败")
def test_expected_failure():
    """预期失败的测试"""
    assert 1 == 2, "这个断言预期会失败"


@pytest.mark.xfail(strict=True, reason="应该失败但通过了，这是问题")
def test_unexpected_success():
    """预期失败但可能通过的测试"""
    assert 1 == 1, "这个断言应该失败但通过了"


@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
])
def test_parametrized_doubling(input_value, expected):
    """参数化测试 - 测试数字翻倍"""
    result = input_value * 2
    assert result == expected, f"{input_value} * 2 应该等于 {expected}"


@pytest.mark.parametrize("a,b,expected_sum,expected_product", [
    (1, 2, 3, 2),
    (3, 4, 7, 12),
    (0, 5, 5, 0),
])
def test_multiple_parameters(a, b, expected_sum, expected_product):
    """多参数参数化测试"""
    assert a + b == expected_sum, f"{a} + {b} 应该等于 {expected_sum}"
    assert a * b == expected_product, f"{a} * {b} 应该等于 {expected_product}"


class TestTimeout:
    """超时测试"""
    
    @pytest.mark.timeout(1)  # 1秒超时
    def test_fast_operation(self):
        """快速操作测试"""
        time.sleep(0.5)  # 应该能完成
        assert True
    
    @pytest.mark.timeout(1)  # 1秒超时
    def test_slow_operation(self):
        """慢速操作测试（应该超时）"""
        time.sleep(2)  # 应该超时
        assert False, "这个测试应该超时"


@pytest.mark.custom_marker
class TestCustomMarkers:
    """自定义标记测试"""
    
    @pytest.mark.high_priority
    def test_high_priority(self):
        """高优先级测试"""
        assert True
    
    @pytest.mark.low_priority
    def test_low_priority(self):
        """低优先级测试"""
        assert True
    
    @pytest.mark.api_test
    def test_api_endpoint(self):
        """API测试"""
        assert True


def test_assertion_messages():
    """测试断言消息"""
    result = 2 + 2
    
    # 使用自定义消息
    assert result == 4, f"期望4，实际得到{result}"
    
    # 使用更详细的断言
    expected = 4
    actual = result
    assert actual == expected, f"断言失败: 实际值{actual} != 期望值{expected}"


class TestExceptionTesting:
    """异常测试"""
    
    def test_raises_exception(self):
        """测试抛出异常"""
        with pytest.raises(ValueError) as exc_info:
            int("not_a_number")
        
        # 验证异常类型
        assert exc_info.type is ValueError
        
        # 验证异常消息
        assert "invalid literal" in str(exc_info.value).lower()
    
    def test_raises_specific_exception(self):
        """测试抛出特定异常"""
        with pytest.raises(ValueError, match="invalid literal"):
            int("abc")
    
    def test_no_exception(self):
        """测试没有异常"""
        # 这应该不会抛出异常
        result = int("123")
        assert result == 123


@pytest.mark.filterwarnings("ignore:这是一个警告")
def test_warnings():
    """测试警告"""
    import warnings
    
    # 发出一个警告
    warnings.warn("这是一个警告", UserWarning)
    
    # 这个测试应该通过，因为警告被过滤了
    assert True


def test_setup_and_teardown_fixtures(calculator, user_manager):
    """
    测试setup和teardown fixtures
    
    Args:
        calculator: 计算器fixture
        user_manager: 用户管理器fixture
    """
    # 使用来自fixtures的对象
    result = calculator.add(2, 3)
    assert result == 5
    
    users = user_manager.get_all_users()
    assert len(users) == 3
    
    # fixtures会在测试后自动清理