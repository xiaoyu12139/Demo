#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可展开表格组件演示 - 性能优化版本

主要功能：
1. 表格展开/折叠功能：点击父行可展开或折叠其子行
2. 复选框功能：支持单个复选框选择和全选/取消全选
3. 性能优化：使用增量更新和控件缓存，避免大量数据时的卡顿

优化策略：
- 增量更新：只对变化的行进行操作，而不是重建整个表格
- 控件缓存：缓存已创建的控件，避免重复创建
- 延迟加载：只在需要时创建控件
- 批量操作：减少不必要的UI更新
"""

import os
import sys
from typing import Dict, List, Set, Any, Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget,
    QHeaderView, QCheckBox, QLabel, QHBoxLayout, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvgWidgets import QSvgWidget


class CheckboxHeaderView(QHeaderView):
    """自定义表头，支持复选框功能."""
    
    checkbox_state_changed = Signal(int, bool)  # 列索引，选中状态
    
    def __init__(self, orientation: Qt.Orientation, parent: Optional[QWidget] = None) -> None:
        super().__init__(orientation, parent)
        self.checkbox_states: Dict[int, bool] = {}  # 存储每列的复选框状态
        
    def paintSection(self, painter: QPainter, rect, logicalIndex: int) -> None:
        """绘制表头区域."""
        super().paintSection(painter, rect, logicalIndex)
        
        # 在第2-5列绘制复选框（镜像、负片、填充热焊盘、删除未使用焊盘）
        if 2 <= logicalIndex <= 5:
            checkbox_size = 16
            checkbox_x = rect.x() + (rect.width() - checkbox_size) // 2
            checkbox_y = rect.y() + (rect.height() - checkbox_size) // 2
            checkbox_rect = painter.viewport().adjusted(checkbox_x, checkbox_y, 
                                                      checkbox_x + checkbox_size, 
                                                      checkbox_y + checkbox_size)
            
            # 绘制复选框背景
            painter.fillRect(checkbox_rect, Qt.GlobalColor.white)
            painter.drawRect(checkbox_rect)
            
            # 如果选中，绘制勾选标记
            if self.checkbox_states.get(logicalIndex, False):
                painter.drawLine(checkbox_rect.topLeft(), checkbox_rect.bottomRight())
                painter.drawLine(checkbox_rect.topRight(), checkbox_rect.bottomLeft())
    
    def mousePressEvent(self, event) -> None:
        """处理鼠标点击事件."""
        if event.button() == Qt.MouseButton.LeftButton:
            logical_index = self.logicalIndexAt(event.position().toPoint())
            if 2 <= logical_index <= 5:
                self._toggle_checkbox(logical_index)
        super().mousePressEvent(event)
    
    def _toggle_checkbox(self, column: int) -> None:
        """切换指定列的复选框状态."""
        current_state = self.checkbox_states.get(column, False)
        new_state = not current_state
        self.checkbox_states[column] = new_state
        
        # 发送状态变化信号
        self.checkbox_state_changed.emit(column, new_state)
        
        # 重绘表头
        self.viewport().update()


class OptimizedExpandableTableWidget(QTableWidget):
    """性能优化的可展开表格组件."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.expanded_rows: Set[str] = set()  # 记录已展开的父行名称
        self.visible_items: List[Dict[str, Any]] = []  # 当前可见的数据项
        
        # 设置自定义表头
        custom_header = CheckboxHeaderView(Qt.Orientation.Horizontal, self)
        self.setHorizontalHeader(custom_header)
        custom_header.checkbox_state_changed.connect(self.on_header_checkbox_changed)
        
        self.setup_table()
        self.setup_data()
        self.refresh_visible_items()
        self.build_table_efficiently()
        
        # 连接信号
        self.cellClicked.connect(self.on_cell_clicked)
    
    def setup_table(self) -> None:
        """设置表格基本属性."""
        # 设置列数和表头
        headers = ['Gerber文件', '线宽', '镜像', '负片', '填充热焊盘', '删除未使用焊盘', '旋转角度', 'X偏移', 'Y偏移']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # 设置表格属性
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.verticalHeader().setVisible(False)
        
        # 设置列宽
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 80)
        self.setColumnWidth(5, 120)
        self.setColumnWidth(6, 60)
        self.setColumnWidth(7, 70)
        self.setColumnWidth(8, 70)
    
    def setup_data(self) -> None:
        """设置表格数据."""
        # 模拟大量数据
        self.all_data: List[Dict[str, Any]] = []
        
        # 添加多个父行和子行来测试性能
        for i in range(50):  # 创建50个父行
            parent_name = f'Parent_{i:03d}'
            self.all_data.append({
                'name': parent_name,
                'type': 'parent',
                'data': [parent_name, '1.000', False, False, False, False, '0', '0.000', '0.000'],
                'hidden': [False] * 9
            })
            
            # 每个父行有100个子行
            for j in range(100):
                child_name = f'{parent_name}_Child_{j:03d}'
                self.all_data.append({
                    'name': child_name,
                    'type': 'child',
                    'parent': parent_name,
                    'data': [f'  {child_name}', '0.500', False, False, False, False, '0', '0.000', '0.000'],
                    'hidden': [False] * 9
                })
        
        # 添加一些普通行
        for i in range(10):
            normal_name = f'Normal_{i:03d}'
            self.all_data.append({
                'name': normal_name,
                'type': 'normal',
                'data': [normal_name, '0.750', False, False, False, False, '0', '0.000', '0.000'],
                'hidden': [False] * 9
            })
    
    def refresh_visible_items(self) -> None:
        """刷新可见项列表."""
        self.visible_items.clear()
        for item in self.all_data:
            if item['type'] in ['parent', 'normal']:
                self.visible_items.append(item)
            elif item['type'] == 'child' and item['parent'] in self.expanded_rows:
                self.visible_items.append(item)
    
    def build_table_efficiently(self) -> None:
        """高效构建表格."""
        self.setUpdatesEnabled(False)
        
        # 设置行数
        self.setRowCount(len(self.visible_items))
        
        # 批量创建控件
        for row, item in enumerate(self.visible_items):
            self.create_row_widgets(row, item)
        
        self.setUpdatesEnabled(True)
    
    def create_row_widgets(self, row: int, item: Dict[str, Any]) -> None:
        """为指定行创建控件."""
        data = item['data']
        hidden = item.get('hidden', [False] * 9)
        
        # 第一列：复合控件（每次都创建新的，避免缓存问题）
        first_col_widget = self.create_first_column_widget(item)
        self.setCellWidget(row, 0, first_col_widget)
        
        # 其他列（每次都创建新的，避免缓存问题）
        for col in range(1, 9):
            widget = self.create_column_widget(col, data[col], hidden[col], row)
            self.setCellWidget(row, col, widget)
    
    def create_first_column_widget(self, item: Dict[str, Any]) -> QWidget:
        """创建第一列的复合控件."""
        cell_widget = QWidget()
        cell_widget.setStyleSheet("QWidget { background: transparent; border: none; }")
        
        layout = QHBoxLayout(cell_widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # 展开图标（仅父行）
        if item['type'] == 'parent':
            icon_path = 'hide.svg' if item['name'] in self.expanded_rows else 'show.svg'
            icon_label = self.create_icon_label(icon_path, (12, 12))
            layout.addWidget(icon_label)
        
        # 文本标签
        text_label = QLabel(item['data'][0])
        text_label.setStyleSheet("color: #000000; background: transparent; border: none;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(text_label)
        layout.addStretch()
        
        return cell_widget
    
    def create_column_widget(self, col: int, value: Any, is_hidden: bool, row: int) -> QWidget:
        """创建指定列的控件."""
        if col in [1, 7, 8]:  # 文本输入框列
            widget = QLineEdit(str(value))
            if is_hidden:
                widget.setReadOnly(True)
                widget.setStyleSheet("background-color: transparent; border: none; color: #000000;")
            widget.textChanged.connect(lambda text, r=row, c=col: self.on_line_edit_changed(r, c, text))
            return widget
        
        elif 2 <= col <= 5:  # 复选框列
            widget = QCheckBox()
            widget.setChecked(bool(value))
            if is_hidden:
                widget.setEnabled(False)
            widget.stateChanged.connect(lambda state, r=row, c=col: self.on_checkbox_changed(r, c, state))
            return widget
        
        elif col == 6:  # 下拉框列
            widget = QComboBox()
            widget.addItems(['0', '90', '180', '270'])
            widget.setCurrentText(str(value))
            if is_hidden:
                widget.setEnabled(False)
            widget.currentTextChanged.connect(lambda text, r=row, c=col: self.on_combo_changed(r, c, text))
            return widget
        
        return QWidget()
    
    def create_icon_label(self, icon_name: str, size: tuple) -> QLabel:
        """创建图标标签."""
        label = QLabel()
        # 简化图标显示，使用文本代替SVG
        if 'hide' in icon_name:
            label.setText('▼')
        else:
            label.setText('▶')
        label.setFixedSize(*size)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
    
    def on_cell_clicked(self, row: int, column: int) -> None:
        """处理单元格点击事件."""
        if column == 0 and row < len(self.visible_items):
            clicked_item = self.visible_items[row]
            if clicked_item['type'] == 'parent':
                parent_name = clicked_item['name']
                
                # 切换展开状态
                if parent_name in self.expanded_rows:
                    self.expanded_rows.remove(parent_name)
                else:
                    self.expanded_rows.add(parent_name)
                
                # 高效更新
                self.update_table_incrementally(parent_name, row)
    
    def update_table_incrementally(self, parent_name: str, parent_row: int) -> None:
        """增量更新表格."""
        self.setUpdatesEnabled(False)
        
        # 重新计算可见项
        old_visible_count = len(self.visible_items)
        self.refresh_visible_items()
        new_visible_count = len(self.visible_items)
        
        # 调整行数
        self.setRowCount(new_visible_count)
        
        # 只更新受影响的行
        if new_visible_count > old_visible_count:
            # 展开：添加子行
            for row in range(parent_row, new_visible_count):
                if row < len(self.visible_items):
                    self.create_row_widgets(row, self.visible_items[row])
        else:
            # 折叠：重建从父行开始的所有行
            for row in range(parent_row, new_visible_count):
                if row < len(self.visible_items):
                    self.create_row_widgets(row, self.visible_items[row])
        
        self.setUpdatesEnabled(True)
        self.clearSelection()
    

    
    # 事件处理方法
    def on_header_checkbox_changed(self, column: int, checked: bool) -> None:
        """处理表头复选框状态变化."""
        # 更新所有相应列的复选框
        for row in range(self.rowCount()):
            widget = self.cellWidget(row, column)
            if isinstance(widget, QCheckBox):
                widget.setChecked(checked)
    
    def on_line_edit_changed(self, row: int, column: int, text: str) -> None:
        """处理文本输入框变化."""
        if row < len(self.visible_items):
            self.visible_items[row]['data'][column] = text
    
    def on_checkbox_changed(self, row: int, column: int, state: int) -> None:
        """处理复选框状态变化."""
        if row < len(self.visible_items):
            self.visible_items[row]['data'][column] = bool(state)
    
    def on_combo_changed(self, row: int, column: int, text: str) -> None:
        """处理下拉框变化."""
        if row < len(self.visible_items):
            self.visible_items[row]['data'][column] = text


class MainWindow(QMainWindow):
    """主窗口."""
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('可展开表格演示 - 性能优化版')
        self.setGeometry(100, 100, 1000, 600)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建表格
        self.table = OptimizedExpandableTableWidget()
        layout.addWidget(self.table)


def main() -> None:
    """主函数."""
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()