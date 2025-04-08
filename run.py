import sys
import logging
import os
from PyQt6.QtWidgets import QApplication

# 添加项目根目录和src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)

from src.main_window import MainWindow

def main():
    """应用程序入口"""
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    main_window = MainWindow()
    
    # 显示主窗口
    main_window.show()
    
    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 