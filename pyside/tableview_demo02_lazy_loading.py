import sys
from typing import Dict, List, Any, Set
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget,
    QTableWidgetItem, QCheckBox, QLineEdit, QComboBox, QHeaderView,
    QAbstractItemView, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont


class LazyLoadingTableWidget(QTableWidget):
    """延迟加载表格控件 - 创建完整控件但延迟加载.
    
    这个类实现了一个高性能的表格控件，通过延迟加载策略来优化大量数据的显示。
    初始时只创建占位符文本项，当行变为可见或被点击时才创建完整的交互控件。
    
    Attributes:
        expanded_rows (Set[str]): 已展开的父行名称集合
        all_data (List[Dict[str, Any]]): 所有数据的完整列表
        visible_items (List[Dict[str, Any]]): 当前可见项的列表
        widgets_created (Set[int]): 已创建完整控件的行号集合
        pending_widget_creation (Set[int]): 待创建控件的行号集合
        lazy_timer (QTimer): 延迟创建控件的定时器
        viewport_timer (QTimer): 视口变化检测定时器
    """
    
    def __init__(self, parent=None):
        """初始化延迟加载表格控件.
        
        Args:
            parent: 父控件，默认为None
        """
        super().__init__(parent)
        self.expanded_rows: Set[str] = set()
        self.all_data: List[Dict[str, Any]] = []
        self.visible_items: List[Dict[str, Any]] = []
        self.widgets_created: Set[int] = set()  # 已创建控件的行
        self.pending_widget_creation: Set[int] = set()  # 待创建控件的行
        
        # 性能优化设置
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        
        # 延迟加载定时器
        self.lazy_timer = QTimer()
        self.lazy_timer.setSingleShot(True)
        self.lazy_timer.timeout.connect(self.create_pending_widgets)
        
        # 视口变化检测定时器
        self.viewport_timer = QTimer()
        self.viewport_timer.timeout.connect(self.check_visible_rows)
        self.viewport_timer.start(100)  # 每100ms检查一次
        
        self.setup_table()
        self.generate_test_data()
        self.build_table_with_lazy_loading()
        
        # 连接信号
        self.cellClicked.connect(self.on_cell_clicked)
        self.verticalScrollBar().valueChanged.connect(self.on_scroll)
    
    def setup_table(self) -> None:
        """设置表格基本属性.
        
        配置表格的列标题、列宽和基本显示属性。
        设置9列：Name, Value1, Check1-4, Count, Value2, Value3。
        """
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
        """生成测试数据.
        
        创建层次化的测试数据结构，包含50个父行，每个父行有200个子行。
        每个数据项包含名称、类型、数据数组和唯一ID。
        
        数据结构:
            - parent: 父行数据，包含展开/折叠功能
            - child: 子行数据，属于特定的父行
        """
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
            for j in range(200):
                child_name = f'Child_{i:03d}_{j:03d}'
                self.all_data.append({
                    'name': child_name,
                    'type': 'child',
                    'parent': parent_name,
                    'data': [f'  {child_name}', '0.500', False, False, False, False, '0', '0.000', '0.000'],
                    'row_id': f'child_{i}_{j}'
                })
    
    def refresh_visible_items(self) -> None:
        """刷新可见项列表.
        
        根据当前的展开状态重新构建可见项列表。
        只有展开的父行的子项才会被添加到可见项列表中。
        这个方法在展开/折叠操作后被调用以更新显示状态。
        """
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
    
    def build_table_with_lazy_loading(self) -> None:
        """构建表格 - 只创建占位符.
        
        初始化表格显示，只创建轻量级的占位符文本项。
        这个方法显著提高了大数据集的初始加载速度。
        完整的交互控件将在需要时延迟创建。
        
        流程:
            1. 禁用界面更新以提高性能
            2. 刷新可见项列表
            3. 清除现有内容并设置行数
            4. 为每行创建占位符项
            5. 重新启用界面更新
            6. 调度可见行的控件创建
        """
        self.setUpdatesEnabled(False)
        self.refresh_visible_items()
        
        # 清除现有内容
        self.clearContents()
        self.setRowCount(len(self.visible_items))
        self.widgets_created.clear()
        
        # 只创建占位符文本项
        for row, item in enumerate(self.visible_items):
            self.create_placeholder_items(row, item)
        
        self.setUpdatesEnabled(True)
        
        # 立即为可见行创建控件
        self.schedule_visible_widgets_creation()
    
    def create_placeholder_items(self, row: int, item: Dict[str, Any]) -> None:
        """创建占位符文本项.
        
        为指定行创建轻量级的文本占位符，用于快速显示数据概览。
        占位符显示数据的文本表示，但不提供交互功能。
        
        Args:
            row: 表格中的行索引
            item: 包含行数据的字典
                - 'type': 行类型 ('parent' 或 'child')
                - 'name': 行名称
                - 'data': 包含各列数据的列表
        
        Note:
            - 父行的第一列包含展开/折叠图标 (▶/▼)
            - 复选框列显示为符号 (☑/☐)
            - 其他列显示为纯文本
            - 所有占位符项都标记为不可编辑
        """
        data = item['data']
        
        # 第一列：名称和展开图标
        first_col_text = data[0]
        if item['type'] == 'parent':
            icon = '▼ ' if item['name'] in self.expanded_rows else '▶ '
            first_col_text = icon + first_col_text
        
        first_item = QTableWidgetItem(first_col_text)
        first_item.setFlags(first_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row, 0, first_item)
        
        # 其他列：创建占位符文本项
        for col in range(1, 9):
            if col in [2, 3, 4, 5]:  # 复选框列
                placeholder_text = '☑' if data[col] else '☐'
            else:
                placeholder_text = str(data[col])
            
            placeholder_item = QTableWidgetItem(placeholder_text)
            placeholder_item.setFlags(placeholder_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            placeholder_item.setData(Qt.ItemDataRole.UserRole, 'placeholder')  # 标记为占位符
            self.setItem(row, col, placeholder_item)
    
    def create_full_widgets_for_row(self, row: int) -> None:
        """为指定行创建完整的控件.
        
        将占位符替换为完整的交互控件，包括QLineEdit、QCheckBox和QComboBox。
        这个方法在行变为可见或被用户点击时调用。
        
        Args:
            row: 要创建控件的行索引
        
        控件类型映射:
            - 列1,7,8: QLineEdit (文本输入框)
            - 列2,3,4,5: QCheckBox (复选框)
            - 列6: QComboBox (下拉选择框，选项0-5)
        
        Note:
            - 如果行已经创建过控件或行索引无效，则跳过创建
            - 所有控件都连接了相应的信号处理函数
            - 创建完成后将行号添加到widgets_created集合中
        """
        # 多重安全检查，防止索引越界
        visible_items_count = len(self.visible_items)
        if (row >= visible_items_count or 
            row < 0 or 
            row >= self.rowCount() or 
            row in self.widgets_created):
            return
        
        item = self.visible_items[row]
        data = item['data']
        
        # 为每列创建完整的控件
        for col in range(1, 9):
            if col in [1, 7, 8]:  # 文本输入框列
                widget = QLineEdit(str(data[col]))
                widget.textChanged.connect(lambda text, r=row, c=col: self.on_line_edit_changed(r, c, text))
                self.setCellWidget(row, col, widget)
            
            elif col in [2, 3, 4, 5]:  # 复选框列
                widget = QCheckBox()
                widget.setChecked(bool(data[col]))
                widget.stateChanged.connect(lambda state, r=row, c=col: self.on_checkbox_changed(r, c, state))
                self.setCellWidget(row, col, widget)
            
            elif col == 6:  # 下拉框列
                widget = QComboBox()
                widget.addItems(['0', '1', '2', '3', '4', '5'])
                widget.setCurrentText(str(data[col]))
                widget.currentTextChanged.connect(lambda text, r=row, c=col: self.on_combo_changed(r, c, text))
                self.setCellWidget(row, col, widget)
        
        self.widgets_created.add(row)
    
    def get_visible_row_range(self) -> tuple:
        """获取当前可见的行范围.
        
        计算当前视口中可见的行范围，用于优化控件创建。
        使用两种方法确保准确性：项目检测和滚动条计算。
        
        Returns:
            tuple: (start_row, end_row) 可见行的起始和结束索引
                - start_row: 可见区域的第一行（包含）
                - end_row: 可见区域的最后一行（不包含）
        
        算法:
            1. 优先使用itemAt()方法获取实际可见项目
            2. 如果无法获取项目，回退到基于滚动条的计算
            3. 在可见范围前后各扩展3行以提前创建控件
        
        Note:
            - 扩展范围有助于提供更流畅的滚动体验
            - 返回的范围会被限制在有效的行索引范围内
        """
        # 使用更准确的方法获取可见行范围
        top_item = self.itemAt(0, 0)
        bottom_item = self.itemAt(0, self.viewport().height() - 1)
        
        if top_item is None or bottom_item is None:
            # 如果无法获取项目，使用滚动条计算
            viewport_top = self.verticalScrollBar().value()
            viewport_height = self.viewport().height()
            row_height = self.rowHeight(0) if self.rowCount() > 0 else 30
            
            start_row = max(0, viewport_top // row_height - 3)
            end_row = min(self.rowCount(), (viewport_top + viewport_height) // row_height + 3)
        else:
            # 使用实际可见项目计算
            start_row = max(0, self.row(top_item) - 3)  # 提前3行
            end_row = min(self.rowCount(), self.row(bottom_item) + 3)  # 延后3行
        
        return start_row, end_row
    
    def schedule_visible_widgets_creation(self) -> None:
        """调度可见行的控件创建.
        
        识别当前可见范围内尚未创建控件的行，并将它们添加到待创建队列中。
        使用定时器延迟创建以避免在快速滚动时创建过多控件。
        
        流程:
            1. 获取当前可见行范围
            2. 识别需要创建控件的行
            3. 将这些行添加到待创建队列
            4. 如果有新的待创建项，启动延迟定时器
        
        Note:
            - 使用10ms的短延迟以提供快速响应
            - 避免为已创建控件的行重复创建
            - 只处理有效的行索引范围
        """
        start_row, end_row = self.get_visible_row_range()
        
        # 添加调试信息和安全检查
        new_pending = set()
        visible_items_count = len(self.visible_items)
        table_row_count = self.rowCount()
        
        for row in range(start_row, end_row):
            # 多重安全检查：确保行索引在所有相关范围内都有效
            if (row not in self.widgets_created and 
                row < visible_items_count and 
                row < table_row_count and 
                row >= 0):
                new_pending.add(row)
                self.pending_widget_creation.add(row)
        
        # 如果有新的待创建控件，启动定时器
        if new_pending:
            self.lazy_timer.start(10)  # 减少延迟到10ms
    
    def create_pending_widgets(self) -> None:
        """创建待处理的控件.
        
        批量创建所有在待创建队列中的行的完整控件。
        使用批量操作和界面更新控制来优化性能。
        
        流程:
            1. 禁用界面更新以提高批量操作性能
            2. 遍历待创建队列，为每行创建完整控件
            3. 清空待创建队列
            4. 重新启用界面更新
        
        Note:
            - 这个方法由lazy_timer定时器触发
            - 批量操作可以显著提高大量控件创建的性能
            - 创建完成后队列会被清空以避免重复创建
        """
        # 批量创建控件
        self.setUpdatesEnabled(False)
        
        for row in list(self.pending_widget_creation):
            self.create_full_widgets_for_row(row)
        
        self.pending_widget_creation.clear()
        self.setUpdatesEnabled(True)
    
    def check_visible_rows(self) -> None:
        """检查可见行并创建控件.
        
        定期检查当前可见的行并调度控件创建。
        这个方法由viewport_timer定时器每100ms调用一次。
        
        Note:
            - 提供了除滚动事件外的额外检测机制
            - 确保在各种情况下都能及时创建可见行的控件
        """
        self.schedule_visible_widgets_creation()
    
    def on_scroll(self) -> None:
        """处理滚动事件.
        
        当用户滚动表格时触发，立即调度新可见行的控件创建。
        这确保了滚动时能够及时显示完整的交互控件。
        
        Note:
            - 连接到verticalScrollBar().valueChanged信号
            - 提供即时响应以改善用户体验
        """
        self.schedule_visible_widgets_creation()
    
    def on_cell_clicked(self, row: int, column: int) -> None:
        """处理单元格点击事件.
        
        处理用户点击表格单元格的操作，包括展开/折叠父行和确保点击行有完整控件。
        
        Args:
            row: 被点击的行索引
            column: 被点击的列索引
        
        功能:
            1. 如果点击父行的第一列，切换展开/折叠状态
            2. 确保被点击的行有完整的交互控件
            3. 更新表格显示以反映状态变化
        
        Note:
            - 只有父行的第一列点击才会触发展开/折叠
            - 点击任何行都会确保该行有完整控件
            - 无效的行索引会被忽略
        """
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
            
            # 更新表格
            self.update_table_incrementally(parent_name, row)
        
        # 确保点击的行有完整控件
        if row not in self.widgets_created:
            self.create_full_widgets_for_row(row)
    
    def update_table_incrementally(self, parent_name: str, parent_row: int) -> None:
        """增量更新表格.
        
        高效地处理父行的展开和折叠操作，只更新受影响的行而不重建整个表格。
        
        Args:
            parent_name: 要展开/折叠的父行名称
            parent_row: 父行在表格中的索引
        
        展开操作:
            1. 查找所有属于该父行的子项
            2. 在父行后批量插入子行
            3. 为新插入的行创建占位符
            4. 更新父行图标为展开状态 (▼)
        
        折叠操作:
            1. 计算子行数量
            2. 批量删除父行后的所有子行
            3. 更新父行图标为折叠状态 (▶)
        
        性能优化:
            - 使用setUpdatesEnabled(False)暂停界面更新
            - 批量插入/删除操作
            - 清理受影响行的控件状态
            - 重新调度可见控件创建
        """
        self.setUpdatesEnabled(False)
        
        if parent_name in self.expanded_rows:
            # 展开：插入子行
            child_items = [item for item in self.all_data 
                          if item['type'] == 'child' and item.get('parent') == parent_name]
            
            # 批量插入
            insert_position = parent_row + 1
            for i, child_item in enumerate(child_items):
                self.insertRow(insert_position + i)
                self.create_placeholder_items(insert_position + i, child_item)
            
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
        
        # 清理控件创建状态
        self.cleanup_widget_states_after_row(parent_row)
        
        self.setUpdatesEnabled(True)
        self.refresh_visible_items()
        
        # 延迟调度可见控件创建，确保表格完全更新后再检测
        # 使用QTimer.singleShot直接创建控件，避免与lazy_timer冲突
        def delayed_widget_creation():
            self.schedule_visible_widgets_creation()
            # 立即创建待处理的控件，避免依赖lazy_timer
            if self.pending_widget_creation:
                self.create_pending_widgets()
        
        QTimer.singleShot(50, delayed_widget_creation)
    
    def cleanup_widget_states_after_row(self, row: int) -> None:
        """清理指定行之后的控件状态.
        
        在表格结构发生变化（如展开/折叠）后，清理受影响行的控件创建状态。
        这确保了行号映射的正确性和内存的有效使用。
        
        Args:
            row: 起始行索引，该行之后的所有控件状态都会被清理
        
        清理内容:
            - widgets_created集合中大于指定行号的记录
            - pending_widget_creation集合中大于指定行号的记录
        
        Note:
            - 这个方法在表格行数发生变化后调用
            - 确保控件状态与实际表格结构保持同步
            - 避免内存泄漏和状态不一致问题
        """
        # 清理已创建控件的记录
        widgets_to_remove = {r for r in self.widgets_created if r > row}
        self.widgets_created -= widgets_to_remove
        
        # 清理待创建控件的记录
        pending_to_remove = {r for r in self.pending_widget_creation if r > row}
        self.pending_widget_creation -= pending_to_remove
    
    # 事件处理方法
    def on_line_edit_changed(self, row: int, column: int, text: str) -> None:
        """处理文本框变化.
        
        当QLineEdit控件的文本发生变化时更新底层数据。
        
        Args:
            row: 发生变化的行索引
            column: 发生变化的列索引
            text: 新的文本内容
        
        Note:
            - 只有在行索引有效时才更新数据
            - 直接更新visible_items中对应的数据项
        """
        if row < len(self.visible_items):
            self.visible_items[row]['data'][column] = text
    
    def on_checkbox_changed(self, row: int, column: int, state: int) -> None:
        """处理复选框变化.
        
        当QCheckBox控件的状态发生变化时更新底层数据。
        
        Args:
            row: 发生变化的行索引
            column: 发生变化的列索引
            state: 新的复选框状态（Qt.CheckState枚举值）
        
        Note:
            - 将Qt状态值转换为布尔值存储
            - 只有在行索引有效时才更新数据
        """
        if row < len(self.visible_items):
            self.visible_items[row]['data'][column] = (state == Qt.CheckState.Checked.value)
    
    def on_combo_changed(self, row: int, column: int, text: str) -> None:
        """处理下拉框变化.
        
        当QComboBox控件的选择发生变化时更新底层数据。
        
        Args:
            row: 发生变化的行索引
            column: 发生变化的列索引
            text: 新选择的文本内容
        
        Note:
            - 只有在行索引有效时才更新数据
            - 直接存储选择的文本值
        """
        if row < len(self.visible_items):
            self.visible_items[row]['data'][column] = text


class MainWindow(QMainWindow):
    """主窗口.
    
    应用程序的主窗口，包含延迟加载表格控件和相关的用户界面元素。
    提供了演示延迟加载功能的完整界面。
    
    Attributes:
        table (LazyLoadingTableWidget): 主要的延迟加载表格控件
    """
    
    def __init__(self):
        """初始化主窗口.
        
        设置窗口属性、创建用户界面布局和初始化表格控件。
        
        界面组成:
            - 信息标签：显示延迟加载策略的说明
            - 延迟加载表格：主要的数据显示和交互区域
        
        窗口配置:
            - 标题：延迟加载表格演示
            - 尺寸：1200x800像素
            - 位置：屏幕坐标(100, 100)
        """
        super().__init__()
        self.setWindowTitle('延迟加载表格演示 - 完整控件 + 延迟创建')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加说明标签
        info_label = QLabel(
            '延迟加载优化策略：\n'
            '1. 初始只创建占位符文本项\n'
            '2. 根据视口可见性延迟创建完整控件\n'
            '3. 滚动时自动创建可见行的控件\n'
            '4. 点击时立即创建该行的完整控件\n'
            '5. 使用完整的QLineEdit、QCheckBox、QComboBox控件\n'
            '测试：50个父行，每个包含100个子行（共5050行数据）'
        )
        info_label.setStyleSheet('background-color: #e8f4fd; padding: 10px; border: 1px solid #b3d9ff;')
        layout.addWidget(info_label)
        
        # 创建表格
        self.table = LazyLoadingTableWidget()
        layout.addWidget(self.table)


def main():
    """应用程序主入口函数.
    
    创建QApplication实例，初始化主窗口并启动事件循环。
    
    流程:
        1. 创建QApplication实例
        2. 创建并显示主窗口
        3. 启动Qt事件循环
        4. 应用程序退出时返回退出代码
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()