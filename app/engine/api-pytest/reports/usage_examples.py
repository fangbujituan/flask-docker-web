"""
测试报告使用示例

展示如何使用封装的测试报告工具。
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from reports.generator import run_tests_with_reports
from reports.config_manager import setup_report_environment


def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("基本使用示例")
    print("=" * 60)
    
    # 示例1: 运行所有测试并生成所有报告
    print("\n1. 运行所有测试并生成所有报告:")
    result = run_tests_with_reports(
        report_type="all",
        name="full-run"
    )
    
    if result["success"]:
        print("✅ 测试通过!")
    else:
        print("❌ 测试失败!")
    
    return result


def example_html_report():
    """HTML报告示例"""
    print("\n" + "=" * 60)
    print("HTML报告示例")
    print("=" * 60)
    
    # 示例2: 只生成HTML报告
    print("\n2. 只生成HTML报告:")
    result = run_tests_with_reports(
        report_type="html",
        test_path="tests/test_calculator.py",
        name="calculator-tests"
    )
    
    return result


def example_coverage_report():
    """覆盖率报告示例"""
    print("\n" + "=" * 60)
    print("覆盖率报告示例")
    print("=" * 60)
    
    # 示例3: 生成覆盖率报告
    print("\n3. 生成覆盖率报告:")
    result = run_tests_with_reports(
        report_type="coverage",
        name="coverage-report"
    )
    
    return result


def example_custom_run():
    """自定义运行示例"""
    print("\n" + "=" * 60)
    print("自定义运行示例")
    print("=" * 60)
    
    # 示例4: 运行冒烟测试
    print("\n4. 运行冒烟测试:")
    result = run_tests_with_reports(
        report_type="html",
        test_path="-m smoke",
        name="smoke-test"
    )
    
    return result


def example_command_line():
    """命令行使用示例"""
    print("\n" + "=" * 60)
    print("命令行使用示例")
    print("=" * 60)
    
    examples = [
        "# 运行所有测试并生成所有报告",
        "python -m reports.runner",
        "",
        "# 只生成HTML报告",
        "python -m reports.runner --type html",
        "",
        "# 运行特定测试文件",
        "python -m reports.runner --path tests/test_calculator.py",
        "",
        "# 使用自定义名称",
        "python -m reports.runner --name my-test-run",
        "",
        "# 列出所有报告",
        "python -m reports.runner --list",
        "",
        "# 在浏览器中打开最新报告",
        "python -m reports.runner --open",
        "",
        "# 运行冒烟测试",
        "python -m reports.runner --quick",
        "",
        "# 设置报告环境",
        "python -m reports.config_manager --setup",
    ]
    
    for example in examples:
        print(example)


def main():
    """主函数"""
    print("=" * 60)
    print("pytest测试报告工具 - 使用示例")
    print("=" * 60)
    
    print("\n📦 已安装的报告工具:")
    print("  • pytest-html - HTML格式报告")
    print("  • pytest-cov - 代码覆盖率报告")
    print("  • allure-pytest - Allure测试报告")
    print("  • pytest-xdist - 并行测试")
    print("  • pytest-metadata - 测试元数据")
    
    print("\n🚀 使用步骤:")
    print("1. 设置报告环境")
    print("2. 运行测试并生成报告")
    print("3. 查看报告结果")
    print("4. 分析测试覆盖率")
    
    try:
        # 询问用户要运行的示例
        print("\n" + "-" * 60)
        print("选择示例 (输入数字):")
        print("1. 基本使用示例")
        print("2. HTML报告示例")
        print("3. 覆盖率报告示例")
        print("4. 自定义运行示例")
        print("5. 查看命令行示例")
        print("6. 设置报告环境")
        print("0. 退出")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "1":
            example_basic_usage()
        elif choice == "2":
            example_html_report()
        elif choice == "3":
            example_coverage_report()
        elif choice == "4":
            example_custom_run()
        elif choice == "5":
            example_command_line()
        elif choice == "6":
            setup_report_environment()
        elif choice == "0":
            print("再见!")
        else:
            print("无效选择")
            
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
    
    print("\n" + "=" * 60)
    print("更多信息:")
    print("  查看README.md文件获取详细文档")
    print("  使用 --help 查看命令行选项")
    print("=" * 60)


if __name__ == "__main__":
    main()