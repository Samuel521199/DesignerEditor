"""
Project Saver Module
项目保存器模块

This module handles project saving operations.
此模块处理项目保存操作。
"""

import os
import json
from typing import Dict, Any
from ..project_model.project_info_model import ProjectInfoModel

class ProjectSaver:
    """项目保存器类"""
    
    def save_project(self, project_info: ProjectInfoModel, project_path: str) -> bool:
        """
        保存项目
        
        Args:
            project_info: 项目信息对象
            project_path: 项目保存路径
            
        Returns:
            bool: 是否保存成功
        """
        try:
            # 创建项目目录
            project_dir = os.path.dirname(project_path)
            if not os.path.exists(project_dir):
                os.makedirs(project_dir)
            
            # 创建项目结构
            project_structure = {
                "version": "1.0.0",
                "project_info": {
                    "name": project_info.name,
                    "description": project_info.description,
                    "game_type": project_info.game_type.name if project_info.game_type else None,
                    "target_platforms": [platform.name for platform in project_info.target_platforms],
                    "game_style": project_info.game_style.name if project_info.game_style else None,
                    "time_setting": project_info.time_setting.name if project_info.time_setting else None,
                    "target_audience": [audience.name for audience in project_info.target_audience] if project_info.target_audience else None
                },
                "scenes": [],
                "formulas": [],
                "resources": []
            }
            
            # 保存项目描述文件
            dep_file = os.path.join(project_dir, "project.dep")
            with open(dep_file, 'w', encoding='utf-8') as f:
                json.dump(project_structure, f, ensure_ascii=False, indent=4)
            
            # 创建其他目录
            self._create_project_directories(project_dir)
            
            return True
            
        except Exception as e:
            print(f"保存项目失败: {str(e)}")
            return False
            
    def _create_project_directories(self, project_dir: str):
        """创建项目目录结构"""
        directories = [
            "scenes",    # 场景目录
            "formulas",  # 公式目录
            "resources", # 资源目录
            "configs",   # 配置目录
            "scripts"    # 脚本目录
        ]
        
        for directory in directories:
            dir_path = os.path.join(project_dir, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path) 