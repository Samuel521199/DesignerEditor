"""
Menu Bar Module
菜单栏模块

This module provides the main menu bar functionality.
此模块提供主菜单栏功能。
"""

from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from .new_project_dialog import NewProjectDialog
from ..file_manager.api import FileManagerAPI
from ..project_model.project_info_model import ProjectInfoModel
from ..message_box.api import MessageBoxAPI

class MenuBar(QMenuBar):
    """主菜单栏类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_manager = FileManagerAPI()
        self.current_project: ProjectInfoModel = None
        self.message_box_api = MessageBoxAPI()
        self.setup_ui()
        self.setup_styles()
    
    def setup_ui(self):
        """设置菜单栏界面"""
        # 文件菜单
        file_menu = self.addMenu("文件")
        
        # 新建项目
        new_project_action = QAction("新建项目", self)
        new_project_action.triggered.connect(self.show_new_project_dialog)
        file_menu.addAction(new_project_action)
        
        # 打开项目
        open_project_action = QAction("打开项目", self)
        open_project_action.triggered.connect(self.show_open_project_dialog)
        file_menu.addAction(open_project_action)
        
        # 保存项目
        save_project_action = QAction("保存项目", self)
        save_project_action.triggered.connect(self.save_current_project)
        file_menu.addAction(save_project_action)
        
        # 另存为
        save_as_action = QAction("另存为", self)
        save_as_action.triggered.connect(self.show_save_as_dialog)
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
        
        # 帮助
        help_action = QAction("帮助", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        # 关于
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_new_project_dialog(self):
        """显示新建项目对话框"""
        dialog = NewProjectDialog(self)
        if dialog.exec() == NewProjectDialog.DialogCode.Accepted:
            self.current_project = dialog.get_project_info()
            # 更新项目信息面板
            main_window = self.parent()
            if hasattr(main_window, 'project_info_panel'):
                main_window.project_info_panel.update_project_info(self.current_project)
            # 提示用户保存项目
            reply = QMessageBox.question(
                self,
                "保存项目",
                "是否现在保存项目？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.show_save_as_dialog()
            
    def show_open_project_dialog(self):
        """显示打开项目对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "打开项目",
            "",
            "项目文件 (*.dep)"
        )
        
        if file_path:
            project_info = self.file_manager.load_project(file_path)
            if project_info:
                self.current_project = project_info
                # 更新项目信息面板
                main_window = self.parent()
                if hasattr(main_window, 'project_info_panel'):
                    main_window.project_info_panel.update_project_info(project_info)
                QMessageBox.information(self, "成功", "项目加载成功！")
            else:
                QMessageBox.warning(self, "错误", "项目加载失败！")
                
    def save_current_project(self):
        """保存当前项目"""
        if not self.current_project:
            QMessageBox.warning(self, "警告", "没有正在编辑的项目！")
            return
            
        current_path = self.file_manager.get_project_directory()
        if not current_path:
            self.show_save_as_dialog()
            return
            
        if self.file_manager.save_project(self.current_project, current_path):
            QMessageBox.information(self, "成功", "项目保存成功！")
        else:
            QMessageBox.warning(self, "错误", "项目保存失败！")
            
    def show_save_as_dialog(self):
        """显示另存为对话框"""
        if not self.current_project:
            QMessageBox.warning(self, "警告", "没有正在编辑的项目！")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存项目",
            "",
            "项目文件 (*.dep)"
        )
        
        if file_path:
            if self.file_manager.save_project(self.current_project, file_path):
                QMessageBox.information(self, "成功", "项目保存成功！")
            else:
                QMessageBox.warning(self, "错误", "项目保存失败！")
    
    def show_help(self):
        help_text = """
        DesignerEditor 帮助信息

        主要功能：
        1. 项目管理
           - 新建项目
           - 打开项目
           - 保存项目

        2. 场景管理
           - 创建场景
           - 编辑场景
           - 删除场景

        3. 公式管理
           - 创建公式
           - 编辑公式
           - 删除公式

        4. 资源管理
           - 添加资源
           - 编辑资源
           - 删除资源

        更多功能正在开发中...
        """
        self.message_box_api.show_message("帮助", help_text)

    def show_about(self):
        about_text = """
        DesignerEditor v0.10

        作者：Samuel-Jiang
        日期：2024-03-21

        一个用于游戏设计的编辑器工具。
        """
        self.message_box_api.show_message("关于", about_text)
    
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