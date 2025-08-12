#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TableWidget自定义表头演示程序

这个演示展示了如何在PySide6中使用QTableWidget并实现自定义表头功能。
包含以下特性：
- 自定义表头视图
- 表头复选框功能
- 表格数据展示
- 响应式布局
"""

import sys
from typing import Optional, Dict, Set
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QHeaderView, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox,
    QFrame, QAbstractItemView
)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QFont, QPalette


class CustomHeaderView(QHeaderView):
    """自定义表头视图类
    
    提供带复选框的表头功能，支持全选/取消全选操作。
    """
    
    def __init__(self, orientation: Qt.Orientation, parent: Optional[QWidget] = None):
        """初始化自定义表头视图
        
        Args:
            orientation: 表头方向（水平或垂直）
            parent: 父组件
        """
        super().__init__(orientation, parent)
        
        # 设置表头属性
        # self.setSectionsClickable(True)
        # self.setSectionsMovable(False)
        # self.setDefaultSectionSize(120)
        
        # 定义需要复选框的列
        self.checkbox_columns: Set[int] = {1, 2, 3}  # 第1、2、3列有复选框
        
        # 存储复选框状态
        self.checkbox_states: Dict[int, bool] = {}
        for col in self.checkbox_columns:
            self.checkbox_states[col] = False
        
        # 存储复选框区域用于点击检测
        self.checkbox_rects: Dict[int, QRect] = {}
    
    def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
        """绘制表头区域
        
        Args:
            painter: 绘制器
            rect: 绘制区域
            logicalIndex: 逻辑列索引
        """
        painter.save()
        
        # 获取表头文本
        text = self.model().headerData(logicalIndex, self.orientation(), Qt.ItemDataRole.DisplayRole)
        
        # 绘制背景
        painter.fillRect(rect, self.palette().button())
        
        # 绘制边框
        painter.setPen(self.palette().dark().color())
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
        
        # 设置文本颜色
        painter.setPen(self.palette().buttonText().color())
        
        if logicalIndex in self.checkbox_columns:
            # 有复选框的列：绘制复选框和文本
            self._draw_checkbox(painter, rect, logicalIndex)
            # 文本右移为复选框留空间
            text_rect = rect.adjusted(25, 0, 0, 0)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, str(text))
        else:
            # 普通列：居中绘制文本
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(text))
        
        painter.restore()
    
    def _draw_checkbox(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
        """绘制复选框
        
        Args:
            painter: 绘制器
            rect: 表头区域
            logicalIndex: 列索引
        """
        # 复选框参数
        checkbox_size = 16
        margin = 5
        
        # 计算复选框位置
        checkbox_x = rect.left() + margin
        checkbox_y = rect.center().y() - checkbox_size // 2
        checkbox_rect = QRect(checkbox_x, checkbox_y, checkbox_size, checkbox_size)
        
        # 保存复选框区域用于点击检测
        self.checkbox_rects[logicalIndex] = checkbox_rect
        
        # 绘制复选框边框
        painter.setPen(self.palette().dark().color())
        painter.drawRect(checkbox_rect)
        
        # 如果选中，绘制勾选标记
        if self.checkbox_states.get(logicalIndex, False):
            painter.fillRect(checkbox_rect.adjusted(2, 2, -2, -2), self.palette().highlight())
            # 绘制简单的勾选标记
            painter.setPen(self.palette().highlightedText().color())
            painter.drawLine(
                checkbox_rect.left() + 4, checkbox_rect.center().y(),
                checkbox_rect.center().x(), checkbox_rect.bottom() - 4
            )
            painter.drawLine(
                checkbox_rect.center().x(), checkbox_rect.bottom() - 4,
                checkbox_rect.right() - 3, checkbox_rect.top() + 3
            )
    
    def mousePressEvent(self, event) -> None:
        """处理鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            logical_index = self.logicalIndexAt(event.position().toPoint())
            
            # 检查是否点击了复选框
            if logical_index in self.checkbox_columns:
                checkbox_rect = self.checkbox_rects.get(logical_index)
                if checkbox_rect and checkbox_rect.contains(event.position().toPoint()):
                    # 切换复选框状态
                    self.checkbox_states[logical_index] = not self.checkbox_states.get(logical_index, False)
                    
                    # 通知父组件状态变化
                    if hasattr(self.parent(), 'on_header_checkbox_changed'):
                        self.parent().on_header_checkbox_changed(logical_index, self.checkbox_states[logical_index])
                    
                    # 重绘表头
                    self.viewport().update()
                    return
        
        super().mousePressEvent(event)


