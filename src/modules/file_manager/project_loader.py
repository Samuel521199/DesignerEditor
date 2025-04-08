"""
Project Loader Module
项目加载器模块

This module handles project loading operations.
此模块处理项目加载操作。
"""

import os
import json
from typing import Dict, Any, Optional
from ..project_model.project_info_model import (
    ProjectInfoModel, GameType, TargetPlatform,
    GameStyle, TimeSetting, TargetAudience
)

class ProjectLoader:
    """项目加载器类"""
    
    def __init__(self):
        self.project_structure: Dict[str, Any] = {}
        
    def load_project(self, project_path: str) -> Optional[ProjectInfoModel]:
        """
        加载项目
        
        Args:
            project_path: 项目文件路径
            
        Returns:
            Optional[ProjectInfoModel]: 加载的项目信息对象，失败返回None
        """
        try:
            # 读取项目描述文件
            dep_file = os.path.join(os.path.dirname(project_path), "project.dep")
            if not os.path.exists(dep_file):
                print(f"项目描述文件不存在: {dep_file}")
                return None
                
            with open(dep_file, 'r', encoding='utf-8') as f:
                self.project_structure = json.load(f)
                
            project_info = self.project_structure.get("project_info", {})
            
            # 转换枚举值
            game_type = None
            if "game_type" in project_info and project_info["game_type"]:
                try:
                    game_type = GameType[project_info["game_type"]]
                except KeyError:
                    print(f"无效的游戏类型: {project_info['game_type']}")
            
            target_platforms = []
            if "target_platforms" in project_info and project_info["target_platforms"]:
                for platform in project_info["target_platforms"]:
                    try:
                        target_platforms.append(TargetPlatform[platform])
                    except KeyError:
                        print(f"无效的目标平台: {platform}")
            
            game_style = None
            if "game_style" in project_info and project_info["game_style"]:
                try:
                    game_style = GameStyle[project_info["game_style"]]
                except KeyError:
                    print(f"无效的游戏风格: {project_info['game_style']}")
            
            time_setting = None
            if "time_setting" in project_info and project_info["time_setting"]:
                try:
                    time_setting = TimeSetting[project_info["time_setting"]]
                except KeyError:
                    print(f"无效的时代背景: {project_info['time_setting']}")
            
            target_audiences = []
            if "target_audience" in project_info and project_info["target_audience"]:
                if isinstance(project_info["target_audience"], list):
                    for audience in project_info["target_audience"]:
                        try:
                            target_audiences.append(TargetAudience[audience])
                        except KeyError:
                            print(f"无效的目标受众: {audience}")
                else:
                    try:
                        target_audiences.append(TargetAudience[project_info["target_audience"]])
                    except KeyError:
                        print(f"无效的目标受众: {project_info['target_audience']}")
            
            # 创建项目信息对象
            project_info = ProjectInfoModel(
                name=project_info["name"],
                description=project_info.get("description"),
                game_type=game_type,
                target_platforms=target_platforms,
                game_style=game_style,
                time_setting=time_setting,
                target_audience=target_audiences
            )
            
            return project_info
            
        except Exception as e:
            print(f"加载项目失败: {str(e)}")
            return None
            
    def get_project_info(self, project_path: str) -> Optional[Dict[str, Any]]:
        """
        获取项目信息
        
        Args:
            project_path: 项目文件路径
            
        Returns:
            Optional[Dict[str, Any]]: 项目信息字典，失败返回None
        """
        try:
            dep_file = os.path.join(os.path.dirname(project_path), "project.dep")
            if not os.path.exists(dep_file):
                return None
                
            with open(dep_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"获取项目信息失败: {str(e)}")
            return None
            
    def get_scene_files(self, project_path: str) -> list:
        """
        获取场景文件列表
        
        Args:
            project_path: 项目文件路径
            
        Returns:
            list: 场景文件列表
        """
        try:
            scenes_dir = os.path.join(os.path.dirname(project_path), "scenes")
            if not os.path.exists(scenes_dir):
                return []
                
            return [f for f in os.listdir(scenes_dir) if f.endswith('.scene')]
            
        except Exception as e:
            print(f"获取场景文件失败: {str(e)}")
            return []
            
    def get_formula_files(self, project_path: str) -> list:
        """
        获取公式文件列表
        
        Args:
            project_path: 项目文件路径
            
        Returns:
            list: 公式文件列表
        """
        try:
            formulas_dir = os.path.join(os.path.dirname(project_path), "formulas")
            if not os.path.exists(formulas_dir):
                return []
                
            return [f for f in os.listdir(formulas_dir) if f.endswith('.formula')]
            
        except Exception as e:
            print(f"获取公式文件失败: {str(e)}")
            return []
            
    def get_resource_files(self, project_path: str) -> list:
        """
        获取资源文件列表
        
        Args:
            project_path: 项目文件路径
            
        Returns:
            list: 资源文件列表
        """
        try:
            resources_dir = os.path.join(os.path.dirname(project_path), "resources")
            if not os.path.exists(resources_dir):
                return []
                
            return os.listdir(resources_dir)
            
        except Exception as e:
            print(f"获取资源文件失败: {str(e)}")
            return [] 