from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QTextEdit, QPushButton, QComboBox, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
import json

from .api import AIAssistantAPI, AssistantType

class AIAssistantWidget(QWidget):
    """AI助手窗口部件"""
    
    suggestion_requested = pyqtSignal(str)  # 请求建议信号
    help_requested = pyqtSignal(str)  # 请求帮助信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        # 助手类型选择
        type_layout = QHBoxLayout()
        type_label = QLabel("助手类型:")
        self.assistant_type = QComboBox()
        self.assistant_type.addItems([t.value for t in AssistantType])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.assistant_type)
        layout.addLayout(type_layout)
        
        # 输入区域
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("请输入您的问题或需求...")
        layout.addWidget(self.input_area)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.suggest_btn = QPushButton("获取建议")
        self.help_btn = QPushButton("获取帮助")
        button_layout.addWidget(self.suggest_btn)
        button_layout.addWidget(self.help_btn)
        layout.addLayout(button_layout)
        
        # 输出区域
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)
        
        self.setLayout(layout)
        
        # 连接信号
        self.suggest_btn.clicked.connect(self._on_suggest)
        self.help_btn.clicked.connect(self._on_help)
        
    def _on_suggest(self):
        """请求建议"""
        query = self.input_area.toPlainText()
        if query:
            context = {
                "type": self.assistant_type.currentText(),
                "query": query
            }
            self.suggestion_requested.emit(json.dumps(context))
            
    def _on_help(self):
        """请求帮助"""
        query = self.input_area.toPlainText()
        if query:
            context = {
                "type": self.assistant_type.currentText(),
                "query": query
            }
            self.help_requested.emit(json.dumps(context))
            
    def show_suggestion(self, suggestion):
        """显示建议"""
        self.output_area.setPlainText(suggestion)
        
    def show_help(self, help_text):
        """显示帮助"""
        self.output_area.setPlainText(help_text)
        
    def clear_output(self):
        """清空输出"""
        self.output_area.clear() 