"""场景编辑器模块API"""
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import os

class NodeType(Enum):
    """节点类型枚举"""
    SCENE = "场景"
    CHARACTER = "角色"
    PROP = "道具"
    EVENT = "事件"
    CONDITION = "条件"

@dataclass
class SceneNode:
    """场景节点"""
    name: str
    type: NodeType
    description: str = ""
    properties: Dict[str, str] = None
    children: List['SceneNode'] = None
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
        if self.children is None:
            self.children = []
            
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.type.value,
            "description": self.description,
            "properties": self.properties,
            "children": [child.to_dict() for child in self.children]
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneNode':
        """从字典创建"""
        node = cls(
            name=data["name"],
            type=NodeType(data["type"]),
            description=data.get("description", ""),
            properties=data.get("properties", {})
        )
        node.children = [cls.from_dict(child) for child in data.get("children", [])]
        return node

@dataclass
class Scene:
    """场景"""
    name: str
    description: str = ""
    nodes: List[SceneNode] = None
    
    def __post_init__(self):
        if self.nodes is None:
            self.nodes = []
            
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "nodes": [node.to_dict() for node in self.nodes]
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Scene':
        """从字典创建"""
        scene = cls(
            name=data["name"],
            description=data.get("description", "")
        )
        scene.nodes = [SceneNode.from_dict(node) for node in data.get("nodes", [])]
        return scene

@dataclass
class NodeData:
    """节点数据类"""
    id: str
    type: NodeType
    position: Tuple[float, float]
    properties: Dict[str, str]

@dataclass
class ConnectionData:
    """连接数据类"""
    id: str
    source_node_id: str
    target_node_id: str
    properties: Dict[str, str]

class SceneEditorAPI:
    """场景编辑器模块API接口"""
    
    @staticmethod
    def create_scene(name: str) -> Optional[Scene]:
        """创建新场景"""
        try:
            return Scene(name)
        except Exception as e:
            print(f"创建场景失败: {str(e)}")
            return None
            
    @staticmethod
    def save_scene(scene: Scene) -> bool:
        """保存场景"""
        try:
            # 获取当前项目
            from modules.project_info.api import ProjectInfoAPI
            project = ProjectInfoAPI.get_current_project()
            if not project:
                return False
                
            # 创建场景目录
            scenes_dir = os.path.join(project.project_dir, "scenes")
            os.makedirs(scenes_dir, exist_ok=True)
            
            # 保存场景文件
            scene_file = os.path.join(scenes_dir, f"{scene.name}.json")
            with open(scene_file, "w", encoding="utf-8") as f:
                json.dump(scene.to_dict(), f, ensure_ascii=False, indent=2)
                
            return True
        except Exception as e:
            print(f"保存场景失败: {str(e)}")
            return False
            
    @staticmethod
    def load_scene(name: str) -> Optional[Scene]:
        """加载场景"""
        try:
            # 获取当前项目
            from modules.project_info.api import ProjectInfoAPI
            project = ProjectInfoAPI.get_current_project()
            if not project:
                return None
                
            # 加载场景文件
            scene_file = os.path.join(project.project_dir, "scenes", f"{name}.json")
            if not os.path.exists(scene_file):
                return None
                
            with open(scene_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Scene.from_dict(data)
        except Exception as e:
            print(f"加载场景失败: {str(e)}")
            return None
            
    @staticmethod
    def delete_scene(scene: Scene) -> bool:
        """删除场景"""
        try:
            # 获取当前项目
            from modules.project_info.api import ProjectInfoAPI
            project = ProjectInfoAPI.get_current_project()
            if not project:
                return False
                
            # 删除场景文件
            scene_file = os.path.join(project.project_dir, "scenes", f"{scene.name}.json")
            if os.path.exists(scene_file):
                os.remove(scene_file)
                
            return True
        except Exception as e:
            print(f"删除场景失败: {str(e)}")
            return False
            
    def get_nodes(self) -> List[NodeData]:
        """获取所有节点"""
        raise NotImplementedError
        
    def add_node(self, node_type: NodeType, position: Tuple[float, float]) -> Optional[NodeData]:
        """添加新节点"""
        raise NotImplementedError
        
    def remove_node(self, node_id: str) -> bool:
        """删除节点"""
        raise NotImplementedError
        
    def get_connections(self) -> List[ConnectionData]:
        """获取所有连接"""
        raise NotImplementedError
        
    def add_connection(self, source_id: str, target_id: str) -> Optional[ConnectionData]:
        """添加新连接"""
        raise NotImplementedError
        
    def remove_connection(self, connection_id: str) -> bool:
        """删除连接"""
        raise NotImplementedError
        
    def update_node_position(self, node_id: str, position: Tuple[float, float]) -> bool:
        """更新节点位置"""
        raise NotImplementedError
        
    def update_node_properties(self, node_id: str, properties: Dict[str, str]) -> bool:
        """更新节点属性"""
        raise NotImplementedError 