"""
Scene View
场景视图

This module provides the scene view implementation.
此模块提供场景视图的实现。
"""

from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush

class SceneView(QGraphicsView):
    """Scene view class."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setup_view()
        
    def setup_view(self):
        """Set up the view."""
        # 启用抗锯齿
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 设置视图更新模式
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        
        # 设置滚动条策略
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
        # 设置背景色
        self.setBackgroundBrush(QBrush(QColor("#1e1e1e")))
        
        # 设置拖拽模式
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
        # 设置变换属性
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
    def draw_grid(self, size: int = 20):
        """Draw grid lines."""
        # 清除现有网格
        self.scene.clear()
        
        # 获取视图大小
        rect = self.viewport().rect()
        scene_rect = QRectF(
            -rect.width() // 2,
            -rect.height() // 2,
            rect.width(),
            rect.height()
        )
        self.scene.setSceneRect(scene_rect)
        
        # 设置网格画笔
        pen = QPen(QColor("#2d2d2d"))
        pen.setWidth(1)
        
        # 绘制垂直线
        x = scene_rect.left() - (scene_rect.left() % size)
        while x < scene_rect.right():
            self.scene.addLine(x, scene_rect.top(), x, scene_rect.bottom(), pen)
            x += size
            
        # 绘制水平线
        y = scene_rect.top() - (scene_rect.top() % size)
        while y < scene_rect.bottom():
            self.scene.addLine(scene_rect.left(), y, scene_rect.right(), y, pen)
            y += size
            
    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # 计算缩放因子
            factor = 1.2 if event.angleDelta().y() > 0 else 1 / 1.2
            
            # 应用缩放
            self.scale(factor, factor)
            
            # 更新网格
            self.draw_grid()
        else:
            super().wheelEvent(event)
            
    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        self.draw_grid()
        
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.MiddleButton:
            # 启用平移模式
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            # 模拟左键按下以开始拖动
            fake_event = event
            fake_event.setButton(Qt.MouseButton.LeftButton)
            super().mousePressEvent(fake_event)
        else:
            super().mousePressEvent(event)
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        if event.button() == Qt.MouseButton.MiddleButton:
            # 恢复选择模式
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            # 模拟左键释放以结束拖动
            fake_event = event
            fake_event.setButton(Qt.MouseButton.LeftButton)
            super().mouseReleaseEvent(fake_event)
        else:
            super().mouseReleaseEvent(event)
            
    def get_scene_pos(self, view_pos) -> QPointF:
        """Convert view coordinates to scene coordinates."""
        return self.mapToScene(view_pos) 