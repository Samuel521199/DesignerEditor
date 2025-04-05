import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class ProjectStep:
    def __init__(self, name: str, description: str, code: str = "", is_generated: bool = False):
        self.name = name
        self.description = description
        self.code = code
        self.is_generated = is_generated
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "is_generated": self.is_generated,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ProjectStep':
        step = cls(
            name=data["name"],
            description=data["description"],
            code=data.get("code", ""),
            is_generated=data.get("is_generated", False)
        )
        step.created_at = data.get("created_at", datetime.now().isoformat())
        step.updated_at = data.get("updated_at", step.created_at)
        return step

class Project:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.steps: List[ProjectStep] = []
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def add_step(self, step: ProjectStep):
        self.steps.append(step)
        self.updated_at = datetime.now().isoformat()

    def update_step(self, index: int, step: ProjectStep):
        if 0 <= index < len(self.steps):
            self.steps[index] = step
            self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        project = cls(
            name=data["name"],
            description=data.get("description", "")
        )
        project.created_at = data.get("created_at", datetime.now().isoformat())
        project.updated_at = data.get("updated_at", project.created_at)
        project.steps = [ProjectStep.from_dict(step_data) for step_data in data.get("steps", [])]
        return project

class ProjectManager:
    def __init__(self, projects_dir: str = "projects"):
        self.projects_dir = projects_dir
        self.current_project: Optional[Project] = None
        self._ensure_projects_dir()

    def _ensure_projects_dir(self):
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)

    def create_project(self, name: str, description: str = "") -> Project:
        project = Project(name, description)
        self.current_project = project
        return project

    def save_project(self, project: Project) -> str:
        if not project.name:
            raise ValueError("Project name cannot be empty")

        filename = f"{project.name}.json"
        filepath = os.path.join(self.projects_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project.to_dict(), f, ensure_ascii=False, indent=2)
        
        return filepath

    def load_project(self, name: str) -> Project:
        filename = f"{name}.json"
        filepath = os.path.join(self.projects_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Project file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        project = Project.from_dict(data)
        self.current_project = project
        return project

    def list_projects(self) -> List[str]:
        if not os.path.exists(self.projects_dir):
            return []
        
        projects = []
        for filename in os.listdir(self.projects_dir):
            if filename.endswith('.json'):
                projects.append(filename[:-5])  # Remove .json extension
        return projects

    def delete_project(self, name: str) -> bool:
        filename = f"{name}.json"
        filepath = os.path.join(self.projects_dir, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            if self.current_project and self.current_project.name == name:
                self.current_project = None
            return True
        return False 