"""蓝图编辑器"""
from PyQt6.QtWidgets import (QGraphicsScene, QGraphicsItem, QMenu, QGraphicsLineItem)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath

from ..project_model.blueprint_node_model import (
    BlueprintNode, BlueprintPin, BlueprintConnection,
    PinType, PinDirection
)

class BlueprintPinItem(QGraphicsItem):
    """蓝图引脚图形项"""
    
    def __init__(self, pin: BlueprintPin, parent=None):
        super().__init__(parent)
        self.pin = pin
        self.radius = 5
        self.setAcceptHoverEvents(True)
        self.hovered = False
        
    def boundingRect(self) -> QRectF:
        """返回引脚边界矩形"""
        return QRectF(-self.radius, -self.radius, 
                     self.radius * 2, self.radius * 2)
        
    def paint(self, painter: QPainter, option, widget=None):
        """绘制引脚"""
        pin_colors = {
            PinType.EXEC: "#00ff00",
            PinType.BOOL: "#ff0000",
            PinType.INT: "#0000ff",
            PinType.FLOAT: "#00ffff",
            PinType.STRING: "#ffff00",
            PinType.OBJECT: "#8000ff",
        }
        
        pin_color = QColor(pin_colors.get(self.pin.pin_type, "#ffffff"))
        if self.hovered:
            pin_color = pin_color.lighter()
            
        painter.setBrush(QBrush(pin_color))
        painter.setPen(QPen(pin_color.lighter(), 1))
        painter.drawEllipse(self.boundingRect())
        
    def hoverEnterEvent(self, event):
        """鼠标进入事件"""
        self.hovered = True
        self.update()
        super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        """鼠标离开事件"""
        self.hovered = False
        self.update()
        super().hoverLeaveEvent(event)

