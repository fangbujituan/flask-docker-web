"""
用户管理器测试模块

测试UserManager和User类的功能，包括用户注册、登录、验证等。
"""

import pytest
from demo.user_manager import UserManager, User, validate_email, validate_password


class TestUserClass:
    """测试User类的功能"""
    
    def test_user_creation(self, sample_user):
        """测试用户创建"""
        assert sample_user.username == "testuser", "用户名应该是'testuser'"
        assert sample_user.email == "test@example.com", "邮箱应该是'test@example.com'"
        assert sample_user.is_active is True, "新用户应该是活跃状态"
        assert sample_user.last_login is None, "新用户的最后登录时间应该为None"
    
    def test_password_verification(self, sample_user):
        """测试密码验证"""
        # 正确的密码应该验证通过
        assert sample_user.verify_password("testpass123") is True, "正确密码应该验证通过"
        
        # 错误的密码应该验证失败
        assert sample_user.verify_password("wrongpass") is False, "错误密码应该验证失败"
    
    def test_login_success(self, sample_user):
        """测试成功登录"""
        result = sample_user.login("testpass123")
        assert result is True, "使用正确密码应该登录成功"
        assert sample_user.last_login is not None, "登录后最后登录时间应该被设置"
    
    def test_login_failure(self, sample_user):
        """测试失败登录"""
        result = sample_user.login("wrongpass")
        assert result is False, "使用错误密码应该登录失败"
        assert sample_user.last_login is None, "登录失败后最后登录时间应该保持为None"
    
    def test_user_status_changes(self, sample_user):
        """测试用户状态变化"""
        # 初始状态应该是活跃
        assert sample_user.is_active is True, "初始状态应该是活跃"
        
        # 禁用用户
        sample_user.deactivate()
        assert sample_user.is_active is False, "禁用后用户应该不活跃"
        
        # 重新激活用户
        sample_user.activate()
        assert sample_user.is_active is True, "激活后用户应该活跃"
    
    def test_to_dict(self, sample_user):
        """测试转换为字典"""
        user_dict = sample_user.to_dict()
        
        assert user_dict["username"] == "testuser", "字典应包含用户名"
        assert user_dict["email"] == "test@example.com", "字典应包含邮箱"
        assert user_dict["is_active"] is True, "字典应包含活跃状态"
        assert "created_at" in user_dict, "字典应包含创建时间"
        assert user_dict["last_login"] is None, "字典应包含最后登录时间"


class TestUserManagerClass:
    """测试UserManager类的功能"""
    
    def test_register_new_user(self, user_manager):
        """测试注册新用户"""
        # 初始用户数量
        initial_count = len(user_manager.users)
        
        # 注册新用户
        result = user_manager.register("david", "david@example.com", "pass123")
        
        assert result is True, "注册应该成功"
        assert len(user_manager.users) == initial_count + 1, "用户数量应该增加1"
        assert "david" in user_manager.users, "新用户应该被添加"
    
    def test_register_duplicate_username(self, user_manager):
        """测试注册重复用户名"""
        with pytest.raises(ValueError) as exc_info:
            user_manager.register("alice", "newalice@example.com", "newpass123")
        
        assert "已存在" in str(exc_info.value), "应该提示用户名已存在"
    
    def test_register_duplicate_email(self, user_manager):
        """测试注册重复邮箱"""
        with pytest.raises(ValueError) as exc_info:
            user_manager.register("newalice", "alice@example.com", "newpass123")
        
        assert "已存在" in str(exc_info.value), "应该提示邮箱已存在"
    
    def test_login_success(self, user_manager):
        """测试用户登录成功"""
        result = user_manager.login("alice", "pass123")
        assert result is True, "正确的用户名和密码应该登录成功"
        
        # 验证最后登录时间被更新
        user = user_manager.get_user("alice")
        assert user.last_login is not None, "登录后最后登录时间应该被设置"
    
    def test_login_wrong_password(self, user_manager):
        """测试错误密码登录"""
        result = user_manager.login("alice", "wrongpass")
        assert result is False, "错误密码应该登录失败"
    
    def test_login_nonexistent_user(self, user_manager):
        """测试不存在的用户登录"""
        result = user_manager.login("nonexistent", "pass123")
        assert result is False, "不存在的用户应该登录失败"
    
    def test_get_user(self, user_manager):
        """测试获取用户"""
        user = user_manager.get_user("alice")
        assert user is not None, "应该能获取到存在的用户"
        assert user.username == "alice", "获取的用户用户名应该是'alice'"
        
        # 测试获取不存在的用户
        user = user_manager.get_user("nonexistent")
        assert user is None, "不存在的用户应该返回None"
    
    def test_deactivate_user(self, user_manager):
        """测试禁用用户"""
        result = user_manager.deactivate_user("alice")
        assert result is True, "禁用用户应该成功"
        
        user = user_manager.get_user("alice")
        assert user.is_active is False, "用户应该被禁用"
    
    def test_activate_user(self, user_manager):
        """测试激活用户"""
        # 先禁用用户
        user_manager.deactivate_user("alice")
        
        # 再激活用户
        result = user_manager.activate_user("alice")
        assert result is True, "激活用户应该成功"
        
        user = user_manager.get_user("alice")
        assert user.is_active is True, "用户应该被激活"
    
    def test_get_all_users(self, user_manager):
        """测试获取所有用户"""
        users = user_manager.get_all_users()
        
        assert len(users) == 3, "应该有3个用户"
        # 验证每个用户都包含必要字段
        for user in users:
            assert "username" in user, "用户字典应包含用户名"
            assert "email" in user, "用户字典应包含邮箱"
            assert "is_active" in user, "用户字典应包含活跃状态"
    
    def test_get_active_users(self, user_manager):
        """测试获取活跃用户"""
        # 禁用一个用户
        user_manager.deactivate_user("alice")
        
        active_users = user_manager.get_active_users()
        
        # 应该只有2个活跃用户
        assert len(active_users) == 2, "应该有2个活跃用户"
        
        # 验证所有返回的用户都是活跃的
        for user in active_users:
            assert user["is_active"] is True, "所有用户都应该是活跃的"
    
    def test_clear_all_users(self, user_manager):
        """测试清空所有用户"""
        assert len(user_manager.users) > 0, "初始应该有用户"
        
        user_manager.clear_all_users()
        
        assert len(user_manager.users) == 0, "清空后应该没有用户"


