"""
Project Manager API
项目管理API接口

This module provides the API interface for project management functionality.
此模块提供项目管理功能的API接口。
"""

import os
from typing import Optional, List
from .models import GameProject, DesignStep

class ProjectManagerAPI:
    """Project manager API interface class."""
    
    def __init__(self):
        self.current_project: Optional[GameProject] = None
        self.project_changed_callbacks = []
    
    def create_project(self, project_data: dict) -> GameProject:
        """Create a new project."""
        project = GameProject(**project_data)
        self.current_project = project
        self._notify_project_changed()
        return project
    
    def open_project(self, project_path: str) -> GameProject:
        """Open an existing project."""
        # TODO: Implement project loading from file
        pass
    
    def save_project(self, project_path: str) -> bool:
        """Save current project."""
        if not self.current_project:
            return False
        # TODO: Implement project saving to file
        return True
    
    def add_design_step(self, step_data: dict) -> DesignStep:
        """Add a new design step to current project."""
        if not self.current_project:
            raise RuntimeError("No project is currently open")
        step = DesignStep(**step_data)
        self.current_project.design_steps.append(step)
        self._notify_project_changed()
        return step
    
    def get_project_structure(self) -> List[dict]:
        """Get the current project structure."""
        if not self.current_project:
            return []
        return self.current_project.get_structure()
    
    def register_project_changed_callback(self, callback):
        """Register a callback for project changes."""
        self.project_changed_callbacks.append(callback)
    
    def _notify_project_changed(self):
        """Notify all registered callbacks about project changes."""
        for callback in self.project_changed_callbacks:
            callback() 