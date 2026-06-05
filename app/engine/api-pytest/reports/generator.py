"""
测试报告生成器

提供多种格式的测试报告生成功能，包括HTML、JSON、XML、Allure等。
"""

import subprocess
import sys
import os
import json
import webbrowser
from pathlib import Path
from datetime import datetime
from . import TestReportConfig, create_custom_html_report


def run_tests_with_reports(report_type="all", test_path=None, name=None):
    """
    运行测试并生成报告
    
    Args:
        report_type: 报告类型，可选值: all, html, json, xml, allure, coverage
        test_path: 测试路径，默认运行所有测试
        name: 报告名称前缀
        
    Returns:
        测试结果字典
    """
    config = TestReportConfig()
    
    # 构建pytest命令
    cmd = [sys.executable, "-m", "pytest"]
    
    # 添加测试路径
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    # 添加报告选项
    report_options = config.generate_pytest_options(report_type, name)
    cmd.extend(report_options)
    
    # 添加其他选项
    cmd.extend([
        "-v",
        "--tb=short",
    ])
    
    print("=" * 60)
    print("运行测试并生成报告")
    print("=" * 60)
    print(f"命令: {' '.join(cmd)}")
    print(f"报告类型: {report_type}")
    print(f"报告名称: {name}")
    print()
    
    # 运行测试
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        # 解析输出
        output = result.stdout
        
        # 提取测试结果统计
        stats = extract_test_stats(output)
        
        print("测试输出摘要:")
        print("-" * 40)
        print(f"标准输出:\n{output[-1000:]}")  # 打印最后1000字符
        if result.stderr:
            print(f"错误输出:\n{result.stderr[-1000:]}")
        
        print("\n" + "=" * 60)
        print("报告生成完成")
        print("=" * 60)
        
        # 显示报告位置
        report_summary = config.get_report_summary()
        print("\n📁 报告位置:")
        for report_type, path in report_summary["报告目录"].items():
            print(f"  {report_type}: {path}")
        
        # 如果生成Allure报告，尝试打开
        if report_type in ["all", "allure"]:
            try:
                generate_allure_report(config)
            except Exception as e:
                print(f"⚠️  Allure报告生成失败: {e}")
                print("请确保已安装Allure命令行工具: https://docs.qameta.io/allure/#_installing_a_commandline")
        
        # 如果生成HTML报告，显示路径
        if report_type in ["all", "html"]:
            html_path = config.get_html_report_path(name)
            print(f"\n🌐 HTML报告: file://{html_path.absolute()}")
            
            # 询问是否打开浏览器
            try:
                response = input("\n是否在浏览器中打开HTML报告? (y/n): ").lower()
                if response == 'y':
                    webbrowser.open(f"file://{html_path.absolute()}")
            except:
                pass  # 如果无法获取输入，跳过
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stats": stats,
            "output": output,
            "reports": report_summary,
        }
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 测试运行失败: {e}")
        return {
            "success": False,
            "returncode": e.returncode,
            "error": str(e),
            "output": e.stdout + e.stderr,
        }


def extract_test_stats(output):
    """
    从pytest输出中提取测试统计信息
    
    Args:
        output: pytest输出文本
        
    Returns:
        统计信息字典
    """
    stats = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
        "duration": 0,
    }
    
    # 简单的解析逻辑
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        
        if "collected" in line and "items" in line:
            # 解析格式: "collected 20 items"
            parts = line.split()
            if len(parts) >= 2:
                try:
                    stats["total"] = int(parts[1])
                except:
                    pass
        
        # 匹配多种格式的测试结果行
        if ("passed" in line or "failed" in line or "skipped" in line or "error" in line.lower()) and "in" in line and "s" in line:
            # 解析格式: "1 passed, 2 warnings in 0.04s"
            # 或: "20 passed, 0 failed, 0 skipped in 0.12s"
            parts = line.split()
            for i, part in enumerate(parts):
                if part.isdigit():
                    # 检查下一个词是什么
                    if i + 1 < len(parts):
                        next_word = parts[i + 1].lower()
                        if "passed" in next_word:
                            try:
                                stats["passed"] = int(part)
                            except:
                                pass
                        elif "failed" in next_word:
                            try:
                                stats["failed"] = int(part)
                            except:
                                pass
                        elif "skipped" in next_word:
                            try:
                                stats["skipped"] = int(part)
                            except:
                                pass
                        elif "error" in next_word:
                            try:
                                stats["errors"] = int(part)
                            except:
                                pass
                elif part.endswith("s") and part[:-1].replace('.', '').isdigit():
                    # 可能是时间，如 "0.04s"
                    try:
                        stats["duration"] = float(part[:-1])
                    except:
                        pass
    
    # 如果没有明确的总数，尝试计算总数
    if stats["total"] == 0:
        stats["total"] = stats["passed"] + stats["failed"] + stats["skipped"] + stats["errors"]
    
    # 计算通过率
    if stats["total"] > 0:
        pass_rate = (stats["passed"] / stats["total"]) * 100
        stats["pass_rate"] = f"{pass_rate:.1f}%"
    else:
        stats["pass_rate"] = "0%"
    
    return stats


