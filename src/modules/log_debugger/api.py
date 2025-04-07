"""日志调试模块API"""
from enum import Enum
import logging
import os
from typing import Optional

class LogLevel(Enum):
    """日志级别"""
    DEBUG = "调试"
    INFO = "信息"
    WARNING = "警告"
    ERROR = "错误"
    CRITICAL = "严重"

class LogDebuggerAPI:
    """日志调试API"""
    
    @staticmethod
    def setup_logging(project_dir: str) -> None:
        """设置日志系统"""
        try:
            # 创建日志目录
            log_dir = os.path.join(project_dir, "logs")
            os.makedirs(log_dir, exist_ok=True)
            
            # 配置日志
            log_file = os.path.join(log_dir, "debug.log")
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )
        except Exception as e:
            print(f"设置日志系统失败: {str(e)}")
            
    @staticmethod
    def get_log_file(project_dir: str) -> Optional[str]:
        """获取日志文件路径"""
        try:
            log_file = os.path.join(project_dir, "logs", "debug.log")
            if os.path.exists(log_file):
                return log_file
            return None
        except Exception as e:
            print(f"获取日志文件失败: {str(e)}")
            return None
            
    @staticmethod
    def clear_logs(project_dir: str) -> bool:
        """清空日志"""
        try:
            log_file = os.path.join(project_dir, "logs", "debug.log")
            if os.path.exists(log_file):
                with open(log_file, "w", encoding="utf-8") as f:
                    f.write("")
                return True
            return False
        except Exception as e:
            print(f"清空日志失败: {str(e)}")
            return False 