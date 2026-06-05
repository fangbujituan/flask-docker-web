"""
测试报告模块 - 提供多种测试报告工具

这个模块封装了pytest的各种报告插件，提供统一的报告生成接口。
"""

import os
import json
import datetime
from pathlib import Path


REPORTS_DIR = Path(__file__).parent
HTML_REPORT_DIR = REPORTS_DIR / "html"
JSON_REPORT_DIR = REPORTS_DIR / "json"
XML_REPORT_DIR = REPORTS_DIR / "xml"
ALLURE_REPORT_DIR = REPORTS_DIR / "allure-results"
ALLURE_REPORT_OUTPUT = REPORTS_DIR / "allure-report"


def ensure_directories():
    """确保报告目录存在"""
    directories = [
        REPORTS_DIR,
        HTML_REPORT_DIR,
        JSON_REPORT_DIR,
        XML_REPORT_DIR,
        ALLURE_REPORT_DIR,
        ALLURE_REPORT_OUTPUT,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    return directories


def get_timestamp():
    """获取时间戳字符串"""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class TestReportConfig:
    """测试报告配置类"""
    
    def __init__(self):
        self.timestamp = get_timestamp()
        self.project_name = "pytest-demo"
        self.environment = {
            "Python版本": "3.10+",
            "操作系统": "macOS/Linux/Windows",
            "pytest版本": "9.0+",
            "测试框架": "pytest",
        }
        
        ensure_directories()
    
    def get_html_report_path(self, name=None):
        """获取HTML报告路径"""
        if name:
            filename = f"test_report_{name}_{self.timestamp}.html"
        else:
            filename = f"test_report_{self.timestamp}.html"
        return HTML_REPORT_DIR / filename
    
    def get_json_report_path(self, name=None):
        """获取JSON报告路径"""
        if name:
            filename = f"test_report_{name}_{self.timestamp}.json"
        else:
            filename = f"test_report_{self.timestamp}.json"
        return JSON_REPORT_DIR / filename
    
    def get_xml_report_path(self, name=None):
        """获取XML报告路径"""
        if name:
            filename = f"test_report_{name}_{self.timestamp}.xml"
        else:
            filename = f"test_report_{self.timestamp}.xml"
        return XML_REPORT_DIR / filename
    
    def get_allure_results_dir(self):
        """获取Allure结果目录"""
        return ALLURE_REPORT_DIR
    
    def get_allure_report_dir(self):
        """获取Allure报告目录"""
        return ALLURE_REPORT_OUTPUT
    
    def generate_pytest_options(self, report_type="all", name=None):
        """
        生成pytest命令行选项
        
        Args:
            report_type: 报告类型，可选值: all, html, json, xml, allure, coverage
            name: 报告名称前缀
            
        Returns:
            pytest命令行选项列表
        """
        options = []
        
        if report_type in ["all", "html"]:
            html_path = self.get_html_report_path(name)
            options.extend([
                f"--html={html_path}",
                "--self-contained-html",
            ])
        
        if report_type in ["all", "json"]:
            json_path = self.get_json_report_path(name)
            options.extend([
                f"--report-log={json_path}",
            ])
        
        if report_type in ["all", "xml"]:
            xml_path = self.get_xml_report_path(name)
            options.extend([
                f"--junitxml={xml_path}",
            ])
        
        if report_type in ["all", "allure"]:
            allure_dir = self.get_allure_results_dir()
            options.extend([
                f"--alluredir={allure_dir}",
            ])
        
        if report_type in ["all", "coverage"]:
            options.extend([
                "--cov=demo",
                "--cov-report=html",
                "--cov-report=term-missing",
            ])
        
        # 暂时移除metadata选项，避免格式问题
        # metadata选项在某些pytest版本中可能需要不同的格式
        # 如果需要metadata，可以使用以下格式：
        # options.extend(["--metadata", f"{{'项目名称': '{self.project_name}'}}"])
        pass
        
        return options
    
    def get_report_summary(self):
        """获取报告摘要"""
        return {
            "项目名称": self.project_name,
            "测试时间": self.timestamp,
            "环境信息": self.environment,
            "报告目录": {
                "HTML报告": str(HTML_REPORT_DIR.absolute()),
                "JSON报告": str(JSON_REPORT_DIR.absolute()),
                "XML报告": str(XML_REPORT_DIR.absolute()),
                "Allure结果": str(ALLURE_REPORT_DIR.absolute()),
                "Allure报告": str(ALLURE_REPORT_OUTPUT.absolute()),
            }
        }


def create_custom_html_report(data, output_path):
    """
    创建自定义HTML报告
    
    Args:
        data: 测试数据字典
        output_path: 输出文件路径
    """
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试报告 - {data.get('project_name', 'pytest-demo')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 0; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
        .header .subtitle {{ font-size: 1.2rem; opacity: 0.9; }}
        .summary {{ background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 30px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .summary-item {{ background: white; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .summary-item h3 {{ color: #667eea; margin-bottom: 8px; }}
        .summary-item .value {{ font-size: 2rem; font-weight: bold; }}
        .status-pass {{ color: #28a745; }}
        .status-fail {{ color: #dc3545; }}
        .status-skip {{ color: #ffc107; }}
        .status-error {{ color: #6f42c1; }}
        .test-results {{ margin-top: 30px; }}
        .test-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .test-table th, .test-table td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        .test-table th {{ background: #f8f9fa; font-weight: 600; }}
        .test-table tr:hover {{ background: #f5f5f5; }}
        .status-badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.85rem; font-weight: 600; }}
        .badge-pass {{ background: #d4edda; color: #155724; }}
        .badge-fail {{ background: #f8d7da; color: #721c24; }}
        .badge-skip {{ background: #fff3cd; color: #856404; }}
        .badge-error {{ background: #e2d9f3; color: #382149; }}
        .footer {{ margin-top: 40px; text-align: center; color: #666; font-size: 0.9rem; }}
        @media (max-width: 768px) {{
            .container {{ padding: 10px; }}
            .test-table {{ display: block; overflow-x: auto; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>📊 测试报告</h1>
            <div class="subtitle">{data.get('project_name', 'pytest-demo')} - {data.get('timestamp', '')}</div>
        </div>
    </div>
    
    <div class="container">
        <div class="summary">
            <h2>测试摘要</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <h3>总测试数</h3>
                    <div class="value">{data.get('total', 0)}</div>
                </div>
                <div class="summary-item">
                    <h3>通过</h3>
                    <div class="value status-pass">{data.get('passed', 0)}</div>
                </div>
                <div class="summary-item">
                    <h3>失败</h3>
                    <div class="value status-fail">{data.get('failed', 0)}</div>
                </div>
                <div class="summary-item">
                    <h3>跳过</h3>
                    <div class="value status-skip">{data.get('skipped', 0)}</div>
                </div>
                <div class="summary-item">
                    <h3>错误</h3>
                    <div class="value status-error">{data.get('errors', 0)}</div>
                </div>
                <div class="summary-item">
                    <h3>通过率</h3>
                    <div class="value status-pass">{data.get('pass_rate', '0%')}</div>
                </div>
            </div>
        </div>
        
        <div class="test-results">
            <h2>测试详情</h2>
            <table class="test-table">
                <thead>
                    <tr>
                        <th>测试名称</th>
                        <th>状态</th>
                        <th>耗时(秒)</th>
                        <th>详细信息</th>
                    </tr>
                </thead>
                <tbody>
                    {data.get('test_rows', '<tr><td colspan="4">暂无测试数据</td></tr>')}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>报告生成时间: {data.get('generated_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>
            <p>测试框架: pytest | 报告工具: pytest-html, allure-pytest</p>
        </div>
    </div>
</body>
</html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return output_path