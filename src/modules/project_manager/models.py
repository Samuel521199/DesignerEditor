"""
Project Manager Models
项目管理数据模型

This module provides data models for project management.
此模块提供项目管理的数据模型。
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime

class DesignType(Enum):
    """Design type enumeration."""
    GAMEPLAY = "玩法设计"
    LEVEL = "关卡设计"
    SYSTEM = "系统设计"
    UI = "界面设计"
    STORY = "剧情设计"
    ECONOMY = "经济设计"

@dataclass
class DesignStep:
    """Design step data class."""
    name: str
    design_type: DesignType
    description: str
    priority: int = 0
    status: str = "未开始"
    estimated_time: float = 0.0
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class GameProject:
    """Game project data class."""
    name: str
    description: str
    game_type: str
    target_platform: str
    target_audience: List[str]
    game_style: str
    core_mechanics: List[str]
    game_features: List[str] = field(default_factory=list)
    design_steps: List[DesignStep] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def get_structure(self) -> List[Dict[str, Any]]:
        """Get project structure as a tree."""
        structure = []
        
        # 基本信息
        info = {
            "name": "项目信息",
            "type": "folder",
            "children": [
                {"name": f"名称: {self.name}", "type": "info"},
                {"name": f"类型: {self.game_type}", "type": "info"},
                {"name": f"平台: {self.target_platform}", "type": "info"},
                {"name": f"风格: {self.game_style}", "type": "info"}
            ]
        }
        structure.append(info)
        
        # 设计步骤
        steps = {
            "name": "设计步骤",
            "type": "folder",
            "children": []
        }
        for step in self.design_steps:
            steps["children"].append({
                "name": step.name,
                "type": "step",
                "data": step
            })
        structure.append(steps)
        
        return structure 