def generate_allure_report(config):
    """
    生成Allure报告
    
    Args:
        config: TestReportConfig实例
    """
    try:
        # 检查是否安装了allure命令行工具
        allure_cmd = ["allure", "--version"]
        result = subprocess.run(allure_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("⚠️  Allure命令行工具未安装")
            print("请参考: https://docs.qameta.io/allure/#_installing_a_commandline")
            return
        
        print("\n🎨 生成Allure报告...")
        
        # 生成Allure报告
        allure_results = config.get_allure_results_dir()
        allure_report = config.get_allure_report_dir()
        
        cmd = [
            "allure", "generate",
            str(allure_results),
            "-o", str(allure_report),
            "--clean"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅  Allure报告已生成: file://{allure_report.absolute()}/index.html")
            
            # 询问是否打开Allure报告
            try:
                response = input("是否在浏览器中打开Allure报��? (y/n): ").lower()
                if response == 'y':
                    webbrowser.open(f"file://{allure_report.absolute()}/index.html")
            except:
                pass
        else:
            print(f"❌  Allure报告生成失败: {result.stderr}")
            
    except FileNotFoundError:
        print("❌  Allure命令行工具未找到")
        print("安装指南:")
        print("1. macOS: brew install allure")
        print("2. Linux: sudo apt-add-repository ppa:qameta/allure && sudo apt update && sudo apt install allure")
        print("3. Windows: scoop install allure")
    except Exception as e:
        print(f"❌  Allure报告生成失败: {e}")


def generate_custom_report(test_results, name=None):
    """
    生成自定义格式的报告
    
    Args:
        test_results: 测试结果数据
        name: 报告名称
        
    Returns:
        报告文件路径
    """
    config = TestReportConfig()
    
    # 准备报告数据
    report_data = {
        "project_name": config.project_name,
        "timestamp": config.timestamp,
        "total": test_results.get("total", 0),
        "passed": test_results.get("passed", 0),
        "failed": test_results.get("failed", 0),
        "skipped": test_results.get("skipped", 0),
        "errors": test_results.get("errors", 0),
        "pass_rate": test_results.get("pass_rate", "0%"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    # 生成自定义HTML报告
    output_path = config.get_html_report_path(name or "custom")
    create_custom_html_report(report_data, output_path)
    
    print(f"✅  自定义报告已生成: {output_path}")
    return output_path


def open_report_in_browser(report_path):
    """
    在浏览器中打开报告
    
    Args:
        report_path: 报告文件路径
    """
    try:
        if isinstance(report_path, Path):
            report_path = str(report_path.absolute())
        
        webbrowser.open(f"file://{report_path}")
        print(f"🌐  已在浏览器中打开报告: {report_path}")
    except Exception as e:
        print(f"❌  无法打开报告: {e}")


def list_reports():
    """
    列出所有生成的报告
    """
    config = TestReportConfig()
    report_summary = config.get_report_summary()
    
    print("📋 可用报告:")
    print("-" * 40)
    
    for report_type, directory in report_summary["报告目录"].items():
        dir_path = Path(directory)
        if dir_path.exists():
            reports = list(dir_path.glob("*"))
            if reports:
                print(f"\n{report_type}:")
                for report in sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:  # 显示最近5个
                    mtime = datetime.fromtimestamp(report.stat().st_mtime)
                    size_mb = report.stat().st_size / (1024 * 1024)
                    print(f"  • {report.name} ({mtime.strftime('%Y-%m-%d %H:%M')}, {size_mb:.2f} MB)")
            else:
                print(f"\n{report_type}: 暂无报告")
    
    print("\n" + "=" * 60)
    print("使用说明:")
    print("  1. 运行测试并生成报告: python -m reports.runner")
    print("  2. 查看报告列表: python -m reports.runner --list")
    print("  3. 打开最新报告: python -m reports.runner --open")
    print("=" * 60)