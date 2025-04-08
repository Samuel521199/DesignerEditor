"""
Tree Resources
树形控件资源

This module provides resources for the tree widget.
此模块提供树形控件的资源。
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPen
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt

class TreeResources:
    """树形控件资源类"""
    
    @staticmethod
    def create_branch_icons():
        """创建分支图标"""
        icon_size = 20  # 增加图标大小
        line_width = 3  # 增加线条宽度
        icon_color = Qt.GlobalColor.red  # 使用亮红色
        
        print("创建树形图标...")
        
        # 创建展开图标
        open_icon = QPixmap(icon_size, icon_size)
        open_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(open_icon)
        pen = QPen(icon_color, line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)  # 设置线条端点为圆形
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制减号
        painter.drawLine(4, icon_size//2, icon_size-4, icon_size//2)
        painter.end()
        print("展开图标创建完成")
        
        # 创建折叠图标
        closed_icon = QPixmap(icon_size, icon_size)
        closed_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(closed_icon)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制加号
        center = icon_size//2
        painter.drawLine(4, center, icon_size-4, center)
        painter.drawLine(center, 4, center, icon_size-4)
        painter.end()
        print("折叠图标创建完成")
        
        # 创建更多分支图标
        more_icon = QPixmap(icon_size, icon_size)
        more_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(more_icon)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制垂直线
        painter.drawLine(center, 4, center, icon_size-4)
        painter.end()
        print("更多分支图标创建完成")
        
        # 创建结束分支图标
        end_icon = QPixmap(icon_size, icon_size)
        end_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(end_icon)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制L形线
        painter.drawLine(center, 4, center, center)
        painter.drawLine(center, center, icon_size-4, center)
        painter.end()
        print("结束分支图标创建完成")
        
        icons = {
            'branch-open': QIcon(open_icon),
            'branch-closed': QIcon(closed_icon),
            'branch-more': QIcon(more_icon),
            'branch-end': QIcon(end_icon)
        }
        print("所有图标创建完成")
        return icons 