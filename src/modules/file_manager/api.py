"""
File Manager API Module
文件管理器API模块

This module provides the public API for file management operations.
Other modules should only use the methods defined in this file.
此模块提供文件管理操作的公共API。
其他模块只能使用此文件中定义的方法。
"""

from typing import Optional, Dict, Any
from .project_saver import ProjectSaver
from .project_loader import ProjectLoader
from ..project_model.project_info_model import ProjectInfoModel

class FileManagerAPI:
    """文件管理器API类"""
    
    def __init__(self):
        self._saver = ProjectSaver()
        self._loader = ProjectLoader()
        self._current_project_path: Optional[str] = None
        
    def save_project(self, project_info: ProjectInfoModel, project_path: str) -> bool:
        """
        保存项目
        Save project
        
        Args:
            project_info: 项目信息对象
            project_path: 项目保存路径
            
        Returns:
            bool: 是否保存成功
        """
        try:
            success = self._saver.save_project(project_info, project_path)
            if success:
                self._current_project_path = project_path
            return success
        except Exception as e:
            print(f"保存项目失败: {str(e)}")
            return False
            
    def load_project(self, project_path: str) -> Optional[ProjectInfoModel]:
        """
        加载项目
        Load project
        
        Args:
            project_path: 项目文件路径
            
        Returns:
            Optional[ProjectInfoModel]: 加载的项目信息对象，失败返回None
        """
        try:
            project_info = self._loader.load_project(project_path)
            if project_info:
                self._current_project_path = project_path
            return project_info
        except Exception as e:
            print(f"加载项目失败: {str(e)}")
            return None
            
    def get_project_info(self) -> Optional[Dict[str, Any]]:
        """
        获取当前项目信息
        Get current project info
        
        Returns:
            Optional[Dict[str, Any]]: 项目信息字典，无项目时返回None
        """
        if not self._current_project_path:
            return None
        try:
            return self._loader.get_project_info(self._current_project_path)
        except Exception as e:
            print(f"获取项目信息失败: {str(e)}")
            return None
            
    def get_project_directory(self) -> Optional[str]:
        """
        获取当前项目目录
        Get current project directory
        
        Returns:
            Optional[str]: 项目目录路径，无项目时返回None
        """
        return self._current_project_path 