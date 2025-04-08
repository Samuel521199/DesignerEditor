"""
Project Info Panel
项目信息面板

This module implements the project information panel.
此模块实现项目信息面板。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                           QLabel, QLineEdit, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QIcon, QPixmap
from ..project_model.project_info_model import ProjectInfoModel
from .tree_resources import TreeResources

class ProjectInfoPanel(QWidget):
    """项目信息面板类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_branch_icons()  # 先设置图标
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout()
        
        # 创建树形控件
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # 隐藏表头
        self.tree.setColumnCount(1)  # 只显示一列
        self.tree.setIndentation(20)  # 设置缩进
        
        # 创建根节点
        self.basic_info_root = QTreeWidgetItem(self.tree)
        self.basic_info_root.setText(0, "项目基本信息")
        self.basic_info_root.setFlags(self.basic_info_root.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        # 创建场景根节点
        self.scene_root = QTreeWidgetItem(self.tree)
        self.scene_root.setText(0, "场景")
        self.scene_root.setFlags(self.scene_root.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        # 添加一些测试子节点
        for i in range(3):
            child = QTreeWidgetItem(self.basic_info_root)
            child.setText(0, f"测试项 {i+1}")
            
        for i in range(2):
            child = QTreeWidgetItem(self.scene_root)
            child.setText(0, f"场景 {i+1}")
        
        layout.addWidget(self.tree)
        self.setLayout(layout)
        
    def setup_branch_icons(self):
        """设置分支图标"""
        print("开始设置分支图标...")
        self.icons = TreeResources.create_branch_icons()
        
        # 设置树形控件的展开/折叠图标
        self.tree.setIndentation(20)
        self.tree.setAnimated(True)
        
        # 为每个项目设置图标
        print("设置根节点图标...")
        self.basic_info_root.setIcon(0, self.icons['branch-closed'])
        self.scene_root.setIcon(0, self.icons['branch-closed'])
        
        # 连接展开/折叠信号
        self.tree.itemExpanded.connect(self.on_item_expanded)
        self.tree.itemCollapsed.connect(self.on_item_collapsed)
        
        # 设置样式
        style = """
            QTreeWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3b3b3b;
                font-size: 12px;
                outline: 0;
            }
            
            QTreeWidget::item {
                padding: 4px;
                border-bottom: 1px solid #3b3b3b;
                height: 20px;
            }
            
            QTreeWidget::item:selected {
                background-color: #3b3b3b;
                color: #ffffff;
            }
            
            QTreeWidget::item:hover {
                background-color: #3b3b3b;
            }
            
            QTreeWidget::branch {
                background-color: transparent;
            }
        """
        self.tree.setStyleSheet(style)
        
        # 设置字体
        font = QFont("Microsoft YaHei", 9)
        self.tree.setFont(font)
        print("分支图标设置完成")
        
    def on_item_expanded(self, item):
        """项目展开时的处理"""
        if item.childCount() > 0:
            item.setIcon(0, self.icons['branch-open'])
            
    def on_item_collapsed(self, item):
        """项目折叠时的处理"""
        if item.childCount() > 0:
            item.setIcon(0, self.icons['branch-closed'])
        
    def update_project_info(self, project_info: ProjectInfoModel):
        """更新项目信息"""
        # 清除现有内容
        self.basic_info_root.takeChildren()
        
        # 添加项目名称
        name_item = QTreeWidgetItem(self.basic_info_root)
        name_item.setText(0, "项目名称")
        name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        name_value = QTreeWidgetItem(name_item)
        name_value.setText(0, project_info.name)
        
        # 添加项目描述
        desc_item = QTreeWidgetItem(self.basic_info_root)
        desc_item.setText(0, "项目描述")
        desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        desc_value = QTreeWidgetItem(desc_item)
        desc_value.setText(0, project_info.description)
        
        # 添加游戏类型
        type_item = QTreeWidgetItem(self.basic_info_root)
        type_item.setText(0, "游戏类型")
        type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        type_value = QTreeWidgetItem(type_item)
        type_value.setText(0, project_info.game_type.value)
        
        # 添加目标平台
        platform_item = QTreeWidgetItem(self.basic_info_root)
        platform_item.setText(0, "目标平台")
        platform_item.setFlags(platform_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        platforms = [p.value for p in project_info.target_platforms]
        for platform in platforms:
            platform_value = QTreeWidgetItem(platform_item)
            platform_value.setText(0, platform)
        
        # 添加游戏风格
        style_item = QTreeWidgetItem(self.basic_info_root)
        style_item.setText(0, "游戏风格")
        style_item.setFlags(style_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        style_value = QTreeWidgetItem(style_item)
        style_value.setText(0, project_info.game_style.value)
        
        # 添加时代背景
        time_item = QTreeWidgetItem(self.basic_info_root)
        time_item.setText(0, "时代背景")
        time_item.setFlags(time_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        time_value = QTreeWidgetItem(time_item)
        time_value.setText(0, project_info.time_setting.value)
        
        # 添加目标受众
        audience_item = QTreeWidgetItem(self.basic_info_root)
        audience_item.setText(0, "目标受众")
        audience_item.setFlags(audience_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        audiences = [a.value for a in project_info.target_audience]
        for audience in audiences:
            audience_value = QTreeWidgetItem(audience_item)
            audience_value.setText(0, audience)
        
        # 展开所有节点
        self.tree.expandAll() 