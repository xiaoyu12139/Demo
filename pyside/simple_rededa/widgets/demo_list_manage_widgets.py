"""列表管理模式相关组件。

本模块包含列表管理模式下使用的画布组件和操作组件，
提供列表管理相关的用户界面和功能。

Classes:
    ListCanvasWidget: 列表视图画布组件
    ListOperationWidget: 列表管理操作控件组件
"""

from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QLabel, QListWidget, QLineEdit, QGroupBox,
    QPushButton
)


class ListCanvasWidget(QWidget):
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


class ListOperationWidget(QWidget):
    """操作控件区域组件2 - 列表管理。
    
    这个类创建一个专门用于列表管理的操作面板，包含列表操作相关的控件，
    如添加项目、删除项目、排序等功能。
    
    Attributes:
        item_input: 文本输入框，用于输入新项目。
        add_btn: 添加按钮。
        delete_btn: 删除按钮。
        sort_btn: 排序按钮。
        clear_btn: 清空按钮。
        count_label: 显示项目数量的标签。
        selected_label: 显示选中项目的标签。
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