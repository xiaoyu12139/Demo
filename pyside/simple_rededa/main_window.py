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
    QStackedWidget, QLabel, QPushButton, QMenuBar, QMenu, QTextEdit,
    QListWidget, QGroupBox, QFormLayout, QLineEdit, QSpinBox,
    QCheckBox, QRadioButton, QButtonGroup, QSlider, QProgressBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QPainter, QPen, QColor, QPaintEvent


class OperationWidget1(QWidget):
    """操作控件区域组件。
    
    这个类创建一个包含各种控件的操作面板，包括文本输入框、数值选择器、
    复选框、单选按钮组、滑块、进度条和操作按钮。所有控件都组织在
    不同的分组框中以提供清晰的用户界面。
    
    Attributes:
        line_edit: 文本输入框，用于输入文本内容。
        spin_box: 数值选择器，范围为0-100。
        checkbox: 复选框，用于启用/禁用功能。
        button_group: 单选按钮组，包含三种模式选择。
        slider: 水平滑块，用于调整数值。
        progress_bar: 进度条，显示当前进度。
        btn_action1: 操作按钮1。
        btn_action2: 操作按钮2。
        btn_clear: 清空按钮。
    """
    
    def __init__(self) -> None:
        """初始化操作控件区域。"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self) -> None:
        """初始化用户界面。
        
        创建并布局所有的控件，包括基本控件组、单选按钮组、
        滑块控制组和操作按钮。
        """
        layout = QVBoxLayout()
        
        # 基本控件组
        basic_group = QGroupBox("基本控件")
        basic_layout = QFormLayout()
        
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("输入文本...")
        basic_layout.addRow("文本输入:", self.line_edit)
        
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        self.spin_box.setValue(50)
        basic_layout.addRow("数值:", self.spin_box)
        
        self.checkbox = QCheckBox("启用功能")
        basic_layout.addRow(self.checkbox)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # 单选按钮组
        radio_group = QGroupBox("选择模式")
        radio_layout = QVBoxLayout()
        
        self.button_group = QButtonGroup()
        self.radio1 = QRadioButton("模式 1")
        self.radio2 = QRadioButton("模式 2")
        self.radio3 = QRadioButton("模式 3")
        
        self.button_group.addButton(self.radio1, 1)
        self.button_group.addButton(self.radio2, 2)
        self.button_group.addButton(self.radio3, 3)
        
        self.radio1.setChecked(True)
        
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        
        radio_group.setLayout(radio_layout)
        layout.addWidget(radio_group)
        
        # 滑块和进度条
        slider_group = QGroupBox("控制")
        slider_layout = QVBoxLayout()
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(30)
        slider_layout.addWidget(QLabel("滑块:"))
        slider_layout.addWidget(self.slider)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(30)
        slider_layout.addWidget(QLabel("进度:"))
        slider_layout.addWidget(self.progress_bar)
        
        # 连接滑块和进度条
        self.slider.valueChanged.connect(self.progress_bar.setValue)
        
        slider_group.setLayout(slider_layout)
        layout.addWidget(slider_group)
        
        # 操作按钮
        button_layout = QVBoxLayout()
        self.btn_action1 = QPushButton("操作 1")
        self.btn_action2 = QPushButton("操作 2")
        self.btn_clear = QPushButton("清空")
        
        button_layout.addWidget(self.btn_action1)
        button_layout.addWidget(self.btn_action2)
        button_layout.addWidget(self.btn_clear)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)


class OperationWidget2(QWidget):
    """操作控件区域组件2 - 列表管理。
    
    这个类创建一个专门用于列表管理的操作面板，包含列表操作相关的控件，
    如添加项目、删除项目、排序等功能。
    
    Attributes:
        item_input: 文本输入框，用于输入新项目。
        add_btn: 添加按钮。
        delete_btn: 删除按钮。
        sort_btn: 排序按钮。
        clear_btn: 清空按钮。
    """
    
    def __init__(self) -> None:
        """初始化列表管理操作区域。"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self) -> None:
        """初始化用户界面。
        
        创建并布局列表管理相关的控件。
        """
        layout = QVBoxLayout()
        
        # 列表管理组
        list_group = QGroupBox("列表管理")
        list_layout = QFormLayout()
        
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("输入新项目...")
        list_layout.addRow("新项目:", self.item_input)
        
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # 操作按钮组
        button_group = QGroupBox("操作")
        button_layout = QVBoxLayout()
        
        self.add_btn = QPushButton("添加项目")
        self.delete_btn = QPushButton("删除选中")
        self.sort_btn = QPushButton("排序列表")
        self.clear_btn = QPushButton("清空列表")
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.sort_btn)
        button_layout.addWidget(self.clear_btn)
        
        button_group.setLayout(button_layout)
        layout.addWidget(button_group)
        
        # 列表统计组
        stats_group = QGroupBox("统计信息")
        stats_layout = QFormLayout()
        
        self.count_label = QLabel("0")
        self.selected_label = QLabel("无")
        
        stats_layout.addRow("项目数量:", self.count_label)
        stats_layout.addRow("选中项目:", self.selected_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        layout.addStretch()
        self.setLayout(layout)


class OperationWidget3(QWidget):
    """操作控件区域组件3 - 绘图工具。
    
    这个类创建一个专门用于绘图工具的操作面板，包含绘图相关的控件，
    如颜色选择、画笔大小、图形类型等功能。
    
    Attributes:
        color_buttons: 颜色选择按钮组。
        brush_size_slider: 画笔大小滑块。
        shape_buttons: 图形类型按钮组。
        clear_canvas_btn: 清空画布按钮。
    """
    
    def __init__(self) -> None:
        """初始化绘图工具操作区域。"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self) -> None:
        """初始化用户界面。
        
        创建并布局绘图工具相关的控件。
        """
        layout = QVBoxLayout()
        
        # 颜色选择组
        color_group = QGroupBox("颜色选择")
        color_layout = QVBoxLayout()
        
        self.color_buttons = QButtonGroup()
        colors = [("红色", "red"), ("蓝色", "blue"), ("绿色", "green"), ("黑色", "black")]
        
        for i, (name, color) in enumerate(colors):
            btn = QRadioButton(name)
            btn.setStyleSheet(f"QRadioButton::indicator::checked {{ background-color: {color}; }}")
            self.color_buttons.addButton(btn, i)
            color_layout.addWidget(btn)
        
        # 默认选择黑色
        self.color_buttons.button(3).setChecked(True)
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # 画笔设置组
        brush_group = QGroupBox("画笔设置")
        brush_layout = QFormLayout()
        
        self.brush_size_slider = QSlider(Qt.Horizontal)
        self.brush_size_slider.setRange(1, 20)
        self.brush_size_slider.setValue(2)
        
        self.size_label = QLabel("2")
        self.brush_size_slider.valueChanged.connect(lambda v: self.size_label.setText(str(v)))
        
        brush_layout.addRow("画笔大小:", self.brush_size_slider)
        brush_layout.addRow("当前大小:", self.size_label)
        
        brush_group.setLayout(brush_layout)
        layout.addWidget(brush_group)
        
        # 图形工具组
        shape_group = QGroupBox("绘图工具")
        shape_layout = QVBoxLayout()
        
        self.shape_buttons = QButtonGroup()
        shapes = ["自由绘制", "直线", "矩形", "圆形"]
        
        for i, shape in enumerate(shapes):
            btn = QRadioButton(shape)
            self.shape_buttons.addButton(btn, i)
            shape_layout.addWidget(btn)
        
        # 默认选择自由绘制
        self.shape_buttons.button(0).setChecked(True)
        
        shape_group.setLayout(shape_layout)
        layout.addWidget(shape_group)
        
        # 操作按钮
        self.clear_canvas_btn = QPushButton("清空画布")
        self.save_btn = QPushButton("保存图片")
        
        layout.addWidget(self.clear_canvas_btn)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        
        self.setLayout(layout)


class CanvasWidget1(QWidget):
    """文本编辑器画布组件。
    
    这个类实现了一个包含文本编辑器的画布区域，用户可以在其中
    输入和编辑文本内容。
    
    Attributes:
        text_edit: QTextEdit实例，用于文本编辑功能。
    """
    
    def __init__(self) -> None:
        """初始化文本编辑器画布。"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self) -> None:
        """初始化用户界面。
        
        创建标题标签和文本编辑器，并设置相应的布局。
        """
        layout = QVBoxLayout()
        
        label = QLabel("文本编辑器")
        label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入文本内容...")
        layout.addWidget(self.text_edit)
        
        self.setLayout(layout)


class CanvasWidget2(QWidget):
    """列表视图画布组件。
    
    这个类实现了一个包含列表视图的画布区域，显示预定义的
    列表项供用户查看和选择。
    
    Attributes:
        list_widget: QListWidget实例，用于显示列表项。
    """
    
    def __init__(self) -> None:
        """初始化列表视图画布。"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self) -> None:
        """初始化用户界面。
        
        创建标题标签和列表控件，并添加示例列表项。
        """
        layout = QVBoxLayout()
        
        label = QLabel("列表视图")
        label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(label)
        
        self.list_widget = QListWidget()
        for i in range(1, 11):
            self.list_widget.addItem(f"列表项 {i}")
        
        layout.addWidget(self.list_widget)
        
        self.setLayout(layout)


class CanvasWidget3(QWidget):
    """绘图画布组件。
    
    这个类实现了一个包含绘图区域的画布，用于显示图形绘制功能。
    包含一个自定义的绘图区域用于演示基本的图形绘制。
    
    Attributes:
        drawing_area: DrawingArea实例，用于图形绘制。
    """
    
    def __init__(self) -> None:
        """初始化绘图画布。"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self) -> None:
        """初始化用户界面。
        
        创建标题标签和绘图区域组件。
        """
        layout = QVBoxLayout()
        
        label = QLabel("绘图区域")
        label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(label)
        
        # 创建一个简单的绘图区域
        self.drawing_area = DrawingArea()
        layout.addWidget(self.drawing_area)
        
        self.setLayout(layout)


class DrawingArea(QWidget):
    """自定义绘图区域组件。
    
    这个类实现了一个自定义的绘图区域，使用QPainter在paintEvent中
    绘制示例图形，包括矩形、圆形和线条。
    
    该组件设置了最小尺寸和白色背景，并在绘制时使用抗锯齿渲染。
    """
    
    def __init__(self) -> None:
        """初始化绘图区域。
        
        设置最小尺寸为400x300像素，并应用白色背景和灰色边框样式。
        """
        super().__init__()
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: white; border: 1px solid gray;")
    
    def paintEvent(self, event: QPaintEvent) -> None:
        """处理绘制事件。
        
        在组件上绘制示例图形，包括蓝色矩形、红色圆形和绿色十字线。
        使用抗锯齿渲染以获得更好的视觉效果。
        
        Args:
            event: QPaintEvent实例，包含绘制事件信息。
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制一些示例图形
        pen = QPen(QColor(0, 0, 255), 2)
        painter.setPen(pen)
        
        # 绘制矩形
        painter.drawRect(50, 50, 100, 80)
        
        # 绘制圆形
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)
        painter.drawEllipse(200, 50, 80, 80)
        
        # 绘制线条
        pen.setColor(QColor(0, 255, 0))
        painter.setPen(pen)
        painter.drawLine(50, 200, 300, 200)
        painter.drawLine(175, 150, 175, 250)


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
        
        # 创建主布局
        main_layout = QHBoxLayout()
        
        # 左侧画布区域（使用QStackedWidget）
        self.canvas_stack = QStackedWidget()
        
        # 创建不同的画布页面
        self.canvas1 = CanvasWidget1()
        self.canvas2 = CanvasWidget2()
        self.canvas3 = CanvasWidget3()
        
        # 添加到堆叠部件
        self.canvas_stack.addWidget(self.canvas1)
        self.canvas_stack.addWidget(self.canvas2)
        self.canvas_stack.addWidget(self.canvas3)
        
        # 设置默认显示第一个画布
        self.canvas_stack.setCurrentIndex(0)
        
        # 右侧操作区域（使用QStackedWidget）
        self.operation_stack = QStackedWidget()
        self.operation_stack.setFixedWidth(300)
        
        # 创建不同的操作页面
        self.operation1 = OperationWidget1()
        self.operation2 = OperationWidget2()
        self.operation3 = OperationWidget3()
        
        # 添加到操作堆叠部件
        self.operation_stack.addWidget(self.operation1)
        self.operation_stack.addWidget(self.operation2)
        self.operation_stack.addWidget(self.operation3)
        
        # 设置默认显示第一个操作区域
        self.operation_stack.setCurrentIndex(0)
        
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
        
        # 添加到主布局
        main_layout.addWidget(self.canvas_stack, 1)  # 画布区域占据剩余空间
        main_layout.addWidget(self.operation_stack)
        
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
        
        text_action = QAction('文本编辑模式', self)
        text_action.triggered.connect(lambda: self.switch_view(0))
        view_menu.addAction(text_action)
        
        list_action = QAction('列表管理模式', self)
        list_action.triggered.connect(lambda: self.switch_view(1))
        view_menu.addAction(list_action)
        
        draw_action = QAction('绘图设计模式', self)
        draw_action.triggered.connect(lambda: self.switch_view(2))
        view_menu.addAction(draw_action)
        
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