class CustomTableWidget(QTableWidget):
    """自定义表格组件
    
    使用自定义表头视图的QTableWidget。
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """初始化自定义表格"""
        super().__init__(parent)
        
        # 设置自定义表头
        custom_header = CustomHeaderView(Qt.Orientation.Horizontal, self)
        self.setHorizontalHeader(custom_header)
        
        self._setup_table()
        self._setup_data()
    
    def _setup_table(self) -> None:
        """设置表格属性"""
        # 设置列数和表头标签
        self.setColumnCount(5)
        headers = ['姓名', '数学', '英语', '物理', '总分']
        self.setHorizontalHeaderLabels(headers)
        
        # 设置表格属性
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        
        # 设置列宽
        self.setColumnWidth(0, 100)  # 姓名列
        self.setColumnWidth(1, 80)   # 数学列
        self.setColumnWidth(2, 80)   # 英语列
        self.setColumnWidth(3, 80)   # 物理列
        self.setColumnWidth(4, 80)   # 总分列
        
        # 设置字体
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
    
    def _setup_data(self) -> None:
        """设置表格数据"""
        # 示例数据
        data = [
            ['张三', 85, 92, 78, 255],
            ['李四', 90, 88, 85, 263],
            ['王五', 78, 95, 82, 255],
            ['赵六', 92, 87, 90, 269],
            ['钱七', 88, 91, 86, 265],
            ['孙八', 85, 89, 88, 262],
            ['周九', 91, 93, 87, 271],
            ['吴十', 87, 85, 89, 261]
        ]
        
        # 设置行数
        self.setRowCount(len(data))
        
        # 填充数据
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                if col >= 1 and col <= 3:  # 成绩列添加复选框
                    # 创建包含复选框的单元格
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    layout.setContentsMargins(5, 0, 5, 0)
                    
                    checkbox = QCheckBox()
                    checkbox.setChecked(value >= 85)  # 85分以上默认选中
                    
                    label = QLabel(str(value))
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    layout.addWidget(checkbox)
                    layout.addWidget(label)
                    layout.addStretch()
                    
                    self.setCellWidget(row, col, widget)
                else:
                    # 普通文本单元格
                    item = self.item(row, col)
                    if item is None:
                        from PySide6.QtWidgets import QTableWidgetItem
                        item = QTableWidgetItem()
                        self.setItem(row, col, item)
                    item.setText(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def on_header_checkbox_changed(self, column: int, checked: bool) -> None:
        """处理表头复选框状态变化
        
        Args:
            column: 列索引
            checked: 是否选中
        """
        print(f"表头复选框变化 - 列: {column}, 选中: {checked}")
        
        # 遍历所有行，设置对应列的复选框状态
        for row in range(self.rowCount()):
            widget = self.cellWidget(row, column)
            if widget:
                # 查找复选框组件
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(checked)


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.setWindowTitle('TableWidget自定义表头演示')
        self.setGeometry(100, 100, 600, 400)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 添加标题
        title_label = QLabel('学生成绩表 - 自定义表头演示')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # 添加说明
        info_label = QLabel('点击表头的复选框可以全选/取消全选对应列的所有复选框')
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet('color: #666666; margin: 5px;')
        main_layout.addWidget(info_label)
        
        # 创建表格
        self.table = CustomTableWidget()
        main_layout.addWidget(self.table)
        
        # 添加按钮区域
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton('刷新数据')
        refresh_btn.clicked.connect(self._refresh_data)
        button_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton('清除选择')
        clear_btn.clicked.connect(self._clear_selection)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        
        info_btn = QPushButton('关于')
        info_btn.clicked.connect(self._show_info)
        button_layout.addWidget(info_btn)
        
        main_layout.addLayout(button_layout)
    
    def _refresh_data(self) -> None:
        """刷新表格数据"""
        self.table._setup_data()
        print('数据已刷新')
    
    def _clear_selection(self) -> None:
        """清除所有选择"""
        # 清除表头复选框
        header = self.table.horizontalHeader()
        if isinstance(header, CustomHeaderView):
            for col in header.checkbox_columns:
                header.checkbox_states[col] = False
            header.viewport().update()
        
        # 清除单元格复选框
        for row in range(self.table.rowCount()):
            for col in range(1, 4):  # 成绩列
                widget = self.table.cellWidget(row, col)
                if widget:
                    checkbox = widget.findChild(QCheckBox)
                    if checkbox:
                        checkbox.setChecked(False)
        
        print('已清除所有选择')
    
    def _show_info(self) -> None:
        """显示关于信息"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            '关于',
            'TableWidget自定义表头演示\n\n'
            '功能特性：\n'
            '• 自定义表头视图\n'
            '• 表头复选框功能\n'
            '• 全选/取消全选\n'
            '• 响应式布局\n\n'
            '使用PySide6开发'
        )


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == '__main__':
    main()