class BlueprintNodeItem(QGraphicsItem):
    """蓝图节点图形项"""
    
    def __init__(self, node: BlueprintNode, parent=None):
        super().__init__(parent)
        self.node = node
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        
        # 节点样式
        self.title_height = 30
        self.pin_height = 20
        self.pin_spacing = 5
        self.node_width = 200
        self.node_padding = 10
        
        # 计算节点高度
        total_pins = max(len(self.node.pins), 1)
        self.node_height = (self.title_height + 
                          (total_pins * self.pin_height) +
                          (total_pins + 1) * self.pin_spacing)
        
        # 设置节点位置
        self.setPos(self.node.position[0], self.node.position[1])
        
        # 创建引脚图形项
        self.pin_items = {}
        self._create_pin_items()
        
    def _create_pin_items(self):
        """创建引脚图形项"""
        y = self.title_height + self.pin_spacing
        for pin_name, pin in self.node.pins.items():
            pin_item = BlueprintPinItem(pin, self)
            if pin.direction == PinDirection.INPUT:
                pin_item.setPos(0, y + self.pin_height/2)
            else:
                pin_item.setPos(self.node_width, y + self.pin_height/2)
            self.pin_items[pin_name] = pin_item
            y += self.pin_height + self.pin_spacing
        
    def boundingRect(self) -> QRectF:
        """返回节点边界矩形"""
        return QRectF(0, 0, self.node_width, self.node_height)
        
    def paint(self, painter: QPainter, option, widget=None):
        """绘制节点"""
        # 绘制节点背景
        painter.setBrush(QBrush(QColor("#2b2b2b")))
        painter.setPen(QPen(QColor("#3b3b3b"), 2))
        painter.drawRoundedRect(self.boundingRect(), 10, 10)
        
        # 绘制标题背景
        title_rect = QRectF(0, 0, self.node_width, self.title_height)
        painter.setBrush(QBrush(QColor("#3b3b3b")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(title_rect, 10, 10)
        
        # 绘制标题
        painter.setPen(QPen(QColor("#ffffff")))
        painter.drawText(QRectF(10, 0, self.node_width - 20, self.title_height),
                        Qt.AlignmentFlag.AlignCenter,
                        self.node.name)
        
        # 绘制引脚标签
        y = self.title_height + self.pin_spacing
        for pin_name, pin in self.node.pins.items():
            if pin.direction == PinDirection.INPUT:
                painter.drawText(QRectF(15, y, self.node_width - 30, self.pin_height),
                               Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                               pin.name)
            else:
                painter.drawText(QRectF(15, y, self.node_width - 30, self.pin_height),
                               Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                               pin.name)
            y += self.pin_height + self.pin_spacing

class BlueprintConnectionItem(QGraphicsItem):
    """蓝图连接线图形项"""
    
    def __init__(self, connection: BlueprintConnection, parent=None):
        super().__init__(parent)
        self.connection = connection
        self.setZValue(-1)  # 确保连接线在节点下方
        self.start_pos = QPointF(0, 0)
        self.end_pos = QPointF(0, 0)
        self.update_positions()
        
    def update_positions(self):
        """更新连接线的起点和终点位置"""
        # 获取起点和终点引脚的位置
        scene = self.scene()
        if not scene:
            return
            
        # 遍历场景中的所有节点项
        for item in scene.items():
            if isinstance(item, BlueprintNodeItem):
                # 检查输出引脚
                for pin_name, pin_item in item.pin_items.items():
                    if pin_name == self.connection.output_pin.name:
                        self.start_pos = pin_item.mapToScene(
                            pin_item.boundingRect().center()
                        )
                # 检查输入引脚
                for pin_name, pin_item in item.pin_items.items():
                    if pin_name == self.connection.input_pin.name:
                        self.end_pos = pin_item.mapToScene(
                            pin_item.boundingRect().center()
                        )
        
    def boundingRect(self) -> QRectF:
        """返回连接线边界矩形"""
        return QRectF(
            min(self.start_pos.x(), self.end_pos.x()) - 5,
            min(self.start_pos.y(), self.end_pos.y()) - 5,
            abs(self.end_pos.x() - self.start_pos.x()) + 10,
            abs(self.end_pos.y() - self.start_pos.y()) + 10
        )
        
    def paint(self, painter: QPainter, option, widget=None):
        """绘制连接线"""
        # 更新位置
        self.update_positions()
        
        # 创建路径
        path = QPainterPath()
        path.moveTo(self.start_pos)
        
        # 计算贝塞尔曲线的控制点
        ctrl1 = QPointF(self.start_pos.x() + 50, self.start_pos.y())
        ctrl2 = QPointF(self.end_pos.x() - 50, self.end_pos.y())
        
        path.cubicTo(ctrl1, ctrl2, self.end_pos)
        
        # 绘制路径
        painter.setPen(QPen(QColor("#4b4b4b"), 2))
        painter.drawPath(path)

class BlueprintEditor(QGraphicsScene):
    """蓝图编辑器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nodes = {}  # 存储节点项
        self.connections = {}  # 存储连接项
        
        # 网格设置
        self.grid_size = 20
        self.grid_color = QColor("#2a2a2a")  # 普通网格线颜色
        self.major_grid_color = QColor("#3a3a3a")  # 主网格线颜色
        self.major_grid_interval = 5  # 每5个格子显示主网格线
        
        # 设置背景颜色
        self.setBackgroundBrush(QBrush(QColor("#1a1a1a")))  # 背景色
        
        # 连线相关
        self.temp_connection = None  # 临时连线
        self.start_pin = None  # 起始引脚
        self.end_pin = None  # 结束引脚
        
    def drawBackground(self, painter: QPainter, rect: QRectF):
        """绘制背景网格"""
        # 先调用父类方法绘制背景色
        super().drawBackground(painter, rect)
        
        # 获取可见区域
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        right = int(rect.right())
        bottom = int(rect.bottom())
        
        # 绘制网格线
        painter.save()  # 保存当前画笔状态
        
        # 绘制普通网格线
        painter.setPen(QPen(self.grid_color, 1, Qt.PenStyle.SolidLine))
        
        # 绘制垂直线
        for x in range(left, right + 1, self.grid_size):
            if (x // self.grid_size) % self.major_grid_interval != 0:  # 跳过主网格线的位置
                painter.drawLine(int(x), int(rect.top()), int(x), int(rect.bottom()))
        
        # 绘制水平线
        for y in range(top, bottom + 1, self.grid_size):
            if (y // self.grid_size) % self.major_grid_interval != 0:  # 跳过主网格线的位置
                painter.drawLine(int(rect.left()), int(y), int(rect.right()), int(y))
        
        # 绘制主网格线
        painter.setPen(QPen(self.major_grid_color, 1.5, Qt.PenStyle.SolidLine))
        
        # 绘制主垂直线
        for x in range(left, right + 1, self.grid_size * self.major_grid_interval):
            painter.drawLine(int(x), int(rect.top()), int(x), int(rect.bottom()))
        
        # 绘制主水平线
        for y in range(top, bottom + 1, self.grid_size * self.major_grid_interval):
            painter.drawLine(int(rect.left()), int(y), int(rect.right()), int(y))
        
        painter.restore()  # 恢复画笔状态
        
    def add_node(self, node: BlueprintNode):
        """添加节点到场景"""
        # 创建节点图形项
        node_item = BlueprintNodeItem(node)
        self.addItem(node_item)
        self.nodes[node.name] = node_item
        return node_item
        
    def add_connection(self, connection: BlueprintConnection):
        """添加连接"""
        connection_item = BlueprintConnectionItem(connection)
        self.addItem(connection_item)
        self.connections[connection] = connection_item
        return connection_item
        
    def remove_node(self, node_name: str):
        """移除节点"""
        if node_name in self.nodes:
            node_item = self.nodes[node_name]
            self.removeItem(node_item)
            del self.nodes[node_name]
            
    def remove_connection(self, connection: BlueprintConnection):
        """移除连接"""
        if connection in self.connections:
            connection_item = self.connections[connection]
            self.removeItem(connection_item)
            del self.connections[connection]
        
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if isinstance(item, BlueprintPinItem):
            self.start_pin = item
            self.temp_connection = QGraphicsLineItem()
            self.temp_connection.setPen(QPen(QColor("#4b4b4b"), 2))
            self.addItem(self.temp_connection)
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.temp_connection and self.start_pin:
            start_pos = self.start_pin.mapToScene(self.start_pin.boundingRect().center())
            self.temp_connection.setLine(start_pos.x(), start_pos.y(),
                                       event.scenePos().x(), event.scenePos().y())
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if self.temp_connection:
            item = self.itemAt(event.scenePos(), self.views()[0].transform())
            if isinstance(item, BlueprintPinItem) and item != self.start_pin:
                # 检查引脚类型和方向是否匹配
                if (self.start_pin.pin.pin_type == item.pin.pin_type and
                    self.start_pin.pin.direction != item.pin.direction):
                    # 创建连接
                    connection = BlueprintConnection(
                        self.start_pin.pin if self.start_pin.pin.direction == PinDirection.OUTPUT else item.pin,
                        self.start_pin.pin if self.start_pin.pin.direction == PinDirection.INPUT else item.pin
                    )
                    self.add_connection(connection)
            
            # 清理临时连线
            self.removeItem(self.temp_connection)
            self.temp_connection = None
            self.start_pin = None
            
        super().mouseReleaseEvent(event) 