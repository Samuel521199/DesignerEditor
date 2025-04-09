"""
Scene Editor API
场景编辑器API接口

This module provides the API interface for scene editing functionality.
此模块提供场景编辑功能的API接口。
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import os
from PyQt6.QtWidgets import QDockWidget
from .scene_editor_panel import SceneEditorPanel

class NodeType(Enum):
    """Scene node type enumeration."""
    CONTAINER = "容器"
    SPRITE = "精灵"
    TEXT = "文本"
    BUTTON = "按钮"
    INPUT = "输入框"
    CUSTOM = "自定义"

@dataclass
class SceneNode:
    """Scene node data class."""
    id: str
    name: str
    node_type: NodeType
    position: tuple[float, float] = (0.0, 0.0)
    size: tuple[float, float] = (100.0, 100.0)
    properties: Dict[str, Any] = field(default_factory=dict)
    children: List['SceneNode'] = field(default_factory=list)

@dataclass
class Scene:
    """Scene data class."""
    name: str
    root_node: SceneNode
    background_color: str = "#1e1e1e"
    grid_size: int = 20
    snap_to_grid: bool = True

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
    """Scene editor API interface class."""
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'SceneEditorAPI':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Initialize the scene editor."""
        if SceneEditorAPI._instance is not None:
            raise Exception("This class is a singleton!")
        SceneEditorAPI._instance = self
        self.current_scene: Optional[Scene] = None
        self.scene_changed_callbacks = []
        self._panel = None
        
    def set_panel(self, panel):
        """Set the scene editor panel."""
        self._panel = panel
        
    def get_panel(self):
        """Get the scene editor panel."""
        return self._panel
        
    def show_panel(self):
        """Show the scene editor panel."""
        if self._panel:
            self._panel.show()
            
    def hide_panel(self):
        """Hide the scene editor panel."""
        if self._panel:
            self._panel.hide()
            
    def is_panel_visible(self) -> bool:
        """Check if the scene editor panel is visible."""
        return self._panel.isVisible() if self._panel else False
        
    def toggle_scene_editor_window(self, is_open: bool = True) -> Optional[bool]:
        """Toggle the visibility of the scene editor window."""
        if self._panel:
            if is_open:
                self.show_panel()
            else:
                self.hide_panel()
            return True
        return None
    
    def create_scene(self, name: str) -> Scene:
        """Create a new scene."""
        root_node = SceneNode(
            id="root",
            name="Root",
            node_type=NodeType.CONTAINER
        )
        scene = Scene(name=name, root_node=root_node)
        self.current_scene = scene
        self._notify_scene_changed()
        return scene
    
    def add_node(self, parent_id: str, node_data: dict) -> SceneNode:
        """Add a new node to the scene."""
        if not self.current_scene:
            raise RuntimeError("No scene is currently open")
            
        node = SceneNode(**node_data)
        parent = self._find_node(self.current_scene.root_node, parent_id)
        if parent:
            parent.children.append(node)
            self._notify_scene_changed()
        return node
    
    def update_node(self, node_id: str, properties: dict) -> bool:
        """Update node properties."""
        if not self.current_scene:
            return False
            
        node = self._find_node(self.current_scene.root_node, node_id)
        if node:
            for key, value in properties.items():
                setattr(node, key, value)
            self._notify_scene_changed()
            return True
        return False
    
    def delete_node(self, node_id: str) -> bool:
        """Delete a node from the scene."""
        if not self.current_scene:
            return False
            
        result = self._delete_node_recursive(
            self.current_scene.root_node,
            node_id
        )
        if result:
            self._notify_scene_changed()
        return result
    
    def register_scene_changed_callback(self, callback):
        """Register a callback for scene changes."""
        self.scene_changed_callbacks.append(callback)
    
    def _notify_scene_changed(self):
        """Notify all registered callbacks about scene changes."""
        for callback in self.scene_changed_callbacks:
            callback()
    
    def _find_node(self, root: SceneNode, node_id: str) -> Optional[SceneNode]:
        """Find a node by its ID."""
        if root.id == node_id:
            return root
        for child in root.children:
            result = self._find_node(child, node_id)
            if result:
                return result
        return None
    
    def _delete_node_recursive(self, root: SceneNode, node_id: str) -> bool:
        """Delete a node recursively."""
        for i, child in enumerate(root.children):
            if child.id == node_id:
                root.children.pop(i)
                return True
            if self._delete_node_recursive(child, node_id):
                return True
        return False
    
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

    @staticmethod
    def create_scene_editor() -> QDockWidget:
        """创建场景编辑器面板"""
        dock = QDockWidget("场景编辑器")
        editor = SceneEditorPanel()
        dock.setWidget(editor)
        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable |
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        return dock 
