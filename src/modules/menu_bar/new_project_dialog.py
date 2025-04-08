"""
New Project Dialog
新建项目对话框

This module implements the new project dialog window.
此模块实现新建项目对话框窗口。
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QTextEdit, QComboBox, QPushButton,
                            QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt
from ..project_model.project_info_model import (ProjectInfoModel, GameType, 
                                              TargetPlatform, GameStyle, 
                                              TimeSetting, TargetAudience)

class NewProjectDialog(QDialog):
    """新建项目对话框类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建项目")
        self.setMinimumWidth(500)
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout()
        
        # 项目名称
        name_layout = QHBoxLayout()
        name_label = QLabel("项目名称:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # 项目描述
        desc_layout = QVBoxLayout()
        desc_label = QLabel("项目描述:")
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        layout.addLayout(desc_layout)
        
        # 游戏类型
        type_layout = QHBoxLayout()
        type_label = QLabel("游戏类型:")
        self.type_combo = QComboBox()
        self.type_combo.addItems([t.value for t in GameType])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # 目标平台
        platform_layout = QVBoxLayout()
        platform_label = QLabel("目标平台:")
        self.platform_list = QListWidget()
        self.platform_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for platform in TargetPlatform:
            item = QListWidgetItem(platform.value)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.platform_list.addItem(item)
        platform_layout.addWidget(platform_label)
        platform_layout.addWidget(self.platform_list)
        layout.addLayout(platform_layout)
        
        # 游戏风格
        style_layout = QHBoxLayout()
        style_label = QLabel("游戏风格:")
        self.style_combo = QComboBox()
        self.style_combo.addItems([s.value for s in GameStyle])
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combo)
        layout.addLayout(style_layout)
        
        # 时代背景
        time_layout = QHBoxLayout()
        time_label = QLabel("时代背景:")
        self.time_combo = QComboBox()
        self.time_combo.addItems([t.value for t in TimeSetting])
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_combo)
        layout.addLayout(time_layout)
        
        # 目标受众
        audience_layout = QVBoxLayout()
        audience_label = QLabel("目标受众:")
        self.audience_list = QListWidget()
        self.audience_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for audience in TargetAudience:
            item = QListWidgetItem(audience.value)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.audience_list.addItem(item)
        audience_layout.addWidget(audience_label)
        audience_layout.addWidget(self.audience_list)
        layout.addLayout(audience_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_project_info(self) -> ProjectInfoModel:
        """获取项目信息"""
        # 获取选中的平台
        selected_platforms = []
        for i in range(self.platform_list.count()):
            item = self.platform_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                platform_value = item.text()
                selected_platforms.append(TargetPlatform(platform_value))
        
        # 获取选中的受众
        selected_audiences = []
        for i in range(self.audience_list.count()):
            item = self.audience_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                audience_value = item.text()
                selected_audiences.append(TargetAudience(audience_value))
        
        # 创建项目信息模型
        project_info = ProjectInfoModel(
            name=self.name_edit.text(),
            description=self.desc_edit.toPlainText(),
            game_type=GameType(self.type_combo.currentText()),
            target_platforms=selected_platforms,
            game_style=GameStyle(self.style_combo.currentText()),
            time_setting=TimeSetting(self.time_combo.currentText()),
            target_audience=selected_audiences
        )
        
        return project_info
    
    def validate_input(self) -> bool:
        """验证输入"""
        if not self.name_edit.text():
            QMessageBox.warning(self, "警告", "项目名称不能为空")
            return False
            
        if not any(self.platform_list.item(i).checkState() == Qt.CheckState.Checked 
                  for i in range(self.platform_list.count())):
            QMessageBox.warning(self, "警告", "请至少选择一个目标平台")
            return False
            
        if not any(self.audience_list.item(i).checkState() == Qt.CheckState.Checked 
                  for i in range(self.audience_list.count())):
            QMessageBox.warning(self, "警告", "请至少选择一个目标受众")
            return False
            
        return True
    
    def accept(self):
        """重写accept方法，添加验证"""
        if self.validate_input():
            super().accept()
    
    def setup_styles(self):
        """设置样式"""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 14px;
                padding: 4px 0;
            }
            
            QLineEdit, QTextEdit, QComboBox {
                background-color: #3b3b3b;
                color: #ffffff;
                border: 1px solid #4b4b4b;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
                selection-background-color: #4b4b4b;
                selection-color: #ffffff;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #5b5b5b;
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
                background-color: #3b3b3b;
                color: #ffffff;
                border: 1px solid #4b4b4b;
                selection-background-color: #4b4b4b;
                selection-color: #ffffff;
            }
            
            QListWidget {
                background-color: #3b3b3b;
                color: #ffffff;
                border: 1px solid #4b4b4b;
                border-radius: 4px;
                font-size: 14px;
            }
            
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #4b4b4b;
            }
            
            QListWidget::item:selected {
                background-color: #4b4b4b;
                color: #ffffff;
            }
            
            QListWidget::item:hover {
                background-color: #4b4b4b;
            }
            
            QPushButton {
                background-color: #3b3b3b;
                color: #ffffff;
                border: 1px solid #4b4b4b;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #4b4b3b;
            }
            
            QPushButton:pressed {
                background-color: #5b5b5b;
            }
            
            QPushButton:focus {
                border: 1px solid #5b5b5b;
            }
            
            QScrollBar:vertical {
                border: none;
                background-color: #3b3b3b;
                width: 10px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #4b4b4b;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #5b5b5b;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """) 