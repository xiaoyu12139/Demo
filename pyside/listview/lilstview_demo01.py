#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ListView Demo 01 - 使用 setIndexWidget 添加带复选框的列表视图

本示例演示如何在 QListView 中使用 setIndexWidget 方法添加自定义控件（复选框）。
主要功能：
1. 创建带复选框的列表项
2. 使用 setIndexWidget 方法设置自定义控件
3. 处理复选框状态变化事件
4. 获取所有选中项的功能
"""

import sys
from typing import List, Dict, Any
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QListView, QCheckBox, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem


class CheckboxWidget(QWidget):
    """带复选框的自定义控件.
    
    用于在 ListView 中显示复选框和文本标签。
    """
    
    def __init__(self, text: str, checked: bool = False, parent=None):
        super().__init__(parent)
        self.text = text
        self.list_view = None  # 将在设置时由父窗口设置
        self.model_index = None  # 将在设置时由父窗口设置
        self.setup_ui(checked)
    
    def setup_ui(self, checked: bool) -> None:
        """设置UI布局.
        
        Args:
            checked: 初始选中状态
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # 创建复选框
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(checked)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        
        # 创建文本标签
        self.label = QLabel(self.text)
        
        # 添加到布局，设置垂直居中对齐
        layout.addWidget(self.checkbox, 0, Qt.AlignVCenter)
        layout.addWidget(self.label, 0, Qt.AlignVCenter)
        layout.addStretch()  # 添加弹性空间
        
        self.setLayout(layout)
        
        # 设置透明背景
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color: transparent;")
    
    def is_checked(self) -> bool:
        """获取复选框选中状态.
        
        Returns:
            bool: 是否选中
        """
        return self.checkbox.isChecked()
    
    def set_checked(self, checked: bool) -> None:
        """设置复选框选中状态.
        
        Args:
            checked: 是否选中
        """
        self.checkbox.setChecked(checked)
    
    def get_text(self) -> str:
        """获取文本内容.
        
        Returns:
            str: 文本内容
        """
        return self.text
    
    def on_checkbox_changed(self, state: int) -> None:
        """处理复选框状态变化.
        
        Args:
            state: 复选框状态
        """
        checked = state == Qt.CheckState.Checked.value
        print(f"项目 '{self.text}' 复选框状态变化: {checked}")
        
        # 同步ListView选中状态
        if self.list_view and self.model_index:
            selection_model = self.list_view.selectionModel()
            if checked:
                selection_model.select(self.model_index, selection_model.SelectionFlag.Select)
            else:
                selection_model.select(self.model_index, selection_model.SelectionFlag.Deselect)


