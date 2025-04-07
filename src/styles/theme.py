"""主题样式定义"""

DARK_THEME = """
    /* 主窗口 */
    QMainWindow, QWidget {
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    
    /* 菜单栏 */
    QMenuBar {
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    QMenuBar::item:selected {
        background-color: #3b3b3b;
    }
    QMenu {
        background-color: #2b2b2b;
        color: #e0e0e0;
        border: 1px solid #3b3b3b;
    }
    QMenu::item:selected {
        background-color: #3b3b3b;
    }
    
    /* 工具栏 */
    QToolBar {
        background-color: #2b2b2b;
        border: none;
        spacing: 3px;
        padding: 3px;
    }
    QToolButton {
        background-color: #2b2b2b;
        color: #e0e0e0;
        border: none;
        padding: 5px;
    }
    QToolButton:hover {
        background-color: #3b3b3b;
    }
    
    /* Dock窗口 */
    QDockWidget {
        background-color: #2b2b2b;
        color: #e0e0e0;
        titlebar-close-icon: url(close.png);
        titlebar-normal-icon: url(float.png);
    }
    QDockWidget::title {
        background-color: #3b3b3b;
        padding: 6px;
        border: none;
    }
    
    /* 输入控件 */
    QLineEdit, QTextEdit, QComboBox {
        background-color: #1e1e1e;
        color: #e0e0e0;
        border: 1px solid #3b3b3b;
        border-radius: 3px;
        padding: 5px;
    }
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #5b5b5b;
    }
    
    /* 按钮 */
    QPushButton {
        background-color: #3b3b3b;
        color: #e0e0e0;
        border: none;
        border-radius: 3px;
        padding: 5px 15px;
    }
    QPushButton:hover {
        background-color: #4b4b4b;
    }
    QPushButton:pressed {
        background-color: #2b2b2b;
    }
    
    /* 树形视图 */
    QTreeWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
        border: 1px solid #3b3b3b;
    }
    QTreeWidget::item:selected {
        background-color: #3b3b3b;
    }
    
    /* 状态栏 */
    QStatusBar {
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    
    /* 滚动条 */
    QScrollBar:vertical {
        background-color: #2b2b2b;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background-color: #3b3b3b;
        min-height: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #4b4b4b;
    }
""" 