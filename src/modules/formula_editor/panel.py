"""
Formula Panel
公式面板

This module provides the formula panel implementation.
此模块提供公式面板的实现。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolBar,
                           QLabel, QPushButton, QComboBox, QListWidget,
                           QListWidgetItem, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

from .editor import FormulaEditor
from .api import FormulaEditorAPI, FormulaType, Function

class FunctionList(QListWidget):
    """Function list widget class."""
    
    function_selected = pyqtSignal(Function)  # 函数选中信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_list()
        
    def setup_list(self):
        """Set up the list widget."""
        self.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #0d47a1;
            }
            QListWidget::item:hover {
                background-color: #2d2d2d;
            }
        """)
        
        # 连接信号
        self.itemClicked.connect(self._handle_item_clicked)
        
    def update_functions(self, functions: list[Function]):
        """Update function list."""
        self.clear()
        for func in functions:
            item = QListWidgetItem(func.name)
            item.setData(Qt.ItemDataRole.UserRole, func)
            self.addItem(item)
            
    def _handle_item_clicked(self, item: QListWidgetItem):
        """Handle item click event."""
        func = item.data(Qt.ItemDataRole.UserRole)
        self.function_selected.emit(func)

class FormulaPanel(QWidget):
    """Formula panel class."""
    
    formula_changed = pyqtSignal(str)  # 公式变化信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = FormulaEditorAPI()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 函数列表
        self.function_list = FunctionList()
        self.function_list.function_selected.connect(self._handle_function_selected)
        splitter.addWidget(self.function_list)
        
        # 公式编辑器
        self.formula_editor = FormulaEditor()
        self.formula_editor.content_changed.connect(self._handle_content_changed)
        splitter.addWidget(self.formula_editor)
        
        # 设置分割比例
        splitter.setStretchFactor(0, 1)  # 函数列表
        splitter.setStretchFactor(1, 2)  # 公式编辑器
        
        layout.addWidget(splitter)
        
        # 更新函数列表
        self.function_list.update_functions(self.api.get_functions())
        
    def create_toolbar(self) -> QToolBar:
        """Create the toolbar."""
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
        
        # 公式类型选择
        self.formula_type_combo = QComboBox()
        for formula_type in FormulaType:
            self.formula_type_combo.addItem(formula_type.value)
        toolbar.addWidget(QLabel("公式类型:"))
        toolbar.addWidget(self.formula_type_combo)
        toolbar.addSeparator()
        
        # 验证按钮
        validate = QAction("验证公式", self)
        validate.triggered.connect(self._validate_formula)
        toolbar.addAction(validate)
        
        # 清除按钮
        clear = QAction("清除", self)
        clear.triggered.connect(self.formula_editor.clear_content)
        toolbar.addAction(clear)
        
        return toolbar
        
    def _handle_function_selected(self, func: Function):
        """Handle function selection."""
        self.formula_editor.insert_function(
            func.name,
            len(func.parameters)
        )
        
    def _handle_content_changed(self, content: str):
        """Handle content changes."""
        self.formula_changed.emit(content)
        
    def _validate_formula(self):
        """Validate current formula."""
        content = self.formula_editor.get_content()
        formula_type = FormulaType(self.formula_type_combo.currentText())
        
        formula = self.api.create_formula(content, formula_type)
        if self.api.validate_formula(formula):
            # TODO: 显示验证成功提示
            pass
        else:
            # TODO: 显示错误信息
            pass 