class ListViewDemo(QMainWindow):
    """ListView 演示主窗口.
    
    展示如何使用 setIndexWidget 方法在 ListView 中添加自定义控件。
    """
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_data()
        self.setup_widgets()
    
    def setup_ui(self) -> None:
        """设置用户界面."""
        self.setWindowTitle("ListView Demo 01 - 带复选框的列表视图")
        self.setGeometry(100, 100, 400, 500)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建 ListView
        self.list_view = QListView()
        self.list_view.setAlternatingRowColors(True)
        
        # 设置选择模式为扩展选择，允许多选
        self.list_view.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        
        # 设置样式表，确保选中项保持高亮状态
        self.list_view.setStyleSheet("""
            QListView::item:selected {
                background-color: #0D99FF;
                color: white;
            }
            QListView::item:selected:!active {
                background-color: #0D99FF;
                color: white;
            }
            QListView::item:hover {
                background-color: #0D99FF;
            }
        """)
        
        main_layout.addWidget(self.list_view)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建按钮
        self.btn_select_all = QPushButton("全选")
        self.btn_deselect_all = QPushButton("取消全选")
        self.btn_get_selected = QPushButton("获取选中项")
        self.btn_add_item = QPushButton("添加项目")
        
        # 连接按钮信号
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_deselect_all.clicked.connect(self.deselect_all)
        self.btn_get_selected.clicked.connect(self.get_selected_items)
        self.btn_add_item.clicked.connect(self.add_new_item)
        
        # 添加按钮到布局
        button_layout.addWidget(self.btn_select_all)
        button_layout.addWidget(self.btn_deselect_all)
        button_layout.addWidget(self.btn_get_selected)
        button_layout.addWidget(self.btn_add_item)
        
        main_layout.addLayout(button_layout)
    
    def setup_data(self) -> None:
        """设置数据模型."""
        # 创建标准项目模型
        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)
        
        # 连接选择变化信号（在设置模型之后）
        self.list_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        # 初始数据
        self.items_data = [
            {"text": "项目 1", "checked": False},
            {"text": "项目 2", "checked": True},
            {"text": "项目 3", "checked": False},
            {"text": "项目 4", "checked": True},
            {"text": "项目 5", "checked": False},
        ]
        
        # 添加项目到模型
        for item_data in self.items_data:
            item = QStandardItem("")
            self.model.appendRow(item)
    
    def setup_widgets(self) -> None:
        """为每个列表项设置自定义控件."""
        for row in range(self.model.rowCount()):
            index = self.model.index(row, 0)
            item_data = self.items_data[row]
            
            # 创建自定义控件
            widget = CheckboxWidget(
                text=item_data["text"],
                checked=item_data["checked"]
            )
            
            # 设置ListView和模型索引引用，用于双向同步
            widget.list_view = self.list_view
            widget.model_index = index
            
            # 使用 setIndexWidget 设置自定义控件
            self.list_view.setIndexWidget(index, widget)
    
    def select_all(self) -> None:
        """全选所有项目."""
        for row in range(self.model.rowCount()):
            index = self.model.index(row, 0)
            widget = self.list_view.indexWidget(index)
            if isinstance(widget, CheckboxWidget):
                widget.set_checked(True)
        print("已全选所有项目")
    
    def deselect_all(self) -> None:
        """取消全选所有项目."""
        for row in range(self.model.rowCount()):
            index = self.model.index(row, 0)
            widget = self.list_view.indexWidget(index)
            if isinstance(widget, CheckboxWidget):
                widget.set_checked(False)
        print("已取消全选所有项目")
    
    def get_selected_items(self) -> None:
        """获取所有选中的项目."""
        selected_items = []
        
        for row in range(self.model.rowCount()):
            index = self.model.index(row, 0)
            widget = self.list_view.indexWidget(index)
            if isinstance(widget, CheckboxWidget) and widget.is_checked():
                selected_items.append(widget.get_text())
        
        if selected_items:
            message = "选中的项目:\n" + "\n".join(selected_items)
        else:
            message = "没有选中任何项目"
        
        QMessageBox.information(self, "选中项目", message)
        print(f"选中的项目: {selected_items}")
    
    def add_new_item(self) -> None:
        """添加新项目."""
        row_count = self.model.rowCount()
        new_text = f"新项目 {row_count + 1}"
        
        # 添加到数据
        self.items_data.append({"text": new_text, "checked": False})
        
        # 添加到模型
        item = QStandardItem(new_text)
        self.model.appendRow(item)
        
        # 为新项目设置控件
        index = self.model.index(row_count, 0)
        widget = CheckboxWidget(text=new_text, checked=False)
        
        # 设置ListView和模型索引引用，用于双向同步
        widget.list_view = self.list_view
        widget.model_index = index
        
        self.list_view.setIndexWidget(index, widget)
        
        print(f"已添加新项目: {new_text}")
    
    def on_selection_changed(self, selected, deselected) -> None:
        """处理ListView选择变化事件.
        
        Args:
            selected: 新选中的项目
            deselected: 取消选中的项目
        """
        # 处理新选中的项目
        for index in selected.indexes():
            widget = self.list_view.indexWidget(index)
            if isinstance(widget, CheckboxWidget):
                widget.set_checked(True)
        
        # 处理取消选中的项目
        for index in deselected.indexes():
            widget = self.list_view.indexWidget(index)
            if isinstance(widget, CheckboxWidget):
                widget.set_checked(False)


def main():
    """主函数."""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    window = ListViewDemo()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()