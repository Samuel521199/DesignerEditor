"""
Main Program
主程序

This is the main entry point of the application.
这是应用程序的主入口点。
"""

import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    """主函数"""
    try:
        app = QApplication(sys.argv)
        
        # 设置应用程序信息
        app.setApplicationName("游戏设计编辑器")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("UnityMindFlowPro")
        
        print("创建主窗口...")
        window = MainWindow()
        print("显示主窗口...")
        window.show()
        
        print("运行应用程序...")
        sys.exit(app.exec())
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 