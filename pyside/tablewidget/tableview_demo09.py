#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TableView with Custom HeaderView Demo
自定义HeaderView的TableView示例
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QTableView, QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtWidgets import QStyle, QStyleOptionHeader


class CustomTableModel(QAbstractTableModel):
    """自定义表格模型"""
    
    def __init__(self):
        super().__init__()
        self.headers = ["Name", "Age", "City", "Email", "Phone"]
        self.data_list = [
            ["Alice", "25", "New York", "alice@email.com", "123-456-7890"],
            ["Bob", "30", "Los Angeles", "bob@email.com", "098-765-4321"],
            ["Charlie", "35", "Chicago", "charlie@email.com", "555-123-4567"],
            ["Diana", "28", "Houston", "diana@email.com", "777-888-9999"],
            ["Eve", "32", "Phoenix", "eve@email.com", "111-222-3333"]
        ]
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.data_list)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole:
            return self.data_list[index.row()][index.column()]
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None


class CustomHeaderView(QHeaderView):
    """自定义水平表头视图"""
    
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setDefaultSectionSize(120)
        self.setMinimumSectionSize(80)
        self.setSectionResizeMode(QHeaderView.Interactive)
        
    def paintSection(self, painter, rect, logicalIndex):
        """重写paintSection方法，使用style().drawControl绘制表头"""
        painter.save()
        
        # 获取表头文本
        text = self.model().headerData(logicalIndex, self.orientation(), Qt.DisplayRole)
        if text is None:
            text = ""
        
        # 设置绘制选项
        option = QStyleOptionHeader()
        option.rect = rect
        option.text = str(text)
        option.textAlignment = Qt.AlignCenter
        option.state = QStyle.State_Enabled
        
        # 检查是否为当前选中的列
        if self.parent() and hasattr(self.parent(), 'currentIndex'):
            current_column = self.parent().currentIndex().column()
            if logicalIndex == current_column:
                option.state |= QStyle.State_Selected
        
        # 检查鼠标悬停状态
        if self.logicalIndexAt(self.mapFromGlobal(self.cursor().pos())) == logicalIndex:
            option.state |= QStyle.State_MouseOver
        
        # 设置表头方向
        option.orientation = self.orientation()
        option.position = QStyleOptionHeader.Middle
        
        # 设置第一个和最后一个表头的位置
        if logicalIndex == 0:
            option.position = QStyleOptionHeader.Beginning
        elif logicalIndex == self.count() - 1:
            option.position = QStyleOptionHeader.End
        
        # 使用系统样式绘制表头
        self.style().drawControl(self.style().CE_Header, option, painter, self)
        
        painter.restore()


class TableViewDemo(QMainWindow):
    """TableView演示主窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("TableView with Custom HeaderView Demo")
        self.setGeometry(100, 100, 800, 600)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTableView {
                background-color: white;
                alternate-background-color: #f8f8f8;
                selection-background-color: #3daee9;
                selection-color: white;
                gridline-color: #d0d0d0;
                border: 1px solid #c0c0c0;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                border: 1px solid #c0c0c0;
                padding: 4px;
                font-weight: bold;
            }
            QHeaderView::section:hover {
                background-color: #d0d0d0;
            }
            QHeaderView::section:pressed {
                background-color: #c0c0c0;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建表格视图
        self.table_view = QTableView()
        
        # 创建并设置模型
        self.model = CustomTableModel()
        self.table_view.setModel(self.model)
        
        # 创建并设置自定义水平表头
        custom_header = CustomHeaderView(Qt.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(custom_header)
        
        # 设置表格属性
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSortingEnabled(True)
        
        # 调整列宽
        self.table_view.resizeColumnsToContents()
        
        # 添加到布局
        layout.addWidget(self.table_view)


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = TableViewDemo()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == '__main__':
    main()