"""
Log Manager Panel
日志管理面板

This module implements the log manager panel.
此模块实现日志管理面板。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit,
                           QHBoxLayout, QPushButton, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor

class LogManagerPanel(QWidget):
    """日志管理面板类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)
        
        # 创建工具栏
        toolbar = QHBoxLayout()
        
        # 添加日志级别选择器
        self.level_combo = QComboBox()
        self.level_combo.addItems(["全部", "信息", "警告", "错误"])
        
        # 添加清除按钮
        clear_button = QPushButton("清除")
        export_button = QPushButton("导出")
        
        toolbar.addWidget(self.level_combo)
        toolbar.addStretch()
        toolbar.addWidget(clear_button)
        toolbar.addWidget(export_button)
        
        # 创建日志文本编辑器
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        # 设置日志文本编辑器的样式
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
        """)
        
        # 将组件添加到主布局
        main_layout.addLayout(toolbar)
        main_layout.addWidget(self.log_text)
        
        # 添加一些示例日志
        self.add_log("应用程序启动", "info")
        self.add_log("加载项目文件", "info")
        self.add_log("无法找到资源文件", "warning")
        self.add_log("渲染错误", "error")
        
    def add_log(self, message, level="info"):
        """添加日志"""
        format = QTextCharFormat()
        
        if level == "info":
            format.setForeground(QColor("#ffffff"))
        elif level == "warning":
            format.setForeground(QColor("#ffd700"))
        elif level == "error":
            format.setForeground(QColor("#ff4444"))
            
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(f"[{level.upper()}] {message}\n", format) 