# pytest应用demo

这是一个完整的pytest应用演示项目，展示了pytest的各种功能和最佳实践。

## 📁 项目结构

```
api-pytest/
├── demo/                    # 演示应用代码
│   ├── calculator.py       # 计算器模块
│   └── user_manager.py     # 用户管理模块
├── fixtures/               # 测试fixtures
│   └── test_data.py       # 测试数据fixtures
├── tests/                  # 测试代码
│   ├── test_calculator.py # 计算器测试
│   ├── test_user_manager.py # 用户管理测试
│   └── test_markers.py    # 标记和装饰器测试
├── conftest.py            # pytest配置
├── pytest.ini            # pytest配置文件
├── run_tests.sh          # 测试运行脚本
└── README.md            # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入项目目录
cd /app/engine/api-pytest

# 安装pytest（如果尚未安装）
pip install pytest pytest-timeout pytest-cov pytest-xdist
```

### 2. 运行测试

有多种方式运行测试：

#### 方式一：使用运行脚本（推荐）

```bash
./run_tests.sh
```

这个脚本会自动：
- 检查并安装必要的依赖
- 运行所有测试
- 运行特定标记的测试
- 生成HTML测试报告
- 运行覆盖率测试

#### 方式二：直接使用pytest命令

```bash
# 运行所有测试
pytest -v

# 运行特定测试文件
pytest tests/test_calculator.py -v

# 运行包含特定关键词的测试
pytest -k "add" -v

# 运行特定标记的测试
pytest -m smoke -v          # 冒烟测试
pytest -m regression -v     # 回归测试
pytest -m integration -v    # 集成测试

# 生成HTML报告
pytest --html=report.html --self-contained-html

# 运行覆盖率测试
pytest --cov=demo --cov-report=html --cov-report=term-missing
```

## 📚 演示内容

### 1. 基本测试功能

**计算器模块测试** (`tests/test_calculator.py`):
- 基本数学运算测试（加法、减法、乘法、除法）
- 异常处理测试（除以零、负数平方根、负数阶乘）
- 参数化测试
- 辅助函数测试

**用户管理模块测试** (`tests/test_user_manager.py`):
- 用户创建和验证
- 密码验证和登录流程
- 用户状态管理（激活/禁用）
- 数据验证函数测试
- 集成测试和工作流测试

### 2. pytest高级功能

**标记和装饰器** (`tests/test_markers.py`):
- `@pytest.mark.smoke` - 冒烟测试标记
- `@pytest.mark.regression` - 回归测试标记
- `@pytest.mark.skip` - 跳过测试
- `@pytest.mark.xfail` - 预期失败测试
- `@pytest.mark.parametrize` - 参数化测试
- `@pytest.mark.timeout` - 超时测试
- 自定义标记

**fixtures使用** (`fixtures/test_data.py`):
- 共享测试数据
- 测试资源管理
- 作用域控制（function, class, module, session）

**pytest配置** (`conftest.py`, `pytest.ini`):
- 全局配置
- 自定义命令行选项
- 测试收集和运行钩子
- 环境设置和清理

### 3. 测试类型展示

- **单元测试**: 测试单个函数或类的功能
- **集成测试**: 测试多个模块的协作
- **异常测试**: 测试错误处理
- **边界测试**: 测试边界条件
- **性能测试**: 测试执行时间
- **覆盖率测试**: 测量代码覆盖率

## 🎯 学习要点

### 测试组织最佳实践

1. **测试命名规范**:
   - 测试文件: `test_*.py` 或 `*_test.py`
   - 测试类: `Test*`
   - 测试方法: `test_*`

2. **测试结构清晰**:
   - 每个测试类专注于一个模块或功能
   - 测试方法名称描述测试内容
   - 使用有意义的断言消息

3. **测试隔离**:
   - 每个测试应该独立运行
   - 使用fixtures管理测试数据
   - 避免测试间的依赖

### pytest特性使用

1. **fixtures**:
   ```python
   @pytest.fixture
   def calculator():
       return Calculator()
   
   def test_add(calculator):
       result = calculator.add(2, 3)
       assert result == 5
   ```

2. **参数化测试**:
   ```python
   @pytest.mark.parametrize("a,b,expected", [
       (2, 3, 5),
       (0, 0, 0),
       (-5, 5, 0),
   ])
   def test_add_parametrized(calculator, a, b, expected):
       result = calculator.add(a, b)
       assert result == expected
   ```

3. **异常测试**:
   ```python
   def test_divide_by_zero(calculator):
       with pytest.raises(ValueError) as exc_info:
           calculator.divide(5, 0)
       assert "除数不能为0" in str(exc_info.value)
   ```

4. **标记和筛选**:
   ```bash
   # 运行特定标记的测试
   pytest -m smoke
   
   # 跳过慢速测试
   pytest -m "not slow"
   
   # 运行名称包含关键词的测试
   pytest -k "add"
   ```

