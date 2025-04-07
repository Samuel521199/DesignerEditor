from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget,
                            QTreeWidgetItem, QPushButton, QLabel, QLineEdit,
                            QTextEdit, QComboBox, QSplitter, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional, List

from .api import SceneEditorAPI, Scene, SceneNode, NodeType

class SceneEditorWidget(QWidget):
    """场景编辑窗口部件"""
    
    # 信号定义
    scene_loaded = pyqtSignal()  # 场景加载完成
    scene_saved = pyqtSignal()   # 场景保存完成
    error_occurred = pyqtSignal(str)  # 错误发生
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        # 场景操作按钮
        self.new_scene_btn = QPushButton("新建场景")
        self.save_scene_btn = QPushButton("保存场景")
        self.delete_scene_btn = QPushButton("删除场景")
        
        toolbar.addWidget(self.new_scene_btn)
        toolbar.addWidget(self.save_scene_btn)
        toolbar.addWidget(self.delete_scene_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # 主分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 场景树
        self.scene_tree = QTreeWidget()
        self.scene_tree.setHeaderLabels(["场景节点"])
        self.scene_tree.itemSelectionChanged.connect(self._on_selection_changed)
        
        # 节点属性编辑区
        self.node_edit = QWidget()
        node_layout = QFormLayout()
        
        # 节点名称
        self.node_name_edit = QLineEdit()
        node_layout.addRow("节点名称:", self.node_name_edit)
        
        # 节点类型
        self.node_type_combo = QComboBox()
        self.node_type_combo.addItems([t.name for t in NodeType])
        node_layout.addRow("节点类型:", self.node_type_combo)
        
        # 节点描述
        self.node_desc_edit = QTextEdit()
        self.node_desc_edit.setMaximumHeight(100)
        node_layout.addRow("节点描述:", self.node_desc_edit)
        
        # 节点属性
        self.node_props_edit = QTextEdit()
        self.node_props_edit.setMaximumHeight(100)
        node_layout.addRow("节点属性:", self.node_props_edit)
        
        self.node_edit.setLayout(node_layout)
        
        # 添加到分割器
        splitter.addWidget(self.scene_tree)
        splitter.addWidget(self.node_edit)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
        self.setLayout(layout)
        
        # 连接信号
        self.new_scene_btn.clicked.connect(self._on_new_scene)
        self.save_scene_btn.clicked.connect(self._on_save_scene)
        self.delete_scene_btn.clicked.connect(self._on_delete_scene)
        self.node_name_edit.textChanged.connect(self._on_node_changed)
        self.node_type_combo.currentTextChanged.connect(self._on_node_changed)
        self.node_desc_edit.textChanged.connect(self._on_node_changed)
        self.node_props_edit.textChanged.connect(self._on_node_changed)
        
    def load_scene(self, scene: Optional[Scene] = None):
        """加载场景"""
        self.scene_tree.clear()
        
        if not scene:
            return
            
        # 创建根节点
        root = QTreeWidgetItem(self.scene_tree)
        root.setText(0, scene.name)
        root.setData(0, Qt.ItemDataRole.UserRole, scene)
        
        # 递归添加子节点
        self._add_nodes_to_tree(root, scene.nodes)
        
        self.scene_tree.expandAll()
        self.scene_loaded.emit()
        
    def _add_nodes_to_tree(self, parent_item: QTreeWidgetItem, nodes: List[SceneNode]):
        """递归添加节点到树中"""
        for node in nodes:
            item = QTreeWidgetItem(parent_item)
            item.setText(0, node.name)
            item.setData(0, Qt.ItemDataRole.UserRole, node)
            self._add_nodes_to_tree(item, node.children)
            
    def _on_selection_changed(self):
        """选中节点改变"""
        items = self.scene_tree.selectedItems()
        if not items:
            return
            
        node = items[0].data(0, Qt.ItemDataRole.UserRole)
        if isinstance(node, SceneNode):
            self.node_name_edit.setText(node.name)
            self.node_type_combo.setCurrentText(node.type.name)
            self.node_desc_edit.setText(node.description)
            self.node_props_edit.setText(str(node.properties))
            
    def _on_node_changed(self):
        """节点属性改变"""
        items = self.scene_tree.selectedItems()
        if not items:
            return
            
        node = items[0].data(0, Qt.ItemDataRole.UserRole)
        if isinstance(node, SceneNode):
            node.name = self.node_name_edit.text()
            node.type = NodeType[self.node_type_combo.currentText()]
            node.description = self.node_desc_edit.toPlainText()
            # TODO: 解析属性文本
            
    def _on_new_scene(self):
        """新建场景"""
        try:
            scene = SceneEditorAPI.create_scene("新场景")
            if scene:
                self.load_scene(scene)
            else:
                self.error_occurred.emit("创建场景失败")
        except Exception as e:
            self.error_occurred.emit(f"创建场景时出错: {str(e)}")
            
    def _on_save_scene(self):
        """保存场景"""
        try:
            items = self.scene_tree.selectedItems()
            if not items:
                self.error_occurred.emit("请先选择一个场景")
                return
                
            scene = items[0].data(0, Qt.ItemDataRole.UserRole)
            if not isinstance(scene, Scene):
                self.error_occurred.emit("选中的不是场景")
                return
                
            if SceneEditorAPI.save_scene(scene):
                self.scene_saved.emit()
            else:
                self.error_occurred.emit("保存场景失败")
        except Exception as e:
            self.error_occurred.emit(f"保存场景时出错: {str(e)}")
            
    def _on_delete_scene(self):
        """删除场景"""
        try:
            items = self.scene_tree.selectedItems()
            if not items:
                self.error_occurred.emit("请先选择一个场景")
                return
                
            scene = items[0].data(0, Qt.ItemDataRole.UserRole)
            if not isinstance(scene, Scene):
                self.error_occurred.emit("选中的不是场景")
                return
                
            if SceneEditorAPI.delete_scene(scene):
                self.scene_tree.takeTopLevelItem(self.scene_tree.indexOfTopLevelItem(items[0]))
            else:
                self.error_occurred.emit("删除场景失败")
        except Exception as e:
            self.error_occurred.emit(f"删除场景时出错: {str(e)}") 