#!/usr/bin/env python3
"""
Code Agent - 智能编程助手
基于大语言模型的代码生成和文件操作工具
"""

import sys
import os
import argparse
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

from agent.coding_agent import CodingAgent


def main():
    parser = argparse.ArgumentParser(description="Code Agent - 智能编程助手")
    parser.add_argument("--model", default="qwen2.5:32b", help="使用的模型名称")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--load", help="加载对话历史文件")
    parser.add_argument("--save", help="保存对话历史到文件")
    parser.add_argument("--command", help="直接执行单个命令")

    args = parser.parse_args()

    # 初始化Code Agent
    agent = CodingAgent(model=args.model, debug=args.debug)

    # 加载对话历史
    if args.load and os.path.exists(args.load):
        agent.load_conversation(args.load)

    print("🤖 Code Agent 已启动！")
    print("📝 输入 'help' 查看帮助，输入 'quit' 退出")
    print("-" * 50)

    # 如果有单个命令，执行后退出
    if args.command:
        response = agent.chat(args.command)
        print(f"\n🤖 Assistant: {response}")
        if args.save:
            agent.save_conversation(args.save)
        return

    # 交互式聊天循环
    try:
        while True:
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            elif user_input.lower() == 'help':
                show_help()
                continue
            elif user_input.lower() == 'reset':
                agent.reset_conversation()
                print("🔄 对话历史已重置")
                continue
            elif user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue

            # 处理用户输入
            response = agent.chat(user_input)
            print(f"\n🤖 Assistant: {response}")

    except KeyboardInterrupt:
        print("\n👋 再见！")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
    finally:
        # 保存对话历史
        if args.save:
            agent.save_conversation(args.save)


def show_help():
    """显示帮助信息"""
    help_text = """
🆘 Code Agent 帮助

基本命令：
  help     - 显示此帮助信息
  quit     - 退出程序
  reset    - 重置对话历史
  clear    - 清屏

示例用法：
  📁 "列出当前目录的文件"
  📄 "读取 main.py 文件的内容"
  ✏️  "创建一个名为 test.py 的 Python 文件，包含 Hello World 程序"
  🔍 "在项目中搜索包含 'import' 的代码行"
  ⚡ "运行 python --version 命令"
  🐛 "分析这段代码并找出潜在的问题"
  🚀 "帮我优化这个函数的性能"

高级功能：
  - 文件读写操作
  - 命令行执行
  - 代码分析和优化
  - 项目结构分析
    """
    print(help_text)


if __name__ == "__main__":
    main()
