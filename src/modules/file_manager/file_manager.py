"""
File Manager Module
文件管理器模块

This module handles all file operations including saving, loading, and managing project files.
此模块处理所有文件操作，包括保存、加载和管理项目文件。
"""

import os
import json
from typing import Any, Dict
from ..project_model.project_info_model import ProjectInfoModel

class FileManager:
    """文件管理器类"""
    
    def __init__(self):
        self.current_project_path = None
        
    def save_project(self, project_info: ProjectInfoModel, file_path: str = None) -> bool:
        """保存项目到文件"""
        try:
            if file_path is None:
                if self.current_project_path is None:
                    return False
                file_path = self.current_project_path
                
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 将项目信息转换为字典
            project_data = project_info.to_dict()
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=4)
                
            self.current_project_path = file_path
            return True
            
        except Exception as e:
            print(f"保存项目失败: {str(e)}")
            return False
            
    def load_project(self, file_path: str) -> ProjectInfoModel:
        """从文件加载项目"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
                
            self.current_project_path = file_path
            return ProjectInfoModel.from_dict(project_data)
            
        except Exception as e:
            print(f"加载项目失败: {str(e)}")
            return None
            
    def export_project(self, project_info: ProjectInfoModel, export_path: str) -> bool:
        """导出项目"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            
            # 将项目信息转换为字典
            project_data = project_info.to_dict()
            
            # 导出到文件
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=4)
                
            return True
            
        except Exception as e:
            print(f"导出项目失败: {str(e)}")
            return False
            
    def get_project_directory(self) -> str:
        """获取项目目录"""
        if self.current_project_path:
            return os.path.dirname(self.current_project_path)
        return None 