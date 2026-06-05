"""
测试报告运行器 - 命令行接口

提供统一的命令行接口来运行测试和生成报告。
"""

import argparse
import sys
from pathlib import Path
from .generator import (
    run_tests_with_reports,
    generate_allure_report,
    open_report_in_browser,
    list_reports,
)
from . import TestReportConfig


def main():
    """主函数 - 命令行入口点"""
    parser = argparse.ArgumentParser(
        description="pytest测试报告生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 运行所有测试并生成所有报告
  python -m reports.runner
  
  # 只生成HTML报告
  python -m reports.runner --type html
  
  # 运行特定测试并生成报告
  python -m reports.runner --path tests/test_calculator.py
  
  # 使用自定义名称
  python -m reports.runner --name smoke-test
  
  # 列出所有报告
  python -m reports.runner --list
  
  # 打开最新报告
  python -m reports.runner --open
  
  # 生成Allure报告（需要安装allure命令行工具）
  python -m reports.runner --allure
        """
    )
    
    parser.add_argument(
        "--type", "-t",
        choices=["all", "html", "json", "xml", "allure", "coverage"],
        default="all",
        help="报告类型 (默认: all)"
    )
    
    parser.add_argument(
        "--path", "-p",
        help="测试路径 (默认: tests/)"
    )
    
    parser.add_argument(
        "--name", "-n",
        help="报告名称前缀"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出所有生成的报告"
    )
    
    parser.add_argument(
        "--open", "-o",
        action="store_true",
        help="在浏览器中打开最新报告"
    )
    
    parser.add_argument(
        "--allure",
        action="store_true",
        help="生成Allure报告（需要安装allure命令行工具）"
    )
    
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="快速模式，只运行冒烟测试"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出模式"
    )
    
    args = parser.parse_args()
    
    if args.list:
        # 列出报告
        list_reports()
        return
    
    if args.open:
        # 打开最新报告
        config = TestReportConfig()
        html_dir = config.get_html_report_path().parent
        
        # 查找最新的HTML报告
        html_reports = list(html_dir.glob("*.html"))
        if html_reports:
            latest_report = max(html_reports, key=lambda x: x.stat().st_mtime)
            open_report_in_browser(latest_report)
        else:
            print("❌ 未找到HTML报告")
            print("请先运行测试生成报告: python -m reports.runner")
        return
    
    if args.allure:
        # 只生成Allure报告（假设已有测试结果）
        config = TestReportConfig()
        try:
            generate_allure_report(config)
        except Exception as e:
            print(f"❌ Allure报告生成失败: {e}")
        return
    
    # 运行测试
    report_type = args.type
    test_path = args.path
    
    if args.quick:
        # 快速模式，只运行冒烟测试
        test_path = test_path or "-m smoke"
        if not args.name:
            args.name = "smoke-test"
    
    # 运行测试并生成报告
    result = run_tests_with_reports(
        report_type=report_type,
        test_path=test_path,
        name=args.name,
    )
    
    # 根据结果退出
    if result["success"]:
        print("\n✅ 测试通过!")
        sys.exit(0)
    else:
        print("\n❌ 测试失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()