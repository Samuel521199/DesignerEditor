"""
AI Assistant Panel
AI助理面板

This module implements the AI assistant panel.
此模块实现AI助理面板。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit,
                           QHBoxLayout, QPushButton, QLineEdit, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor
from .api import AIAssistantAPI, AssistantType

class AIAssistantPanel(QWidget):
    """AI助理面板类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = AIAssistantAPI.get_instance()
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout()
        
        # 临时标签
        label = QLabel("AI助理面板")
        layout.addWidget(label)
        
        # 创建对话历史文本编辑器
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        
        # 设置对话历史的样式
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
                font-size: 12px;
            }
        """)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        # 创建输入框
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("输入您的问题...")
        self.input_edit.returnPressed.connect(self.send_message)
        
        # 创建发送按钮
        send_button = QPushButton("发送")
        send_button.clicked.connect(self.send_message)
        
        # 创建清除按钮
        clear_button = QPushButton("清除")
        clear_button.clicked.connect(self.clear_history)
        
        # 添加组件到输入布局
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(send_button)
        input_layout.addWidget(clear_button)
        
        # 将组件添加到主布局
        layout.addWidget(self.chat_history)
        layout.addLayout(input_layout)
        
        # 添加欢迎消息
        self.add_message("AI助理", "您好！我是您的AI助理，有什么可以帮您的吗？")
        
        self.setLayout(layout)
        
    def send_message(self):
        """发送消息"""
        message = self.input_edit.text().strip()
        if message:
            self.add_message("用户", message)
            self.input_edit.clear()
            # 使用API生成响应
            response = self.api.generate_response(message, AssistantType.QA)
            self.add_message("AI助理", response)
            
    def clear_history(self):
        """清除历史记录"""
        self.chat_history.clear()
        self.add_message("AI助理", "历史记录已清除。有什么可以帮您的吗？")
        
    def add_message(self, sender, message):
        """添加消息到对话历史"""
        format = QTextCharFormat()
        
        if sender == "AI助理":
            format.setForeground(QColor("#4CAF50"))
        else:
            format.setForeground(QColor("#2196F3"))
            
        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(f"{sender}: ", format)
        
        format.setForeground(QColor("#ffffff"))
        cursor.insertText(f"{message}\n", format) 