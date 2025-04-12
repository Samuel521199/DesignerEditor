# 右键节点创建场景面板

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QPushButton, QMenu, QMessageBox, QDockWidget)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from ..project_model.scene_info_model import SceneType, SceneInfoModel

class CreateScenePanel(QDockWidget):
    """创建场景面板"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("创建场景")
        self.setObjectName("CreateScenePanel")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.setFixedSize(300, 200)
        # 创建一个菜单
        self.menu = QMenu()
        
        # 添加菜单项并设置显示文本
        create_action = QAction("创建新场景", self)
        create_action.triggered.connect(self.create_new_scene)
        
        modify_action = QAction("修改场景", self)
        modify_action.triggered.connect(self.modify_scene)
        
        cancel_action = QAction("取消", self)
        cancel_action.triggered.connect(self.cancel)
        
        self.menu.addAction(create_action)
        self.menu.addAction(modify_action)
        self.menu.addSeparator()  # 添加分隔线
        self.menu.addAction(cancel_action)

    def create_new_scene(self):
        """创建新场景"""
        # 创建新场景对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("创建新场景")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # 场景名称输入
        name_layout = QHBoxLayout()
        name_label = QLabel("场景名称:", dialog)
        name_input = QLineEdit(dialog)
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_input)
        
        # 场景类型选择
        type_layout = QHBoxLayout()
        type_label = QLabel("场景类型:", dialog)
        type_combo = QComboBox(dialog)
        for scene_type in SceneType:
            type_combo.addItem(scene_type.value, scene_type)
        type_layout.addWidget(type_label)
        type_layout.addWidget(type_combo)
        
        # 按钮
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定", dialog)
        cancel_button = QPushButton("取消", dialog)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        # 添加所有布局
        layout.addLayout(name_layout)
        layout.addLayout(type_layout)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        # 连接按钮信号
        ok_button.clicked.connect(lambda: self._handle_create_scene(dialog, name_input, type_combo))
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec()

    def _handle_create_scene(self, dialog, name_input, type_combo):
        """处理场景创建"""
        name = name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "场景名称不能为空！")
            return
            
        scene_type = type_combo.currentData()
        scene_info = SceneInfoModel(name=name, scene_type=scene_type)
        
        if scene_info.validate():
            # TODO: 将场景信息添加到项目中
            dialog.accept()
            QMessageBox.information(self, "成功", f"场景 '{name}' 创建成功！")
        else:
            QMessageBox.warning(self, "错误", "场景信息验证失败！")

    def modify_scene(self):
        """修改场景"""
        # TODO: 实现场景修改功能
        QMessageBox.information(self, "提示", "场景修改功能正在开发中...")

    def cancel(self):
        """取消"""
        self.close()
