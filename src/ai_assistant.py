import json
import requests
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                           QPushButton, QComboBox, QLabel, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sys
from dotenv import load_dotenv

class AIResponseThread(QThread):
    response_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, api_type, prompt):
        super().__init__()
        self.api_type = api_type
        self.prompt = prompt

    def run(self):
        try:
            if self.api_type == "gemini":
                response = self.call_gemini()
            else:
                response = self.call_chatgpt()
            self.response_received.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def call_gemini(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise Exception("GEMINI_API_KEY 环境变量未设置")
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{
                    "text": self.prompt
                }]
            }]
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()['candidates'][0]['content']['parts'][0]['text']

    def call_chatgpt(self):
        api_key = os.getenv('CHATGPT_API_KEY')
        if not api_key:
            raise Exception("CHATGPT_API_KEY 环境变量未设置")
            
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": self.prompt}
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']

class AIAssistantPanel(QWidget):
    def __init__(self):
        print("Initializing AIAssistantPanel...")
        super().__init__()
        
        try:
            print("Setting up UI...")
            self.setup_ui()
            
            print("Setting up connections...")
            self.setup_connections()
            
            print("Checking API keys...")
            self.check_api_keys()
            
            print("AIAssistantPanel initialization completed.")
        except Exception as e:
            print(f"Error initializing AIAssistantPanel: {e}")
            import traceback
            traceback.print_exc()
            raise

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # AI选择器
        ai_selector_layout = QHBoxLayout()
        self.ai_selector = QComboBox()
        self.ai_selector.addItems(["Gemini", "ChatGPT"])
        self.api_key_status = QLabel()
        self.api_key_status.setStyleSheet("color: #ff4444;")
        ai_selector_layout.addWidget(QLabel("选择AI:"))
        ai_selector_layout.addWidget(self.ai_selector)
        ai_selector_layout.addWidget(self.api_key_status)
        layout.addLayout(ai_selector_layout)

        # 输入输出区域
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 输入区域
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("输入您的问题或指令...")
        splitter.addWidget(self.input_area)
        
        # 输出区域
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        splitter.addWidget(self.output_area)
        
        layout.addWidget(splitter)

        # 按钮区域
        button_layout = QHBoxLayout()
        self.send_button = QPushButton("发送")
        self.clear_button = QPushButton("清除")
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)

        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #3d3d3d;
                padding: 5px;
                font-family: 'Consolas', monospace;
            }
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #3d3d3d;
                padding: 3px;
                min-width: 100px;
            }
            QLabel {
                padding: 5px;
            }
        """)

    def setup_connections(self):
        self.send_button.clicked.connect(self.send_request)
        self.clear_button.clicked.connect(self.clear_output)
        self.ai_selector.currentTextChanged.connect(self.check_api_keys)

    def check_api_keys(self):
        try:
            # 获取应用程序的基础路径
            if getattr(sys, 'frozen', False):
                # 如果是打包后的可执行文件
                base_path = os.path.dirname(sys.executable)
            else:
                # 如果是开发环境
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            # 加载环境变量
            env_path = os.path.join(base_path, '.env')
            if os.path.exists(env_path):
                print(f"Loading environment variables from: {env_path}")
                load_dotenv(env_path)
            else:
                print(f"Warning: .env file not found at: {env_path}")
        except Exception as e:
            print(f"Warning: Failed to load environment variables: {e}")

        api_type = "gemini" if self.ai_selector.currentText() == "Gemini" else "chatgpt"
        api_key = os.getenv('GEMINI_API_KEY' if api_type == "gemini" else 'CHATGPT_API_KEY')
        
        if api_key:
            self.api_key_status.setText("API Key 已配置")
            self.api_key_status.setStyleSheet("color: #4CAF50;")
            self.send_button.setEnabled(True)
        else:
            self.api_key_status.setText("API Key 未配置")
            self.api_key_status.setStyleSheet("color: #ff4444;")
            self.send_button.setEnabled(False)

    def send_request(self):
        prompt = self.input_area.toPlainText()
        if not prompt:
            return

        api_type = "gemini" if self.ai_selector.currentText() == "Gemini" else "chatgpt"
        
        self.output_area.append(f"\n[用户] {prompt}\n")
        self.output_area.append("[AI] 正在思考...\n")

        self.thread = AIResponseThread(api_type, prompt)
        self.thread.response_received.connect(self.handle_response)
        self.thread.error_occurred.connect(self.handle_error)
        self.thread.start()

    def handle_response(self, response):
        self.output_area.append(f"{response}\n")
        self.output_area.append("-" * 50 + "\n")

    def handle_error(self, error):
        self.output_area.append(f"错误: {error}\n")
        self.output_area.append("-" * 50 + "\n")

    def clear_output(self):
        self.output_area.clear() 