## 🔧 配置说明

### pytest.ini
```ini
[pytest]
testpaths = tests                    # 测试文件目录
python_files = test_*.py *_test.py   # 测试文件模式
python_classes = Test*               # 测试类模式
python_functions = test_*            # 测试方法模式
addopts = -v                         # 默认选项：详细输出
tb = short                           # 错误回溯：简短格式
```

### conftest.py
- 全局fixtures定义
- pytest配置钩子
- 自定义命令行选项
- 测试环境设置

## 📊 测试报告和覆盖率

### 生成HTML测试报告
```bash
pytest --html=test_report.html --self-contained-html
```

### 生成覆盖率报告
```bash
pytest --cov=demo --cov-report=html --cov-report=term-missing
```

报告文件:
- `test_report.html` - 测试结果报告
- `htmlcov/index.html` - 代码覆盖率报告

## 🐛 调试技巧

1. **详细输出**:
   ```bash
   pytest -v                    # 详细模式
   pytest -vv                   # 更详细模式
   pytest --tb=long            # 完整错误回溯
   ```

2. **调试特定测试**:
   ```bash
   pytest tests/test_calculator.py::TestCalculator::test_add -v
   ```

3. **使用pdb调试**:
   ```bash
   pytest --pdb                # 失败时进入pdb调试
   pytest --trace              # 每个测试前进入pdb
   ```

## 📝 扩展建议

1. **添加更多测试类型**:
   - API接口测试
   - 数据库测试
   - 文件操作测试
   - 网络请求测试

2. **集成CI/CD**:
   - GitHub Actions
   - GitLab CI
   - Jenkins

3. **性能测试扩展**:
   - 使用`pytest-benchmark`进行基准测试
   - 内存使用分析
   - 并发测试

## 🤝 贡献指南

1. 遵循现有代码风格和测试结构
2. 为新功能添加相应的测试
3. 确保所有测试通过
4. 更新相关文档

## 📄 许可证

本项目仅供学习和演示用途。

---

**祝您测试愉快！** 🎉
## 📊 测试报告工具

本项目封装了完整的测试报告解决方案，支持多种报告格式和工具。

### 1. 已安装的报告工具

- **pytest-html**: 生成美观的HTML格式报告
- **pytest-cov**: 代码覆盖率分析报告
- **allure-pytest**: 生成专业的Allure测试报告
- **pytest-xdist**: 支持并行测试，提高测试速度
- **pytest-metadata**: 添加测试元数据信息
- **pytest-timeout**: 测试超时控制

### 2. 报告类型

#### 2.1 HTML报告 (`pytest-html`)
```bash
# 生成HTML报告
pytest --html=reports/html/test_report.html --self-contained-html

# 使用封装工具
python -m reports.runner --type html
```

**特点**:
- 美观的网页界面
- 测试统计摘要
- 详细的测试结果表格
- 支持筛选和搜索
- 可嵌入截图和日志

#### 2.2 覆盖率报告 (`pytest-cov`)
```bash
# 生成覆盖率报告
pytest --cov=demo --cov-report=html --cov-report=term-missing

# 使用封装工具
python -m reports.runner --type coverage
```

**特点**:
- 代码覆盖率统计
- 行覆盖率、分支覆盖率
- 未覆盖代码高亮显示
- HTML交互式报告

#### 2.3 Allure报告 (`allure-pytest`)
```bash
# 生成Allure报告（需要安装allure命令行工具）
pytest --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean

# 使用封装工具
python -m reports.runner --allure
```

**特点**:
- 专业的测试报告框架
- 丰富的图表和统计
- 测试分类和标签
- 历史趋势分析
- 支持附件（截图、日志等）

#### 2.4 JSON/XML报告
```bash
# JSON报告
pytest --report-log=reports/json/test_report.json

# JUnit XML报告（CI/CD集成）
pytest --junitxml=reports/xml/test_report.xml
```

**特点**:
- 机器可读格式
- 便于CI/CD流水线集成
- 支持自动化分析

### 3. 使用封装的报告工具

#### 3.1 设置环境
```bash
# 安装所有依赖
pip install pytest-html pytest-cov allure-pytest pytest-xdist pytest-metadata pytest-timeout

# 设置报告环境
python -m reports.config_manager --setup
```

#### 3.2 基本使用
```bash
# 运行所有测试并生成所有报告
python -m reports.runner

# 只生成HTML报告
python -m reports.runner --type html

# 运行特定测试
python -m reports.runner --path tests/test_calculator.py

# 使用自定义名称
python -m reports.runner --name smoke-test-2024
```

#### 3.3 高级功能
```bash
# 列出所有生成的报告
python -m reports.runner --list

# 在浏览器中打开最新报告
python -m reports.runner --open

# 运行冒烟测试
python -m reports.runner --quick

# 生成Allure报告
python -m reports.runner --allure
```

