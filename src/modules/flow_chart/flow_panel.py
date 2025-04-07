"""
Flow Chart Panel
流程图面板

This module provides the flow chart panel implementation.
此模块提供流程图面板的实现。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolBar,
                           QLabel, QPushButton, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

from .flow_view import FlowChartView
from .api import FlowChartAPI, NodeType

class FlowChartPanel(QWidget):
    """Flow chart panel class."""
    
    node_created = pyqtSignal(NodeType, tuple)  # 节点创建信号
    connection_created = pyqtSignal(str, str)  # 连接创建信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = FlowChartAPI()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 流程图视图
        self.flow_view = FlowChartView()
        layout.addWidget(self.flow_view)
        
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
        
        # 添加节点按钮
        add_node = QAction("添加节点", self)
        add_node.triggered.connect(self.add_node)
        toolbar.addAction(add_node)
        
        # 添加连接按钮
        add_connection = QAction("添加连接", self)
        add_connection.triggered.connect(self.add_connection)
        toolbar.addAction(add_connection)
        toolbar.addSeparator()
        
        # 缩放控制
        zoom_in = QAction("放大", self)
        zoom_in.triggered.connect(lambda: self.flow_view.scale(1.2, 1.2))
        toolbar.addAction(zoom_in)
        
        zoom_out = QAction("缩小", self)
        zoom_out.triggered.connect(lambda: self.flow_view.scale(1/1.2, 1/1.2))
        toolbar.addAction(zoom_out)
        
        reset_view = QAction("重置视图", self)
        reset_view.triggered.connect(self.reset_view)
        toolbar.addAction(reset_view)
        
        return toolbar
        
    def add_node(self):
        """Add a new node."""
        node_type = NodeType(self.node_type_combo.currentText())
        # 获取视图中心点作为新节点位置
        center = self.flow_view.mapToScene(
            self.flow_view.viewport().rect().center()
        )
        self.node_created.emit(node_type, (center.x(), center.y()))
        
    def add_connection(self):
        """Add a new connection."""
        # TODO: 实现连接创建逻辑
        pass
        
    def reset_view(self):
        """Reset the view transformation."""
        self.flow_view.resetTransform() 