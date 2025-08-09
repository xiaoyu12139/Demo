#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 TableView 演示程序
功能包括：
- 显示表格数据
- 添加/删除行
- 编辑单元格
- 排序功能
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QTableView, QPushButton, QHeaderView,
    QMessageBox, QInputDialog, QLineEdit
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QFont


class TableModel(QAbstractTableModel):
    """自定义表格数据模型"""
    
    def __init__(self, data=None):
        super().__init__()
        self.headers = ['姓名', '年龄', '职业', '城市', '薪资']
        self.table_data = data or [
            ['张三', 25, '软件工程师', '北京', 15000],
            ['李四', 30, '产品经理', '上海', 18000],
            ['王五', 28, '设计师', '深圳', 12000],
            ['赵六', 35, '项目经理', '广州', 20000],
            ['钱七', 26, '测试工程师', '杭州', 13000],
        ]
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.table_data)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return str(self.table_data[index.row()][index.column()])
        
        if role == Qt.TextAlignmentRole:
            # 所有文本居中对齐
            return Qt.AlignCenter
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            else:
                return str(section + 1)
        return None
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
    
    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False
        
        # 数据类型转换
        try:
            if index.column() == 1:  # 年龄列
                value = int(value)
            elif index.column() == 4:  # 薪资列
                value = int(value)
        except ValueError:
            return False
        
        self.table_data[index.row()][index.column()] = value
        self.dataChanged.emit(index, index, [Qt.DisplayRole])
        return True
    
    def insertRow(self, row, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.table_data.insert(row, ['新员工', 25, '职位', '城市', 10000])
        self.endInsertRows()
        return True
    
    def removeRow(self, row, parent=QModelIndex()):
        if 0 <= row < len(self.table_data):
            self.beginRemoveRows(parent, row, row)
            del self.table_data[row]
            self.endRemoveRows()
            return True
        return False


class TableViewDemo(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_model()
        self.setup_connections()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('PySide6 TableView 演示程序')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建表格视图
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)  # 启用排序
        self.table_view.setAlternatingRowColors(True)  # 交替行颜色
        self.table_view.setSelectionBehavior(QTableView.SelectRows)  # 选择整行
        
        # 设置字体
        font = QFont()
        font.setPointSize(10)
        self.table_view.setFont(font)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建按钮
        self.add_button = QPushButton('添加行')
        self.delete_button = QPushButton('删除行')
        self.clear_button = QPushButton('清空数据')
        self.refresh_button = QPushButton('刷新数据')
        
        # 添加按钮到布局
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()  # 添加弹性空间
        
        # 添加到主布局
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(button_layout)
    
    def setup_model(self):
        """设置数据模型"""
        self.model = TableModel()
        self.table_view.setModel(self.model)
        
        # 设置列宽
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 姓名列自适应
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 年龄列
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 职业列
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # 城市列
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 薪资列
    
    def setup_connections(self):
        """设置信号连接"""
        self.add_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_row)
        self.clear_button.clicked.connect(self.clear_data)
        self.refresh_button.clicked.connect(self.refresh_data)
    
    def add_row(self):
        """添加新行"""
        row_count = self.model.rowCount()
        self.model.insertRow(row_count)
        
        # 选中新添加的行
        new_index = self.model.index(row_count, 0)
        self.table_view.setCurrentIndex(new_index)
        self.table_view.scrollTo(new_index)
    
    def delete_row(self):
        """删除选中的行"""
        current_index = self.table_view.currentIndex()
        if current_index.isValid():
            row = current_index.row()
            reply = QMessageBox.question(
                self, '确认删除', 
                f'确定要删除第 {row + 1} 行数据吗？',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.model.removeRow(row)
        else:
            QMessageBox.information(self, '提示', '请先选择要删除的行')
    
    def clear_data(self):
        """清空所有数据"""
        reply = QMessageBox.question(
            self, '确认清空', 
            '确定要清空所有数据吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.model.beginResetModel()
            self.model.table_data.clear()
            self.model.endResetModel()
    
    def refresh_data(self):
        """刷新数据到初始状态"""
        initial_data = [
            ['张三', 25, '软件工程师', '北京', 15000],
            ['李四', 30, '产品经理', '上海', 18000],
            ['王五', 28, '设计师', '深圳', 12000],
            ['赵六', 35, '项目经理', '广州', 20000],
            ['钱七', 26, '测试工程师', '杭州', 13000],
        ]
        
        self.model.beginResetModel()
        self.model.table_data = initial_data
        self.model.endResetModel()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName('TableView Demo')
    app.setApplicationVersion('1.0')
    
    # 创建并显示主窗口
    window = TableViewDemo()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == '__main__':
    main()