#### 3.4 配置管理
```bash
# 显示当前配置
python -m reports.config_manager --show

# 更新配置
python -m reports.config_manager --update pytest addopts "-v --tb=short"

# 重新设置环境
python -m reports.config_manager --setup
```

### 4. 报告目录结构

```
reports/
├── html/                    # HTML报告
│   ├── test_report_20240101_120000.html
│   └── test_report_smoke_20240101_120100.html
├── json/                   # JSON格式报告
│   └── test_report_20240101_120000.json
├── xml/                    # XML格式报告
│   └── test_report_20240101_120000.xml
├── allure-results/         # Allure原始结果
│   └── ...（多个JSON文件）
├── allure-report/          # Allure生成报告
│   ├── index.html
│   └── ...（HTML/CSS/JS文件）
└── htmlcov/               # 覆盖率报告
    ├── index.html
    └── ...（覆盖率详情）
```

### 5. 报告工具架构

```
reports/
├── __init__.py           # 报告模块初始化
├── generator.py          # 报告生成器
├── runner.py            # 命令行运行器
├── config_manager.py    # 配置管理器
├── usage_examples.py    # 使用示例
└── reports.ini          # 报告配置文件
```

### 6. 自定义报告

#### 6.1 添加自定义标记
在 `pytest.ini` 中添加：
```ini
[tool:pytest]
markers =
    smoke: 冒烟测试
    regression: 回归测试
    api_test: API测试
    performance_test: 性能测试
```

#### 6.2 配置报告选项
在 `reports/reports.ini` 中配置：
```ini
[reports]
default_type = all
auto_open = false
keep_history = 7

[html]
theme = light
show_details = true

[coverage]
threshold = 80
exclude = __pycache__/*,tests/*,venv/*
```

#### 6.3 扩展报告功能
```python
# 自定义报告生成逻辑
from reports.generator import run_tests_with_reports

result = run_tests_with_reports(
    report_type="all",
    test_path="tests/",
    name="custom-run",
    additional_options=["--maxfail=5", "--disable-warnings"]
)
```

### 7. CI/CD集成

#### 7.1 GitHub Actions 示例
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest-html pytest-cov
    
    - name: Run tests with coverage
      run: |
        cd app/engine/api-pytest
        pytest --cov=demo --cov-report=xml --junitxml=test-results.xml
    
    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: |
          app/engine/api-pytest/test-results.xml
          app/engine/api-pytest/coverage.xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        file: app/engine/api-pytest/coverage.xml
```

#### 7.2 Jenkins Pipeline 示例
```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                sh '''
                    cd app/engine/api-pytest
                    python -m reports.runner --type all
                '''
            }
            
            post {
                always {
                    junit 'reports/xml/*.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'reports/html',
                        reportFiles: '*.html',
                        reportName: 'HTML Test Report'
                    ])
                }
            }
        }
    }
}
```

### 8. 最佳实践

1. **分层报告**:
   - 冒烟测试: 快速反馈
   - 回归测试: 全面验证
   - 集成测试: 系统验证

2. **报告管理**:
   - 定期清理旧报告
   - 使用时间戳命名
   - 保留重要历史报告

3. **性能优化**:
   - 使用并行测试 (`pytest-xdist`)
   - 合理设置超时时间
   - 避免生成不必要的报告

4. **团队协作**:
   - 统一报告格式
   - 标准化标记使用
   - 共享报告模板

### 9. 故障排除

#### 9.1 Allure报告无法生成
```bash
# 检查allure是否安装
allure --version

# 安装allure
# macOS: brew install allure
# Linux: sudo apt install allure
# Windows: scoop install allure
```

#### 9.2 覆盖率报告为空
```bash
# 确保正确配置覆盖路径
pytest --cov=demo --cov-config=.coveragerc

# 检查.coveragerc���件
[run]
source = demo
omit = */test_*, */__pycache__/*
```

#### 9.3 HTML报告样式问题
```bash
# 使用自包含的HTML
pytest --html=report.html --self-contained-html

# 或指定CSS
pytest --html=report.html --css=style.css
```

### 10. 扩展建议

1. **添加截图功能**: 集成 `pytest-screenshot` 在失败时自动截图
2. **性能监控**: 集成 `pytest-benchmark` 进行性能基准测试
3. **数据库报告**: 添加数据库测试结果报告
4. **API文档生成**: 基于测试生成API文档
5. **自定义仪表板**: 创建测试结果可视化仪表板

### 11. 相关资源

- [pytest-html文档](https://pytest-html.readthedocs.io/)
- [pytest-cov文档](https://pytest-cov.readthedocs.io/)
- [Allure文档](https://docs.qameta.io/allure/)
- [pytest官方文档](https://docs.pytest.org/)

---

**报告工具已就绪！** 🚀 使用 `python -m reports.runner --help` 查看所有可用选项。