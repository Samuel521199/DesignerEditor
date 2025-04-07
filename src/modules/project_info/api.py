"""项目信息模块API"""
from enum import Enum
from typing import Optional, List
import json
import os

class GameType(Enum):
    """游戏类型"""
    ACTION = "动作"
    RPG = "角色扮演"
    STRATEGY = "策略"
    SIMULATION = "模拟"
    PUZZLE = "解谜"
    ADVENTURE = "冒险"
    SPORTS = "体育"
    RACING = "竞速"
    SHOOTER = "射击"
    FIGHTING = "格斗"

class GameStyle(Enum):
    """游戏风格"""
    REALISTIC = "写实"
    CARTOON = "卡通"
    PIXEL = "像素"
    LOW_POLY = "低多边形"
    ANIME = "动漫"
    RETRO = "复古"
    ABSTRACT = "抽象"
    MINIMALIST = "极简"

class Platform(Enum):
    """平台"""
    PC = "PC"
    MOBILE = "移动设备"
    CONSOLE = "游戏主机"
    WEB = "网页"
    VR = "虚拟现实"
    AR = "增强现实"

class ProjectConfig:
    """项目配置"""
    def __init__(self, name: str, game_type: GameType, platforms: List[Platform], 
                 game_style: GameStyle, description: str = "", version: str = "1.0.0", 
                 author: str = ""):
        self.name = name
        self.game_type = game_type
        self.platforms = platforms
        self.game_style = game_style
        self.description = description
        self.version = version
        self.author = author
        
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "game_type": self.game_type.value,
            "platforms": [p.value for p in self.platforms],
            "game_style": self.game_style.value,
            "description": self.description,
            "version": self.version,
            "author": self.author
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectConfig':
        """从字典创建"""
        return cls(
            name=data["name"],
            game_type=GameType(data["game_type"]),
            platforms=[Platform(p) for p in data["platforms"]],
            game_style=GameStyle(data["game_style"]),
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            author=data.get("author", "")
        )

class SceneProject:
    """场景项目"""
    def __init__(self):
        self.config: Optional[ProjectConfig] = None
        self.project_dir: str = ""
        
    def save(self) -> bool:
        """保存项目"""
        try:
            if not self.config or not self.project_dir:
                return False
                
            # 创建项目目录
            os.makedirs(self.project_dir, exist_ok=True)
            
            # 保存项目配置
            config_file = os.path.join(self.project_dir, "project.json")
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(self.config.to_dict(), f, ensure_ascii=False, indent=2)
                
            return True
        except Exception as e:
            print(f"保存项目失败: {str(e)}")
            return False
            
    def load(self) -> bool:
        """加载项目"""
        try:
            if not self.project_dir:
                return False
                
            # 加载项目配置
            config_file = os.path.join(self.project_dir, "project.json")
            if not os.path.exists(config_file):
                return False
                
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.config = ProjectConfig.from_dict(data)
                
            return True
        except Exception as e:
            print(f"加载项目失败: {str(e)}")
            return False

class ProjectInfoAPI:
    """项目信息API"""
    
    _current_project: Optional[SceneProject] = None
    
    @classmethod
    def get_current_project(cls) -> Optional[SceneProject]:
        """获取当前项目"""
        return cls._current_project
        
    @classmethod
    def set_current_project(cls, project: SceneProject) -> None:
        """设置当前项目"""
        cls._current_project = project 