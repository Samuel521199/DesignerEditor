"""
Scene Panel
场景面板

This module provides the scene panel implementation.
此模块提供场景面板的实现。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolBar,
                           QLabel, QPushButton, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon

from .scene_view import SceneView
from .api import SceneEditorAPI, NodeType

class ScenePanel(QWidget):
    """Scene panel class."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = SceneEditorAPI()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 场景视图
        self.scene_view = SceneView()
        layout.addWidget(self.scene_view)
        
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
        
        # 节点类型选择
        self.node_type_combo = QComboBox()
        for node_type in NodeType:
            self.node_type_combo.addItem(node_type.value)
        toolbar.addWidget(QLabel("节点类型:"))
        toolbar.addWidget(self.node_type_combo)
        toolbar.addSeparator()
        
        # 网格设置
        self.grid_size_combo = QComboBox()
        self.grid_size_combo.addItems(["10", "20", "40", "80"])
        self.grid_size_combo.setCurrentText("20")
        self.grid_size_combo.currentTextChanged.connect(
            lambda s: self.scene_view.draw_grid(int(s))
        )
        toolbar.addWidget(QLabel("网格大小:"))
        toolbar.addWidget(self.grid_size_combo)
        
        # 对齐网格
        self.snap_to_grid = QAction("对齐网格", self)
        self.snap_to_grid.setCheckable(True)
        self.snap_to_grid.setChecked(True)
        toolbar.addAction(self.snap_to_grid)
        
        # 缩放控制
        zoom_in = QAction("放大", self)
        zoom_in.triggered.connect(lambda: self.scene_view.scale(1.2, 1.2))
        toolbar.addAction(zoom_in)
        
        zoom_out = QAction("缩小", self)
        zoom_out.triggered.connect(lambda: self.scene_view.scale(1/1.2, 1/1.2))
        toolbar.addAction(zoom_out)
        
        reset_view = QAction("重置视图", self)
        reset_view.triggered.connect(self.reset_view)
        toolbar.addAction(reset_view)
        
        return toolbar
        
    def reset_view(self):
        """Reset the view transformation."""
        self.scene_view.resetTransform()
        self.scene_view.draw_grid(
            int(self.grid_size_combo.currentText())
        ) 