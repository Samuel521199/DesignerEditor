"""
Scene Editor Panel
场景编辑面板

This module implements the scene editor panel.
此模块实现场景编辑面板。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                           QGraphicsView, QGraphicsScene, QToolBar,
                           QLabel, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter

class SceneEditorPanel(QWidget):
    """场景编辑面板类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建工具栏
        toolbar = QToolBar()
        select_button = QPushButton("选择")
        move_button = QPushButton("移动")
        rotate_button = QPushButton("旋转")
        scale_button = QPushButton("缩放")
        
        toolbar.addWidget(select_button)
        toolbar.addWidget(move_button)
        toolbar.addWidget(rotate_button)
        toolbar.addWidget(scale_button)
        
        # 创建场景视图
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setBackgroundBrush(QBrush(QColor("#2d2d2d")))
        
        # 创建状态栏
        status_bar = QHBoxLayout()
        position_label = QLabel("位置: 0, 0")
        scale_label = QLabel("缩放: 100%")
        status_bar.addWidget(position_label)
        status_bar.addStretch()
        status_bar.addWidget(scale_label)
        
        # 将组件添加到主布局
        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.view)
        main_layout.addLayout(status_bar) 