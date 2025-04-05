import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QTreeWidget, QTreeWidgetItem, QTabWidget, QMenuBar, QMenu,
                           QToolBar, QStatusBar, QLabel, QTextEdit, QSplitter,
                           QPushButton, QGraphicsView, QGraphicsScene, QDockWidget,
                           QInputDialog, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPainter, QPen, QColor, QFont
from ai_assistant import AIAssistantPanel
from project_manager import ProjectManager, Project, ProjectStep

class FlowChartView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setBackgroundBrush(QColor("#1e1e1e"))

class FormulaEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # 添加公式编辑器
        self.editor = QTextEdit()
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                font-family: 'Consolas', monospace;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.editor)
        
        # 添加工具按钮
        tools_layout = QHBoxLayout()
        buttons = ["插入变量", "验证公式", "保存公式"]
        for text in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0d47a1;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
            """)
            tools_layout.addWidget(btn)
        layout.addLayout(tools_layout)

class DesignerEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing DesignerEditor window...")
        
        # 初始化项目管理器
        self.project_manager = ProjectManager()
        
        # 设置窗口标题
        self.setWindowTitle("UnityMindFlowPro Designer Editor")
        
        # 设置窗口大小和位置
        screen = QApplication.primaryScreen().geometry()
        width = min(1600, screen.width() - 100)
        height = min(900, screen.height() - 100)
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        self.setGeometry(x, y, width, height)
        
        # 设置窗口标志
        self.setWindowState(Qt.WindowState.WindowActive)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        
        print("Creating menu bar...")
        self.create_menu_bar()
        
        print("Creating tool bar...")
        self.create_tool_bar()
        
        print("Creating status bar...")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        print("Creating central widget...")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        print("Creating main layout...")
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        print("Creating left panel...")
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        print("Setting up planning tree...")
        self.planning_tree = QTreeWidget()
        self.planning_tree.setHeaderLabel("策划案结构")
        self.setup_planning_tree()
        left_layout.addWidget(self.planning_tree)
        
        print("Creating framework tabs...")
        framework_tabs = QTabWidget()
        framework_tabs.addTab(QWidget(), "系统架构")
        framework_tabs.addTab(QWidget(), "数据结构")
        framework_tabs.addTab(QWidget(), "接口定义")
        left_layout.addWidget(framework_tabs)
        
        print("Creating right panel...")
        right_panel = QTabWidget()
        
        print("Creating flow chart view...")
        self.flow_chart = FlowChartView()
        right_panel.addTab(self.flow_chart, "游戏流程")
        
        print("Creating formula editor...")
        self.formula_editor = FormulaEditor()
        right_panel.addTab(self.formula_editor, "公式编辑器")
        
        print("Adding panels to splitter...")
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)
        
        print("Setting up central layout...")
        central_layout = QHBoxLayout(central_widget)
        central_layout.addWidget(main_splitter)
        
        print("Creating docks...")
        self.create_docks()
        
        print("Applying styles...")
        self.apply_styles()
        
        print("DesignerEditor window initialization completed.")
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        # 项目操作
        new_project_action = QAction("新建项目", self)
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)
        
        open_project_action = QAction("打开项目", self)
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)
        
        save_project_action = QAction("保存项目", self)
        save_project_action.triggered.connect(self.save_project)
        file_menu.addAction(save_project_action)
        
        file_menu.addSeparator()
        
        # 步骤操作
        add_step_action = QAction("添加步骤", self)
        add_step_action.triggered.connect(self.add_step)
        file_menu.addAction(add_step_action)
        
        file_menu.addSeparator()
        
        # 退出操作
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        edit_actions = [
            ("撤销", "Ctrl+Z"),
            ("重做", "Ctrl+Y"),
            None,
            ("剪切", "Ctrl+X"),
            ("复制", "Ctrl+C"),
            ("粘贴", "Ctrl+V")
        ]
        
        for action in edit_actions:
            if action is None:
                edit_menu.addSeparator()
            else:
                name, shortcut = action
                act = QAction(name, self)
                act.setShortcut(shortcut)
                edit_menu.addAction(act)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图")
        # 工具菜单
        tools_menu = menubar.addMenu("工具")
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
    
    def create_tool_bar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        # 添加常用工具按钮
        tools = [
            ("新建", "新建项目"),
            ("打开", "打开项目"),
            ("保存", "保存项目"),
            None,  # 分隔符
            ("运行", "运行流程"),
            ("调试", "调试模式"),
            None,  # 分隔符
            ("导出", "导出项目")
        ]
        
        for tool in tools:
            if tool is None:
                toolbar.addSeparator()
            else:
                name, tooltip = tool
                action = QAction(name, self)
                action.setToolTip(tooltip)
                toolbar.addAction(action)
    
    def create_docks(self):
        # 创建AI助手面板
        ai_dock = QDockWidget("AI助手", self)
        ai_panel = AIAssistantPanel()
        ai_dock.setWidget(ai_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, ai_dock)
        
        # 创建属性面板
        properties_dock = QDockWidget("属性", self)
        properties_widget = QWidget()
        properties_layout = QVBoxLayout(properties_widget)
        properties_edit = QTextEdit()
        properties_layout.addWidget(properties_edit)
        properties_dock.setWidget(properties_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, properties_dock)
        
        # 创建输出面板
        output_dock = QDockWidget("输出", self)
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_text = QTextEdit()
        output_text.setReadOnly(True)
        output_layout.addWidget(output_text)
        output_dock.setWidget(output_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, output_dock)
    
    def setup_planning_tree(self):
        # 添加示例树形结构
        root = QTreeWidgetItem(self.planning_tree, ["游戏设计文档"])
        
        # 添加主要分类
        categories = [
            ("游戏概述", ["游戏背景", "核心玩法", "目标受众"]),
            ("游戏系统", ["战斗系统", "养成系统", "社交系统"]),
            ("内容设计", ["关卡设计", "任务系统", "剧情设计"]),
            ("技术需求", ["性能指标", "平台要求", "开发规范"])
        ]
        
        for category, subcategories in categories:
            cat_item = QTreeWidgetItem(root, [category])
            for sub in subcategories:
                QTreeWidgetItem(cat_item, [sub])
        
        self.planning_tree.expandAll()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                color: #ffffff;
                font-size: 12px;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #3b3b3b;
            }
            QMenu {
                background-color: #2b2b2b;
                border: 1px solid #3b3b3b;
            }
            QMenu::item:selected {
                background-color: #3b3b3b;
            }
            QToolBar {
                background-color: #2b2b2b;
                border: none;
                spacing: 3px;
            }
            QStatusBar {
                background-color: #2b2b2b;
                color: #a0a0a0;
            }
            QTreeWidget {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
            }
            QTreeWidget::item:hover {
                background-color: #3d3d3d;
            }
            QTreeWidget::item:selected {
                background-color: #0d47a1;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                padding: 5px 10px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0d47a1;
            }
            QDockWidget {
                color: white;
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(float.png);
            }
            QDockWidget::title {
                background-color: #2b2b2b;
                padding-left: 5px;
                padding-top: 2px;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
            }
        """)

    def new_project(self):
        name, ok = QInputDialog.getText(self, "新建项目", "请输入项目名称:")
        if ok and name:
            description, ok = QInputDialog.getText(self, "新建项目", "请输入项目描述:")
            if ok:
                self.project_manager.create_project(name, description)
                self.statusBar().showMessage(f"已创建新项目: {name}")
                self.update_project_tree()

    def open_project(self):
        projects = self.project_manager.list_projects()
        if not projects:
            QMessageBox.information(self, "打开项目", "没有找到任何项目")
            return
            
        name, ok = QInputDialog.getItem(self, "打开项目", "选择项目:", projects, 0, False)
        if ok and name:
            try:
                self.project_manager.load_project(name)
                self.statusBar().showMessage(f"已打开项目: {name}")
                self.update_project_tree()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"打开项目失败: {str(e)}")

    def save_project(self):
        if not self.project_manager.current_project:
            QMessageBox.warning(self, "保存项目", "没有当前项目")
            return
            
        try:
            self.project_manager.save_project(self.project_manager.current_project)
            self.statusBar().showMessage(f"项目已保存: {self.project_manager.current_project.name}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存项目失败: {str(e)}")

    def add_step(self):
        if not self.project_manager.current_project:
            QMessageBox.warning(self, "添加步骤", "请先创建或打开一个项目")
            return
            
        name, ok = QInputDialog.getText(self, "添加步骤", "请输入步骤名称:")
        if ok and name:
            description, ok = QInputDialog.getText(self, "添加步骤", "请输入步骤描述:")
            if ok:
                step = ProjectStep(name, description)
                self.project_manager.current_project.add_step(step)
                self.update_project_tree()
                self.statusBar().showMessage(f"已添加步骤: {name}")

    def update_project_tree(self):
        self.planning_tree.clear()
        if not self.project_manager.current_project:
            return
            
        root = QTreeWidgetItem(self.planning_tree, [self.project_manager.current_project.name])
        root.setToolTip(0, self.project_manager.current_project.description)
        
        for step in self.project_manager.current_project.steps:
            step_item = QTreeWidgetItem(root, [step.name])
            step_item.setToolTip(0, step.description)
            if step.is_generated:
                step_item.setIcon(0, QIcon("resources/icons/check.png"))
            else:
                step_item.setIcon(0, QIcon("resources/icons/cross.png"))
        
        self.planning_tree.expandAll()

def main():
    try:
        print("Starting application...")
        
        # 设置 DPI 感知
        if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # 获取应用程序的基础路径
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
            print(f"Running in frozen mode from: {base_path}")
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            print(f"Running in development mode from: {base_path}")
        
        # 加载环境变量
        env_path = os.path.join(base_path, '.env')
        if os.path.exists(env_path):
            print(f"Loading environment variables from: {env_path}")
            load_dotenv(env_path)
        else:
            print(f"Warning: .env file not found at: {env_path}")
            
        # 确保 QApplication 在主线程中创建
        app = QApplication.instance()
        if app is None:
            print("Creating new QApplication instance...")
            app = QApplication(sys.argv)
        
        # 设置应用程序样式
        print("Setting application style...")
        app.setStyle("Fusion")
        
        # 创建主窗口
        print("Creating main window...")
        window = DesignerEditor()
        
        # 显示窗口
        print("Showing main window...")
        window.show()
        window.raise_()  # 将窗口提升到最前
        window.activateWindow()  # 激活窗口
        
        print("Entering event loop...")
        return app.exec()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main()) 