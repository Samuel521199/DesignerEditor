"""
Tree Resources
树形控件资源

This module provides resources for the tree widget.
此模块提供树形控件的资源。
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt

class TreeResources:
    """树形控件资源类"""
    
    @staticmethod
    def create_branch_icons():
        """创建分支图标"""
        # 创建展开图标
        open_icon = QPixmap(12, 12)
        open_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(open_icon)
        painter.setPen(Qt.GlobalColor.white)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制减号
        painter.drawLine(2, 6, 10, 6)
        painter.end()
        
        # 创建折叠图标
        closed_icon = QPixmap(12, 12)
        closed_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(closed_icon)
        painter.setPen(Qt.GlobalColor.white)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制加号
        painter.drawLine(2, 6, 10, 6)
        painter.drawLine(6, 2, 6, 10)
        painter.end()
        
        # 创建更多分支图标
        more_icon = QPixmap(12, 12)
        more_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(more_icon)
        painter.setPen(Qt.GlobalColor.white)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制垂直线
        painter.drawLine(6, 2, 6, 10)
        painter.end()
        
        # 创建结束分支图标
        end_icon = QPixmap(12, 12)
        end_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(end_icon)
        painter.setPen(Qt.GlobalColor.white)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制L形线
        painter.drawLine(6, 2, 6, 6)
        painter.drawLine(6, 6, 12, 6)
        painter.end()
        
        return {
            'branch-open': QIcon(open_icon),
            'branch-closed': QIcon(closed_icon),
            'branch-more': QIcon(more_icon),
            'branch-end': QIcon(end_icon)
        } 