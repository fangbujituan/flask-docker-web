#!/bin/bash

# pytest应用demo - 测试运行脚本
# 中文注释，结构清晰

echo "========================================"
echo "pytest应用demo - 测试运行脚本"
echo "========================================"
echo ""

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  警告: 建议在Python虚拟环境中运行测试"
    echo "   可以使用: python -m venv venv && source venv/bin/activate"
    echo ""
fi

# 安装pytest（如果需要）
echo "1. 检查并安装pytest..."
pip install pytest pytest-timeout --quiet
echo "   ✅ pytest已安装"
echo ""

# 运行所有测试
echo "2. 运行所有测试..."
echo "   📊 测试统计:"
pytest -v --tb=short
echo ""

# 运行特定标记的测试
echo "3. 运行冒烟测试 (smoke标记)..."
pytest -v -m smoke --tb=short
echo ""

echo "4. 运行回归测试 (regression标记)..."
pytest -v -m regression --tb=short
echo ""

# 生成测试报告
echo "5. 生成HTML测试报告..."
pytest --html=test_report.html --self-contained-html
echo "   📄 报告已生成: test_report.html"
echo ""

# 运行特定测试文件
echo "6. 运行计算器测试..."
pytest tests/test_calculator.py -v --tb=short
echo ""

echo "7. 运行用户管理器测试..."
pytest tests/test_user_manager.py -v --tb=short
echo ""

# 带覆盖率的测试
echo "8. 运行带覆盖率的测试..."
pip install pytest-cov --quiet
pytest --cov=demo --cov-report=html --cov-report=term-missing
echo "   📊 覆盖率报告已生成: htmlcov/index.html"
echo ""

# 并行测试（可选）
echo "9. 并行运行测试（可选）..."
pip install pytest-xdist --quiet
pytest -n auto --tb=short
echo ""

echo "========================================"
echo "测试完成！"
echo "========================================"
echo ""
echo "📋 可用命令:"
echo "   ./run_tests.sh                # 运行所有测试"
echo "   pytest -v                     # 运行所有测试（详细模式）"
echo "   pytest -m smoke               # 只运行冒烟测试"
echo "   pytest -m regression          # 只运行回归测试"
echo "   pytest tests/test_calculator.py # 运行特定测试文件"
echo "   pytest -k \"add\"              # 运行名称包含'add'的测试"
echo "   pytest --html=report.html     # 生成HTML报告"
echo "   pytest --cov=demo             # 运行覆盖率测试"
echo ""


echo "10. 使用封装的报告工具..."
echo "   🔧 设置报告环境"
python -m reports.config_manager --setup
echo ""
echo "   📊 生成完整报告"
python -m reports.runner --type all
echo ""
echo "   🎯 运行冒烟测试"
python -m reports.runner --quick
echo ""
echo "   📈 查看覆盖率报告"
python -m reports.runner --type coverage
echo ""
echo "   📋 列出所有报告"
python -m reports.runner --list
echo ""