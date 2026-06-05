"""
计算器测试模块

测试Calculator类的各种功能，包括基本运算和异常处理。
"""

import pytest
from demo.calculator import Calculator, validate_number_input, calculate_average


class TestCalculator:
    """测试Calculator类的功能"""
    
    def test_add(self, calculator):
        """测试加法运算"""
        result = calculator.add(2, 3)
        assert result == 5, "2 + 3 应该等于 5"
        
        result = calculator.add(-2, 3)
        assert result == 1, "-2 + 3 应该等于 1"
        
        result = calculator.add(2.5, 3.5)
        assert result == 6.0, "2.5 + 3.5 应该等于 6.0"
    
    def test_subtract(self, calculator):
        """测试减法运算"""
        result = calculator.subtract(5, 3)
        assert result == 2, "5 - 3 应该等于 2"
        
        result = calculator.subtract(3, 5)
        assert result == -2, "3 - 5 应该等于 -2"
        
        result = calculator.subtract(2.5, 1.5)
        assert result == 1.0, "2.5 - 1.5 应该等于 1.0"
    
    def test_multiply(self, calculator):
        """测试乘法运算"""
        result = calculator.multiply(2, 3)
        assert result == 6, "2 * 3 应该等于 6"
        
        result = calculator.multiply(-2, 3)
        assert result == -6, "-2 * 3 应该等于 -6"
        
        result = calculator.multiply(2.5, 4)
        assert result == 10.0, "2.5 * 4 应该等于 10.0"
        
        result = calculator.multiply(0, 100)
        assert result == 0, "0 * 100 应该等于 0"
    
    def test_divide(self, calculator):
        """测试除法运算"""
        result = calculator.divide(6, 3)
        assert result == 2, "6 / 3 应该等于 2"
        
        result = calculator.divide(5, 2)
        assert result == 2.5, "5 / 2 应该等于 2.5"
        
        result = calculator.divide(-6, 3)
        assert result == -2, "-6 / 3 应该等于 -2"
    
    def test_divide_by_zero(self, calculator):
        """测试除以零的异常处理"""
        with pytest.raises(ValueError) as exc_info:
            calculator.divide(5, 0)
        
        assert "除数不能为0" in str(exc_info.value), "应该提示'除数不能为0'"
    
    def test_power(self, calculator):
        """测试幂运算"""
        result = calculator.power(2, 3)
        assert result == 8, "2^3 应该等于 8"
        
        result = calculator.power(5, 0)
        assert result == 1, "5^0 应该等于 1"
        
        result = calculator.power(4, 0.5)
        assert result == 2.0, "4^0.5 应该等于 2.0"
    
    def test_square_root(self, calculator):
        """测试平方根运算"""
        result = calculator.square_root(9)
        assert result == 3, "9的平方根应该等于3"
        
        result = calculator.square_root(0)
        assert result == 0, "0的平方根应该等于0"
        
        result = calculator.square_root(2.25)
        assert result == 1.5, "2.25的平方根应该等于1.5"
    
    def test_square_root_negative(self, calculator):
        """测试负数平方根的异常处理"""
        with pytest.raises(ValueError) as exc_info:
            calculator.square_root(-4)
        
        assert "不能计算负数的平方根" in str(exc_info.value), "应该提示'不能计算负数的平方根'"
    
    def test_factorial(self, calculator):
        """测试阶乘运算"""
        result = calculator.factorial(5)
        assert result == 120, "5的阶乘应该等于120"
        
        result = calculator.factorial(0)
        assert result == 1, "0的阶乘应该等于1"
        
        result = calculator.factorial(1)
        assert result == 1, "1的阶乘应该等于1"
    
    def test_factorial_negative(self, calculator):
        """测试负数阶乘的异常处理"""
        with pytest.raises(ValueError) as exc_info:
            calculator.factorial(-1)
        
        assert "不能计算负数的阶乘" in str(exc_info.value), "应该提示'不能计算负数的阶乘'"
    
    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (0, 0, 0),
        (-5, 5, 0),
        (2.5, 3.5, 6.0),
    ])
    def test_add_parametrized(self, calculator, a, b, expected):
        """使用参数化测试加法"""
        result = calculator.add(a, b)
        assert result == expected, f"{a} + {b} 应该等于 {expected}"
    
    def test_multiple_operations(self, calculator):
        """测试组合运算"""
        # (2 + 3) * 4 = 20
        add_result = calculator.add(2, 3)
        multiply_result = calculator.multiply(add_result, 4)
        assert multiply_result == 20, "(2 + 3) * 4 应该等于 20"


class TestUtilityFunctions:
    """测试辅助函数"""
    
    def test_validate_number_input_valid(self):
        """测试有效的数字输入"""
        result = validate_number_input("123")
        assert result == 123.0, "'123' 应该转换为 123.0"
        
        result = validate_number_input("12.34")
        assert result == 12.34, "'12.34' 应该转换为 12.34"
        
        result = validate_number_input("-5.5")
        assert result == -5.5, "'-5.5' 应该转换为 -5.5"
    
    def test_validate_number_input_invalid(self):
        """测试无效的数字输入"""
        with pytest.raises(ValueError) as exc_info:
            validate_number_input("abc")
        
        assert "不是有效的数字" in str(exc_info.value), "应该提示输入无效"
        
        with pytest.raises(ValueError) as exc_info:
            validate_number_input("12a34")
        
        assert "不是有效的数字" in str(exc_info.value), "应该提示输入无效"
    
    def test_calculate_average(self):
        """测试平均值计算"""
        numbers = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = calculate_average(numbers)
        assert result == 3.0, "[1,2,3,4,5]的平均值应该等于3"
        
        numbers = [10.0, 20.0, 30.0]
        result = calculate_average(numbers)
        assert result == 20.0, "[10,20,30]的平均值应该等于20"
    
    def test_calculate_average_empty(self):
        """测试空列表的平均值计算异常"""
        with pytest.raises(ValueError) as exc_info:
            calculate_average([])
        
        assert "数字列表不能为空" in str(exc_info.value), "应该提示列表不能为空"


@pytest.mark.error_handling
class TestErrorHandling:
    """测试错误处理"""
    
    def test_all_errors(self, calculator):
        """测试所有可能错误场景"""
        # 除以零错误
        with pytest.raises(ValueError):
            calculator.divide(10, 0)
        
        # 负数平方根错误
        with pytest.raises(ValueError):
            calculator.square_root(-1)
        
        # 负数阶乘错误
        with pytest.raises(ValueError):
            calculator.factorial(-5)