"""
Project Manager Module
项目管理模块

This module provides project management functionality for the Designer Editor.
此模块提供设计器编辑器的项目管理功能。
"""

from .api import ProjectManagerAPI
from .models import GameProject, DesignStep, DesignType
from .project_tree import ProjectTreeWidget
from .project_info import ProjectInfoWidget

__all__ = [
    'ProjectManagerAPI',
    'GameProject',
    'DesignStep',
    'DesignType',
    'ProjectTreeWidget',
    'ProjectInfoWidget'
] 