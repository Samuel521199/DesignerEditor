from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from typing import Optional, Callable

from .api import MessageType, MessageBoxAPI

class MessageBoxWidget(QDialog):
    """信息窗口部件"""
    
    def __init__(self, title: str, message: str, message_type: MessageType,
                 callback: Optional[Callable[[], None]] = None,
                 confirm_callback: Optional[Callable[[], None]] = None,
                 cancel_callback: Optional[Callable[[], None]] = None,
                 parent=None):
        super().__init__(parent)
        self.callback = callback
        self.confirm_callback = confirm_callback
        self.cancel_callback = cancel_callback
        
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setModal(True)
        self.setMinimumSize(400, 200)
        
        self._init_ui(message, message_type)
        
    def _init_ui(self, message: str, message_type: MessageType):
        """初始化UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 消息内容
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        message_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                background: transparent;
            }
        """)
        layout.addWidget(message_label)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        if message_type == MessageType.QUESTION:
            # 问题模式：确认和取消按钮
            confirm_btn = QPushButton("确认")
            confirm_btn.clicked.connect(self._on_confirm)
            cancel_btn = QPushButton("取消")
            cancel_btn.clicked.connect(self._on_cancel)
            
            button_layout.addWidget(confirm_btn)
            button_layout.addWidget(cancel_btn)
        else:
            # 普通模式：确定按钮
            ok_btn = QPushButton("确定")
            ok_btn.clicked.connect(self._on_ok)
            button_layout.addWidget(ok_btn)
            
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                border: 1px solid #3b3b3b;
            }
            QPushButton {
                background-color: #3b3b3b;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4b4b4b;
            }
            QPushButton:pressed {
                background-color: #5b5b5b;
            }
        """)
        
    def _on_ok(self):
        """确定按钮点击"""
        if self.callback:
            self.callback()
        self.accept()
        
    def _on_confirm(self):
        """确认按钮点击"""
        if self.confirm_callback:
            self.confirm_callback()
        self.accept()
        
    def _on_cancel(self):
        """取消按钮点击"""
        if self.cancel_callback:
            self.cancel_callback()
        self.reject() 