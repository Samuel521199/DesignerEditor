"""
Designer Editor Main Window
设计器编辑器主窗口

This module provides the main window implementation for the Designer Editor.
此模块提供设计器编辑器的主窗口实现。
"""

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
from modules.ai_assistant import AIAssistantPanel
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
    """Designer Editor main window class."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Designer Editor")
        self.setMinimumSize(1200, 800)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 设置中央部件
        self.setup_central_widget()
        
        # 创建停靠窗口
        self.create_dock_windows()
        
        # 应用样式
        self.apply_style()
        
        # 设置默认布局
        self.setup_default_layout()
        
        print("DesignerEditor window initialization completed.")

    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        new_action = QAction("新建项目", self)
        open_action = QAction("打开项目", self)
        save_action = QAction("保存项目", self)
        file_menu.addActions([new_action, open_action, save_action])
        
        # 视图菜单
        view_menu = menubar.addMenu("视图")
        
        # 项目窗口
        self.project_action = QAction("项目", self)
        self.project_action.setCheckable(True)
        self.project_action.setChecked(True)
        self.project_action.triggered.connect(self.toggle_project_window)
        
        # 场景制作窗口
        self.scene_editor_action = QAction("场景制作", self)
        self.scene_editor_action.setCheckable(True)
        self.scene_editor_action.setChecked(True)
        self.scene_editor_action.triggered.connect(self.toggle_scene_editor_window)
        
        # AI助手窗口
        self.ai_assistant_action = QAction("AI助手", self)
        self.ai_assistant_action.setCheckable(True)
        self.ai_assistant_action.setChecked(True)
        self.ai_assistant_action.triggered.connect(self.toggle_ai_assistant_window)
        
        # 日志窗口
        self.log_action = QAction("日志调试", self)
        self.log_action.setCheckable(True)
        self.log_action.setChecked(True)
        self.log_action.triggered.connect(self.toggle_log_window)
        
        # 默认布局
        default_layout_action = QAction("默认布局", self)
        default_layout_action.triggered.connect(self.setup_default_layout)
        
        view_menu.addActions([
            self.project_action,
            self.scene_editor_action,
            self.ai_assistant_action,
            self.log_action
        ])
        view_menu.addSeparator()
        view_menu.addAction(default_layout_action)

    def create_tool_bar(self):
        """Create the tool bar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # 添加工具按钮
        new_action = QAction("新建", self)
        open_action = QAction("打开", self)
        save_action = QAction("保存", self)
        toolbar.addActions([new_action, open_action, save_action])

    def create_status_bar(self):
        """Create the status bar."""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("就绪")

    def setup_central_widget(self):
        """Set up the central widget."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

    def create_dock_windows(self):
        """Create dock windows."""
        # 项目窗口（左上，包含项目信息和项目结构）
        self.project_dock = QDockWidget("项目", self)
        project_widget = QWidget()
        project_layout = QVBoxLayout(project_widget)
        project_layout.setContentsMargins(0, 0, 0, 0)
        project_layout.setSpacing(0)
        
        # 项目结构树
        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel("项目结构")
        project_layout.addWidget(self.project_tree, 1)  # 1表示拉伸系数
        
        # 项目信息编辑器
        self.project_info = QTextEdit()
        self.project_info.setPlaceholderText("项目信息...")
        project_layout.addWidget(self.project_info, 1)  # 1表示拉伸系数
        
        self.project_dock.setWidget(project_widget)
        
        # 场景制作窗口（右上）
        self.scene_editor_dock = QDockWidget("场景制作", self)
        self.scene_editor = QWidget()
        self.scene_editor_dock.setWidget(self.scene_editor)
        
        # AI助手窗口（右下）
        self.ai_assistant_dock = QDockWidget("AI助手", self)
        self.ai_assistant_dock.setWidget(AIAssistantPanel())
        
        # 日志窗口（左下）
        self.log_dock = QDockWidget("日志调试", self)
        self.log_dock.setWidget(QTextEdit())
        
        # 允许所有窗口浮动和关闭
        for dock in [self.project_dock, self.scene_editor_dock, self.ai_assistant_dock, self.log_dock]:
            dock.setFeatures(
                QDockWidget.DockWidgetFeature.DockWidgetMovable |
                QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                QDockWidget.DockWidgetFeature.DockWidgetClosable
            )
        
        # 初始布局设置
        self.setup_default_layout()

    def setup_default_layout(self):
        """Set up the default layout."""
        # 移除所有停靠窗口，以便重新布局
        for dock in [self.project_dock, self.scene_editor_dock, self.ai_assistant_dock, self.log_dock]:
            self.removeDockWidget(dock)
            dock.show()  # 确保窗口可见
        
        # 添加停靠窗口到指定位置
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scene_editor_dock)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.log_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.ai_assistant_dock)
        
        # 分割窗口
        self.splitDockWidget(self.project_dock, self.log_dock, Qt.Orientation.Vertical)
        self.splitDockWidget(self.scene_editor_dock, self.ai_assistant_dock, Qt.Orientation.Vertical)
        
        # 设置水平和垂直分割的大小比例
        self.resizeDocks(
            [self.project_dock, self.scene_editor_dock], 
            [int(self.width() * 0.5), int(self.width() * 0.5)],
            Qt.Orientation.Horizontal
        )
        self.resizeDocks(
            [self.project_dock, self.log_dock],
            [int(self.height() * 0.5), int(self.height() * 0.5)],
            Qt.Orientation.Vertical
        )
        self.resizeDocks(
            [self.scene_editor_dock, self.ai_assistant_dock],
            [int(self.height() * 0.5), int(self.height() * 0.5)],
            Qt.Orientation.Vertical
        )
        
        # 更新菜单项状态
        self.project_action.setChecked(True)
        self.scene_editor_action.setChecked(True)
        self.ai_assistant_action.setChecked(True)
        self.log_action.setChecked(True)
        
        # 设置停靠区域
        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.TopRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)
        self.setCorner(Qt.Corner.BottomLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

    def toggle_project_window(self):
        """Toggle project window visibility."""
        self.project_dock.setVisible(self.project_action.isChecked())

    def toggle_scene_editor_window(self):
        """Toggle scene editor window visibility."""
        self.scene_editor_dock.setVisible(self.scene_editor_action.isChecked())

    def toggle_ai_assistant_window(self):
        """Toggle AI assistant window visibility."""
        self.ai_assistant_dock.setVisible(self.ai_assistant_action.isChecked())

    def toggle_log_window(self):
        """Toggle log window visibility."""
        self.log_dock.setVisible(self.log_action.isChecked())

    def apply_style(self):
        """Apply dark theme style."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #3d3d3d;
            }
            QToolBar {
                background-color: #2d2d2d;
                border: none;
            }
            QToolButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #3d3d3d;
            }
            QDockWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(float.png);
            }
            QDockWidget::title {
                background-color: #2d2d2d;
                padding: 5px;
            }
            QTreeWidget, QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #ffffff;
            }
        """)

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = DesignerEditor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 