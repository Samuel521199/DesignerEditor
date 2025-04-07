"""
Log Manager Module
日志管理模块

This module provides logging functionality for the Designer Editor.
此模块提供设计器编辑器的日志功能。
"""

from .api import LogManagerAPI
from .log_panel import LogPanel

__all__ = [
    'LogManagerAPI',
    'LogPanel'
] 