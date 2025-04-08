"""
Menu Bar Module
菜单栏模块

This module implements the main menu bar functionality.
此模块实现主菜单栏功能。
"""

from PyQt6.QtWidgets import QMenuBar, QMenu, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from .new_project_dialog import NewProjectDialog
from ..file_manager.file_manager import FileManager

class MenuBar(QMenuBar):
    """主菜单栏类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_manager = FileManager()
        self.setup_ui()
        self.setup_styles()
    
    def setup_ui(self):
        """设置界面"""
        # 文件菜单
        file_menu = self.addMenu("文件")
        
        # 新建项目
        new_project_action = QAction("新建项目", self)
        new_project_action.triggered.connect(self.show_new_project_dialog)
        file_menu.addAction(new_project_action)
        
        # 打开
        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        # 保存
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        # 另存为
        save_as_action = QAction("另存为", self)
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.parent().close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = self.addMenu("编辑")
        
        # 撤销
        undo_action = QAction("撤销", self)
        edit_menu.addAction(undo_action)
        
        # 重做
        redo_action = QAction("重做", self)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # 剪切
        cut_action = QAction("剪切", self)
        edit_menu.addAction(cut_action)
        
        # 复制
        copy_action = QAction("复制", self)
        edit_menu.addAction(copy_action)
        
        # 粘贴
        paste_action = QAction("粘贴", self)
        edit_menu.addAction(paste_action)
        
        # 视图菜单
        view_menu = self.addMenu("视图")
        
        # 工具栏
        toolbar_action = QAction("工具栏", self)
        toolbar_action.setCheckable(True)
        toolbar_action.setChecked(True)
        view_menu.addAction(toolbar_action)
        
        # 状态栏
        statusbar_action = QAction("状态栏", self)
        statusbar_action.setCheckable(True)
        statusbar_action.setChecked(True)
        view_menu.addAction(statusbar_action)
        
        # 工具菜单
        tools_menu = self.addMenu("工具")
        
        # 选项
        options_action = QAction("选项", self)
        tools_menu.addAction(options_action)
        
        # 帮助菜单
        help_menu = self.addMenu("帮助")
        
        # 帮助内容
        help_content_action = QAction("帮助内容", self)
        help_menu.addAction(help_content_action)
        
        # 关于
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)
    
    def show_new_project_dialog(self):
        """显示新建项目对话框"""
        dialog = NewProjectDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            project_info = dialog.get_project_info()
            # 更新项目信息面板
            main_window = self.parent()
            if hasattr(main_window, 'project_info_panel'):
                main_window.project_info_panel.update_project_info(project_info)
            # 保存项目
            self.file_manager.save_project(project_info, "project.json")
    
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
    
    def setup_styles(self):
        """设置样式"""
        self.setStyleSheet("""
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border-bottom: 1px solid #3b3b3b;
                font-size: 14px;
            }
            
            QMenuBar::item {
                padding: 4px 8px;
                background-color: transparent;
            }
            
            QMenuBar::item:selected {
                background-color: #3b3b3b;
            }
            
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3b3b3b;
                font-size: 14px;
            }
            
            QMenu::item {
                padding: 6px 20px;
            }
            
            QMenu::item:selected {
                background-color: #3b3b3b;
            }
            
            QMenu::separator {
                height: 1px;
                background-color: #3b3b3b;
                margin: 4px 0;
            }
        """) 