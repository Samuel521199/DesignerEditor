"""
Log Panel
日志面板

This module provides the log panel implementation.
此模块提供日志面板的实现。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolBar,
                           QLabel, QPushButton, QComboBox, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QTextCharFormat, QColor, QTextCursor

from .api import LogManagerAPI, LogLevel, LogEntry

class LogPanel(QWidget):
    """日志面板类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = LogManagerAPI.get_instance()
        self.setup_ui()
        self.setup_formats()
        self.setup_connections()
        
    def setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 日志显示区域
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                font-family: 'Consolas', monospace;
                font-size: 13px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.log_edit)
        
    def create_toolbar(self) -> QToolBar:
        """创建工具栏"""
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2d2d2d;
                border: none;
                spacing: 4px;
                padding: 4px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 4px;
                color: #ffffff;
            }
            QToolButton:hover {
                background-color: #3d3d3d;
            }
            QToolButton:pressed {
                background-color: #1e1e1e;
            }
            QComboBox {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 3px;
                color: #ffffff;
                padding: 4px;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        
        # 日志级别过滤
        self.level_combo = QComboBox()
        self.level_combo.addItem("全部")
        for level in LogLevel:
            self.level_combo.addItem(level.value)
        toolbar.addWidget(QLabel("日志级别:"))
        toolbar.addWidget(self.level_combo)
        toolbar.addSeparator()
        
        # 清除按钮
        clear = QAction("清除日志", self)
        clear.triggered.connect(self._clear_logs)
        toolbar.addAction(clear)
        
        return toolbar
        
    def setup_formats(self):
        """设置不同日志级别的文本格式"""
        self.formats = {
            LogLevel.DEBUG: self._create_format("#90a4ae"),    # 灰色
            LogLevel.INFO: self._create_format("#4fc3f7"),     # 蓝色
            LogLevel.WARNING: self._create_format("#ffb74d"),   # 橙色
            LogLevel.ERROR: self._create_format("#e57373"),     # 红色
            LogLevel.CRITICAL: self._create_format("#f06292")   # 粉色
        }
        
    def _create_format(self, color: str) -> QTextCharFormat:
        """创建指定颜色的文本格式"""
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        return fmt
        
    def setup_connections(self):
        """设置信号连接"""
        self.api.register_log_added_callback(self._handle_log_added)
        self.api.register_log_cleared_callback(self._handle_log_cleared)
        self.level_combo.currentTextChanged.connect(self._handle_level_changed)
        
    def _handle_log_added(self, entry: LogEntry):
        """处理新日志条目"""
        # 检查是否需要显示此级别的日志
        current_level = self.level_combo.currentText()
        if current_level != "全部" and entry.level.value != current_level:
            return
            
        # 获取对应格式
        fmt = self.formats[entry.level]
        
        # 添加日志条目
        cursor = self.log_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # 添加时间戳
        cursor.insertText(
            f"[{entry.timestamp.strftime('%H:%M:%S')}] ",
            self._create_format("#666666")  # 时间戳使用暗灰色
        )
        
        # 添加日志级别
        cursor.insertText(
            f"[{entry.level.value}] ",
            fmt
        )
        
        # 添加来源（如果有）
        if entry.source:
            cursor.insertText(
                f"[{entry.source}] ",
                self._create_format("#81c784")  # 来源使用绿色
            )
        
        # 添加消息
        cursor.insertText(f"{entry.message}\n", fmt)
        
        # 滚动到底部
        self.log_edit.setTextCursor(cursor)
        
    def _handle_log_cleared(self):
        """处理日志清除"""
        self.log_edit.clear()
        
    def _handle_level_changed(self, level: str):
        """处理日志级别过滤变化"""
        self.log_edit.clear()
        
        # 获取过滤后的日志条目
        if level == "全部":
            entries = self.api.get_entries()
        else:
            entries = self.api.get_entries(
                level=next(l for l in LogLevel if l.value == level)
            )
            
        # 重新显示过滤后的日志
        for entry in entries:
            self._handle_log_added(entry)
            
    def _clear_logs(self):
        """清除所有日志"""
        self.api.clear_entries() 