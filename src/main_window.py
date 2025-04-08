"""
Main Window
主窗口模块

This module implements the main window of the application.
此模块实现应用程序的主窗口。
"""

import sys
print("Importing PyQt6 widgets...")
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                          QHBoxLayout, QDockWidget, QApplication)
from PyQt6.QtCore import Qt

print("Importing custom modules...")
from modules.menu_bar.menu_bar import MenuBar
from modules.project_info.project_info_panel import ProjectInfoPanel
from modules.scene_editor.api import SceneEditorAPI
from modules.log_manager.log_panel import LogPanel
from modules.ai_assistant.ai_assistant_panel import AIAssistantPanel

class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        print("Initializing MainWindow...")
        super().__init__()
        self.setWindowTitle("游戏设计编辑器")
        
        # 设置窗口大小和位置
        screen = QApplication.primaryScreen().geometry()
        window_width = 1600
        window_height = 900
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)
        
        print("Creating menu bar...")
        # 创建菜单栏
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        print("Setting up dock widgets...")
        # 创建并添加停靠窗口
        self.setup_dock_widgets()
        
        print("Setting up styles...")
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
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
        """)
        
    def setup_dock_widgets(self):
        """设置停靠窗口"""
        # 1. 项目信息面板（左侧）
        self.project_info_dock = QDockWidget("项目信息", self)
        self.project_info_panel = ProjectInfoPanel()  # 创建面板实例
        self.project_info_dock.setWidget(self.project_info_panel)  # 设置面板到dock中
        self.project_info_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable |
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_info_dock)
        
        # 2. 场景编辑器（中央）
        self.scene_editor = SceneEditorAPI.create_scene_editor()  # 创建并存储场景编辑器实例
        self.setCentralWidget(self.scene_editor)  # 使用存储的实例
        
        # 3. 日志面板（底部）
        self.log_dock = QDockWidget("日志", self)
        self.log_dock.setWidget(LogPanel())
        self.log_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable |
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dock)
        
        # 4. AI助手面板（右侧）
        self.assistant_dock = QDockWidget("AI助手", self)
        self.assistant_dock.setWidget(AIAssistantPanel())
        self.assistant_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable |
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.assistant_dock)
        
        # 设置初始布局和大小
        self.resizeDocks([self.project_info_dock], [300], Qt.Orientation.Horizontal)
        self.resizeDocks([self.assistant_dock], [300], Qt.Orientation.Horizontal)
        self.resizeDocks([self.log_dock], [200], Qt.Orientation.Vertical)
        
        # 设置停靠窗口的初始大小策略
        self.project_info_dock.setMinimumWidth(200)
        self.assistant_dock.setMinimumWidth(200)
        self.log_dock.setMinimumHeight(100)
        
        # 设置停靠窗口的初始位置
        self.splitDockWidget(self.project_info_dock, self.log_dock, Qt.Orientation.Vertical)
        self.splitDockWidget(self.project_info_dock, self.assistant_dock, Qt.Orientation.Horizontal)
