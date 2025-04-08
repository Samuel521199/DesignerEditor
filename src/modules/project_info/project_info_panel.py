"""
Project Info Panel
项目信息面板

This module implements the project information panel.
此模块实现项目信息面板。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QTreeView, QPushButton, QHBoxLayout)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class ProjectInfoPanel(QWidget):
    """项目信息面板类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)
        
        # 创建项目树视图
        self.project_tree = QTreeView()
        self.project_tree.setHeaderHidden(True)
        self.project_model = QStandardItemModel()
        self.project_tree.setModel(self.project_model)
        
        # 添加根节点
        root = QStandardItem("项目")
        self.project_model.appendRow(root)
        
        # 添加子节点
        scenes = QStandardItem("场景")
        assets = QStandardItem("资源")
        scripts = QStandardItem("脚本")
        root.appendRow(scenes)
        root.appendRow(assets)
        root.appendRow(scripts)
        
        # 添加按钮布局
        button_layout = QHBoxLayout()
        
        # 添加按钮
        add_button = QPushButton("添加")
        remove_button = QPushButton("删除")
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        
        # 将组件添加到主布局
        main_layout.addWidget(self.project_tree)
        main_layout.addLayout(button_layout) 