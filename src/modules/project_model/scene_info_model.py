from enum import Enum
from dataclasses import dataclass

class SceneType(Enum):
    """主菜单，游戏场景，对话场景，战斗场景，过场动画，结束场景"""
    MAIN_MENU       = "主菜单"
    GAME_SCENE      = "游戏场景"
    DIALOGUE_SCENE  = "对话场景"
    BATTLE_SCENE    = "战斗场景"
    CUT_SCENE       = "过场动画"
    END_SCENE       = "结束场景"



class SceneOperationContainer:
    """场景操作容器类-基类"""
    def __init__(self, scene_type: SceneType):
        self.scene_type = scene_type

    def set_blueprint(self, blueprint: str):
        """设置蓝图"""
        self.blueprint = blueprint

    def get_blueprint(self) -> str:
        """获取蓝图"""
        return self.blueprint
    
class MainCameraContainer(SceneOperationContainer):
    """主相机容器类"""
    def __init__(self, scene_type: SceneType):
        super().__init__(scene_type)

    def set_blueprint(self, blueprint: str):
        """设置蓝图"""
        self.blueprint = blueprint

    def get_blueprint(self) -> str:
        """获取蓝图"""
        return self.blueprint
    

class GameOperationContainer(SceneOperationContainer):
    """游戏操作容器类"""
    def __init__(self, scene_type: SceneType):
        super().__init__(scene_type)

    def set_blueprint(self, blueprint: str):
        """设置蓝图"""
        self.blueprint = blueprint

    def get_blueprint(self) -> str:
        """获取蓝图"""
        return self.blueprint
    

    
class SceneInfoModel:
    """场景信息模型类"""
    name: str
    # 场景类型包括：主菜单，游戏场景，对话场景，战斗场景，过场动画，结束场景
    scene_type: SceneType

    def to_dict(self) -> dict:
        """将项目信息模型转换为字典"""
        return {
            "name": self.name,
            "scene_type": self.scene_type.name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SceneInfoModel':
        """从字典创建场景信息模型"""
        return cls(name=data["name"], scene_type=SceneType(data["scene_type"]))
    
    def validate(self) -> bool:
        """验证场景信息模型的有效性"""
        if not self.name:
            return False
        if not self.scene_type:
            return False
        return True