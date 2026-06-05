"""
计算器模块 - 提供基本数学运算功能

这个模块展示了如何编写可测试的Python代码，包含各种数学运算方法。
"""

class Calculator:
    """计算器类，提供基本数学运算功能"""
    
    def add(self, a: float, b: float) -> float:
        """
        加法运算
        
        Args:
            a: 第一个数
            b: 第二个数
            
        Returns:
            两数之和
        """
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """
        减法运算
        
        Args:
            a: 被减数
            b: 减数
            
        Returns:
            两数之差
        """
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """
        乘法运算
        
        Args:
            a: 第一个数
            b: 第二个数
            
        Returns:
            两数之积
        """
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """
        除法运算
        
        Args:
            a: 被除数
            b: 除数
            
        Returns:
            两数之商
            
        Raises:
            ValueError: 当除数为0时抛出异常
        """
        if b == 0:
            raise ValueError("除数不能为0")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """
        幂运算
        
        Args:
            base: 底数
            exponent: 指数
            
        Returns:
            base的exponent次幂
        """
        return base ** exponent
    
    def square_root(self, x: float) -> float:
        """
        平方根运算
        
        Args:
            x: 需要计算平方根的数
            
        Returns:
            x的平方根
            
        Raises:
            ValueError: 当x为负数时抛出异常
        """
        if x < 0:
            raise ValueError("不能计算负数的平方根")
        return x ** 0.5
    
    def factorial(self, n: int) -> int:
        """
        阶乘运算
        
        Args:
            n: 需要计算阶乘的数
            
        Returns:
            n的阶乘
            
        Raises:
            ValueError: 当n为负数时抛出异常
        """
        if n < 0:
            raise ValueError("不能计算负数的阶乘")
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result


def validate_number_input(value: str) -> float:
    """
    验证并转换用户输入为数字
    
    Args:
        value: 用户输入的字符串
        
    Returns:
        转换后的浮点数
        
    Raises:
        ValueError: 当输入无法转换为数字时抛出异常
    """
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"'{value}' 不是有效的数字")


def calculate_average(numbers: list[float]) -> float:
    """
    计算平均值
    
    Args:
        numbers: 数字列表
        
    Returns:
        平均值
        
    Raises:
        ValueError: 当列表为空时抛出异常
    """
    if not numbers:
        raise ValueError("数字列表不能为空")
    return sum(numbers) / len(numbers)