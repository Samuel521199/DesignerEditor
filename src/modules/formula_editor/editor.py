"""
Formula Editor
公式编辑器

This module provides the formula editor implementation.
此模块提供公式编辑器的实现。
"""

from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import (QTextCharFormat, QSyntaxHighlighter,
                        QColor, QTextCursor)

class FormulaHighlighter(QSyntaxHighlighter):
    """Formula syntax highlighter class."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_formats()
    
    def setup_formats(self):
        """Set up text formats for different syntax elements."""
        # 函数格式
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor("#4fc3f7"))
        self.function_format.setFontWeight(700)
        
        # 变量格式
        self.variable_format = QTextCharFormat()
        self.variable_format.setForeground(QColor("#81c784"))
        
        # 数字格式
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#ff8a65"))
        
        # 运算符格式
        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor("#ba68c8"))
        
        # 括号格式
        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor("#90a4ae"))
        
        # 字符串格式
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#ffb74d"))
    
    def highlightBlock(self, text: str):
        """Highlight a block of text."""
        # TODO: 实现语法高亮逻辑
        pass

class FormulaEditor(QTextEdit):
    """Formula editor class."""
    
    content_changed = pyqtSignal(str)  # 内容变化信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        
    def setup_editor(self):
        """Set up the editor."""
        # 设置字体
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                padding: 8px;
            }
        """)
        
        # 添加语法高亮
        self.highlighter = FormulaHighlighter(self.document())
        
        # 连接信号
        self.textChanged.connect(self._handle_text_changed)
        
    def _handle_text_changed(self):
        """Handle text changes."""
        self.content_changed.emit(self.toPlainText())
        
    def insert_text(self, text: str):
        """Insert text at cursor position."""
        cursor = self.textCursor()
        cursor.insertText(text)
        
    def insert_function(self, name: str, param_count: int):
        """Insert function at cursor position."""
        cursor = self.textCursor()
        params = ", ".join(["" for _ in range(param_count)])
        cursor.insertText(f"{name}({params})")
        
        # 移动光标到第一个参数位置
        pos = cursor.position()
        cursor.setPosition(pos - len(params) - 1)
        self.setTextCursor(cursor)
        
    def get_current_word(self) -> str:
        """Get the word under cursor."""
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        return cursor.selectedText()
        
    def get_content(self) -> str:
        """Get editor content."""
        return self.toPlainText()
        
    def set_content(self, content: str):
        """Set editor content."""
        self.setPlainText(content)
        
    def clear_content(self):
        """Clear editor content."""
        self.clear() 