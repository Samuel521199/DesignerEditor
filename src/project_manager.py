import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class DesignType(Enum):
    GAME_OVERVIEW = "游戏概述"
    GAME_MECHANICS = "游戏机制"
    LEVEL_DESIGN = "关卡设计"
    CHARACTER_DESIGN = "角色设计"
    SYSTEM_DESIGN = "系统设计"
    CONTENT_DESIGN = "内容设计"
    TECHNICAL_SPEC = "技术需求"

class DesignStep:
    def __init__(self, name: str, design_type: DesignType, description: str = "", 
                 details: Dict[str, Any] = None, is_generated: bool = False):
        self.name = name
        self.design_type = design_type
        self.description = description
        self.details = details or {}
        self.is_generated = is_generated
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.dependencies: List[str] = []  # 依赖的其他步骤
        self.tags: List[str] = []  # 标签，用于分类和搜索
        self.priority: int = 0  # 优先级
        self.status: str = "未开始"  # 状态：未开始/进行中/已完成
        self.estimated_time: int = 0  # 预计完成时间（小时）
        self.actual_time: int = 0  # 实际完成时间（小时）
        self.notes: str = ""  # 备注

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "design_type": self.design_type.value,
            "description": self.description,
            "details": self.details,
            "is_generated": self.is_generated,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "dependencies": self.dependencies,
            "tags": self.tags,
            "priority": self.priority,
            "status": self.status,
            "estimated_time": self.estimated_time,
            "actual_time": self.actual_time,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DesignStep':
        step = cls(
            name=data["name"],
            design_type=DesignType(data["design_type"]),
            description=data.get("description", ""),
            details=data.get("details", {}),
            is_generated=data.get("is_generated", False)
        )
        step.created_at = datetime.fromisoformat(data["created_at"])
        step.updated_at = datetime.fromisoformat(data["updated_at"])
        step.dependencies = data.get("dependencies", [])
        step.tags = data.get("tags", [])
        step.priority = data.get("priority", 0)
        step.status = data.get("status", "未开始")
        step.estimated_time = data.get("estimated_time", 0)
        step.actual_time = data.get("actual_time", 0)
        step.notes = data.get("notes", "")
        return step

class GameProject:
    def __init__(self, name: str, description: str = "", game_type: str = ""):
        self.name = name
        self.description = description
        self.game_type = game_type
        self.steps: List[DesignStep] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.file_path: Optional[str] = None
        self.version: str = "1.0"
        self.target_platforms: List[str] = []
        self.target_audience: str = ""
        self.game_style: str = ""
        self.core_mechanics: List[str] = []
        self.technical_requirements: Dict[str, Any] = {}
        self.resources: Dict[str, List[str]] = {
            "art": [],
            "audio": [],
            "animation": [],
            "models": []
        }

    def add_step(self, step: DesignStep) -> None:
        self.steps.append(step)
        self.updated_at = datetime.now()

    def update_step(self, step_name: str, new_step: DesignStep) -> None:
        for i, step in enumerate(self.steps):
            if step.name == step_name:
                self.steps[i] = new_step
                self.updated_at = datetime.now()
                break

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "game_type": self.game_type,
            "steps": [step.to_dict() for step in self.steps],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
            "target_platforms": self.target_platforms,
            "target_audience": self.target_audience,
            "game_style": self.game_style,
            "core_mechanics": self.core_mechanics,
            "technical_requirements": self.technical_requirements,
            "resources": self.resources
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameProject':
        project = cls(
            name=data["name"],
            description=data.get("description", ""),
            game_type=data.get("game_type", "")
        )
        project.created_at = datetime.fromisoformat(data["created_at"])
        project.updated_at = datetime.fromisoformat(data["updated_at"])
        project.version = data.get("version", "1.0")
        project.steps = [DesignStep.from_dict(step_data) for step_data in data.get("steps", [])]
        project.target_platforms = data.get("target_platforms", [])
        project.target_audience = data.get("target_audience", "")
        project.game_style = data.get("game_style", "")
        project.core_mechanics = data.get("core_mechanics", [])
        project.technical_requirements = data.get("technical_requirements", {})
        project.resources = data.get("resources", {
            "art": [],
            "audio": [],
            "animation": [],
            "models": []
        })
        return project

class ProjectManager:
    def __init__(self, base_dir: str = "projects"):
        self.base_dir = base_dir
        self.current_project: Optional[GameProject] = None
        os.makedirs(base_dir, exist_ok=True)

    def create_project(self, name: str, description: str = "", game_type: str = "") -> GameProject:
        """创建新项目"""
        project = GameProject(name, description, game_type)
        self.current_project = project
        return project

    def save_project(self, project: GameProject, file_path: Optional[str] = None) -> str:
        """保存项目到文件"""
        if file_path is None:
            if project.file_path:
                file_path = project.file_path
            else:
                file_path = os.path.join(self.base_dir, f"{project.name}.dep")
        
        if not file_path.endswith('.dep'):
            file_path = f"{file_path}.dep"
        
        project.file_path = file_path
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(project.to_dict(), f, ensure_ascii=False, indent=2)
        return file_path

    def load_project(self, file_path: str) -> GameProject:
        """从文件加载项目"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Project file not found: {file_path}")
        
        if not file_path.endswith('.dep'):
            raise ValueError("Invalid project file extension. Expected .dep")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        project = GameProject.from_dict(data)
        project.file_path = file_path
        self.current_project = project
        return project

    def get_project_file_path(self) -> Optional[str]:
        """获取当前项目的文件路径"""
        return self.current_project.file_path if self.current_project else None

    def is_project_modified(self) -> bool:
        """检查项目是否被修改"""
        if not self.current_project or not self.current_project.file_path:
            return False
        
        if not os.path.exists(self.current_project.file_path):
            return True
        
        with open(self.current_project.file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        current_data = self.current_project.to_dict()
        return saved_data != current_data

    def list_projects(self) -> List[str]:
        if not os.path.exists(self.base_dir):
            return []
        
        projects = []
        for filename in os.listdir(self.base_dir):
            if filename.endswith('.dep'):
                projects.append(filename[:-4])
        return projects

    def delete_project(self, name: str) -> bool:
        filename = f"{name}.dep"
        filepath = os.path.join(self.base_dir, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            if self.current_project and self.current_project.name == name:
                self.current_project = None
            return True
        return False 