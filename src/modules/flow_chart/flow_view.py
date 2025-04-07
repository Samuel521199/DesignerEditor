"""
Flow Chart View
流程图视图

This module provides the flow chart view implementation.
此模块提供流程图视图的实现。
"""

from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem,
                           QGraphicsRectItem, QGraphicsTextItem)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath

from .api import NodeType, NodeData, ConnectionData

class FlowChartNode(QGraphicsRectItem):
    """Flow chart node item class."""
    
    def __init__(self, node_data: NodeData):
        super().__init__()
        self.node_data = node_data
        self.setup_node()
        
    def setup_node(self):
        """Set up the node appearance."""
        # 设置位置和大小
        self.setPos(*self.node_data.position)
        self.setRect(0, 0, *self.node_data.size)
        
        # 设置外观
        self.setPen(QPen(QColor("#4d4d4d"), 2))
        self.setBrush(QBrush(QColor("#2d2d2d")))
        
        # 设置标志
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # 添加标题文本
        title = QGraphicsTextItem(self.node_data.title, self)
        title.setDefaultTextColor(QColor("#ffffff"))
        # 居中显示标题
        title_rect = title.boundingRect()
        title.setPos(
            (self.rect().width() - title_rect.width()) / 2,
            (self.rect().height() - title_rect.height()) / 2
        )

class FlowChartConnection(QGraphicsItem):
    """Flow chart connection item class."""
    
    def __init__(self, connection_data: ConnectionData,
                 source_node: FlowChartNode,
                 target_node: FlowChartNode):
        super().__init__()
        self.connection_data = connection_data
        self.source_node = source_node
        self.target_node = target_node
        self.setup_connection()
        
    def setup_connection(self):
        """Set up the connection appearance."""
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(-1)  # 确保连接线在节点下方
        
    def boundingRect(self) -> QRectF:
        """Get the bounding rectangle."""
        source_pos = self.source_node.pos()
        target_pos = self.target_node.pos()
        return QRectF(
            min(source_pos.x(), target_pos.x()),
            min(source_pos.y(), target_pos.y()),
            abs(target_pos.x() - source_pos.x()),
            abs(target_pos.y() - source_pos.y())
        ).adjusted(-10, -10, 10, 10)
        
    def paint(self, painter: QPainter,
              option: 'QStyleOptionGraphicsItem',
              widget: QWidget = None):
        """Paint the connection."""
        # 设置画笔
        painter.setPen(QPen(QColor("#4d4d4d"), 2))
        
        # 获取源节点和目标节点的中心点
        source_rect = self.source_node.rect()
        target_rect = self.target_node.rect()
        source_center = self.source_node.pos() + QPointF(
            source_rect.width() / 2,
            source_rect.height() / 2
        )
        target_center = self.target_node.pos() + QPointF(
            target_rect.width() / 2,
            target_rect.height() / 2
        )
        
        # 创建贝塞尔曲线路径
        path = QPainterPath()
        path.moveTo(source_center)
        
        # 计算控制点
        control1 = QPointF(
            source_center.x() + (target_center.x() - source_center.x()) / 3,
            source_center.y()
        )
        control2 = QPointF(
            source_center.x() + 2 * (target_center.x() - source_center.x()) / 3,
            target_center.y()
        )
        
        # 绘制曲线
        path.cubicTo(control1, control2, target_center)
        painter.drawPath(path)
        
        # 如果有标签，绘制标签
        if self.connection_data.label:
            painter.drawText(
                (source_center + target_center) / 2,
                self.connection_data.label
            )

class FlowChartView(QGraphicsView):
    """Flow chart view class."""
    
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
        
    def add_node(self, node_data: NodeData) -> FlowChartNode:
        """Add a node to the view."""
        node = FlowChartNode(node_data)
        self.scene.addItem(node)
        return node
        
    def add_connection(self, connection_data: ConnectionData,
                      source_node: FlowChartNode,
                      target_node: FlowChartNode) -> FlowChartConnection:
        """Add a connection to the view."""
        connection = FlowChartConnection(
            connection_data,
            source_node,
            target_node
        )
        self.scene.addItem(connection)
        return connection
        
    def clear_chart(self):
        """Clear all items from the chart."""
        self.scene.clear()
        
    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # 计算缩放因子
            factor = 1.2 if event.angleDelta().y() > 0 else 1 / 1.2
            
            # 应用缩放
            self.scale(factor, factor)
        else:
            super().wheelEvent(event)
            
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