class TestValidationFunctions:
    """测试验证函数"""
    
    @pytest.mark.parametrize("email,expected", [
        ("test@example.com", True),
        ("user.name@domain.co.uk", True),
        ("a@b.c", True),
        ("test@example", False),  # 缺少顶级域名
        ("testexample.com", False),  # 缺少@符号
        ("@example.com", False),  # 缺少用户名
        ("", False),  # 空字符串
    ])
    def test_validate_email(self, email, expected):
        """测试邮箱验证"""
        result = validate_email(email)
        assert result == expected, f"邮箱 '{email}' 的验证结果应该是 {expected}"
    
    @pytest.mark.parametrize("password,expected", [
        ("pass123", True),  # 包含字母和数字，长度>=6
        ("password123", True),  # 包含字母和数字，长度>=6
        ("123456a", True),  # 包含字母和数字，长度>=6
        ("12345", False),  # 长度<6
        ("abcdef", False),  # 不包含数字
        ("123456", False),  # 不包含字母
        ("", False),  # 空字符串
        ("a1b2c", False),  # 长度<6
    ])
    def test_validate_password(self, password, expected):
        """测试密码验证"""
        result = validate_password(password)
        assert result == expected, f"密码 '{password}' 的验证结果应该是 {expected}"


@pytest.mark.integration
class TestIntegration:
    """集成测试"""
    
    def test_complete_user_workflow(self):
        """测试完整的用户工作流程"""
        manager = UserManager()
        
        # 1. 注册新用户
        manager.register("newuser", "newuser@example.com", "StrongPass123")
        
        # 2. 验证用户存在
        user = manager.get_user("newuser")
        assert user is not None, "新用户应该存在"
        
        # 3. 登录成功
        login_result = manager.login("newuser", "StrongPass123")
        assert login_result is True, "新用户应该能登录"
        
        # 4. 登录失败（错误密码）
        login_result = manager.login("newuser", "WrongPass123")
        assert login_result is False, "错误密码应该登录失败"
        
        # 5. 禁用用户
        manager.deactivate_user("newuser")
        user = manager.get_user("newuser")
        assert user.is_active is False, "用户应该被禁用"
        
        # 6. 尝试登录被禁用的用户
        login_result = manager.login("newuser", "StrongPass123")
        assert login_result is False, "被禁用的用户应该不能登录"
        
        # 7. 重新激活用户
        manager.activate_user("newuser")
        user = manager.get_user("newuser")
        assert user.is_active is True, "用户应该被重新激活"
        
        # 8. 再次登录应该成功
        login_result = manager.login("newuser", "StrongPass123")
        assert login_result is True, "重新激活后应该能登录"


@pytest.mark.slow
class TestSlowOperations:
    """慢速操作测试"""
    
    def test_slow_user_operations(self):
        """测试大量用户操作"""
        manager = UserManager()
        
        # 注册大量用户
        for i in range(100):
            manager.register(f"user{i}", f"user{i}@example.com", f"pass{i}")
        
        assert len(manager.users) == 103, "应该有103个用户（100个新用户 + 3个初始用户）"
        
        # 验证所有用户
        for i in range(100):
            user = manager.get_user(f"user{i}")
            assert user is not None, f"用户'user{i}'应该存在"
            assert user.email == f"user{i}@example.com", f"用户'user{i}'的邮箱应该正确"