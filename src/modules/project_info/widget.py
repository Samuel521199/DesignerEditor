from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget,
                            QTreeWidgetItem, QPushButton, QLabel, QLineEdit,
                            QTextEdit, QComboBox, QSplitter, QFormLayout)
from PyQt6.QtCore import Qt
from typing import Dict, Any

from .api import ProjectInfoAPI, GameType, GameStyle, Platform

class ProjectInfoWidget(QWidget):
    """项目信息窗口组件"""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        # 基本信息区域
        basic_info_group = QWidget()
        basic_layout = QFormLayout()
        
        # 项目名称
        self.name_label = QLabel("项目名称 / Project Name:")
        self.name_edit = QLineEdit()
        basic_layout.addRow(self.name_label, self.name_edit)
        
        # 项目路径
        self.path_label = QLabel("项目路径 / Project Path:")
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        basic_layout.addRow(self.path_label, self.path_edit)
        
        # 项目类型
        self.type_label = QLabel("项目类型 / Project Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "2D游戏 / 2D Game",
            "3D游戏 / 3D Game",
            "AR/VR应用 / AR/VR Application",
            "其他 / Other"
        ])
        basic_layout.addRow(self.type_label, self.type_combo)
        
        # 目标平台
        self.platform_label = QLabel("目标平台 / Target Platform:")
        self.platform_combo = QComboBox()
        self.platform_combo.addItems([
            "PC",
            "移动设备 / Mobile",
            "主机 / Console",
            "Web / Web"
        ])
        basic_layout.addRow(self.platform_label, self.platform_combo)
        
        basic_info_group.setLayout(basic_layout)
        layout.addWidget(basic_info_group)
        
        # 项目描述
        self.desc_label = QLabel("项目描述 / Project Description:")
        self.desc_edit = QTextEdit()
        layout.addWidget(self.desc_label)
        layout.addWidget(self.desc_edit)
        
        # 项目设置
        settings_group = QWidget()
        settings_layout = QFormLayout()
        
        # 版本控制
        self.vcs_label = QLabel("版本控制 / Version Control:")
        self.vcs_combo = QComboBox()
        self.vcs_combo.addItems([
            "Git",
            "SVN",
            "无 / None"
        ])
        settings_layout.addRow(self.vcs_label, self.vcs_combo)
        
        # 构建设置
        self.build_label = QLabel("构建设置 / Build Settings:")
        self.build_combo = QComboBox()
        self.build_combo.addItems([
            "开发 / Development",
            "测试 / Testing",
            "发布 / Release"
        ])
        settings_layout.addRow(self.build_label, self.build_combo)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存 / Save")
        self.reset_button = QPushButton("重置 / Reset")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def get_project_info(self) -> Dict[str, Any]:
        """获取项目信息"""
        return {
            "name": self.name_edit.text(),
            "path": self.path_edit.text(),
            "type": self.type_combo.currentText().split(" / ")[0],
            "platform": self.platform_combo.currentText().split(" / ")[0],
            "description": self.desc_edit.toPlainText(),
            "vcs": self.vcs_combo.currentText().split(" / ")[0],
            "build": self.build_combo.currentText().split(" / ")[0]
        }
        
    def set_project_info(self, info: Dict[str, Any]):
        """设置项目信息"""
        self.name_edit.setText(info.get("name", ""))
        self.path_edit.setText(info.get("path", ""))
        self.desc_edit.setPlainText(info.get("description", ""))
        
        # 设置下拉框选项
        type_index = self.type_combo.findText(info.get("type", "") + " / ")
        if type_index >= 0:
            self.type_combo.setCurrentIndex(type_index)
            
        platform_index = self.platform_combo.findText(info.get("platform", "") + " / ")
        if platform_index >= 0:
            self.platform_combo.setCurrentIndex(platform_index)
            
        vcs_index = self.vcs_combo.findText(info.get("vcs", "") + " / ")
        if vcs_index >= 0:
            self.vcs_combo.setCurrentIndex(vcs_index)
            
        build_index = self.build_combo.findText(info.get("build", "") + " / ")
        if build_index >= 0:
            self.build_combo.setCurrentIndex(build_index)
        
    def load_project(self, project):
        """加载项目信息"""
        if not project:
            return
            
        self.name_edit.setText(project.config.name)
        self.type_combo.setCurrentText(project.config.game_type.name)
        self.platform_combo.setCurrentText(project.config.platforms[0].name)
        self.desc_edit.setText(project.config.description)
        self.path_edit.setText(project.config.path)
        self.vcs_combo.setCurrentText(project.config.vcs)
        self.build_combo.setCurrentText(project.config.build)
        
    def _on_save(self):
        """保存项目信息"""
        try:
            # 获取当前值
            name = self.name_edit.text()
            game_type = GameType[self.type_combo.currentText()]
            platform = Platform[self.platform_combo.currentText()]
            description = self.desc_edit.toPlainText()
            path = self.path_edit.text()
            vcs = self.vcs_combo.currentText()
            build = self.build_combo.currentText()
            
            # 更新项目配置
            project = ProjectInfoAPI.get_current_project()
            if project:
                project.config.name = name
                project.config.game_type = game_type
                project.config.platforms = [platform]
                project.config.description = description
                project.config.path = path
                project.config.vcs = vcs
                project.config.build = build
                
                # 保存项目
                if project.save():
                    self.project_saved.emit()
                else:
                    self.error_occurred.emit("保存项目失败")
            else:
                self.error_occurred.emit("没有当前项目")
                
        except Exception as e:
            self.error_occurred.emit(f"保存项目时出错: {str(e)}") 