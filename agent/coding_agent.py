from openai import OpenAI
import pathlib
import json
import os
import subprocess
from typing import List, Dict, Any
from .utils import Spinner

class CodingAgent:
    def __init__(self, model="qwen2.5:32b", debug=False):
        self.model = model
        self.client = OpenAI(
            base_url="http://localhost:11434/v1/",
            api_key="ollama"
        )
        self.messages = [{"role": "system", "content": self._system_prompt()}]
        self.current_directory = pathlib.Path.cwd()
        self.debug = debug
        self.tools = self._define_tools()

    def _system_prompt(self) -> str:
        """定义系统提示词"""
        return """你是一个专业的编程助手。你可以：
1. 分析和理解代码
2. 创建、修改和删除文件
3. 执行命令行操作
4. 提供编程建议和解决方案
5. 搜索和浏览文件系统

请始终提供清晰、准确的帮助，并在执行任何操作前解释你的行为。
如果用户要求修改文件，请先分析现有代码，然后提供改进建议。"""

    def _define_tools(self) -> List[Dict[str, Any]]:
        """定义可用的工具"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "读取文件内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "要读取的文件路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "写入或创建文件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "文件路径"
                            },
                            "content": {
                                "type": "string",
                                "description": "文件内容"
                            }
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_command",
                    "description": "执行命令行命令",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "要执行的命令"
                            },
                            "working_dir": {
                                "type": "string",
                                "description": "工作目录路径",
                                "default": "."
                            }
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "列出目录内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "目录路径"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "在文件中搜索文本",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "搜索模式"
                            },
                            "directory": {
                                "type": "string",
                                "description": "搜索目录",
                                "default": "."
                            }
                        },
                        "required": ["pattern"]
                    }
                }
            }
        ]

    def read_file(self, file_path: str) -> str:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"读取文件失败: {str(e)}"

    def write_file(self, file_path: str, content: str) -> str:
        """写入文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"文件 {file_path} 写入成功"
        except Exception as e:
            return f"写入文件失败: {str(e)}"

    def execute_command(self, command: str, working_dir: str = ".") -> str:
        """执行命令行命令"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return f"命令执行成功:\n{result.stdout}"
            else:
                return f"命令执行失败 (返回码: {result.returncode}):\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "命令执行超时"
        except Exception as e:
            return f"执行命令失败: {str(e)}"

    def list_directory(self, path: str = ".") -> str:
        """列出目录内容"""
        try:
            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"📁 {item}/")
                else:
                    items.append(f"📄 {item}")
            return "\n".join(items) if items else "目录为空"
        except Exception as e:
            return f"列出目录失败: {str(e)}"

    def search_files(self, pattern: str, directory: str = ".") -> str:
        """在文件中搜索文本"""
        try:
            results = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(('.py', '.txt', '.md', '.json', '.yaml', '.yml')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if pattern.lower() in content.lower():
                                    results.append(f"📄 {file_path}")
                        except:
                            continue
            return "\n".join(results) if results else "未找到匹配的文件"
        except Exception as e:
            return f"搜索失败: {str(e)}"

    def _execute_tool(self, tool_name: str, parameters: dict) -> str:
        """执行工具函数"""
        if tool_name == "read_file":
            return self.read_file(parameters["file_path"])
        elif tool_name == "write_file":
            return self.write_file(parameters["file_path"], parameters["content"])
        elif tool_name == "execute_command":
            return self.execute_command(parameters["command"], parameters.get("working_dir", "."))
        elif tool_name == "list_directory":
            return self.list_directory(parameters["path"])
        elif tool_name == "search_files":
            return self.search_files(parameters["pattern"], parameters.get("directory", "."))
        else:
            return f"未知工具: {tool_name}"

    def chat(self, message: str) -> str:
        """处理用户消息"""
        self.messages.append({"role": "user", "content": message})

        try:
            with Spinner("思考中"):
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=self.tools,
                    tool_choice="auto"
                )

            assistant_message = response.choices[0].message

            # 如果有工具调用
            if assistant_message.tool_calls:
                self.messages.append(assistant_message)

                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    parameters = json.loads(tool_call.function.arguments)

                    if self.debug:
                        print(f"🔧 执行工具: {tool_name}")
                        print(f"📝 参数: {parameters}")

                    tool_result = self._execute_tool(tool_name, parameters)

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })

                # 获取最终回复
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages
                )

                final_content = final_response.choices[0].message.content
                self.messages.append({"role": "assistant", "content": final_content})
                return final_content
            else:
                content = assistant_message.content
                self.messages.append({"role": "assistant", "content": content})
                return content

        except Exception as e:
            error_msg = f"处理消息时发生错误: {str(e)}"
            if self.debug:
                import traceback
                error_msg += f"\n{traceback.format_exc()}"
            return error_msg

    def reset_conversation(self):
        """重置对话历史"""
        self.messages = [{"role": "system", "content": self._system_prompt()}]

    def save_conversation(self, file_path: str):
        """保存对话历史"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
            print(f"💾 对话历史已保存到 {file_path}")
        except Exception as e:
            print(f"❌ 保存对话历史失败: {str(e)}")

    def load_conversation(self, file_path: str):
        """加载对话历史"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)
            print(f"📂 已加载对话历史: {file_path}")
        except Exception as e:
            print(f"❌ 加载对话历史失败: {str(e)}")
