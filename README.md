python main.py --debug

# 加载之前的对话并保存新对话
python main.py --load previous_chat.json --save new_chat.json

# 直接执行单个命令
python main.py --command "创建一个 Hello World 程序"
```

## 🔧 工具功能

Code Agent 内置了以下工具：

### 1. 文件读取 (`read_file`)
```
👤 You: 读取 config.json 文件的内容
```

### 2. 文件写入 (`write_file`)
```
👤 You: 创建一个名为 test.py 的文件，包含一个简单的 Flask 应用
```

### 3. 命令执行 (`execute_command`)
```
👤 You: 运行 pip list 命令查看已安装的包
```

### 4. 目录列表 (`list_directory`)
```
👤 You: 显示 src 目录下的所有文件
```

### 5. 文件搜索 (`search_files`)
```
👤 You: 在项目中搜索包含 "import requests" 的文件
```

## 📝 使用示例

### 示例 1: 项目初始化
```
👤 You: 帮我创建一个新的 Python 项目结构，包含 src 目录、tests 目录和 requirements.txt

🤖 Assistant: 我来为您创建一个标准的 Python 项目结构...
[Agent 会自动创建目录和文件]
```

### 示例 2: 代码分析
```
👤 You: 分析 main.py 文件，找出可能的性能问题

🤖 Assistant: 我来分析您的 main.py 文件...
[Agent 会读取文件并提供分析报告]
```

### 示例 3: 批量处理
```
👤 You: 读取 data 目录下的所有 JSON 文件，并生成一个汇总报告

🤖 Assistant: 我来处理 data 目录下的 JSON 文件...
[Agent 会自动遍历目录并处理文件]
```

### 示例 4: 环境检查
```
👤 You: 检查我的开发环境，确认 Python、Git 和 Node.js 的版本

🤖 Assistant: 我来检查您的开发环境...
[Agent 会执行相关命令并报告版本信息]
```
# 🤖 Local Code Agent
## ⚙️ 配置说明

### 修改默认模型

编辑 `main.py` 或使用命令行参数：

```python
# 在 main.py 中修改默认模型
parser.add_argument("--model", default="your-preferred-model", help="使用的模型名称")
```

### 自定义 Ollama 服务地址

编辑 `agent/coding_agent.py`：

```python
self.client = OpenAI(
    base_url="http://your-ollama-server:11434/v1/",  # 修改这里
    api_key="ollama"
)
```

### 添加新工具

在 `CodingAgent` 类中添加新的工具函数：

```python
def your_custom_tool(self, param: str) -> str:
    """自定义工具功能"""
    # 实现您的工具逻辑
    return result
```

## 🐛 常见问题

### Q: 启动时提示连接错误
**A:** 确保 Ollama 服务正在运行：
```bash
ollama serve
```

### Q: 模型响应很慢
**A:** 尝试使用更小的模型：
```bash
python main.py --model qwen2.5:7b
```

### Q: 文件操作失败
**A:** 检查文件路径和权限：
- 使用绝对路径
- 确保有读写权限
- 检查文件是否存在

### Q: 命令执行超时
**A:** 当前命令超时设置为 30 秒，对于长时间运行的命令，可以修改 `execute_command` 方法中的 `timeout` 参数。

### Q: 如何扩展新功能
**A:** 
1. 在 `_define_tools()` 中添加工具定义
2. 实现对应的工具函数
3. 在 `_execute_tool_call()` 中添加调用逻辑

## 📄 项目结构

```
local_code_agent/
├── README.md              # 项目说明文档
├── main.py               # 主程序入口
├── __init__.py           # 包初始化文件
└── agent/
    ├── __init__.py       # Agent 包初始化
    ├── coding_agent.py   # 核心 Agent 类
    └── utils.py          # 工具函数
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📜 许可证

本项目采用 MIT 许可证。

---

**💡 提示**: 开始使用时，建议先输入 `help` 命令熟悉基本功能，然后尝试一些简单的文件操作来体验 Agent 的能力。

一个基于大语言模型的智能编程助手，能够自动执行文件操作、代码分析、命令行操作等开发任务。

## 📋 目录

- [功能特性](#功能特性)
- [安装配置](#安装配置)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [命令行参数](#命令行参数)
- [工具功能](#工具功能)
- [使用示例](#使用示例)
- [配置说明](#配置说明)
- [常见问题](#常见问题)

## ✨ 功能特性

- 🔧 **智能工具调用** - 自动选择合适的工具完成任务
- 📁 **文件操作** - 读取、创建、修改文件
- ⚡ **命令执行** - 安全的 shell 命令执行
- 🔍 **项目浏览** - 目录结构查看和文件搜索
- 💬 **自然语言交互** - 用日常语言描述需求
- 📚 **对话历史** - 保存和加载对话记录
- 🎯 **调试模式** - 详细的执行日志
- 🎨 **友好界面** - 加载动画和清晰反馈

## 🛠️ 安装配置

### 前置要求

1. **Python 3.8+**
2. **Ollama** (本地大模型服务)
3. **必要的 Python 包**

### 安装步骤

1. **安装 Ollama**
   ```bash
   # 访问 https://ollama.ai/ 下载安装
   # 或使用包管理器安装
   ```

2. **拉取模型**
   ```bash
   ollama pull qwen2.5:32b
   # 或其他支持的模型
   ```

3. **安装 Python 依赖**
   ```bash
   pip install openai pathlib
   ```

4. **启动 Ollama 服务**
   ```bash
   ollama serve
   ```

## 🚀 快速开始

### 基本使用

```bash
# 进入项目目录
cd local_code_agent

# 启动 Code Agent
python main.py
```

启动后，您将看到交互式界面：

```
🤖 Code Agent 已启动！
📝 输入 'help' 查看帮助，输入 'quit' 退出
--------------------------------------------------

👤 You: 
```

### 第一个示例

```
👤 You: 列出当前目录的文件

🤖 Assistant: 我来为您列出当前目录的文件...

📁 agent/
📄 main.py
📄 README.md
📄 __init__.py
```

## 📖 使用指南

### 交互式模式

在交互式模式下，您可以：

1. **用自然语言描述需求**
   ```
   👤 You: 帮我创建一个计算器的 Python 文件
   ```

2. **使用内置命令**
   - `help` - 显示帮助信息
   - `quit` - 退出程序
   - `reset` - 重置对话历史
   - `clear` - 清屏

3. **组合多个任务**
   ```
   👤 You: 先读取 config.json 文件，然后创建一个 Python 脚本来解析这个配置
   ```

## 🛠️ 命令行参数

```bash
python main.py [选项]
```

### 可用选项

| 参数 | 说明 | 示例 |
|------|------|------|
| `--model` | 指定使用的模型 | `--model qwen2.5:7b` |
| `--debug` | 启用调试模式 | `--debug` |
| `--load` | 加载对话历史 | `--load chat.json` |
| `--save` | 保存对话历史 | `--save chat.json` |
| `--command` | 执行单个命令 | `--command "读取 main.py"` |

### 使用示例

```bash
# 使用不同模型
python main.py --model "llama2:13b"

# 启用调试模式

