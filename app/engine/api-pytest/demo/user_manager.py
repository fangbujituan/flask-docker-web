"""
用户管理模块 - 演示测试数据管理和状态验证

这个模块展示了如何管理用户数据，包括用户注册、登录验证等功能。
"""

from typing import Optional, List, Dict
from datetime import datetime


class User:
    """用户类，表示单个用户的信息"""
    
    def __init__(self, username: str, email: str, password: str):
        """
        初始化用户
        
        Args:
            username: 用户名
            email: 邮箱地址
            password: 密码
        """
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True
        
    def _hash_password(self, password: str) -> str:
        """
        简单的密码哈希函数（演示用途，实际应用中应使用更安全的哈希算法）
        
        Args:
            password: 原始密码
            
        Returns:
            哈希后的密码
        """
        # 这是一个简化的示例，实际应用应该使用bcrypt或argon2
        return f"hashed_{password}_123"
    
    def verify_password(self, password: str) -> bool:
        """
        验证密码
        
        Args:
            password: 待验证的密码
            
        Returns:
            密码是否正确
        """
        return self.password_hash == self._hash_password(password)
    
    def login(self, password: str) -> bool:
        """
        用户登录
        
        Args:
            password: 登录密码
            
        Returns:
            登录是否成功
        """
        if self.verify_password(password) and self.is_active:
            self.last_login = datetime.now()
            return True
        return False
    
    def deactivate(self):
        """禁用用户账户"""
        self.is_active = False
    
    def activate(self):
        """激活用户账户"""
        self.is_active = True
    
    def to_dict(self) -> Dict:
        """
        将用户对象转换为字典
        
        Returns:
            用户信息字典
        """
        return {
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }


class UserManager:
    """用户管理器，管理用户集合"""
    
    def __init__(self):
        """初始化用户管理器"""
        self.users: Dict[str, User] = {}
        
    def register(self, username: str, email: str, password: str) -> bool:
        """
        注册新用户
        
        Args:
            username: 用户名
            email: 邮箱地址
            password: 密码
            
        Returns:
            注册是否成功
            
        Raises:
            ValueError: 当用户名已存在或邮箱已存在时抛出异常
        """
        # 检查用户名是否已存在
        if username in self.users:
            raise ValueError(f"用户名 '{username}' 已存在")
        
        # 检查邮箱是否已存在
        for user in self.users.values():
            if user.email == email:
                raise ValueError(f"邮箱 '{email}' 已存在")
        
        # 创建新用户
        new_user = User(username, email, password)
        self.users[username] = new_user
        return True
    
    def login(self, username: str, password: str) -> bool:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            登录是否成功
        """
        user = self.users.get(username)
        if user and user.login(password):
            return True
        return False
    
    def get_user(self, username: str) -> Optional[User]:
        """
        获取用户
        
        Args:
            username: 用户名
            
        Returns:
            用户对象，如果不存在则返回None
        """
        return self.users.get(username)
    
    def deactivate_user(self, username: str) -> bool:
        """
        禁用用户
        
        Args:
            username: 用户名
            
        Returns:
            操作是否成功
        """
        user = self.get_user(username)
        if user:
            user.deactivate()
            return True
        return False
    
    def activate_user(self, username: str) -> bool:
        """
        激活用户
        
        Args:
            username: 用户名
            
        Returns:
            操作是否成功
        """
        user = self.get_user(username)
        if user:
            user.activate()
            return True
        return False
    
    def get_all_users(self) -> List[Dict]:
        """
        获取所有用户信息
        
        Returns:
            所有用户信息的字典列表
        """
        return [user.to_dict() for user in self.users.values()]
    
    def get_active_users(self) -> List[Dict]:
        """
        获取所有活跃用户信息
        
        Returns:
            所有活跃用户信息的字典列表
        """
        return [user.to_dict() for user in self.users.values() if user.is_active]
    
    def clear_all_users(self):
        """清空所有用户（用于测试清理）"""
        self.users.clear()


def validate_email(email: str) -> bool:
    """
    验证邮箱格式（简化的验证）
    
    Args:
        email: 待验证的邮箱地址
        
    Returns:
        邮箱格式是否有效
    """
    return '@' in email and '.' in email and len(email) > 5


def validate_password(password: str) -> bool:
    """
    验证密码强度（简化的验证）
    
    Args:
        password: 待验证的密码
        
    Returns:
        密码强度是否符合要求
    """
    return len(password) >= 6 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)