#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义表格Demo
实现可通过接口设置全表数据的PySide表格组件
"""

import sys
from typing import List, Dict, Any, Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class CustomTableWidget(QTableWidget):
    """
    自定义表格组件
    提供接口用于设置全表数据
    """
    
    # 信号定义
    data_changed = Signal()  # 数据变更信号
    cell_clicked_signal = Signal(int, int, str)  # 单元格点击信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """初始化UI设置"""
        # 设置表格基本属性
        self.setAlternatingRowColors(True)  # 交替行颜色
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选择整行
        self.setSelectionMode(QAbstractItemView.SingleSelection)  # 单选模式
        
        # 设置表头
        self.horizontalHeader().setStretchLastSection(True)  # 最后一列自动拉伸
        self.verticalHeader().setVisible(False)  # 隐藏行号
        
        # 设置字体
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        
    def _connect_signals(self):
        """连接信号槽"""
        self.cellClicked.connect(self._on_cell_clicked)
        self.itemChanged.connect(self._on_item_changed)
        
    def _on_cell_clicked(self, row: int, column: int):
        """单元格点击事件"""
        item = self.item(row, column)
        text = item.text() if item else ""
        self.cell_clicked_signal.emit(row, column, text)
        
    def _on_item_changed(self, item: QTableWidgetItem):
        """数据项变更事件"""
        self.data_changed.emit()
    
    def set_table_data(self, headers: List[str], data: List[List[Any]], 
                      editable: bool = True) -> bool:
        """
        设置表格数据的主要接口
        
        Args:
            headers: 表头列表
            data: 数据列表，每个元素为一行数据
            editable: 是否可编辑
            
        Returns:
            bool: 设置是否成功
        """
        try:
            if not headers:
                return False
                
            # 设置表格尺寸
            self.setRowCount(len(data))
            self.setColumnCount(len(headers))
            
            # 设置表头
            self.setHorizontalHeaderLabels(headers)
            
            # 填充数据
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    if col_idx < len(headers):  # 防止数据超出列数
                        item = QTableWidgetItem(str(cell_data))
                        
                        # 设置是否可编辑
                        if not editable:
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                            
                        self.setItem(row_idx, col_idx, item)
            
            # 调整列宽
            self.resizeColumnsToContents()
            return True
            
        except Exception as e:
            print(f"设置表格数据失败: {e}")
            return False
    
    def append_row(self, row_data: List[Any]) -> bool:
        """
        追加一行数据
        
        Args:
            row_data: 行数据列表
            
        Returns:
            bool: 追加是否成功
        """
        try:
            row_count = self.rowCount()
            self.insertRow(row_count)
            
            for col_idx, cell_data in enumerate(row_data):
                if col_idx < self.columnCount():
                    item = QTableWidgetItem(str(cell_data))
                    self.setItem(row_count, col_idx, item)
            
            return True
        except Exception as e:
            print(f"追加行数据失败: {e}")
            return False
    
    def update_cell(self, row: int, column: int, value: Any) -> bool:
        """
        更新指定单元格数据
        
        Args:
            row: 行索引
            column: 列索引
            value: 新值
            
        Returns:
            bool: 更新是否成功
        """
        try:
            if 0 <= row < self.rowCount() and 0 <= column < self.columnCount():
                item = self.item(row, column)
                if item:
                    item.setText(str(value))
                else:
                    new_item = QTableWidgetItem(str(value))
                    self.setItem(row, column, new_item)
                return True
            return False
        except Exception as e:
            print(f"更新单元格失败: {e}")
            return False
    
    def get_table_data(self) -> Dict[str, Any]:
        """
        获取表格所有数据
        
        Returns:
            dict: 包含表头和数据的字典
        """
        try:
            # 获取表头
            headers = []
            for col in range(self.columnCount()):
                header_item = self.horizontalHeaderItem(col)
                headers.append(header_item.text() if header_item else f"Column {col}")
            
            # 获取数据
            data = []
            for row in range(self.rowCount()):
                row_data = []
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            
            return {
                "headers": headers,
                "data": data,
                "row_count": self.rowCount(),
                "column_count": self.columnCount()
            }
        except Exception as e:
            print(f"获取表格数据失败: {e}")
            return {}
    
    def clear_table(self):
        """清空表格数据"""
        self.setRowCount(0)
        self.setColumnCount(0)
    
    def set_column_width(self, column: int, width: int):
        """设置指定列宽度"""
        if 0 <= column < self.columnCount():
            self.setColumnWidth(column, width)
    
    def set_row_height(self, row: int, height: int):
        """设置指定行高度"""
        if 0 <= row < self.rowCount():
            self.setRowHeight(row, height)


class MainWindow(QMainWindow):
    """
    主窗口类 - 演示自定义表格的使用
    """
    
    def __init__(self):
        super().__init__()
        self.custom_table = None
        self._setup_ui()
        self._setup_demo_data()
        
    def _setup_ui(self):
        """初始化UI"""
        self.setWindowTitle("自定义表格Demo")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建按钮
        self.btn_load_data1 = QPushButton("加载示例数据1")
        self.btn_load_data2 = QPushButton("加载示例数据2")
        self.btn_append_row = QPushButton("追加行")
        self.btn_clear = QPushButton("清空表格")
        self.btn_get_data = QPushButton("获取数据")
        
        button_layout.addWidget(self.btn_load_data1)
        button_layout.addWidget(self.btn_load_data2)
        button_layout.addWidget(self.btn_append_row)
        button_layout.addWidget(self.btn_clear)
        button_layout.addWidget(self.btn_get_data)
        button_layout.addStretch()
        
        # 创建自定义表格
        self.custom_table = CustomTableWidget()
        
        # 添加到主布局
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.custom_table)
        
        # 连接信号
        self._connect_signals()
    
    def _connect_signals(self):
        """连接信号槽"""
        self.btn_load_data1.clicked.connect(self._load_demo_data1)
        self.btn_load_data2.clicked.connect(self._load_demo_data2)
        self.btn_append_row.clicked.connect(self._append_demo_row)
        self.btn_clear.clicked.connect(self._clear_table)
        self.btn_get_data.clicked.connect(self._show_table_data)
        
        # 连接表格信号
        self.custom_table.cell_clicked_signal.connect(self._on_cell_clicked)
        self.custom_table.data_changed.connect(self._on_data_changed)
    
    def _setup_demo_data(self):
        """设置演示数据"""
        self._load_demo_data1()
    
    def _load_demo_data1(self):
        """加载演示数据1 - 学生信息"""
        headers = ["学号", "姓名", "年龄", "专业", "成绩"]
        data = [
            ["2021001", "张三", 20, "计算机科学", 85.5],
            ["2021002", "李四", 21, "软件工程", 92.0],
            ["2021003", "王五", 19, "数据科学", 78.5],
            ["2021004", "赵六", 22, "人工智能", 88.0],
            ["2021005", "钱七", 20, "网络安全", 95.5]
        ]
        
        success = self.custom_table.set_table_data(headers, data, editable=True)
        if success:
            print("演示数据1加载成功")
    
    def _load_demo_data2(self):
        """加载演示数据2 - 产品信息"""
        headers = ["产品ID", "产品名称", "价格", "库存", "分类"]
        data = [
            ["P001", "笔记本电脑", 5999.00, 50, "电子产品"],
            ["P002", "无线鼠标", 99.00, 200, "电脑配件"],
            ["P003", "机械键盘", 299.00, 80, "电脑配件"],
            ["P004", "显示器", 1299.00, 30, "电子产品"],
            ["P005", "耳机", 199.00, 150, "音频设备"]
        ]
        
        success = self.custom_table.set_table_data(headers, data, editable=True)
        if success:
            print("演示数据2加载成功")
    
    def _append_demo_row(self):
        """追加演示行"""
        import random
        
        # 根据当前表格内容决定追加什么数据
        if self.custom_table.columnCount() == 5:
            header_item = self.custom_table.horizontalHeaderItem(0)
            if header_item and "学号" in header_item.text():
                # 学生数据
                new_row = [f"202100{random.randint(6, 99)}", f"学生{random.randint(1, 100)}", 
                          random.randint(18, 25), "新专业", round(random.uniform(60, 100), 1)]
            else:
                # 产品数据
                new_row = [f"P00{random.randint(6, 99)}", f"新产品{random.randint(1, 100)}", 
                          round(random.uniform(50, 2000), 2), random.randint(10, 200), "新分类"]
            
            success = self.custom_table.append_row(new_row)
            if success:
                print("追加行成功")
    
    def _clear_table(self):
        """清空表格"""
        self.custom_table.clear_table()
        print("表格已清空")
    
    def _show_table_data(self):
        """显示表格数据"""
        data = self.custom_table.get_table_data()
        if data:
            msg = f"表格数据:\n"
            msg += f"行数: {data['row_count']}\n"
            msg += f"列数: {data['column_count']}\n"
            msg += f"表头: {', '.join(data['headers'])}\n"
            msg += f"数据行数: {len(data['data'])}"
            
            QMessageBox.information(self, "表格数据信息", msg)
            
            # 在控制台打印详细数据
            print("\n=== 表格详细数据 ===")
            print(f"表头: {data['headers']}")
            for i, row in enumerate(data['data']):
                print(f"第{i+1}行: {row}")
    
    def _on_cell_clicked(self, row: int, column: int, text: str):
        """单元格点击事件"""
        print(f"点击单元格: 行{row+1}, 列{column+1}, 内容: {text}")
    
    def _on_data_changed(self):
        """数据变更事件"""
        print("表格数据已变更")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()