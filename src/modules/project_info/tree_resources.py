"""
Tree Resources
树形控件资源

This module provides resources for the tree widget.
此模块提供树形控件的资源。
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt

class TreeResources:
    """树形控件资源类"""
    
    @staticmethod
    def create_branch_icons():
        """创建分支图标"""
        icon_size = 20  # 图标大小
        line_width = 1  # 线条宽度
        icon_color = Qt.GlobalColor.white  # 使用白色
        margin = 4  # 边距
        
        print("创建树形图标...")
        
        # 创建展开图标（减号）
        open_icon = QPixmap(icon_size, icon_size)
        open_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(open_icon)
        pen = QPen(icon_color, line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制减号和连接线
        center = icon_size // 2
        # 绘制减号
        painter.drawLine(margin, center, icon_size - margin, center)  # 横线
        # 绘制连接线
        painter.drawLine(0, center, margin, center)  # 左侧连接线
        painter.drawLine(center, 0, center, icon_size)  # 竖线
        painter.end()
        print("展开图标创建完成")
        
        # 创建折叠图标（加号）
        closed_icon = QPixmap(icon_size, icon_size)
        closed_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(closed_icon)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制加号和连接线
        painter.drawLine(margin, center, icon_size - margin, center)  # 横线
        painter.drawLine(center, margin, center, icon_size - margin)  # 竖线（加号的竖线）
        painter.drawLine(0, center, margin, center)  # 左侧连接线
        painter.drawLine(center, 0, center, icon_size)  # 竖线
        painter.end()
        print("折叠图标创建完成")
        
        # 创建更多分支图标（T形连接线）
        more_icon = QPixmap(icon_size, icon_size)
        more_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(more_icon)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制T形连接线
        painter.drawLine(0, center, icon_size, center)  # 横线
        painter.drawLine(center, 0, center, icon_size)  # 竖线
        painter.end()
        print("更多分支图标创建完成")
        
        # 创建结束分支图标（L形线）
        end_icon = QPixmap(icon_size, icon_size)
        end_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(end_icon)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制L形线
        painter.drawLine(0, center, icon_size - margin, center)  # 横线
        painter.drawLine(center, 0, center, center)  # 上半部分竖线
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
    
    @staticmethod
    def get_folder_icon():
        """获取文件夹图标"""
        icon = QIcon()
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        pen = QPen(Qt.GlobalColor.white, 1)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制文件夹图标（更现代的设计）
        painter.drawLine(3, 5, 7, 5)      # 顶部小突出
        painter.drawLine(7, 5, 8, 7)      # 斜线连接
        painter.drawLine(8, 7, 17, 7)     # 顶部主线
        painter.drawLine(3, 5, 3, 15)     # 左边
        painter.drawLine(17, 7, 17, 15)   # 右边
        painter.drawLine(3, 15, 17, 15)   # 底部
        
        painter.end()
        icon.addPixmap(pixmap)
        return icon
        
    @staticmethod
    def get_folder_open_icon():
        """获取打开的文件夹图标"""
        icon = QIcon()
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        pen = QPen(Qt.GlobalColor.white, 1)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制打开的文件夹图标（带透视效果）
        painter.drawLine(3, 5, 7, 5)      # 顶部小突出
        painter.drawLine(7, 5, 8, 7)      # 斜线连接
        painter.drawLine(8, 7, 17, 7)     # 顶部主线
        painter.drawLine(3, 5, 3, 15)     # 左边
        painter.drawLine(3, 15, 15, 15)   # 底部（缩短）
        painter.drawLine(17, 7, 15, 15)   # 右边（斜线）
        painter.drawLine(5, 11, 17, 11)   # 中间装饰线
        
        painter.end()
        icon.addPixmap(pixmap)
        return icon
        
    @staticmethod
    def get_info_icon():
        """获取信息图标"""
        icon = QIcon()
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        pen = QPen(Qt.GlobalColor.white, 1)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制信息图标（文档样式）
        # 绘制主体矩形
        painter.drawLine(6, 5, 14, 5)   # 顶部
        painter.drawLine(6, 5, 6, 15)   # 左边
        painter.drawLine(14, 5, 14, 15) # 右边
        painter.drawLine(6, 15, 14, 15) # 底部
        
        # 绘制内部线条（模拟文本）
        painter.drawLine(8, 8, 12, 8)   # 第一行
        painter.drawLine(8, 10, 12, 10) # 第二行
        painter.drawLine(8, 12, 10, 12) # 第三行（较短）
        
        painter.end()
        icon.addPixmap(pixmap)
        return icon
        
    @staticmethod
    def get_scene_icon():
        """获取场景图标"""
        icon = QIcon()
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        pen = QPen(Qt.GlobalColor.white, 1)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制场景图标（电影场景样式）
        painter.drawRect(4, 6, 12, 8)     # 外框
        painter.drawLine(2, 4, 18, 4)     # 顶部装饰
        painter.drawLine(2, 16, 18, 16)   # 底部装饰
        painter.drawLine(4, 10, 16, 10)   # 中间分隔线
        
        painter.end()
        icon.addPixmap(pixmap)
        return icon 