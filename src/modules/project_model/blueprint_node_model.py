"""
Blueprint Node Model
蓝图节点模型

This module defines the data models for blueprint nodes, pins, and connections.
此模块定义了蓝图节点、引脚和连接的数据模型。
"""

from enum import Enum
from typing import List, Optional, Dict, Any

class PinType(Enum):
    """引脚类型"""
    EXEC = "exec"  # 执行引脚
    BOOL = "bool"  # 布尔值
    INT = "int"    # 整数值
    FLOAT = "float"  # 浮点值
    STRING = "string"  # 字符串
    OBJECT = "object"  # 对象引用

class PinDirection(Enum):
    """引脚方向"""
    INPUT = "input"  # 输入引脚
    OUTPUT = "output"  # 输出引脚

class BlueprintPin:
    """蓝图引脚"""
    
    def __init__(self, name: str, pin_type: PinType, direction: PinDirection, node: 'BlueprintNode'):
        self.name = name
        self.pin_type = pin_type
        self.direction = direction
        self.node = node
        self.connections: List['BlueprintConnection'] = []
        self.value: Any = None

    def connect_to(self, other_pin: 'BlueprintPin') -> 'BlueprintConnection':
        """连接到另一个引脚"""
        if self.direction == other_pin.direction:
            raise ValueError("Cannot connect pins with same direction")
        
        connection = BlueprintConnection(self, other_pin)
        self.connections.append(connection)
        other_pin.connections.append(connection)
        return connection

    def disconnect(self, connection: 'BlueprintConnection'):
        """断开连接"""
        if connection in self.connections:
            self.connections.remove(connection)
            other_pin = connection.input_pin if self == connection.output_pin else connection.output_pin
            other_pin.connections.remove(connection)

class BlueprintConnection:
    """蓝图连接"""
    
    def __init__(self, input_pin: BlueprintPin, output_pin: BlueprintPin):
        self.input_pin = input_pin
        self.output_pin = output_pin

class BlueprintNode:
    """蓝图节点"""
    
    def __init__(self, name: str, node_type: str):
        self.name = name
        self.node_type = node_type
        self.position = (0, 0)  # (x, y) position
        self.pins: Dict[str, BlueprintPin] = {}
        self.properties: Dict[str, Any] = {}

    def add_pin(self, name: str, pin_type: PinType, direction: PinDirection) -> BlueprintPin:
        """添加引脚"""
        if name in self.pins:
            raise ValueError(f"Pin with name {name} already exists")
        
        pin = BlueprintPin(name, pin_type, direction, self)
        self.pins[name] = pin
        return pin

    def get_pin(self, name: str) -> Optional[BlueprintPin]:
        """获取引脚"""
        return self.pins.get(name)

    def remove_pin(self, name: str):
        """移除引脚"""
        if name in self.pins:
            pin = self.pins[name]
            # 断开所有连接
            for connection in pin.connections[:]:
                pin.disconnect(connection)
            del self.pins[name]

    def set_property(self, name: str, value: Any):
        """设置属性"""
        self.properties[name] = value

    def get_property(self, name: str, default: Any = None) -> Any:
        """获取属性"""
        return self.properties.get(name, default) 