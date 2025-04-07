"""
Log Manager API
日志管理API接口

This module provides the API interface for logging functionality.
此模块提供日志功能的API接口。
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = "调试"
    INFO = "信息"
    WARNING = "警告"
    ERROR = "错误"
    CRITICAL = "严重"

@dataclass
class LogEntry:
    """Log entry data class."""
    level: LogLevel
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

class LogManagerAPI:
    """Log manager API interface class."""
    
    def __init__(self):
        self.entries: List[LogEntry] = []
        self.log_added_callbacks = []
        self.log_cleared_callbacks = []
    
    def add_entry(self, level: LogLevel, message: str,
                 source: str = "", details: Dict[str, Any] = None) -> LogEntry:
        """Add a new log entry."""
        entry = LogEntry(
            level=level,
            message=message,
            source=source,
            details=details or {}
        )
        self.entries.append(entry)
        self._notify_log_added(entry)
        return entry
    
    def get_entries(self, level: Optional[LogLevel] = None,
                   source: Optional[str] = None) -> List[LogEntry]:
        """Get log entries with optional filtering."""
        filtered = self.entries
        
        if level:
            filtered = [e for e in filtered if e.level == level]
            
        if source:
            filtered = [e for e in filtered if e.source == source]
            
        return filtered
    
    def clear_entries(self):
        """Clear all log entries."""
        self.entries.clear()
        self._notify_log_cleared()
    
    def register_log_added_callback(self, callback):
        """Register a callback for log entry addition."""
        self.log_added_callbacks.append(callback)
    
    def register_log_cleared_callback(self, callback):
        """Register a callback for log clearing."""
        self.log_cleared_callbacks.append(callback)
    
    def _notify_log_added(self, entry: LogEntry):
        """Notify all registered callbacks about new log entry."""
        for callback in self.log_added_callbacks:
            callback(entry)
    
    def _notify_log_cleared(self):
        """Notify all registered callbacks about log clearing."""
        for callback in self.log_cleared_callbacks:
            callback()
    
    # 便捷方法
    def debug(self, message: str, source: str = "", details: Dict[str, Any] = None):
        """Add a debug level log entry."""
        return self.add_entry(LogLevel.DEBUG, message, source, details)
    
    def info(self, message: str, source: str = "", details: Dict[str, Any] = None):
        """Add an info level log entry."""
        return self.add_entry(LogLevel.INFO, message, source, details)
    
    def warning(self, message: str, source: str = "", details: Dict[str, Any] = None):
        """Add a warning level log entry."""
        return self.add_entry(LogLevel.WARNING, message, source, details)
    
    def error(self, message: str, source: str = "", details: Dict[str, Any] = None):
        """Add an error level log entry."""
        return self.add_entry(LogLevel.ERROR, message, source, details)
    
    def critical(self, message: str, source: str = "", details: Dict[str, Any] = None):
        """Add a critical level log entry."""
        return self.add_entry(LogLevel.CRITICAL, message, source, details) 