"""信息窗口模块API"""
from enum import Enum
from typing import Optional, Callable
from PyQt6.QtCore import Qt

class MessageType(Enum):
    """消息类型"""
    INFO = "信息"
    WARNING = "警告"
    ERROR = "错误"
    QUESTION = "问题"

class MessageBoxAPI:
    """信息窗口API"""
    
    @staticmethod
    def show_message(title: str, message: str, message_type: MessageType = MessageType.INFO,
                    callback: Optional[Callable[[], None]] = None) -> None:
        """显示消息"""
        from .widget import MessageBoxWidget
        widget = MessageBoxWidget(title, message, message_type, callback)
        widget.setWindowModality(Qt.WindowModality.ApplicationModal)
        widget.exec()
        
    @staticmethod
    def show_question(title: str, message: str, 
                     confirm_callback: Optional[Callable[[], None]] = None,
                     cancel_callback: Optional[Callable[[], None]] = None) -> None:
        """显示问题"""
        from .widget import MessageBoxWidget
        widget = MessageBoxWidget(title, message, MessageType.QUESTION, 
                                confirm_callback=confirm_callback,
                                cancel_callback=cancel_callback)
        widget.setWindowModality(Qt.WindowModality.ApplicationModal)
        widget.exec() 