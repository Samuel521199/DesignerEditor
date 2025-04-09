"""
Project Info Panel
项目信息面板

This module implements the project information panel.
此模块实现项目信息面板。
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                           QLabel, QLineEdit, QTextEdit, QDockWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QIcon, QPixmap
from ..project_model.project_info_model import ProjectInfoModel
from .tree_resources import TreeResources
from .api import ProjectInfoAPI

class ProjectInfoPanel(QDockWidget):
    """项目信息面板类"""
    
    def __init__(self, parent=None):
        super().__init__("", parent)
        self.setObjectName("ProjectInfoPanel")
        self.api = ProjectInfoAPI.get_instance()
        self.setup_ui()
        self.current_project = None
        
    def setup_ui(self):
        """设置界面"""
        # 创建主widget和布局
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        # 创建树形控件
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setIndentation(20)
        
        # 设置样式
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border: none;
            }
            QTreeWidget::item {
                height: 25px;
            }
            QTreeWidget::item:hover {
                background-color: #3c3c3c;
            }
            QTreeWidget::item:selected {
                background-color: #4b4b4b;
            }
        """)
        
        # 创建根节点
        self.root = QTreeWidgetItem(self.tree_widget)
        self.root.setText(0, "项目信息")
        self.root.setIcon(0, TreeResources.get_folder_icon())
        
        # 创建子节点
        self.basic_info_root = QTreeWidgetItem(self.root)
        self.basic_info_root.setText(0, "基本信息")
        self.basic_info_root.setIcon(0, TreeResources.get_folder_icon())
        
        self.scenes_root = QTreeWidgetItem(self.root)
        self.scenes_root.setText(0, "场景")
        self.scenes_root.setIcon(0, TreeResources.get_folder_icon())
        
        # 展开根节点
        self.root.setExpanded(True)
        
        # 连接信号
        self.tree_widget.itemExpanded.connect(self.on_item_expanded)
        self.tree_widget.itemCollapsed.connect(self.on_item_collapsed)
        
        layout.addWidget(self.tree_widget)
        self.setWidget(main_widget)
        
    def on_item_expanded(self, item):
        """项目展开时的处理"""
        item.setIcon(0, TreeResources.get_folder_open_icon())
        
    def on_item_collapsed(self, item):
        """项目折叠时的处理"""
        item.setIcon(0, TreeResources.get_folder_icon())
        
    def update_project_info(self, project_info: ProjectInfoModel):
        """更新项目信息显示"""
        self.current_project = project_info
        
        # 清空现有项
        self.basic_info_root.takeChildren()
        self.scenes_root.takeChildren()
        
        if project_info:
            # 更新根节点标题
            self.root.setText(0, f"项目信息 - {project_info.name}")
            
            # 添加基本信息
            items = [
                ("项目描述", project_info.description),
                ("游戏类型", project_info.game_type.value if project_info.game_type else None),
                ("目标平台", [platform.value for platform in project_info.target_platforms] if project_info.target_platforms else None),
                ("游戏风格", project_info.game_style.value if project_info.game_style else None),
                ("时代背景", project_info.time_setting.value if project_info.time_setting else None),
                ("目标受众", [audience.value for audience in project_info.target_audience] if project_info.target_audience else None)
            ]
            
            for label, value in items:
                if value:  # 只显示非空值
                    item = QTreeWidgetItem(self.basic_info_root)
                    # 如果值是列表，则将其转换为逗号分隔的字符串
                    if isinstance(value, list):
                        display_value = "、".join(value)
                    else:
                        display_value = str(value)
                    item.setText(0, f"{label}：{display_value}")
                    item.setIcon(0, TreeResources.get_info_icon())
            
            # 添加场景信息（如果有）
            # 暂时添加一个默认场景作为示例
            scene_item = QTreeWidgetItem(self.scenes_root)
            scene_item.setText(0, "默认场景")
            scene_item.setIcon(0, TreeResources.get_scene_icon())
            
            # 展开所有节点
            self.root.setExpanded(True)
            self.basic_info_root.setExpanded(True)
            self.scenes_root.setExpanded(True) 