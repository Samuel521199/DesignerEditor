import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QTreeWidget, QTreeWidgetItem, QTabWidget, QMenuBar, QMenu,
                           QToolBar, QStatusBar, QLabel, QTextEdit, QSplitter,
                           QPushButton, QGraphicsView, QGraphicsScene, QDockWidget,
                           QInputDialog, QMessageBox, QFileDialog, QDialog,
                           QLineEdit, QComboBox, QSpinBox, QFormLayout,
                           QListWidget, QDialogButtonBox, QCheckBox, QGroupBox,
                           QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPainter, QPen, QColor, QFont
from ai_assistant import AIAssistantPanel
from project_manager import ProjectManager, GameProject, DesignStep, DesignType

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

class DesignStepDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加设计步骤")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # 基本信息
        self.name_edit = QLineEdit()
        layout.addRow("步骤名称:", self.name_edit)

        self.type_combo = QComboBox()
        for design_type in DesignType:
            self.type_combo.addItem(design_type.value)
        layout.addRow("设计类型:", self.type_combo)

        self.description_edit = QTextEdit()
        layout.addRow("描述:", self.description_edit)

        # 优先级和状态
        self.priority_spin = QSpinBox()
        self.priority_spin.setRange(0, 10)
        layout.addRow("优先级:", self.priority_spin)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["未开始", "进行中", "已完成"])
        layout.addRow("状态:", self.status_combo)

        # 时间估算
        self.estimated_time_spin = QSpinBox()
        self.estimated_time_spin.setRange(0, 1000)
        layout.addRow("预计时间(小时):", self.estimated_time_spin)

        # 标签
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("用逗号分隔多个标签")
        layout.addRow("标签:", self.tags_edit)

        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_step_data(self):
        return {
            "name": self.name_edit.text(),
            "design_type": DesignType(self.type_combo.currentText()),
            "description": self.description_edit.toPlainText(),
            "priority": self.priority_spin.value(),
            "status": self.status_combo.currentText(),
            "estimated_time": self.estimated_time_spin.value(),
            "tags": [tag.strip() for tag in self.tags_edit.text().split(",") if tag.strip()]
        }

class ProjectSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("项目设置")
        self.setMinimumSize(900, 600)
        
        # 获取资源路径
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.resource_path = os.path.join(base_path, 'resources')
        
        self.setup_ui()
        self.setup_styles()
        self.setup_connections()
        self.setModal(True)  # 确保对话框是模态的

    def setup_ui(self):
        # 创建主布局
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # 左侧设置面板
        settings_panel = QWidget()
        settings_layout = QVBoxLayout(settings_panel)
        settings_layout.setSpacing(8)
        settings_layout.setContentsMargins(0, 0, 0, 0)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        settings_layout.addWidget(scroll_area)

        # 创建内容容器
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(8)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # 基本信息部分
        basic_info_group = QGroupBox("基本信息")
        basic_info_layout = QFormLayout(basic_info_group)
        basic_info_layout.setSpacing(6)
        basic_info_layout.setContentsMargins(8, 12, 8, 8)
        basic_info_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("输入项目名称")
        self.name_edit.setMinimumWidth(250)
        basic_info_layout.addRow("项目名称*:", self.name_edit)

        description_layout = QHBoxLayout()
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("输入项目描述")
        self.description_edit.setMinimumHeight(120)  # 增加高度
        self.description_edit.setMinimumWidth(300)   # 增加宽度
        self.ai_description_btn = QPushButton("AI生成")
        self.ai_description_btn.setFixedWidth(60)
        description_layout.addWidget(self.description_edit)
        description_layout.addWidget(self.ai_description_btn)
        basic_info_layout.addRow("项目描述*:", description_layout)

        content_layout.addWidget(basic_info_group)

        # 游戏设置部分
        game_settings_group = QGroupBox("游戏设置")
        game_settings_layout = QFormLayout(game_settings_group)
        game_settings_layout.setSpacing(6)
        game_settings_layout.setContentsMargins(8, 12, 8, 8)
        game_settings_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        # 游戏类型
        self.game_type_combo = QComboBox()
        self.game_type_combo.addItems([
            "经营策略", "角色扮演", "动作冒险", "模拟经营",
            "策略战棋", "射击游戏", "体育竞技", "益智解谜"
        ])
        self.game_type_combo.setCurrentText("经营策略")
        game_settings_layout.addRow("游戏类型*:", self.game_type_combo)

        # 目标平台
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["PC", "Mobile", "Console", "Web"])
        self.platform_combo.setCurrentText("PC")
        game_settings_layout.addRow("目标平台*:", self.platform_combo)

        # 游戏风格
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            "写实", "卡通", "像素", "手绘",
            "科幻", "奇幻", "现代", "复古"
        ])
        game_settings_layout.addRow("游戏风格*:", self.style_combo)

        content_layout.addWidget(game_settings_group)

        # 目标受众 - 使用网格布局
        audience_group = QGroupBox("目标受众*")
        audience_layout = QGridLayout(audience_group)
        audience_layout.setSpacing(8)
        audience_layout.setContentsMargins(12, 12, 12, 12)
        
        self.audience_checkboxes = []
        audiences = [
            "6-12岁", "13-17岁", "18-24岁",
            "25-29岁", "30-34岁", "35-39岁",
            "40-44岁", "45-59岁", "60岁以上"
        ]
        
        # 每行3个选项
        for i, audience in enumerate(audiences):
            checkbox = QCheckBox(audience)
            checkbox.setStyleSheet("QCheckBox { padding: 2px; }")
            self.audience_checkboxes.append(checkbox)
            audience_layout.addWidget(checkbox, i // 3, i % 3)
            
        content_layout.addWidget(audience_group)

        # 游戏机制部分 - 使用网格布局
        mechanics_group = QGroupBox("游戏机制")
        mechanics_layout = QGridLayout(mechanics_group)
        mechanics_layout.setSpacing(8)
        mechanics_layout.setContentsMargins(12, 12, 12, 12)

        # 核心机制
        core_mechanics_label = QLabel("核心机制*:")
        mechanics_layout.addWidget(core_mechanics_label, 0, 0, 1, 4)
        
        self.mechanics_checkboxes = []
        mechanics = [
            "资源管理", "城市建设", "经济系统", "科技树",
            "外交系统", "军事系统", "人口管理", "贸易系统",
            "任务系统", "成就系统", "排行榜", "社交系统"
        ]
        
        # 每行4个选项
        for i, mechanic in enumerate(mechanics):
            checkbox = QCheckBox(mechanic)
            checkbox.setStyleSheet("QCheckBox { padding: 2px; }")
            self.mechanics_checkboxes.append(checkbox)
            mechanics_layout.addWidget(checkbox, (i // 4) + 1, i % 4)

        # 游戏特色
        features_label = QLabel("游戏特色:")
        mechanics_layout.addWidget(features_label, 4, 0, 1, 4)
        
        self.features_checkboxes = []
        features = [
            "沙盒模式", "多人联机", "创意工坊", "成就系统",
            "排行榜", "每日任务", "赛季系统", "交易系统",
            "天气系统", "昼夜系统", "季节系统", "灾难系统"
        ]
        
        # 每行4个选项
        for i, feature in enumerate(features):
            checkbox = QCheckBox(feature)
            checkbox.setStyleSheet("QCheckBox { padding: 2px; }")
            self.features_checkboxes.append(checkbox)
            mechanics_layout.addWidget(checkbox, (i // 4) + 5, i % 4)

        content_layout.addWidget(mechanics_group)

        # 按钮
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 8, 0, 0)
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        self.ok_button = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.ok_button.setEnabled(False)
        button_layout.addStretch()
        button_layout.addWidget(self.button_box)
        content_layout.addLayout(button_layout)

        # 添加设置面板到主布局
        main_layout.addWidget(settings_panel, stretch=2)

        # 右侧AI建议面板
        ai_suggestion_group = QGroupBox("AI建议")
        ai_suggestion_layout = QVBoxLayout(ai_suggestion_group)
        ai_suggestion_layout.setSpacing(6)
        ai_suggestion_layout.setContentsMargins(8, 12, 8, 8)

        # AI建议文本框
        self.ai_suggestion_text = QTextEdit()
        self.ai_suggestion_text.setObjectName("ai_suggestion_text")
        self.ai_suggestion_text.setReadOnly(True)
        self.ai_suggestion_text.setMinimumHeight(400)
        self.ai_suggestion_text.setPlaceholderText("AI分析建议将在此显示...")
        ai_suggestion_layout.addWidget(self.ai_suggestion_text)

        # 添加AI建议面板到主布局
        main_layout.addWidget(ai_suggestion_group, stretch=1)

        # 连接信号
        self.name_edit.textChanged.connect(self.validate_form)
        self.description_edit.textChanged.connect(self.validate_form)
        self.game_type_combo.currentTextChanged.connect(self.validate_form)
        self.platform_combo.currentTextChanged.connect(self.validate_form)
        self.style_combo.currentTextChanged.connect(self.validate_form)
        
        # 连接所有选择变化的信号到更新AI建议
        self.game_type_combo.currentTextChanged.connect(self.update_ai_suggestions)
        self.platform_combo.currentTextChanged.connect(self.update_ai_suggestions)
        self.style_combo.currentTextChanged.connect(self.update_ai_suggestions)
        for checkbox in self.audience_checkboxes:
            checkbox.stateChanged.connect(self.update_ai_suggestions)
        for checkbox in self.mechanics_checkboxes:
            checkbox.stateChanged.connect(self.update_ai_suggestions)
        for checkbox in self.features_checkboxes:
            checkbox.stateChanged.connect(self.update_ai_suggestions)

    def validate_form(self):
        # 检查必填项
        name_valid = bool(self.name_edit.text().strip())
        description_valid = bool(self.description_edit.toPlainText().strip())
        game_type_valid = bool(self.game_type_combo.currentText())
        platform_valid = bool(self.platform_combo.currentText())
        style_valid = bool(self.style_combo.currentText())
        audience_valid = any(checkbox.isChecked() for checkbox in self.audience_checkboxes)
        mechanics_valid = any(checkbox.isChecked() for checkbox in self.mechanics_checkboxes)

        # 启用/禁用确定按钮
        self.ok_button.setEnabled(
            name_valid and description_valid and game_type_valid and 
            platform_valid and style_valid and audience_valid and mechanics_valid
        )

        # 显示验证状态
        if not name_valid:
            self.name_edit.setStyleSheet("border: 1px solid #ff0000;")
        else:
            self.name_edit.setStyleSheet("border: 1px solid #444444;")

        if not description_valid:
            self.description_edit.setStyleSheet("border: 1px solid #ff0000;")
        else:
            self.description_edit.setStyleSheet("border: 1px solid #444444;")

        if not audience_valid:
            for checkbox in self.audience_checkboxes:
                checkbox.setStyleSheet("color: #ff0000;")
        else:
            for checkbox in self.audience_checkboxes:
                checkbox.setStyleSheet("color: #ffffff;")

        if not mechanics_valid:
            for checkbox in self.mechanics_checkboxes:
                checkbox.setStyleSheet("color: #ff0000;")
        else:
            for checkbox in self.mechanics_checkboxes:
                checkbox.setStyleSheet("color: #ffffff;")

    def validate_and_accept(self):
        # 检查是否有未填写的必填项
        missing_fields = []
        if not self.name_edit.text().strip():
            missing_fields.append("项目名称")
        if not self.description_edit.toPlainText().strip():
            missing_fields.append("项目描述")
        if not any(checkbox.isChecked() for checkbox in self.audience_checkboxes):
            missing_fields.append("目标受众")
        if not any(checkbox.isChecked() for checkbox in self.mechanics_checkboxes):
            missing_fields.append("核心机制")

        if missing_fields:
            QMessageBox.warning(
                self,
                "缺少必填项",
                f"请填写以下必填项：\n{', '.join(missing_fields)}"
            )
            return

        # 如果所有必填项都已填写，接受对话框
        self.accept()

    def get_project_data(self):
        return {
            "name": self.name_edit.text(),
            "description": self.description_edit.toPlainText(),
            "game_type": self.game_type_combo.currentText(),
            "target_platform": self.platform_combo.currentText(),
            "target_audience": [cb.text() for cb in self.audience_checkboxes if cb.isChecked()],
            "game_style": self.style_combo.currentText(),
            "core_mechanics": [cb.text() for cb in self.mechanics_checkboxes if cb.isChecked()],
            "game_features": [cb.text() for cb in self.features_checkboxes if cb.isChecked()]
        }

    def setup_connections(self):
        self.ai_description_btn.clicked.connect(self.generate_description)

    def generate_description(self):
        try:
            # 获取当前选择的数据
            game_type = self.game_type_combo.currentText()
            platform = self.platform_combo.currentText()
            style = self.style_combo.currentText()
            selected_audience = [cb.text() for cb in self.audience_checkboxes if cb.isChecked()]
            selected_mechanics = [cb.text() for cb in self.mechanics_checkboxes if cb.isChecked()]
            selected_features = [cb.text() for cb in self.features_checkboxes if cb.isChecked()]
            
            # 构建提示词
            prompt = f"""请根据以下信息生成一个游戏项目描述：
游戏类型：{game_type}
目标平台：{platform}
游戏风格：{style}
目标受众：{', '.join(selected_audience)}
核心机制：{', '.join(selected_mechanics)}
游戏特色：{', '.join(selected_features)}

请生成一个详细的项目描述，包括：
1. 游戏概述
2. 核心玩法
3. 特色系统
4. 目标受众分析
5. 市场定位

要求：
- 语言简洁明了
- 突出游戏特色
- 符合目标受众喜好
- 体现游戏类型特点
"""
            # 使用全局的AI助手实例
            ai_assistant = self.parent().findChild(AIAssistantPanel)
            if ai_assistant:
                description = ai_assistant.generate_text(prompt)
                self.description_edit.setPlainText(description)
                
                # 同时更新AI建议
                self.update_ai_suggestions()
            else:
                raise Exception("未找到AI助手实例")
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成描述失败: {str(e)}\n请确保已正确配置AI接口。")

    def setup_styles(self):
        # 获取图标路径
        down_arrow_path = os.path.join(self.resource_path, 'icons', 'down_arrow.svg')
        check_path = os.path.join(self.resource_path, 'icons', 'check.svg')
        down_arrow_path = down_arrow_path.replace('\\', '/')  # 修复路径分隔符
        check_path = check_path.replace('\\', '/')  # 修复路径分隔符
        
        # 设置复选框样式
        checkbox_style = f"""
            QCheckBox {{
                color: #ffffff;
                spacing: 8px;
                font-size: 13px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid #444444;
                border-radius: 3px;
                background-color: #333333;
            }}
            QCheckBox::indicator:checked {{
                background-color: #0d47a1;
                border-color: #0d47a1;
                image: url("{check_path}");
            }}
            QCheckBox::indicator:hover {{
                border-color: #0d47a1;
            }}
        """
        
        for checkbox in self.audience_checkboxes + self.mechanics_checkboxes + self.features_checkboxes:
            checkbox.setStyleSheet(checkbox_style)
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #1a1a1a;
            }}
            QGroupBox {{
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #333333;
                border-radius: 5px;
                margin-top: 12px;
                background-color: #2a2a2a;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #ffffff;
                background-color: #2a2a2a;
            }}
            QLabel {{
                color: #ffffff;
                font-size: 13px;
            }}
            QLineEdit, QTextEdit, QComboBox {{
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #444444;
                padding: 8px;
                border-radius: 4px;
                font-size: 13px;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 1px solid #0d47a1;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: url("{down_arrow_path}");
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #333333;
                color: #ffffff;
                selection-background-color: #0d47a1;
            }}
            QPushButton {{
                background-color: #0d47a1;
                color: #ffffff;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: #1565c0;
            }}
            QPushButton:pressed {{
                background-color: #0a3d91;
            }}
            QPushButton:disabled {{
                background-color: #444444;
                color: #888888;
            }}
            QDialogButtonBox QPushButton {{
                background-color: #0d47a1;
                color: #ffffff;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
                min-width: 80px;
            }}
            QDialogButtonBox QPushButton:hover {{
                background-color: #1565c0;
            }}
            QDialogButtonBox QPushButton:pressed {{
                background-color: #0a3d91;
            }}
            QDialogButtonBox QPushButton:disabled {{
                background-color: #444444;
                color: #888888;
            }}
            QScrollArea, QScrollBar {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                width: 10px;
                margin: 0px;
            }}
            QScrollBar:horizontal {{
                height: 10px;
                margin: 0px;
            }}
            QScrollBar::handle {{
                background-color: #444444;
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::handle:hover {{
                background-color: #555555;
            }}
            QScrollBar::add-line, QScrollBar::sub-line {{
                height: 0px;
                width: 0px;
            }}
        """)

    def update_ai_suggestions(self):
        try:
            # 获取当前选择
            game_type = self.game_type_combo.currentText()
            platform = self.platform_combo.currentText()
            style = self.style_combo.currentText()
            selected_audience = [cb.text() for cb in self.audience_checkboxes if cb.isChecked()]
            selected_mechanics = [cb.text() for cb in self.mechanics_checkboxes if cb.isChecked()]
            selected_features = [cb.text() for cb in self.features_checkboxes if cb.isChecked()]

            # 构建提示词
            prompt = f"""请根据以下游戏设计选择提供简洁的建议：

游戏类型：{game_type}
目标平台：{platform}
游戏风格：{style}
目标受众：{', '.join(selected_audience) if selected_audience else '未选择'}
核心机制：{', '.join(selected_mechanics) if selected_mechanics else '未选择'}
游戏特色：{', '.join(selected_features) if selected_features else '未选择'}

请提供以下方面的建议：
1. 目标受众与游戏类型的匹配度
2. 核心机制是否适合目标平台
3. 游戏特色是否与游戏风格协调
4. 需要补充的关键设计点

要求：
- 每个建议不超过50字
- 直接指出问题或建议
- 避免重复说明
- 重点突出需要改进的地方"""

            # 使用全局的AI助手实例
            ai_assistant = self.parent().findChild(AIAssistantPanel)
            if ai_assistant:
                suggestions = ai_assistant.generate_text(prompt)
                self.ai_suggestion_text.setPlainText(suggestions)
            else:
                raise Exception("未找到AI助手实例")
                
        except Exception as e:
            self.ai_suggestion_text.setPlainText(f"生成AI建议时出错：{str(e)}\n请确保已正确配置AI接口。")

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
        self.planning_tree.setHeaderLabel("项目结构")
        self.setup_planning_tree()
        left_layout.addWidget(self.planning_tree)
        
        print("Creating framework tabs...")
        self.framework_tabs = QTabWidget()
        self.framework_tabs.addTab(QWidget(), "系统架构")
        self.framework_tabs.addTab(QWidget(), "数据结构")
        self.framework_tabs.addTab(QWidget(), "接口定义")
        left_layout.addWidget(self.framework_tabs)
        
        print("Creating right panel...")
        right_panel = QTabWidget()
        
        print("Creating flow chart view...")
        self.flow_chart_view = QTextEdit()
        self.flow_chart_view.setPlaceholderText("流程图视图")
        right_panel.addTab(self.flow_chart_view, "游戏流程")
        
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
        print("Creating new project...")
        dialog = ProjectSettingsDialog(self)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_project_data()
                project = self.project_manager.create_project(
                    data["name"],
                    data["description"],
                    data["game_type"]
                )
                project.target_platforms = [data["target_platform"]]
                project.target_audience = data["target_audience"]
                project.game_style = data["game_style"]
                project.core_mechanics = data["core_mechanics"]
                project.game_features = data["game_features"]
                
                # 更新项目树显示
                self.update_project_tree()
                self.statusBar.showMessage(f'已创建新项目: {data["name"]}')
                
                # 在项目树中显示详细信息
                root = QTreeWidgetItem(self.planning_tree, ["项目信息"])
                QTreeWidgetItem(root, [f"项目名称: {data['name']}"])
                QTreeWidgetItem(root, [f"游戏类型: {data['game_type']}"])
                QTreeWidgetItem(root, [f"目标平台: {data['target_platform']}"])
                QTreeWidgetItem(root, [f"游戏风格: {data['game_style']}"])
                
                # 添加目标受众
                audience_item = QTreeWidgetItem(root, ["目标受众"])
                for audience in data["target_audience"]:
                    QTreeWidgetItem(audience_item, [audience])
                
                # 添加核心机制
                mechanics_item = QTreeWidgetItem(root, ["核心机制"])
                for mechanic in data["core_mechanics"]:
                    QTreeWidgetItem(mechanics_item, [mechanic])
                
                # 添加游戏特色
                features_item = QTreeWidgetItem(root, ["游戏特色"])
                for feature in data["game_features"]:
                    QTreeWidgetItem(features_item, [feature])
                
                # 添加项目描述
                desc_item = QTreeWidgetItem(root, ["项目描述"])
                QTreeWidgetItem(desc_item, [data["description"]])
                
                self.planning_tree.expandAll()
                
            except Exception as e:
                print(f"Error creating project: {str(e)}")
                QMessageBox.critical(self, '错误', f'创建项目失败: {str(e)}')
        else:
            print("Project creation cancelled by user")

    def open_project(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, '打开项目', '', 'DesignerEditor Project (*.dep)')
            
            if file_path:
                project = self.project_manager.load_project(file_path)
                if project:
                    self.project_manager.current_project = project
                    self.update_project_tree()
                    
                    # 在项目树中显示详细信息
                    self.planning_tree.clear()  # 清空现有内容
                    root = QTreeWidgetItem(self.planning_tree, ["项目信息"])
                    QTreeWidgetItem(root, [f"项目名称: {project.name}"])
                    QTreeWidgetItem(root, [f"游戏类型: {project.game_type}"])
                    QTreeWidgetItem(root, [f"目标平台: {', '.join(project.target_platforms)}"])
                    QTreeWidgetItem(root, [f"游戏风格: {project.game_style}"])
                    
                    # 添加目标受众
                    audience_item = QTreeWidgetItem(root, ["目标受众"])
                    for audience in project.target_audience:
                        QTreeWidgetItem(audience_item, [audience])
                    
                    # 添加核心机制
                    mechanics_item = QTreeWidgetItem(root, ["核心机制"])
                    for mechanic in project.core_mechanics:
                        QTreeWidgetItem(mechanics_item, [mechanic])
                    
                    # 添加游戏特色
                    features_item = QTreeWidgetItem(root, ["游戏特色"])
                    for feature in project.game_features:
                        QTreeWidgetItem(features_item, [feature])
                    
                    # 添加项目描述
                    desc_item = QTreeWidgetItem(root, ["项目描述"])
                    QTreeWidgetItem(desc_item, [project.description])
                    
                    self.planning_tree.expandAll()
                    self.statusBar.showMessage(f'已加载项目: {project.name}')
                    
                    # 显示加载成功信息
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('加载成功')
                    msg_box.setText(f'项目已成功加载:\n{project.name}')
                    msg_box.setStyleSheet("""
                        QMessageBox {
                            background-color: #2b2b2b;
                            color: #ffffff;
                        }
                        QMessageBox QLabel {
                            color: #ffffff;
                        }
                        QMessageBox QPushButton {
                            background-color: #3c3c3c;
                            color: #ffffff;
                            border: 1px solid #4a4a4a;
                            padding: 5px 15px;
                            border-radius: 3px;
                        }
                        QMessageBox QPushButton:hover {
                            background-color: #4a4a4a;
                        }
                        QMessageBox QPushButton:pressed {
                            background-color: #5a5a5a;
                        }
                    """)
                    msg_box.exec()
                else:
                    QMessageBox.critical(self, '错误', '加载项目失败')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'打开项目失败: {str(e)}')

    def save_project(self):
        if not self.project_manager.current_project:
            QMessageBox.warning(self, '警告', '没有打开的项目')
            return

        try:
            file_path = self.project_manager.get_project_file_path()
            if not file_path:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, '保存项目', '', 'DesignerEditor Project (*.dep)')
            
            if file_path:
                self.project_manager.save_project(self.project_manager.current_project, file_path)
                # 显示保存成功信息
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('保存成功')
                msg_box.setText(f'项目已成功保存到:\n{file_path}')
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #2b2b2b;
                        color: #ffffff;
                    }
                    QMessageBox QLabel {
                        color: #ffffff;
                    }
                    QMessageBox QPushButton {
                        background-color: #3c3c3c;
                        color: #ffffff;
                        border: 1px solid #4a4a4a;
                        padding: 5px 15px;
                        border-radius: 3px;
                    }
                    QMessageBox QPushButton:hover {
                        background-color: #4a4a4a;
                    }
                    QMessageBox QPushButton:pressed {
                        background-color: #5a5a5a;
                    }
                """)
                msg_box.exec()
                self.statusBar.showMessage(f'项目已保存: {file_path}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'保存项目失败: {str(e)}')

    def add_step(self):
        if not self.project_manager.current_project:
            QMessageBox.warning(self, '警告', '请先创建或打开一个项目')
            return

        dialog = DesignStepDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_step_data()
                step = DesignStep(
                    name=data["name"],
                    design_type=data["design_type"],
                    description=data["description"]
                )
                step.priority = data["priority"]
                step.status = data["status"]
                step.estimated_time = data["estimated_time"]
                step.tags = data["tags"]
                
                self.project_manager.current_project.add_step(step)
                self.update_project_tree()
                self.statusBar().showMessage(f'已添加步骤: {data["name"]}')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'添加步骤失败: {str(e)}')

    def update_project_tree(self):
        self.planning_tree.clear()
        if self.project_manager.current_project:
            project = self.project_manager.current_project
            project_item = QTreeWidgetItem([project.name])
            self.planning_tree.addTopLevelItem(project_item)
            
            # 按设计类型分组
            type_groups = {}
            for step in project.steps:
                if step.design_type.value not in type_groups:
                    type_groups[step.design_type.value] = QTreeWidgetItem([step.design_type.value])
                    project_item.addChild(type_groups[step.design_type.value])
                
                step_item = QTreeWidgetItem([step.name])
                if step.is_generated:
                    step_item.setIcon(0, QIcon('resources/icons/check.png'))
                type_groups[step.design_type.value].addChild(step_item)
            
            self.planning_tree.expandAll()

    def closeEvent(self, event):
        if self.project_manager.is_project_modified():
            reply = QMessageBox.question(self, '保存更改',
                                       '当前项目已修改，是否保存更改？',
                                       QMessageBox.StandardButton.Yes |
                                       QMessageBox.StandardButton.No |
                                       QMessageBox.StandardButton.Cancel)
            
            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
            elif reply == QMessageBox.StandardButton.Yes:
                self.save_project()
        
        event.accept()

def main():
    try:
        # 创建应用实例
        app = QApplication(sys.argv)
        
        # 设置应用信息
        app.setApplicationName("UnityMindFlowPro Designer")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("UnityMindFlowPro")
        
        # 设置资源路径
        if getattr(sys, 'frozen', False):
            # 打包后的路径
            base_path = os.path.dirname(sys.executable)
        else:
            # 开发环境路径
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        resource_path = os.path.join(base_path, 'resources')
        if not os.path.exists(resource_path):
            os.makedirs(resource_path)
            
        icons_path = os.path.join(resource_path, 'icons')
        if not os.path.exists(icons_path):
            os.makedirs(icons_path)
            
        # 加载环境变量
        env_path = os.path.join(base_path, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
        else:
            print("警告: 未找到 .env 文件")
            
        # 创建主窗口
        window = DesignerEditor()
        window.show()
        
        # 运行应用
        sys.exit(app.exec())
        
    except Exception as e:
        # 创建错误窗口
        error_dialog = QDialog()
        error_dialog.setWindowTitle("错误")
        error_dialog.setMinimumSize(600, 400)
        error_dialog.setWindowFlags(error_dialog.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        # 创建布局
        layout = QVBoxLayout(error_dialog)
        
        # 错误信息显示
        error_text = QTextEdit()
        error_text.setReadOnly(True)
        error_text.setPlainText(f"发生错误:\n{str(e)}\n\n详细错误信息:\n{traceback.format_exc()}")
        error_text.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
            }
        """)
        layout.addWidget(error_text)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 复制按钮
        copy_button = QPushButton("复制错误信息")
        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(error_text.toPlainText()))
        button_layout.addWidget(copy_button)
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(error_dialog.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # 显示错误窗口
        error_dialog.exec()
        
        # 保持应用实例运行
        if 'app' in locals():
            sys.exit(app.exec())

if __name__ == '__main__':
    sys.exit(main()) 