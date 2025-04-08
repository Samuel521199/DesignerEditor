"""
Project Info Model
项目信息模型模块

This module defines the project info model class that stores and manages project information.
此模块定义用于存储和管理项目信息的项目信息模型类。
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List

class GameType(Enum):
    """游戏类型枚举"""
    ACTION = "动作游戏"
    ADVENTURE = "冒险游戏"
    RPG = "角色扮演"
    STRATEGY = "策略游戏"
    SIMULATION = "模拟游戏"
    PUZZLE = "解谜游戏"
    SPORTS = "体育游戏"
    RACING = "竞速游戏"
    SHOOTER = "射击游戏"
    FIGHTING = "格斗游戏"
    OTHER = "其他类型"

class TargetPlatform(Enum):
    """目标平台枚举"""
    PC = "PC"
    MOBILE = "移动设备"
    CONSOLE = "游戏主机"
    WEB = "网页游戏"
    VR = "虚拟现实"
    AR = "增强现实"

class GameStyle(Enum):
    """游戏风格枚举"""
    REALISTIC = "写实风格"
    CARTOON = "卡通风格"
    PIXEL = "像素风格"
    ANIME = "动漫风格"
    LOW_POLY = "低多边形"
    HAND_DRAWN = "手绘风格"
    RETRO = "复古风格"
    ABSTRACT = "抽象风格"

class TimeSetting(Enum):
    """时代背景枚举"""
    PREHISTORIC = "史前时代"
    ANCIENT = "古代"
    MEDIEVAL = "中世纪"
    RENAISSANCE = "文艺复兴"
    INDUSTRIAL = "工业时代"
    MODERN = "现代"
    FUTURE = "未来"
    FANTASY = "奇幻世界"
    SCI_FI = "科幻世界"
    ALTERNATE = "平行世界"

class TargetAudience(Enum):
    """目标受众枚举"""
    CHILDREN = "儿童"
    TEENAGERS = "青少年"
    ADULTS = "成年人"
    FAMILY = "家庭"
    CASUAL = "休闲玩家"
    HARDCORE = "硬核玩家"
    PROFESSIONAL = "专业玩家"

@dataclass
class ProjectInfoModel:
    """项目信息模型类"""
    # 必填字段
    name: str
    
    # 可选字段
    description: Optional[str] = None
    game_type: Optional[GameType] = None
    target_platforms: List[TargetPlatform] = field(default_factory=list)
    game_style: Optional[GameStyle] = None
    time_setting: Optional[TimeSetting] = None
    target_audience: Optional[TargetAudience] = None
    
    def to_dict(self) -> dict:
        """将项目信息模型转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "game_type": self.game_type.value if self.game_type else None,
            "target_platforms": [platform.value for platform in self.target_platforms],
            "game_style": self.game_style.value if self.game_style else None,
            "time_setting": self.time_setting.value if self.time_setting else None,
            "target_audience": self.target_audience.value if self.target_audience else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectInfoModel':
        """从字典创建项目信息模型"""
        project = cls(name=data["name"])
        
        if "description" in data:
            project.description = data["description"]
            
        if "game_type" in data:
            project.game_type = GameType(data["game_type"])
            
        if "target_platforms" in data:
            project.target_platforms = [TargetPlatform(platform) for platform in data["target_platforms"]]
            
        if "game_style" in data:
            project.game_style = GameStyle(data["game_style"])
            
        if "time_setting" in data:
            project.time_setting = TimeSetting(data["time_setting"])
            
        if "target_audience" in data:
            project.target_audience = TargetAudience(data["target_audience"])
            
        return project
    
    def validate(self) -> bool:
        """验证项目信息模型的有效性"""
        if not self.name:
            return False
            
        if self.game_type and not isinstance(self.game_type, GameType):
            return False
            
        if not all(isinstance(platform, TargetPlatform) for platform in self.target_platforms):
            return False
            
        if self.game_style and not isinstance(self.game_style, GameStyle):
            return False
            
        if self.time_setting and not isinstance(self.time_setting, TimeSetting):
            return False
            
        if self.target_audience and not isinstance(self.target_audience, TargetAudience):
            return False
            
        return True 