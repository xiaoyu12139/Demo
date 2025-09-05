"""绘图设计模式相关组件。

本模块包含绘图设计模式下使用的画布组件和操作组件，
提供绘图相关的用户界面和功能。

Classes:
    DrawingCanvasWidget: 绘图画布组件
    DrawingArea: 自定义绘图区域组件
    DrawingOperationWidget: 绘图工具操作控件组件
"""

from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QLabel, QGroupBox, QRadioButton, QButtonGroup,
    QSlider, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QPaintEvent


class GetWidgetDataCanvasWidget(QWidget):
    """绘图画布组件。
    
    这个类实现了一个包含绘图区域的画布，用于显示图形绘制功能。
    包含一个自定义的绘图区域用于演示基本的图形绘制。
    
    Attributes:
        drawing_area: DrawingArea实例，用于图形绘制。
    """
    
    def __init__(self) -> None:
        """初始化绘图画布。"""
        super().__init__()

class GetWidgetDataOperationWidget(QWidget):
    """操作控件区域组件3 - 绘图工具。
    
    这个类创建一个专门用于绘图工具的操作面板，包含绘图相关的控件，
    如颜色选择、画笔大小、图形类型等功能。
    
    Attributes:
        color_buttons: 颜色选择按钮组。
        brush_size_slider: 画笔大小滑块。
        size_label: 显示当前画笔大小的标签。
        shape_buttons: 图形类型按钮组。
        clear_canvas_btn: 清空画布按钮。
        save_btn: 保存图片按钮。
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