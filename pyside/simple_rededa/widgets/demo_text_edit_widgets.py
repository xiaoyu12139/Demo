"""文本编辑模式相关组件。

本模块包含文本编辑模式下使用的画布组件和操作组件，
提供文本编辑相关的用户界面和功能。

Classes:
    TextCanvasWidget: 文本编辑器画布组件
    TextOperationWidget: 文本编辑操作控件组件
"""

from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QTextEdit, QLineEdit, QSpinBox, QCheckBox,
    QGroupBox, QRadioButton, QButtonGroup, QSlider,
    QProgressBar, QPushButton
)
from PySide6.QtCore import Qt


class TextCanvasWidget(QWidget):
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


class TextOperationWidget(QWidget):
    """操作控件区域组件1 - 文本编辑。
    
    这个类创建一个包含各种操作控件的侧边栏，用于文本编辑相关的操作，
    包括基本控件、单选按钮组、滑块控制等。
    
    Attributes:
        line_edit: 文本输入框。
        spin_box: 数值选择框。
        checkbox: 复选框。
        button_group: 单选按钮组。
        radio1, radio2, radio3: 单选按钮。
        slider: 水平滑块。
        progress_bar: 进度条。
        btn_action1, btn_action2, btn_clear: 操作按钮。
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