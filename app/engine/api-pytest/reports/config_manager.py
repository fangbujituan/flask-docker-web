"""
报告配置管理器

管理pytest配置文件，提供统一的配置接口。
"""

import configparser
from pathlib import Path


class ReportConfigManager:
    """报告配置管理器"""
    
    def __init__(self, project_root=None):
        """
        初始化配置管理器
        
        Args:
            project_root: 项目根目录，默认为当前目录
        """
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).parent.parent
        
        self.pytest_ini = self.project_root / "pytest.ini"
        self.reports_config = self.project_root / "reports" / "reports.ini"
        
    def ensure_pytest_config(self):
        """确保pytest.ini配置文件存在并配置正确"""
        config = configparser.ConfigParser()
        
        if self.pytest_ini.exists():
            config.read(self.pytest_ini)
        
        # 确保有pytest section
        if "pytest" not in config:
            config["pytest"] = {}
        
        # 设置默认配置
        pytest_config = config["pytest"]
        
        # 基础配置
        defaults = {
            "testpaths": "tests",
            "python_files": "test_*.py *_test.py",
            "python_classes": "Test*",
            "python_functions": "test_*",
            "addopts": "-v --strict-markers",
            "minversion": "6.0",
            "filterwarnings": "ignore::DeprecationWarning",
            "timeout": "30",
        }
        
        # 添加或更新配置
        for key, value in defaults.items():
            if key not in pytest_config:
                pytest_config[key] = value
        
        # 添加标记定义
        self._ensure_markers(config)
        
        # 写入文件
        with open(self.pytest_ini, 'w') as f:
            config.write(f)
        
        print(f"✅ pytest.ini配置已更新: {self.pytest_ini}")
        return config
    
    def _ensure_markers(self, config):
        """确保标记定义"""
        if "tool:pytest" not in config:
            config["tool:pytest"] = {}
        
        markers_section = config["tool:pytest"]
        
        if "markers" not in markers_section:
            markers = [
                "smoke: 冒烟测试 - 基本功能验证",
                "regression: 回归测试 - 验证已有功能",
                "integration: 集成测试 - 测试模块间协作",
                "slow: 慢速测试 - 需要较长时间运行",
                "error_handling: 错误处理测试",
                "fixture_test: fixture测试",
                "api_test: API接口测试",
                "database_test: 数据库测试",
                "security_test: 安全测试",
                "performance_test: 性能测试",
                "ui_test: 用户界面测试",
            ]
            markers_section["markers"] = "\n" + "\n".join(markers)
    
    def create_reports_config(self):
        """创建报告配置文件"""
        config = configparser.ConfigParser()
        
        # 报告配置
        config["reports"] = {
            "default_type": "all",
            "auto_open": "false",
            "keep_history": "7",
            "max_reports_per_type": "10",
        }
        
        # HTML报告配置
        config["html"] = {
            "enabled": "true",
            "theme": "light",
            "show_details": "true",
            "include_logs": "true",
        }
        
        # JSON报告配置
        config["json"] = {
            "enabled": "true",
            "pretty_print": "true",
        }
        
        # XML报告配置
        config["xml"] = {
            "enabled": "true",
        }
        
        # Allure报告配置
        config["allure"] = {
            "enabled": "true",
            "categories": "true",
            "environment": "true",
        }
        
        # 覆盖率报告配置
        config["coverage"] = {
            "enabled": "true",
            "threshold": "80",
            "exclude": "__pycache__/*,tests/*,venv/*",
        }
        
        # 写入文件
        with open(self.reports_config, 'w') as f:
            config.write(f)
        
        print(f"✅ 报告配置文件已创建: {self.reports_config}")
        return config
    
    def get_config(self):
        """获取当前配置"""
        pytest_config = self.ensure_pytest_config()
        
        reports_config = None
        if self.reports_config.exists():
            reports_config = configparser.ConfigParser()
            reports_config.read(self.reports_config)
        
        return {
            "pytest": pytest_config,
            "reports": reports_config,
        }
    
    def update_config(self, section, key, value):
        """
        更新配置
        
        Args:
            section: 配置段
            key: 配置键
            value: 配置值
        """
        if section == "pytest":
            config = configparser.ConfigParser()
            config.read(self.pytest_ini)
            
            if "pytest" not in config:
                config["pytest"] = {}
            
            config["pytest"][key] = value
            
            with open(self.pytest_ini, 'w') as f:
                config.write(f)
            
            print(f"✅ pytest配置已更新: {key}={value}")
            
        elif section == "reports":
            if not self.reports_config.exists():
                self.create_reports_config()
            
            config = configparser.ConfigParser()
            config.read(self.reports_config)
            
            if key in config["reports"]:
                config["reports"][key] = value
            else:
                # 如果section不存在，创建它
                if key not in config:
                    config[key] = {}
                config[key][key.split('.')[-1]] = value
            
            with open(self.reports_config, 'w') as f:
                config.write(f)
            
            print(f"✅ 报告配置已更新: {key}={value}")
    
    def show_config(self):
        """显示当前配置"""
        config = self.get_config()
        
        print("=" * 60)
        print("当前配置")
        print("=" * 60)
        
        print("\n📝 pytest.ini配置:")
        if "pytest" in config["pytest"]:
            for key, value in config["pytest"]["pytest"].items():
                print(f"  {key:20} = {value}")
        
        print("\n📊 报告配置:")
        if config["reports"] and "reports" in config["reports"]:
            for key, value in config["reports"]["reports"].items():
                print(f"  {key:20} = {value}")
        
        print("\n🎨 HTML报告��置:")
        if config["reports"] and "html" in config["reports"]:
            for key, value in config["reports"]["html"].items():
                print(f"  {key:20} = {value}")
        
        print("\n📈 覆盖率配置:")
        if config["reports"] and "coverage" in config["reports"]:
            for key, value in config["reports"]["coverage"].items():
                print(f"  {key:20} = {value}")


def setup_report_environment():
    """设置报告环境"""
    manager = ReportConfigManager()
    
    print("=" * 60)
    print("设置测试报告环境")
    print("=" * 60)
    
    # 1. 配置pytest
    manager.ensure_pytest_config()
    
    # 2. 创建报告配置
    manager.create_reports_config()
    
    # 3. 显示配置
    manager.show_config()
    
    print("\n" + "=" * 60)
    print("环境设置完成!")
    print("=" * 60)
    print("\n下一步:")
    print("  1. 运行测试: python -m reports.runner")
    print("  2. 查看报告: python -m reports.runner --list")
    print("  3. 配置管理: python -m reports.config_manager")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="报告配置管理器")
    parser.add_argument("--setup", action="store_true", help="设置报告环境")
    parser.add_argument("--show", action="store_true", help="显示当前配置")
    parser.add_argument("--update", nargs=3, metavar=("SECTION", "KEY", "VALUE"), 
                       help="更新配置，例如: --update pytest addopts '-v --tb=short'")
    
    args = parser.parse_args()
    
    manager = ReportConfigManager()
    
    if args.setup:
        setup_report_environment()
    elif args.update:
        section, key, value = args.update
        manager.update_config(section, key, value)
    elif args.show:
        manager.show_config()
    else:
        print("使用 --help 查看可用选项")