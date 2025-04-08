"""
Main Window
主窗口模块

This module implements the main window of the application.
此模块实现应用程序的主窗口。
"""

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                          QHBoxLayout, QDockWidget, QApplication)
from PyQt6.QtCore import Qt

from modules.menu_bar.menu_bar import MenuBar
from modules.project_info.project_info_panel import ProjectInfoPanel
from modules.scene_editor.scene_editor_panel import SceneEditorPanel
from modules.log_manager.log_manager_panel import LogManagerPanel
from modules.ai_assistant.ai_assistant_panel import AIAssistantPanel

class MainWindow(QMainWindow):
    """主窗口类"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("游戏设计编辑器")
        self.setMinimumSize(1200, 800)
        
        # 初始化菜单栏
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # 初始化中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 初始化各个面板
        self.setup_panels()
        
        # 设置样式
        self.setup_styles()
        
        # 连接菜单信号
        self.connect_menu_signals()
        
    def setup_panels(self):
        """设置各个面板"""
        # 项目信息面板（左上）
        self.project_info_dock = QDockWidget("项目信息", self)
        self.project_info_panel = ProjectInfoPanel()
        self.project_info_dock.setWidget(self.project_info_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_info_dock)
        
        # 场景编辑面板（右上）
        self.scene_editor_dock = QDockWidget("场景编辑", self)
        self.scene_editor_panel = SceneEditorPanel()
        self.scene_editor_dock.setWidget(self.scene_editor_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scene_editor_dock)
        
        # 日志管理面板（左下）
        self.log_manager_dock = QDockWidget("日志管理", self)
        self.log_manager_panel = LogManagerPanel()
        self.log_manager_dock.setWidget(self.log_manager_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.log_manager_dock)
        
        # AI助理面板（右下）
        self.ai_assistant_dock = QDockWidget("AI助理", self)
        self.ai_assistant_panel = AIAssistantPanel()
        self.ai_assistant_dock.setWidget(self.ai_assistant_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.ai_assistant_dock)
        
        # 设置面板的浮动和停靠属性
        for dock in [self.project_info_dock, self.scene_editor_dock, 
                    self.log_manager_dock, self.ai_assistant_dock]:
            dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable |
                           QDockWidget.DockWidgetFeature.DockWidgetMovable |
                           QDockWidget.DockWidgetFeature.DockWidgetFloatable)
            dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
            
        # 设置初始布局
        self.splitDockWidget(self.project_info_dock, self.scene_editor_dock, Qt.Orientation.Horizontal)
        self.splitDockWidget(self.project_info_dock, self.log_manager_dock, Qt.Orientation.Vertical)
        self.splitDockWidget(self.scene_editor_dock, self.ai_assistant_dock, Qt.Orientation.Vertical)
        
    def setup_styles(self):
        """设置样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            
            /* 停靠窗口样式 */
            QDockWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            
            QDockWidget::title {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 4px;
            }
            
            QDockWidget::close-button, QDockWidget::float-button {
                background-color: transparent;
                border: none;
            }
            
            QDockWidget::close-button:hover, QDockWidget::float-button:hover {
                background-color: #3d3d3d;
            }
            
            /* 按钮样式 */
            QPushButton {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                padding: 4px 8px;
                border-radius: 2px;
            }
            
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            
            QPushButton:pressed {
                background-color: #5d5d5d;
            }
            
            /* 输入框样式 */
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 4px;
            }
            
            QLineEdit:focus {
                border: 1px solid #4d4d4d;
            }
            
            /* 下拉框样式 */
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 4px;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                selection-background-color: #3d3d3d;
            }
        """)
        
    def connect_menu_signals(self):
        """连接菜单信号"""
        # 视图菜单
        self.menu_bar.view_menu.actions()[0].triggered.connect(
            lambda: self.toggle_dock_widget(self.project_info_dock))
        self.menu_bar.view_menu.actions()[1].triggered.connect(
            lambda: self.toggle_dock_widget(self.scene_editor_dock))
        self.menu_bar.view_menu.actions()[2].triggered.connect(
            lambda: self.toggle_dock_widget(self.log_manager_dock))
        self.menu_bar.view_menu.actions()[3].triggered.connect(
            lambda: self.toggle_dock_widget(self.ai_assistant_dock))
            
        # 文件菜单
        self.menu_bar.file_menu.actions()[0].triggered.connect(self.new_project)
        self.menu_bar.file_menu.actions()[1].triggered.connect(self.open_project)
        self.menu_bar.file_menu.actions()[2].triggered.connect(self.save_project)
        self.menu_bar.file_menu.actions()[3].triggered.connect(self.save_project_as)
        self.menu_bar.file_menu.actions()[5].triggered.connect(self.close)
        
    def toggle_dock_widget(self, dock_widget: QDockWidget):
        """切换面板显示状态"""
        dock_widget.setVisible(not dock_widget.isVisible())
        
    def new_project(self):
        """新建项目"""
        # TODO: 实现新建项目功能
        pass
        
    def open_project(self):
        """打开项目"""
        # TODO: 实现打开项目功能
        pass
        
    def save_project(self):
        """保存项目"""
        # TODO: 实现保存项目功能
        pass
        
    def save_project_as(self):
        """另存为项目"""
        # TODO: 实现另存为项目功能
        pass
