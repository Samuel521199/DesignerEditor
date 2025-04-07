from PyQt6.QtWidgets import (QMainWindow, QDockWidget, QWidget, 
                            QVBoxLayout, QMenuBar, QToolBar, QStatusBar,
                            QMessageBox)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal, QByteArray
import logging

from .styles.theme import DARK_THEME
from .modules.project_info import ProjectInfoWidget
from .modules.scene_editor import SceneEditorWidget
from .modules.ai_assistant import AIAssistantWidget
from .modules.log_debugger import LogDebuggerWidget
from .modules.message_box.api import MessageBoxAPI, MessageType

class MainWindow(QMainWindow):
    """主窗口类，负责管理所有Dock窗口和基础功能"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UnityMindFlowPro Designer")
        self.setMinimumSize(1200, 800)
        
        # 初始化日志
        self.logger = logging.getLogger(__name__)
        
        # 创建基础UI组件
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        
        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建Dock窗口
        self._create_docks()
        
        # 保存初始布局状态
        self.default_state = self.saveState()
        
        # 应用样式
        self.setStyleSheet(DARK_THEME)
        
    def _create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        file_menu.addAction("新建项目")
        file_menu.addAction("打开项目")
        file_menu.addAction("保存项目")
        file_menu.addSeparator()
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction("撤销")
        edit_menu.addAction("重做")
        edit_menu.addSeparator()
        edit_menu.addAction("复制")
        edit_menu.addAction("粘贴")
        
        # 视图菜单
        view_menu = menubar.addMenu("视图")
        
        # 项目信息视图选项
        self.project_info_action = QAction("项目信息", self)
        self.project_info_action.setCheckable(True)
        self.project_info_action.setChecked(True)
        self.project_info_action.triggered.connect(
            lambda: self._toggle_dock(self.project_info_dock, self.project_info_action))
        view_menu.addAction(self.project_info_action)
        
        # 场景编辑器视图选项
        self.scene_editor_action = QAction("场景编辑器", self)
        self.scene_editor_action.setCheckable(True)
        self.scene_editor_action.setChecked(True)
        self.scene_editor_action.triggered.connect(
            lambda: self._toggle_dock(self.scene_editor_dock, self.scene_editor_action))
        view_menu.addAction(self.scene_editor_action)
        
        # AI助手视图选项
        self.ai_assistant_action = QAction("AI助手", self)
        self.ai_assistant_action.setCheckable(True)
        self.ai_assistant_action.setChecked(True)
        self.ai_assistant_action.triggered.connect(
            lambda: self._toggle_dock(self.ai_assistant_dock, self.ai_assistant_action))
        view_menu.addAction(self.ai_assistant_action)
        
        # 日志调试视图选项
        self.log_debugger_action = QAction("日志调试", self)
        self.log_debugger_action.setCheckable(True)
        self.log_debugger_action.setChecked(True)
        self.log_debugger_action.triggered.connect(
            lambda: self._toggle_dock(self.log_debugger_dock, self.log_debugger_action))
        view_menu.addAction(self.log_debugger_action)
        
        # 默认布局选项
        default_layout_action = QAction("默认布局", self)
        default_layout_action.triggered.connect(self._reset_layout)
        view_menu.addSeparator()
        view_menu.addAction(default_layout_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        help_menu.addAction("关于")
        
    def _create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar("主工具栏")
        toolbar.setObjectName("mainToolBar")
        self.addToolBar(toolbar)
        
        # 添加常用工具按钮
        toolbar.addAction("新建")
        toolbar.addAction("打开")
        toolbar.addAction("保存")
        toolbar.addSeparator()
        toolbar.addAction("撤销")
        toolbar.addAction("重做")
        
    def _create_status_bar(self):
        """创建状态栏"""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        statusbar.showMessage("就绪")
        
    def _create_docks(self):
        """创建Dock窗口"""
        # 项目信息Dock
        self.project_info_dock = QDockWidget("项目信息", self)
        self.project_info_dock.setObjectName("projectInfoDock")
        self.project_info_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                                             Qt.DockWidgetArea.RightDockWidgetArea)
        self.project_info_widget = ProjectInfoWidget()
        self.project_info_dock.setWidget(self.project_info_widget)
        
        # 场景编辑器Dock
        self.scene_editor_dock = QDockWidget("场景编辑器", self)
        self.scene_editor_dock.setObjectName("sceneEditorDock")
        self.scene_editor_dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.scene_editor_widget = SceneEditorWidget()
        self.scene_editor_dock.setWidget(self.scene_editor_widget)
        
        # AI助手Dock
        self.ai_assistant_dock = QDockWidget("AI助手", self)
        self.ai_assistant_dock.setObjectName("aiAssistantDock")
        self.ai_assistant_dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.ai_assistant_widget = AIAssistantWidget()
        self.ai_assistant_dock.setWidget(self.ai_assistant_widget)
        
        # 日志调试Dock
        self.log_debugger_dock = QDockWidget("日志调试", self)
        self.log_debugger_dock.setObjectName("logDebuggerDock")
        self.log_debugger_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        self.log_debugger_widget = LogDebuggerWidget()
        self.log_debugger_dock.setWidget(self.log_debugger_widget)
        
        # 设置初始布局
        self._reset_layout()
        
    def _toggle_dock(self, dock: QDockWidget, action: QAction):
        """切换Dock窗口的显示状态"""
        if action.isChecked():
            dock.show()
        else:
            dock.hide()
            
    def _reset_layout(self):
        """重置为默认布局"""
        # 确保所有窗口可见
        self.project_info_dock.show()
        self.scene_editor_dock.show()
        self.ai_assistant_dock.show()
        self.log_debugger_dock.show()
        
        # 更新菜单栏的复选框状态
        self.project_info_action.setChecked(True)
        self.scene_editor_action.setChecked(True)
        self.ai_assistant_action.setChecked(True)
        self.log_debugger_action.setChecked(True)
        
        # 设置窗口大小
        self.project_info_dock.setMinimumWidth(300)
        self.project_info_dock.setMaximumWidth(400)
        self.scene_editor_dock.setMinimumWidth(400)
        
        # 设置底部窗口高度
        self.ai_assistant_dock.setMinimumHeight(200)
        self.log_debugger_dock.setMinimumHeight(200)
        
        # 恢复到初始布局状态
        if hasattr(self, 'default_state'):
            self.restoreState(self.default_state)
        else:
            # 如果没有保存的状态，手动设置布局
            self.removeDockWidget(self.project_info_dock)
            self.removeDockWidget(self.scene_editor_dock)
            self.removeDockWidget(self.ai_assistant_dock)
            self.removeDockWidget(self.log_debugger_dock)
            
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_info_dock)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scene_editor_dock)
            self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.ai_assistant_dock)
            self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_debugger_dock)
            
            # 设置AI助手和日志调试窗口各占一半
            self.splitDockWidget(self.ai_assistant_dock, self.log_debugger_dock, Qt.Orientation.Horizontal)
        
        # 恢复窗口大小
        self.resize(1200, 800)