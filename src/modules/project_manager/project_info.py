"""
Project Info Widget
项目信息小部件

This module provides the project information widget implementation.
此模块提供项目信息小部件的实现。
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt

class ProjectInfoWidget(QWidget):
    """Project information widget class."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # 标题标签
        self.title_label = QLabel("项目信息")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                padding: 4px;
            }
        """)
        layout.addWidget(self.title_label)
        
        # 信息编辑器
        self.info_edit = QTextEdit()
        self.info_edit.setReadOnly(True)
        self.info_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.info_edit)
    
    def update_info(self, project_data: dict):
        """Update project information display."""
        if not project_data:
            self.info_edit.clear()
            return
            
        info_text = f"""项目名称：{project_data.get('name', '')}
项目类型：{project_data.get('game_type', '')}
目标平台：{project_data.get('target_platform', '')}
游戏风格：{project_data.get('game_style', '')}

目标受众：{', '.join(project_data.get('target_audience', []))}

核心机制：
{chr(10).join('- ' + m for m in project_data.get('core_mechanics', []))}

游戏特色：
{chr(10).join('- ' + f for f in project_data.get('game_features', []))}

项目描述：
{project_data.get('description', '')}
"""
        self.info_edit.setPlainText(info_text) 