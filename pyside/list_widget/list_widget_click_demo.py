#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QListWidget 单击和双击区分演示

功能特性:
1. 支持单击选择项目
2. 支持双击编辑项目
3. 区分单击和双击事件
4. 显示事件信息
5. 支持添加和删除项目
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QListWidget, QListWidgetItem,
    QLineEdit, QLabel, QTextEdit, QSplitter
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont


class ClickableListWidget(QListWidget):
    """支持单击和双击区分的QListWidget"""
    
    # 自定义信号
    item_single_clicked = Signal(QListWidgetItem)  # 单击信号
    item_double_clicked = Signal(QListWidgetItem)  # 双击信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 单击检测定时器
        self.click_timer = QTimer()
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self._handle_single_click)
        
        # 存储待处理的单击项目
        self.pending_click_item = None
        
        # 连接原始信号
        self.itemClicked.connect(self._on_item_clicked)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # 设置双击间隔时间（毫秒）
        self.double_click_interval = 300
        
    def _on_item_clicked(self, item):
        """处理项目点击事件"""
        # 存储点击的项目
        self.pending_click_item = item
        
        # 启动定时器，如果在指定时间内没有双击，则触发单击事件
        self.click_timer.start(self.double_click_interval)
        
    def _on_item_double_clicked(self, item):
        """处理项目双击事件"""
        # 停止单击定时器
        self.click_timer.stop()
        self.pending_click_item = None
        
        # 发射双击信号
        self.item_double_clicked.emit(item)
        
    def _handle_single_click(self):
        """处理单击事件（定时器超时后调用）"""
        if self.pending_click_item:
            # 发射单击信号
            self.item_single_clicked.emit(self.pending_click_item)
            self.pending_click_item = None


class ListWidgetDemo(QMainWindow):
    """QListWidget 演示主窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
        self.add_sample_data()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("QListWidget 单击双击演示")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧面板
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右侧面板
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割器比例
        splitter.setSizes([400, 400])
        
    def create_left_panel(self):
        """创建左侧面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title_label = QLabel("列表操作")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        # 添加项目区域
        add_layout = QHBoxLayout()
        self.add_input = QLineEdit()
        self.add_input.setPlaceholderText("输入新项目名称...")
        self.add_button = QPushButton("添加项目")
        add_layout.addWidget(self.add_input)
        add_layout.addWidget(self.add_button)
        layout.addLayout(add_layout)
        
        # 列表控件
        self.list_widget = ClickableListWidget()
        self.list_widget.setAlternatingRowColors(True)
        layout.addWidget(self.list_widget)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        self.delete_button = QPushButton("删除选中项")
        self.clear_button = QPushButton("清空列表")
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)
        
        return widget
        
    def create_right_panel(self):
        """创建右侧面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title_label = QLabel("事件日志")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        # 当前选中项显示
        self.current_item_label = QLabel("当前选中: 无")
        self.current_item_label.setStyleSheet(
            "QLabel { background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc; }"
        )
        layout.addWidget(self.current_item_label)
        
        # 事件日志
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_text)
        
        # 清空日志按钮
        self.clear_log_button = QPushButton("清空日志")
        layout.addWidget(self.clear_log_button)
        
        return widget
        
    def setup_connections(self):
        """设置信号连接"""
        # 按钮连接
        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_selected_item)
        self.clear_button.clicked.connect(self.clear_list)
        self.clear_log_button.clicked.connect(self.clear_log)
        
        # 输入框回车添加
        self.add_input.returnPressed.connect(self.add_item)
        
        # 列表事件连接
        self.list_widget.item_single_clicked.connect(self.on_item_single_clicked)
        self.list_widget.item_double_clicked.connect(self.on_item_double_clicked)
        self.list_widget.currentItemChanged.connect(self.on_current_item_changed)
        
    def add_sample_data(self):
        """添加示例数据"""
        sample_items = [
            "项目 1 - 单击选择，双击编辑",
            "项目 2 - 演示单击和双击区分",
            "项目 3 - 支持添加和删除",
            "项目 4 - 实时事件日志",
            "项目 5 - PySide6 QListWidget"
        ]
        
        for item_text in sample_items:
            self.list_widget.addItem(item_text)
            
        self.log_message("已添加示例数据")
        
    def add_item(self):
        """添加新项目"""
        text = self.add_input.text().strip()
        if text:
            self.list_widget.addItem(text)
            self.add_input.clear()
            self.log_message(f"添加项目: {text}")
        
    def delete_selected_item(self):
        """删除选中的项目"""
        current_item = self.list_widget.currentItem()
        if current_item:
            text = current_item.text()
            row = self.list_widget.row(current_item)
            self.list_widget.takeItem(row)
            self.log_message(f"删除项目: {text}")
        else:
            self.log_message("没有选中的项目")
            
    def clear_list(self):
        """清空列表"""
        count = self.list_widget.count()
        self.list_widget.clear()
        self.log_message(f"清空列表，共删除 {count} 个项目")
        self.current_item_label.setText("当前选中: 无")
        
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        
    def on_item_single_clicked(self, item):
        """处理项目单击事件"""
        self.log_message(f"单击: {item.text()}", "#0066cc")
        
    def on_item_double_clicked(self, item):
        """处理项目双击事件"""
        self.log_message(f"双击: {item.text()}", "#cc6600")
        
        # 双击进入编辑模式
        self.list_widget.editItem(item)
        self.log_message("进入编辑模式", "#009900")
        
    def on_current_item_changed(self, current, previous):
        """处理当前项目变更"""
        if current:
            self.current_item_label.setText(f"当前选中: {current.text()}")
            self.log_message(f"选中项目变更: {current.text()}", "#666666")
        else:
            self.current_item_label.setText("当前选中: 无")
            
    def log_message(self, message, color="#000000"):
        """记录日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 添加带颜色的日志
        html_message = f'<span style="color: {color}">[{timestamp}] {message}</span>'
        self.log_text.append(html_message)
        
        # 滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建并显示主窗口
    window = ListWidgetDemo()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()