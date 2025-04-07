"""
Flow Chart API
流程图API接口

This module provides the API interface for flow chart functionality.
此模块提供流程图功能的API接口。
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

class NodeType(Enum):
    """Flow chart node type enumeration."""
    START = "开始"
    END = "结束"
    PROCESS = "处理"
    DECISION = "判断"
    INPUT = "输入"
    OUTPUT = "输出"
    CUSTOM = "自定义"

@dataclass
class NodeData:
    """Flow chart node data class."""
    id: str = field(default_factory=lambda: str(uuid4()))
    type: NodeType = NodeType.PROCESS
    title: str = ""
    content: str = ""
    position: tuple[float, float] = (0.0, 0.0)
    size: tuple[float, float] = (120.0, 60.0)
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConnectionData:
    """Flow chart connection data class."""
    id: str = field(default_factory=lambda: str(uuid4()))
    source_id: str = ""
    target_id: str = ""
    label: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FlowChart:
    """Flow chart data class."""
    name: str
    nodes: List[NodeData] = field(default_factory=list)
    connections: List[ConnectionData] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)

class FlowChartAPI:
    """Flow chart API interface class."""
    
    def __init__(self):
        self.current_chart: Optional[FlowChart] = None
        self.chart_changed_callbacks = []
    
    def create_chart(self, name: str) -> FlowChart:
        """Create a new flow chart."""
        chart = FlowChart(name=name)
        self.current_chart = chart
        self._notify_chart_changed()
        return chart
    
    def add_node(self, node_type: NodeType, position: tuple[float, float]) -> NodeData:
        """Add a new node to the chart."""
        if not self.current_chart:
            raise RuntimeError("No chart is currently open")
            
        node = NodeData(
            type=node_type,
            title=node_type.value,
            position=position
        )
        self.current_chart.nodes.append(node)
        self._notify_chart_changed()
        return node
    
    def update_node(self, node_id: str, properties: dict) -> bool:
        """Update node properties."""
        if not self.current_chart:
            return False
            
        for node in self.current_chart.nodes:
            if node.id == node_id:
                for key, value in properties.items():
                    setattr(node, key, value)
                self._notify_chart_changed()
                return True
        return False
    
    def delete_node(self, node_id: str) -> bool:
        """Delete a node from the chart."""
        if not self.current_chart:
            return False
            
        # 删除节点
        for i, node in enumerate(self.current_chart.nodes):
            if node.id == node_id:
                self.current_chart.nodes.pop(i)
                # 删除相关连接
                self.current_chart.connections = [
                    conn for conn in self.current_chart.connections
                    if conn.source_id != node_id and conn.target_id != node_id
                ]
                self._notify_chart_changed()
                return True
        return False
    
    def add_connection(self, source_id: str, target_id: str, label: str = "") -> ConnectionData:
        """Add a new connection between nodes."""
        if not self.current_chart:
            raise RuntimeError("No chart is currently open")
            
        # 检查节点是否存在
        source_exists = any(node.id == source_id for node in self.current_chart.nodes)
        target_exists = any(node.id == target_id for node in self.current_chart.nodes)
        
        if not (source_exists and target_exists):
            raise ValueError("Source or target node does not exist")
            
        connection = ConnectionData(
            source_id=source_id,
            target_id=target_id,
            label=label
        )
        self.current_chart.connections.append(connection)
        self._notify_chart_changed()
        return connection
    
    def delete_connection(self, connection_id: str) -> bool:
        """Delete a connection from the chart."""
        if not self.current_chart:
            return False
            
        for i, conn in enumerate(self.current_chart.connections):
            if conn.id == connection_id:
                self.current_chart.connections.pop(i)
                self._notify_chart_changed()
                return True
        return False
    
    def register_chart_changed_callback(self, callback):
        """Register a callback for chart changes."""
        self.chart_changed_callbacks.append(callback)
    
    def _notify_chart_changed(self):
        """Notify all registered callbacks about chart changes."""
        for callback in self.chart_changed_callbacks:
            callback() 