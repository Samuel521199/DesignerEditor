"""
Project Tree Widget
项目树小部件

This module provides the project tree widget implementation.
此模块提供项目树小部件的实现。
"""

from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal

class ProjectTreeWidget(QTreeWidget):
    """Project tree widget class."""
    
    item_selected = pyqtSignal(dict)  # 项目项选中信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setHeaderLabel("项目结构")
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #0d47a1;
            }
            QTreeWidget::item:hover {
                background-color: #2d2d2d;
            }
        """)
    
    def setup_connections(self):
        """Set up signal connections."""
        self.itemClicked.connect(self._handle_item_clicked)
    
    def update_tree(self, structure: list):
        """Update tree with new structure."""
        self.clear()
        for item_data in structure:
            self._add_tree_item(None, item_data)
    
    def _add_tree_item(self, parent: QTreeWidgetItem, data: dict):
        """Add a tree item recursively."""
        item = QTreeWidgetItem(parent or self)
        item.setText(0, data["name"])
        item.setData(0, Qt.ItemDataRole.UserRole, data)
        
        if data["type"] == "folder":
            item.setExpanded(True)
            for child in data.get("children", []):
                self._add_tree_item(item, child)
    
    def _handle_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item click event."""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        self.item_selected.emit(data) 