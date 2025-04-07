"""
AI Assistant Panel
AI助手面板

This module provides the panel implementation for the AI assistant.
此模块提供AI助手的面板实现。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, 
                           QPushButton, QComboBox, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal

from .api import AIAssistantAPI, AssistantType

class AIAssistantPanel(QWidget):
    """AI Assistant Panel class."""
    
    # 定义信号
    response_generated = pyqtSignal(str)  # AI响应生成信号
    suggestion_requested = pyqtSignal(str)  # 请求建议信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = AIAssistantAPI()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # 模式选择
        mode_label = QLabel("选择模式:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([t.value for t in AssistantType])
        
        # 输入区域
        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("在此输入您的问题或需求...")
        self.input_edit.setMinimumHeight(100)
        
        # 发送按钮
        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_request)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0a3d91;
            }
        """)
        
        # 响应区域
        self.response_edit = QTextEdit()
        self.response_edit.setPlaceholderText("AI响应将在此显示...")
        self.response_edit.setReadOnly(True)
        
        # 添加组件到布局
        layout.addWidget(mode_label)
        layout.addWidget(self.mode_combo)
        layout.addWidget(self.input_edit)
        layout.addWidget(self.send_button)
        layout.addWidget(self.response_edit)
        
        # 应用样式
        self.apply_style()
        
    def send_request(self):
        """Send request to AI and get response."""
        query = self.input_edit.toPlainText()
        if not query:
            return
            
        # 获取当前选择的助手类型
        mode_text = self.mode_combo.currentText()
        assistant_type = next(t for t in AssistantType if t.value == mode_text)
        
        # 通过API获取响应
        response = self.api.generate_response(query, assistant_type)
        self.response_edit.setPlainText(response)
        
        # 发送响应生成信号
        self.response_generated.emit(response)
        
    def get_suggestions(self, context: str):
        """Get suggestions based on context."""
        suggestions = self.api.generate_suggestions(context)
        return [s.content for s in suggestions]
        
    def apply_style(self):
        """Apply styling to the panel."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLabel {
                font-size: 13px;
            }
            QComboBox {
                background-color: #333333;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 5px;
                min-height: 25px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox:on {
                border: 1px solid #0d47a1;
            }
            QComboBox QAbstractItemView {
                background-color: #333333;
                border: 1px solid #444444;
                selection-background-color: #0d47a1;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 1px solid #0d47a1;
            }
        """) 