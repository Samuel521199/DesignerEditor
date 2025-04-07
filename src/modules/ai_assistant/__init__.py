"""
AI Assistant Module
AI助手模块

This module provides AI assistance functionality for the Designer Editor.
此模块为设计器编辑器提供AI助手功能。
"""

from .api import AIAssistantAPI, AssistantType, Message, Suggestion
from .widget import AIAssistantWidget
from .panel import AIAssistantPanel

__all__ = ['AIAssistantAPI', 'AssistantType', 'Message', 'Suggestion', 'AIAssistantWidget', 'AIAssistantPanel'] 