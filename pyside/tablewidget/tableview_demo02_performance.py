import sys
from typing import Dict, List, Any, Set
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget,
    QTableWidgetItem, QCheckBox, QLineEdit, QComboBox, QHeaderView,
    QAbstractItemView, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont


class PerformanceTableWidget(QTableWidget):
    """高性能表格控件 - 使用最小化控件创建和延迟加载."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.expanded_rows: Set[str] = set()
        self.all_data: List[Dict[str, Any]] = []
        self.visible_items: List[Dict[str, Any]] = []
        self.widget_cache: Dict[int, Dict[int, QWidget]] = {}  # 控件缓存
        self.pending_updates: Set[int] = set()  # 待更新的行
        
        # 性能优化设置
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        
        # 延迟更新定时器
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.process_pending_updates)
        
        self.setup_table()
        self.generate_test_data()
        self.build_table_fast()
        
        # 连接信号
        self.cellClicked.connect(self.on_cell_clicked)
    
    def setup_table(self) -> None:
        """设置表格基本属性."""
        headers = ['Name', 'Value1', 'Check1', 'Check2', 'Check3', 'Check4', 'Count', 'Value2', 'Value3']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # 设置列宽
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(len(headers)):
            if i == 0:
                self.setColumnWidth(i, 200)
            else:
                self.setColumnWidth(i, 80)
    
    def generate_test_data(self) -> None:
        """生成测试数据."""
        self.all_data.clear()
        
        # 生成父行和子行
        for i in range(50):  # 50个父行
            parent_name = f'Parent_{i:03d}'
            self.all_data.append({
                'name': parent_name,
                'type': 'parent',
                'data': [parent_name, '1.000', True, False, True, False, '5', '1.500', '2.000'],
                'row_id': f'parent_{i}'
            })
            
            # 每个父行100个子行
            for j in range(100):
                child_name = f'Child_{i:03d}_{j:03d}'
                self.all_data.append({
                    'name': child_name,
                    'type': 'child',
                    'parent': parent_name,
                    'data': [f'  {child_name}', '0.500', False, False, False, False, '0', '0.000', '0.000'],
                    'row_id': f'child_{i}_{j}'
                })
    
    def refresh_visible_items(self) -> None:
        """刷新可见项列表."""
        self.visible_items.clear()
        for item in self.all_data:
            if item['type'] == 'parent':
                self.visible_items.append(item)
                # 如果展开，添加子项
                if item['name'] in self.expanded_rows:
                    for child_item in self.all_data:
                        if (child_item['type'] == 'child' and 
                            child_item.get('parent') == item['name']):
                            self.visible_items.append(child_item)
    
    def build_table_fast(self) -> None:
        """快速构建表格 - 只创建文本项."""
        self.setUpdatesEnabled(False)
        self.refresh_visible_items()
        
        # 清除现有内容
        self.clearContents()
        self.setRowCount(len(self.visible_items))
        
        # 只创建文本项，不创建控件
        for row, item in enumerate(self.visible_items):
            self.create_text_items_only(row, item)
        
        self.setUpdatesEnabled(True)
    
    def create_text_items_only(self, row: int, item: Dict[str, Any]) -> None:
        """只创建文本项，不创建控件 - 最快的方式."""
        data = item['data']
        
        # 第一列：名称和展开图标
        first_col_text = data[0]
        if item['type'] == 'parent':
            icon = '▼ ' if item['name'] in self.expanded_rows else '▶ '
            first_col_text = icon + first_col_text
        
        first_item = QTableWidgetItem(first_col_text)
        first_item.setFlags(first_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row, 0, first_item)
        
        # 其他列：全部使用文本项
        for col in range(1, 9):
            if col in [2, 3, 4, 5]:  # 复选框列显示为文本
                text = '☑' if data[col] else '☐'
            else:
                text = str(data[col])
            
            item_widget = QTableWidgetItem(text)
            if col in [2, 3, 4, 5]:  # 复选框列可点击
                item_widget.setFlags(item_widget.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item_widget.setCheckState(Qt.CheckState.Checked if data[col] else Qt.CheckState.Unchecked)
            else:
                item_widget.setFlags(item_widget.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            self.setItem(row, col, item_widget)
    
    def create_widgets_for_row(self, row: int) -> None:
        """为指定行创建实际的控件 - 延迟创建."""
        if row >= len(self.visible_items):
            return
        
        item = self.visible_items[row]
        data = item['data']
        
        # 缓存检查
        if row in self.widget_cache:
            return
        
        self.widget_cache[row] = {}
        
        # 只为需要交互的列创建控件
        for col in range(1, 9):
            if col in [1, 7, 8]:  # 文本输入框列
                widget = QLineEdit(str(data[col]))
                widget.textChanged.connect(lambda text, r=row, c=col: self.on_line_edit_changed(r, c, text))
                self.setCellWidget(row, col, widget)
                self.widget_cache[row][col] = widget
            
            elif col == 6:  # 下拉框列
                widget = QComboBox()
                widget.addItems(['0', '1', '2', '3', '4', '5'])
                widget.setCurrentText(str(data[col]))
                widget.currentTextChanged.connect(lambda text, r=row, c=col: self.on_combo_changed(r, c, text))
                self.setCellWidget(row, col, widget)
                self.widget_cache[row][col] = widget
    
    def on_cell_clicked(self, row: int, column: int) -> None:
        """处理单元格点击事件."""
        if row >= len(self.visible_items):
            return
        
        item = self.visible_items[row]
        
        # 处理父行展开/折叠
        if item['type'] == 'parent' and column == 0:
            parent_name = item['name']
            
            # 切换展开状态
            if parent_name in self.expanded_rows:
                self.expanded_rows.remove(parent_name)
            else:
                self.expanded_rows.add(parent_name)
            
            # 超快速更新
            self.update_table_instantly(parent_name, row)
        
        # 处理复选框点击
        elif column in [2, 3, 4, 5]:
            table_item = self.item(row, column)
            if table_item:
                # 切换复选框状态
                current_state = table_item.checkState()
                new_state = Qt.CheckState.Unchecked if current_state == Qt.CheckState.Checked else Qt.CheckState.Checked
                table_item.setCheckState(new_state)
                
                # 更新数据
                item['data'][column] = (new_state == Qt.CheckState.Checked)
        
        # 为点击的行创建控件（如果需要）
        elif column in [1, 6, 7, 8]:
            self.schedule_widget_creation(row)
    
    def update_table_instantly(self, parent_name: str, parent_row: int) -> None:
        """瞬时更新表格."""
        self.setUpdatesEnabled(False)
        
        if parent_name in self.expanded_rows:
            # 展开：插入子行
            child_items = [item for item in self.all_data 
                          if item['type'] == 'child' and item.get('parent') == parent_name]
            
            # 批量插入
            insert_position = parent_row + 1
            for i, child_item in enumerate(child_items):
                self.insertRow(insert_position + i)
                self.create_text_items_only(insert_position + i, child_item)
            
            # 更新父行图标
            parent_item = self.item(parent_row, 0)
            if parent_item:
                text = parent_item.text().replace('▶ ', '▼ ')
                parent_item.setText(text)
        else:
            # 折叠：删除子行
            child_count = sum(1 for item in self.all_data 
                            if item['type'] == 'child' and item.get('parent') == parent_name)
            
            # 批量删除
            for _ in range(child_count):
                if parent_row + 1 < self.rowCount():
                    self.removeRow(parent_row + 1)
            
            # 更新父行图标
            parent_item = self.item(parent_row, 0)
            if parent_item:
                text = parent_item.text().replace('▼ ', '▶ ')
                parent_item.setText(text)
        
        # 清除相关缓存
        self.clear_cache_after_row(parent_row)
        
        self.setUpdatesEnabled(True)
        self.refresh_visible_items()
    
    def schedule_widget_creation(self, row: int) -> None:
        """调度控件创建."""
        self.pending_updates.add(row)
        self.update_timer.start(50)  # 50ms延迟
    
    def process_pending_updates(self) -> None:
        """处理待更新的行."""
        for row in self.pending_updates:
            self.create_widgets_for_row(row)
        self.pending_updates.clear()
    
    def clear_cache_after_row(self, row: int) -> None:
        """清除指定行之后的缓存."""
        rows_to_remove = [r for r in self.widget_cache.keys() if r > row]
        for r in rows_to_remove:
            del self.widget_cache[r]
    
    # 事件处理方法
    def on_line_edit_changed(self, row: int, column: int, text: str) -> None:
        """处理文本框变化."""
        if row < len(self.visible_items):
            self.visible_items[row]['data'][column] = text
    
    def on_combo_changed(self, row: int, column: int, text: str) -> None:
        """处理下拉框变化."""
        if row < len(self.visible_items):
            self.visible_items[row]['data'][column] = text


class MainWindow(QMainWindow):
    """主窗口."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('高性能表格演示 - 虚拟化 + 延迟加载')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加说明标签
        info_label = QLabel(
            '高性能优化策略：\n'
            '1. 只创建文本项，延迟创建控件\n'
            '2. 复选框使用原生TableWidgetItem\n'
            '3. 批量操作和最小化重绘\n'
            '4. 智能缓存管理\n'
            '测试：50个父行，每个包含100个子行（共5050行数据）'
        )
        info_label.setStyleSheet('background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;')
        layout.addWidget(info_label)
        
        # 创建表格
        self.table = PerformanceTableWidget()
        layout.addWidget(self.table)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()