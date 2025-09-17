"""PySide6 主窗口应用程序。

这个模块实现了一个包含菜单栏、操作区域和画布区域的PySide6桌面应用程序。
应用程序支持通过菜单栏在不同的画布视图之间切换。

Typical usage example:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
"""

import sys
from typing import Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QSplitter, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from widgets import GetWidgetDataCanvasWidget, GetWidgetDataOperationWidget



class MainWindow(QMainWindow):
    """应用程序主窗口。
    
    这个类实现了应用程序的主窗口，包含菜单栏、操作区域和可切换的画布区域。
    用户可以通过菜单栏在不同的画布视图（文本编辑器、列表视图、绘图区域）之间切换。
    
    主窗口采用水平布局，左侧为画布区域（QStackedWidget），右侧为操作控件区域。
    
    Attributes:
        operation_widget: OperationWidget实例，包含各种操作控件。
        canvas_stack: QStackedWidget实例，用于切换不同的画布视图。
        canvas1: CanvasWidget1实例，文本编辑器画布。
        canvas2: CanvasWidget2实例，列表视图画布。
        canvas3: CanvasWidget3实例，绘图区域画布。
    """
    
    def __init__(self) -> None:
        """初始化主窗口。
        
        创建主窗口并初始化用户界面和菜单栏。
        """
        super().__init__()
        self.init_ui()
        self.create_menu_bar()
    
    def init_ui(self) -> None:
        """初始化用户界面。
        
        设置窗口标题、大小和布局。创建操作区域和画布区域，
        并将它们添加到主布局中。
        """
        self.setWindowTitle("PySide 窗口应用")
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建可拖动分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧画布区域（使用QStackedWidget）
        self.canvas_stack = QStackedWidget()
        
        # 创建不同的画布页面
        self.canvas1 = GetWidgetDataCanvasWidget()
        # self.canvas1 = TextCanvasWidget()
        # self.canvas2 = ListCanvasWidget()
        # self.canvas3 = DrawingCanvasWidget()
        
        # 添加到堆叠部件
        self.canvas_stack.addWidget(self.canvas1)
        # self.canvas_stack.addWidget(self.canvas1)
        # self.canvas_stack.addWidget(self.canvas2)
        # self.canvas_stack.addWidget(self.canvas3)
        
        # 设置默认显示第一个画布
        self.canvas_stack.setCurrentIndex(0)
        
        # 右侧操作区域（使用QStackedWidget）
        self.operation_stack = QStackedWidget()
        # 移除固定宽度，让控件可以自适应
        self.operation_stack.setMinimumWidth(250)  # 设置最小宽度
        
        # 创建不同的操作页面
        self.operation1 = GetWidgetDataOperationWidget()
        # self.operation1 = TextOperationWidget()
        # self.operation2 = ListOperationWidget()
        # self.operation3 = DrawingOperationWidget()
        
        # 添加到操作堆叠部件
        self.operation_stack.addWidget(self.operation1)
        # self.operation_stack.addWidget(self.operation1)
        # self.operation_stack.addWidget(self.operation2)
        # self.operation_stack.addWidget(self.operation3)
        
        # 设置默认显示第一个操作区域
        self.operation_stack.setCurrentIndex(0)
        
        # 为操作区域添加滚动视图
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.operation_stack)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setMinimumWidth(250)
        
        # 设置滚动区域样式
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # 设置操作区域样式
        self.operation_stack.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid gray;
                border-radius: 5px;
                margin: 5px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # 添加到分割器
        splitter.addWidget(self.canvas_stack)
        splitter.addWidget(self.scroll_area)
        
        # 设置初始分割比例 (70% : 30%)
        splitter.setSizes([700, 300])
        
        # 设置分割器样式
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #d0d0d0;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # 创建主布局并添加分割器
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(splitter)
        
        central_widget.setLayout(main_layout)
    
    def create_menu_bar(self) -> None:
        """创建应用程序菜单栏。
        
        创建文件、视图和帮助菜单，并为每个菜单项设置相应的快捷键和回调函数。
        文件菜单包含新建、打开和退出功能；视图菜单用于切换不同的画布；
        帮助菜单包含关于信息。
        """
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        new_action = QAction('新建', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction('打开', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图')

        get_json_action = QAction('获取JSON数据', self)
        get_json_action.triggered.connect(lambda: self.switch_view(0))
        view_menu.addAction(get_json_action)
        
        # text_action = QAction('文本编辑模式', self)
        # text_action.triggered.connect(lambda: self.switch_view(0))
        # view_menu.addAction(text_action)
        
        # list_action = QAction('列表管理模式', self)
        # list_action.triggered.connect(lambda: self.switch_view(1))
        # view_menu.addAction(list_action)
        
        # draw_action = QAction('绘图设计模式', self)
        # draw_action.triggered.connect(lambda: self.switch_view(2))
        # view_menu.addAction(draw_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def switch_view(self, index: int) -> None:
        """切换视图模式，同时切换左右两个区域。
        
        根据提供的索引同时切换画布区域和操作区域的显示内容。
        
        Args:
            index: 视图索引，0=文本编辑模式，1=列表管理模式，2=绘图设计模式。
        """
        self.canvas_stack.setCurrentIndex(index)
        self.operation_stack.setCurrentIndex(index)
        canvas_names = ["文本编辑模式", "列表管理模式", "绘图设计模式"]
        self.statusBar().showMessage(f"当前视图: {canvas_names[index]}")
    
    def new_file(self) -> None:
        """处理新建文件操作。
        
        当用户选择文件菜单中的新建选项时调用此方法。
        目前只在状态栏显示消息，可以扩展为实际的文件创建功能。
        """
        self.statusBar().showMessage("新建文件")
    
    def open_file(self) -> None:
        """处理打开文件操作。
        
        当用户选择文件菜单中的打开选项时调用此方法。
        目前只在状态栏显示消息，可以扩展为实际的文件打开功能。
        """
        self.statusBar().showMessage("打开文件")
    
    def show_about(self) -> None:
        """显示应用程序关于信息。
        
        当用户选择帮助菜单中的关于选项时调用此方法。
        在状态栏显示关于信息。
        """
        self.statusBar().showMessage("关于 PySide 窗口应用")


def main() -> None:
    """应用程序主入口函数。
    
    创建QApplication实例，初始化主窗口并显示，然后启动应用程序的
    事件循环。当窗口关闭时，程序将退出。
    
    Raises:
        SystemExit: 当应用程序退出时抛出。
    """
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()