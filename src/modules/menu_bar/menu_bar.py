"""
Menu Bar
菜单栏模块

This module defines the menu bar for the main window.
此模块定义主窗口的菜单栏。
"""

from PyQt6.QtWidgets import QMenuBar, QMenu, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

class MenuBar(QMenuBar):
    """菜单栏类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_menus()
        self.setup_styles()
        
    def setup_menus(self):
        """设置菜单"""
        # 文件菜单
        file_menu = self.addMenu("文件")
        
        new_action = QAction("新建", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)
        
        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = self.addMenu("编辑")
        
        undo_action = QAction("撤销", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("重做", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("剪切", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("复制", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("粘贴", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)
        
        # 视图菜单
        view_menu = self.addMenu("视图")
        
        # 默认布局
        default_layout_action = QAction("默认布局", self)
        default_layout_action.triggered.connect(self.restore_default_layout)
        view_menu.addAction(default_layout_action)
        
        view_menu.addSeparator()
        
        # 工具栏
        toolbar_menu = view_menu.addMenu("工具栏")
        
        show_toolbar_action = QAction("显示工具栏", self)
        show_toolbar_action.setCheckable(True)
        show_toolbar_action.setChecked(True)
        toolbar_menu.addAction(show_toolbar_action)
        
        # 状态栏
        statusbar_menu = view_menu.addMenu("状态栏")
        
        show_statusbar_action = QAction("显示状态栏", self)
        show_statusbar_action.setCheckable(True)
        show_statusbar_action.setChecked(True)
        statusbar_menu.addAction(show_statusbar_action)
        
        # 工具菜单
        tools_menu = self.addMenu("工具")
        
        settings_action = QAction("设置", self)
        tools_menu.addAction(settings_action)
        
        # 帮助菜单
        help_menu = self.addMenu("帮助")
        
        documentation_action = QAction("文档", self)
        help_menu.addAction(documentation_action)
        
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)
    
    def restore_default_layout(self):
        """恢复默认布局"""
        if self.main_window:
            # 获取主窗口的中央部件
            central_widget = self.main_window.centralWidget()
            
            # 获取所有可停靠窗口
            dock_widgets = self.main_window.findChildren(QDockWidget)
            
            # 恢复每个可停靠窗口的默认位置和大小
            for dock in dock_widgets:
                # 移除停靠
                dock.setFloating(False)
                
                # 根据窗口标题设置默认位置
                if "项目信息" in dock.windowTitle():
                    self.main_window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
                elif "场景编辑" in dock.windowTitle():
                    self.main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
                elif "日志管理" in dock.windowTitle():
                    self.main_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)
                elif "AI助理" in dock.windowTitle():
                    self.main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
                
                # 设置默认大小
                if "项目信息" in dock.windowTitle():
                    dock.setFixedWidth(300)
                elif "场景编辑" in dock.windowTitle():
                    dock.setFixedWidth(400)
                elif "日志管理" in dock.windowTitle():
                    dock.setFixedHeight(200)
                elif "AI助理" in dock.windowTitle():
                    dock.setFixedWidth(300)
    
    def setup_styles(self):
        """设置样式"""
        self.setStyleSheet("""
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border: none;
                padding: 2px;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
                margin: 2px;
                border-radius: 4px;
            }
            
            QMenuBar::item:selected {
                background-color: #3b3b3b;
            }
            
            QMenuBar::item:pressed {
                background-color: #4b4b4b;
            }
            
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3b3b3b;
                padding: 4px;
            }
            
            QMenu::item {
                background-color: transparent;
                padding: 6px 20px;
                margin: 2px;
                border-radius: 4px;
            }
            
            QMenu::item:selected {
                background-color: #3b3b3b;
            }
            
            QMenu::item:pressed {
                background-color: #4b4b4b;
            }
            
            QMenu::separator {
                height: 1px;
                background-color: #3b3b3b;
                margin: 4px 0;
            }
        """) 