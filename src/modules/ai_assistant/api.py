"""AI助手模块API"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class AssistantType(Enum):
    """助手类型枚举"""
    SCENE_DESIGN = "场景设计"
    CHARACTER_DESIGN = "角色设计"
    STORY_DESIGN = "剧情设计"
    SYSTEM_DESIGN = "系统设计"

@dataclass
class Message:
    """消息数据类"""
    content: str
    role: str  # "user" or "assistant"
    timestamp: datetime
    context: Dict[str, str]

@dataclass
class Suggestion:
    """建议数据类"""
    content: str
    type: AssistantType
    confidence: float
    timestamp: datetime
    context: Dict[str, str]

class AIAssistantAPI:
    """AI助手模块API接口"""
    
    def get_suggestion(self, query: str, assistant_type: AssistantType) -> Optional[Suggestion]:
        """获取AI建议"""
        raise NotImplementedError
        
    def get_help(self, query: str, assistant_type: AssistantType) -> Optional[str]:
        """获取帮助信息"""
        raise NotImplementedError
        
    def get_chat_history(self) -> List[Message]:
        """获取聊天历史"""
        raise NotImplementedError
        
    def clear_chat_history(self) -> bool:
        """清空聊天历史"""
        raise NotImplementedError
        
    def save_chat_history(self, filename: str) -> bool:
        """保存聊天历史"""
        raise NotImplementedError
        
    def load_chat_history(self, filename: str) -> bool:
        """加载聊天历史"""
        raise NotImplementedError 