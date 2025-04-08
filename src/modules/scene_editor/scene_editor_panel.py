"""
Scene Editor Panel
场景编辑面板

This module implements the scene editor panel.
此模块实现场景编辑面板。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                           QGraphicsView, QGraphicsScene, QToolBar,
                           QLabel, QPushButton, QMenu)
from PyQt6.QtCore import Qt, QRectF, QPointF, QSizeF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QAction
from .blueprint_editor import BlueprintEditor
from ..project_model.blueprint_node_model import BlueprintNode, PinType, PinDirection

class GridGraphicsScene(QGraphicsScene):
    """带网格的场景"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 20
        self.grid_color = QColor("#2a2a2a")
        self.major_grid_color = QColor("#3a3a3a")
        self.major_grid_interval = 5  # 每5个格子显示主网格线
        
    def drawBackground(self, painter: QPainter, rect: QRectF):
        """绘制背景网格"""
        super().drawBackground(painter, rect)
        
        # 获取可见区域
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        right = int(rect.right())
        bottom = int(rect.bottom())
        
        # 绘制网格线
        for x in range(left, right + 1, self.grid_size):
            is_major = (x // self.grid_size) % self.major_grid_interval == 0
            painter.setPen(QPen(self.major_grid_color if is_major else self.grid_color))
            painter.drawLine(x, rect.top(), x, rect.bottom())
            
        for y in range(top, bottom + 1, self.grid_size):
            is_major = (y // self.grid_size) % self.major_grid_interval == 0
            painter.setPen(QPen(self.major_grid_color if is_major else self.grid_color))
            painter.drawLine(rect.left(), y, rect.right(), y)

class SceneEditorPanel(QWidget):
    """场景编辑器面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 创建视图
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
        # 设置视图背景为透明
        self.view.setBackgroundBrush(QBrush())  # 使用空画刷
        self.view.viewport().setAutoFillBackground(False)
        
        # 创建蓝图编辑器
        self.blueprint_editor = BlueprintEditor()
        self.blueprint_editor.setSceneRect(QRectF(-2000, -2000, 4000, 4000))
        
        # 设置视图的场景
        self.view.setScene(self.blueprint_editor)
        
        layout.addWidget(self.view)
        
        # 创建状态栏
        status_bar = self.create_status_bar()
        layout.addLayout(status_bar)
        
        # 设置上下文菜单
        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.show_context_menu)
        
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
        """)
        
        # 添加工具按钮
        select_button = QPushButton("选择")
        move_button = QPushButton("移动")
        rotate_button = QPushButton("旋转")
        scale_button = QPushButton("缩放")
        add_node_button = QPushButton("添加节点")
        
        toolbar.addWidget(select_button)
        toolbar.addWidget(move_button)
        toolbar.addWidget(rotate_button)
        toolbar.addWidget(scale_button)
        toolbar.addWidget(add_node_button)
        
        # 连接信号
        add_node_button.clicked.connect(self.show_add_node_menu)
        
        return toolbar
        
    def create_status_bar(self) -> QHBoxLayout:
        """创建状态栏"""
        status_bar = QHBoxLayout()
        self.position_label = QLabel("位置: 0, 0")
        self.scale_label = QLabel("缩放: 100%")
        status_bar.addWidget(self.position_label)
        status_bar.addStretch()
        status_bar.addWidget(self.scale_label)
        return status_bar
        
    def show_context_menu(self, position):
        """显示上下文菜单"""
        menu = QMenu()
        add_node_menu = menu.addMenu("添加节点")
        
        # 添加常用节点类型
        node_types = {
            "事件节点": "Event",
            "函数节点": "Function",
            "变量节点": "Variable",
            "数学运算": "Math",
            "流程控制": "Flow",
            "自定义节点": "Custom"
        }
        
        for label, node_type in node_types.items():
            action = QAction(label, self)
            action.setData(node_type)
            action.triggered.connect(lambda checked, t=node_type: self.add_node(t, self.view.mapToScene(position)))
            add_node_menu.addAction(action)
        
        menu.exec(self.view.viewport().mapToGlobal(position))
        
    def show_add_node_menu(self):
        """显示添加节点菜单"""
        button = self.sender()
        if button:
            pos = button.mapToGlobal(button.rect().bottomLeft())
            self.show_context_menu(self.view.mapFromGlobal(pos))
            
    def add_node(self, node_type: str, position: QPointF):
        """添加节点到场景"""
        # 创建节点
        node = BlueprintNode(f"New {node_type}", node_type)
        node.position = (position.x(), position.y())
        
        # 根据节点类型添加默认引脚
        if node_type == "Event":
            node.add_pin("执行输出", PinType.EXEC, PinDirection.OUTPUT)
        elif node_type == "Function":
            node.add_pin("执行输入", PinType.EXEC, PinDirection.INPUT)
            node.add_pin("执行输出", PinType.EXEC, PinDirection.OUTPUT)
            node.add_pin("参数", PinType.OBJECT, PinDirection.INPUT)
            node.add_pin("返回值", PinType.OBJECT, PinDirection.OUTPUT)
        
        # 将节点添加到场景
        self.blueprint_editor.add_node(node)
        
    def get_blueprint_editor(self) -> BlueprintEditor:
        """获取蓝图编辑器实例"""
        return self.blueprint_editor

    def setup_ui_old(self):
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