from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QTextEdit, QPushButton, QComboBox, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
import logging
from datetime import datetime

from .api import LogDebuggerAPI, LogLevel

class LogDebuggerWidget(QWidget):
    """日志调试窗口部件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._setup_logging()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        # 日志级别选择
        level_label = QLabel("日志级别:")
        self.level_combo = QComboBox()
        self.level_combo.addItems([level.name for level in LogLevel])
        self.level_combo.currentTextChanged.connect(self._on_level_changed)
        
        # 控制按钮
        self.clear_btn = QPushButton("清空日志")
        self.save_btn = QPushButton("保存日志")
        
        toolbar.addWidget(level_label)
        toolbar.addWidget(self.level_combo)
        toolbar.addStretch()
        toolbar.addWidget(self.clear_btn)
        toolbar.addWidget(self.save_btn)
        
        layout.addLayout(toolbar)
        
        # 日志显示区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        
        self.setLayout(layout)
        
        # 连接信号
        self.clear_btn.clicked.connect(self._on_clear)
        self.save_btn.clicked.connect(self._on_save)
        
    def _setup_logging(self):
        """设置日志系统"""
        # 创建日志处理器
        self.log_handler = LogHandler(self)
        self.log_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        
        # 获取根日志记录器
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(logging.DEBUG)
        
    def _on_level_changed(self, level):
        """日志级别改变"""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        logging.getLogger().setLevel(level_map[level])
        
    def _on_clear(self):
        """清空日志"""
        self.log_area.clear()
        
    def _on_save(self):
        """保存日志"""
        # TODO: 实现日志保存功能
        pass
        
    def append_log(self, record):
        """添加日志记录"""
        self.log_area.append(f"{record.asctime} - {record.levelname} - {record.message}")

class LogHandler(logging.Handler):
    """自定义日志处理器"""
    
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        
    def emit(self, record):
        """发送日志记录"""
        try:
            msg = self.format(record)
            self.widget.append_log(record)
        except Exception:
            self.handleError(record) 