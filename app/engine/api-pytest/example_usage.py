"""
pytest使用示例 - 展示如何在代码中使用本demo

这个文件展示了如何使用本demo中的模块，并提供了测试示例。
"""

from demo.calculator import Calculator, calculate_average
from demo.user_manager import UserManager, validate_email, validate_password


def demonstrate_calculator():
    """演示计算器功能"""
    print("=" * 50)
    print("计算器功能演示")
    print("=" * 50)
    
    calc = Calculator()
    
    # 基本运算
    print(f"加法: 2 + 3 = {calc.add(2, 3)}")
    print(f"减法: 5 - 3 = {calc.subtract(5, 3)}")
    print(f"乘法: 4 * 5 = {calc.multiply(4, 5)}")
    print(f"除法: 10 / 2 = {calc.divide(10, 2)}")
    print(f"幂运算: 2^3 = {calc.power(2, 3)}")
    print(f"平方根: √9 = {calc.square_root(9)}")
    print(f"阶乘: 5! = {calc.factorial(5)}")
    
    # 平均值计算
    numbers = [1, 2, 3, 4, 5]
    print(f"平均值: {calculate_average(numbers)}")
    print()


def demonstrate_user_manager():
    """演示用户管理功能"""
    print("=" * 50)
    print("用户管理功能演示")
    print("=" * 50)
    
    manager = UserManager()
    
    # 注册用户
    print("注册用户:")
    manager.register("user1", "user1@example.com", "pass123")
    manager.register("user2", "user2@example.com", "pass456")
    print("✅ 用户注册成功")
    
    # 登录测试
    print("\n登录测试:")
    if manager.login("user1", "pass123"):
        print("✅ user1 登录成功")
    else:
        print("❌ user1 登录失败")
    
    if manager.login("user1", "wrongpass"):
        print("❌ user1 登录成功（不应该）")
    else:
        print("✅ user1 登录失败（预期）")
    
    # 获取用户信息
    print("\n用户信息:")
    users = manager.get_all_users()
    for user in users:
        print(f"  - {user['username']} ({user['email']}) - 活跃: {user['is_active']}")
    
    # 验证函数
    print("\n验证函数测试:")
    print(f"邮箱验证 'test@example.com': {validate_email('test@example.com')}")
    print(f"邮箱验证 'invalid': {validate_email('invalid')}")
    print(f"密码验证 'pass123': {validate_password('pass123')}")
    print(f"密码验证 'weak': {validate_password('weak')}")
    print()


def run_quick_tests():
    """运行快速测试"""
    print("=" * 50)
    print("快速测试演示")
    print("=" * 50)
    
    # 导入测试模块
    import pytest
    
    # 模拟运行一些测试
    print("运行计算器测试...")
    calc = Calculator()
    
    # 测试加法
    assert calc.add(2, 3) == 5, "加法测试失败"
    print("✅ 加法测试通过")
    
    # 测试除法错误
    try:
        calc.divide(5, 0)
        print("❌ 除以零测试失败")
    except ValueError as e:
        print(f"✅ 除以零测试通过: {e}")
    
    print("\n所有快速测试完成！")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("pytest应用demo - 功能演示")
    print("=" * 60 + "\n")
    
    demonstrate_calculator()
    demonstrate_user_manager()
    run_quick_tests()
    
    print("\n" + "=" * 60)
    print("如何使用pytest运行测试:")
    print("=" * 60)
    print("""
1. 安装依赖:
   pip install pytest pytest-timeout pytest-cov pytest-xdist

2. 运行测试:
   cd /app/engine/api-pytest
   
   # 运行所有测试
   pytest -v
   
   # 运行特定测试文件
   pytest tests/test_calculator.py -v
   
   # 使用运行脚本（推荐）
   ./run_tests.sh

3. 查看测试报告:
   # 生成HTML报告
   pytest --html=report.html
   
   # 查看覆盖率
   pytest --cov=demo --cov-report=html
   
详细说明请查看README.md文件。
    """)
    
    print("\n🎉 演示完成！")


if __name__ == "__main__":
    main()