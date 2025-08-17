import sys
from typing import Dict, List, Any, Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QMenu, QMessageBox,
    QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction, QFont


class CustomCellWidget(QWidget):
    """自定义单元格控件，支持选中效果显示.
    
    这个控件用于替代第一列的QTableWidgetItem，能够在行选中时
    显示相应的背景色，解决setCellWidget后选中效果失效的问题。
    """
    
    def __init__(self, text: str, is_parent: bool = False, parent=None):
        """初始化自定义单元格控件.
        
        Args:
            text: 显示的文本内容
            is_parent: 是否为父节点
            parent: 父控件
        """
        super().__init__(parent)
        self.is_parent = is_parent
        self.is_selected = False
        
        # 创建布局和标签
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        self.label = QLabel(text)
        if is_parent:
            font = QFont()
            font.setBold(True)
            self.label.setFont(font)
        
        layout.addWidget(self.label)
        
        # 设置初始样式
        self.update_style()
        
        # 让控件不接收鼠标事件，传递给表格
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    
    def set_text(self, text: str):
        """设置显示文本.
        
        Args:
            text: 要显示的文本
        """
        self.label.setText(text)
    
    def set_selected(self, selected: bool):
        """设置选中状态.
        
        Args:
            selected: 是否选中
        """
        if self.is_selected != selected:
            self.is_selected = selected
            self.update_style()
    
    def update_style(self):
        """更新控件样式.
        
        根据选中状态和节点类型设置不同的背景色。
        """
        if self.is_selected and not self.is_parent:
            # 子节点选中时显示高亮背景
            self.setStyleSheet("""
                QWidget {
                    background-color: palette(highlight);
                    color: palette(highlighted-text);
                }
                QLabel {
                    background-color: transparent;
                    color: palette(highlighted-text);
                }
            """)
        else:
            # 未选中或父节点时显示透明背景
            self.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                }
                QLabel {
                    background-color: transparent;
                }
            """)


class ContextMenuTableWidget(QTableWidget):
    """带右键菜单的表格控件.
    
    支持层次化数据结构，为父节点和子节点提供不同的右键菜单。
    父节点支持展开/折叠、添加子项、删除等操作。
    子节点支持编辑、删除、移动等操作。
    
    Attributes:
        all_data: 所有数据项的列表
        expanded_rows: 已展开的父行集合
        parent_rows: 父行索引到名称的映射
    """
    
    def __init__(self, parent=None):
        """初始化表格控件.
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        
        # 数据存储
        self.all_data: List[Dict[str, Any]] = []
        self.expanded_rows: set = set()
        
        # 存储父节点行索引，用于快速判断
        self.parent_rows: Dict[int, str] = {}  # 行索引 -> 父节点名称
        
        # 存储上次选中的行索引，用于在选择变化时进行比较
        self.previous_selected_row: Optional[int] = None
        
        self.setup_table()
        self.generate_test_data()
        self.build_table()
        
        # 启用右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # 连接双击事件用于展开/折叠
        self.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        # 连接选择变化事件
        self.itemSelectionChanged.connect(self.on_selection_changed)
    
    def setup_table(self) -> None:
        """设置表格基本属性.
        
        配置表格的列标题、列宽和基本显示属性。
        """
        # 设置列数和标题
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['名称', '类型', '值', '描述'])
        
        # 设置列宽
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.setColumnWidth(1, 80)
        
        # 设置表格属性
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
    def generate_test_data(self) -> None:
        """生成测试数据.
        
        创建包含父节点和子节点的层次化测试数据。
        """
        self.all_data = [
            {
                'type': 'parent',
                'name': '系统配置',
                'value': '配置组',
                'description': '系统相关配置项',
                'data': ['系统配置', '配置组', '配置组', '系统相关配置项']
            },
            {
                'type': 'child',
                'parent': '系统配置',
                'name': '最大连接数',
                'value': '1000',
                'description': '系统最大并发连接数',
                'data': ['  └ 最大连接数', '整数', '1000', '系统最大并发连接数']
            },
            {
                'type': 'child',
                'parent': '系统配置',
                'name': '超时时间',
                'value': '30秒',
                'description': '请求超时时间',
                'data': ['  └ 超时时间', '时间', '30秒', '请求超时时间']
            },
            {
                'type': 'parent',
                'name': '数据库配置',
                'value': '配置组',
                'description': '数据库相关配置',
                'data': ['数据库配置', '配置组', '配置组', '数据库相关配置']
            },
            {
                'type': 'child',
                'parent': '数据库配置',
                'name': '主机地址',
                'value': 'localhost',
                'description': '数据库服务器地址',
                'data': ['  └ 主机地址', '字符串', 'localhost', '数据库服务器地址']
            },
            {
                'type': 'child',
                'parent': '数据库配置',
                'name': '端口号',
                'value': '3306',
                'description': '数据库端口',
                'data': ['  └ 端口号', '整数', '3306', '数据库端口']
            },
            {
                'type': 'child',
                'parent': '数据库配置',
                'name': '用户名',
                'value': 'admin',
                'description': '数据库用户名',
                'data': ['  └ 用户名', '字符串', 'admin', '数据库用户名']
            },
            {
                'type': 'parent',
                'name': '网络配置',
                'value': '配置组',
                'description': '网络相关配置',
                'data': ['网络配置', '配置组', '配置组', '网络相关配置']
            },
            {
                'type': 'child',
                'parent': '网络配置',
                'name': 'API地址',
                'value': 'https://api.example.com',
                'description': 'API服务器地址',
                'data': ['  └ API地址', 'URL', 'https://api.example.com', 'API服务器地址']
            }
        ]
    
    def build_table(self) -> None:
        """构建表格显示.
        
        根据展开状态显示相应的行，只显示父行和已展开父行的子行。
        """
        # 清空表格
        self.setRowCount(0)
        self.parent_rows.clear()
        
        visible_items = []
        
        # 收集可见项
        for item in self.all_data:
            if item['type'] == 'parent':
                visible_items.append(item)
                # 如果父行已展开，添加其子行
                if item['name'] in self.expanded_rows:
                    for child_item in self.all_data:
                        if (child_item['type'] == 'child' and 
                            child_item.get('parent') == item['name']):
                            visible_items.append(child_item)
        
        # 设置行数并填充数据
        self.setRowCount(len(visible_items))
        
        for row, item in enumerate(visible_items):
            # 记录父行位置
            if item['type'] == 'parent':
                self.parent_rows[row] = item['name']
            
            # 设置行数据
            for col, text in enumerate(item['data']):
                if col == 0:
                    # 第一列使用自定义控件
                    is_parent = item['type'] == 'parent'
                    
                    # 设置展开/折叠图标文本
                    if is_parent:
                        if item['name'] in self.expanded_rows:
                            display_text = f"▼ {item['name']}"
                        else:
                            display_text = f"▶ {item['name']}"
                    else:
                        display_text = str(text)
                    
                    # 创建自定义控件
                    custom_widget = CustomCellWidget(display_text, is_parent)
                    self.setCellWidget(row, col, custom_widget)
                    
                    # 仍然需要设置一个空的QTableWidgetItem来保持表格结构
                    table_item = QTableWidgetItem()
                    table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # 父节点设置为不可选择
                    if is_parent:
                        table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                    
                    self.setItem(row, col, table_item)
                else:
                    # 其他列正常设置
                    table_item = QTableWidgetItem(str(text))
                    
                    # 设置父行样式
                    if item['type'] == 'parent':
                        font = QFont()
                        font.setBold(True)
                        table_item.setFont(font)
                    
                    # 设置为只读
                    table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # 父节点设置为不可选择
                    if item['type'] == 'parent':
                        table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                    
                    self.setItem(row, col, table_item)
    
    def show_context_menu(self, position: QPoint) -> None:
        """显示右键菜单.
        
        根据点击的行类型（父节点或子节点）显示不同的菜单选项。
        
        Args:
            position: 右键点击的位置
        """
        item = self.itemAt(position)
        if item is None:
            return
        
        row = item.row()
        menu = QMenu(self)
        
        # 判断是父节点还是子节点
        if row in self.parent_rows:
            # 父节点菜单
            self.create_parent_context_menu(menu, row)
        else:
            # 子节点菜单
            self.create_child_context_menu(menu, row)
        
        # 显示菜单
        if menu.actions():
            menu.exec(self.mapToGlobal(position))
    
    def create_parent_context_menu(self, menu: QMenu, row: int) -> None:
        """创建父节点右键菜单.
        
        Args:
            menu: 菜单对象
            row: 行索引
        """
        parent_name = self.parent_rows[row]
        is_expanded = parent_name in self.expanded_rows
        
        # 展开/折叠
        if is_expanded:
            expand_action = QAction("折叠", self)
            expand_action.triggered.connect(lambda: self.toggle_expand(parent_name))
        else:
            expand_action = QAction("展开", self)
            expand_action.triggered.connect(lambda: self.toggle_expand(parent_name))
        menu.addAction(expand_action)
        
        menu.addSeparator()
        
        # 添加子项
        add_child_action = QAction("添加子项", self)
        add_child_action.triggered.connect(lambda: self.add_child_item(parent_name))
        menu.addAction(add_child_action)
        
        # 编辑父项
        edit_action = QAction("编辑", self)
        edit_action.triggered.connect(lambda: self.edit_parent_item(parent_name))
        menu.addAction(edit_action)
        
        menu.addSeparator()
        
        # 删除父项（及其所有子项）
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(lambda: self.delete_parent_item(parent_name))
        menu.addAction(delete_action)
        
        # 属性
        properties_action = QAction("属性", self)
        properties_action.triggered.connect(lambda: self.show_parent_properties(parent_name))
        menu.addAction(properties_action)
    
    def create_child_context_menu(self, menu: QMenu, row: int) -> None:
        """创建子节点右键菜单.
        
        Args:
            menu: 菜单对象
            row: 行索引
        """
        # 获取子项信息
        child_item = self.get_child_item_by_row(row)
        if child_item is None:
            return
        
        # 编辑
        edit_action = QAction("编辑值", self)
        edit_action.triggered.connect(lambda: self.edit_child_item(child_item))
        menu.addAction(edit_action)
        
        # 复制
        copy_action = QAction("复制", self)
        copy_action.triggered.connect(lambda: self.copy_child_item(child_item))
        menu.addAction(copy_action)
        
        menu.addSeparator()
        
        # 上移/下移
        move_up_action = QAction("上移", self)
        move_up_action.triggered.connect(lambda: self.move_child_item(child_item, -1))
        menu.addAction(move_up_action)
        
        move_down_action = QAction("下移", self)
        move_down_action.triggered.connect(lambda: self.move_child_item(child_item, 1))
        menu.addAction(move_down_action)
        
        menu.addSeparator()
        
        # 删除
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(lambda: self.delete_child_item(child_item))
        menu.addAction(delete_action)
        
        # 属性
        properties_action = QAction("属性", self)
        properties_action.triggered.connect(lambda: self.show_child_properties(child_item))
        menu.addAction(properties_action)
    
    def get_child_item_by_row(self, row: int) -> Optional[Dict[str, Any]]:
        """根据行索引获取子项数据.
        
        Args:
            row: 行索引
            
        Returns:
            子项数据字典，如果未找到返回None
        """
        item_name = self.item(row, 0)
        if item_name is None:
            return None
        
        # 提取子项名称（去掉前缀）
        name_text = item_name.text().replace('  └ ', '')
        
        # 在数据中查找对应的子项
        for item in self.all_data:
            if item['type'] == 'child' and item['name'] == name_text:
                return item
        
        return None
    
    def on_cell_double_clicked(self, row: int, column: int) -> None:
        """处理双击事件.
        
        Args:
            row: 行索引
            column: 列索引
        """
        if row in self.parent_rows:
            parent_name = self.parent_rows[row]
            self.toggle_expand(parent_name)
    
    def toggle_expand(self, parent_name: str) -> None:
        """切换展开/折叠状态.
        
        Args:
            parent_name: 父节点名称
        """
        if parent_name in self.expanded_rows:
            self.expanded_rows.remove(parent_name)
        else:
            self.expanded_rows.add(parent_name)
        
        self.build_table()
    
    def add_child_item(self, parent_name: str) -> None:
        """添加子项.
        
        Args:
            parent_name: 父节点名称
        """
        # 计算新子项的编号
        child_count = sum(1 for item in self.all_data 
                         if item['type'] == 'child' and item.get('parent') == parent_name)
        
        new_child = {
            'type': 'child',
            'parent': parent_name,
            'name': f'新配置项{child_count + 1}',
            'value': '默认值',
            'description': '新添加的配置项',
            'data': [f'  └ 新配置项{child_count + 1}', '字符串', '默认值', '新添加的配置项']
        }
        
        # 找到父项的位置，在其后插入子项
        parent_index = -1
        for i, item in enumerate(self.all_data):
            if item['type'] == 'parent' and item['name'] == parent_name:
                parent_index = i
                break
        
        if parent_index >= 0:
            # 找到最后一个子项的位置
            insert_index = parent_index + 1
            for i in range(parent_index + 1, len(self.all_data)):
                if (self.all_data[i]['type'] == 'child' and 
                    self.all_data[i].get('parent') == parent_name):
                    insert_index = i + 1
                elif self.all_data[i]['type'] == 'parent':
                    break
            
            self.all_data.insert(insert_index, new_child)
            
            # 确保父项展开
            self.expanded_rows.add(parent_name)
            self.build_table()
            
            QMessageBox.information(self, "添加成功", f"已为 '{parent_name}' 添加新子项")
    
    def edit_parent_item(self, parent_name: str) -> None:
        """编辑父项.
        
        Args:
            parent_name: 父节点名称
        """
        QMessageBox.information(self, "编辑父项", f"编辑父项: {parent_name}")
    
    def delete_parent_item(self, parent_name: str) -> None:
        """删除父项及其所有子项.
        
        Args:
            parent_name: 父节点名称
        """
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除 '{parent_name}' 及其所有子项吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 删除父项和所有子项
            self.all_data = [item for item in self.all_data 
                           if not (item['name'] == parent_name or 
                                 (item['type'] == 'child' and item.get('parent') == parent_name))]
            
            # 从展开列表中移除
            self.expanded_rows.discard(parent_name)
            
            self.build_table()
            QMessageBox.information(self, "删除成功", f"已删除 '{parent_name}' 及其所有子项")
    
    def show_parent_properties(self, parent_name: str) -> None:
        """显示父项属性.
        
        Args:
            parent_name: 父节点名称
        """
        # 统计子项数量
        child_count = sum(1 for item in self.all_data 
                         if item['type'] == 'child' and item.get('parent') == parent_name)
        
        QMessageBox.information(
            self, "父项属性", 
            f"名称: {parent_name}\n子项数量: {child_count}\n状态: {'已展开' if parent_name in self.expanded_rows else '已折叠'}"
        )
    
    def edit_child_item(self, child_item: Dict[str, Any]) -> None:
        """编辑子项.
        
        Args:
            child_item: 子项数据
        """
        QMessageBox.information(self, "编辑子项", f"编辑子项: {child_item['name']}")
    
    def copy_child_item(self, child_item: Dict[str, Any]) -> None:
        """复制子项.
        
        Args:
            child_item: 子项数据
        """
        QMessageBox.information(self, "复制子项", f"已复制子项: {child_item['name']}")
    
    def move_child_item(self, child_item: Dict[str, Any], direction: int) -> None:
        """移动子项.
        
        Args:
            child_item: 子项数据
            direction: 移动方向，-1为上移，1为下移
        """
        parent_name = child_item.get('parent')
        if not parent_name:
            return
        
        # 获取同一父项下的所有子项
        siblings = [i for i, item in enumerate(self.all_data) 
                   if item['type'] == 'child' and item.get('parent') == parent_name]
        
        # 找到当前子项的索引
        current_index = -1
        for i, item in enumerate(self.all_data):
            if item == child_item:
                current_index = i
                break
        
        if current_index == -1:
            return
        
        # 在兄弟项中的位置
        sibling_pos = siblings.index(current_index)
        new_sibling_pos = sibling_pos + direction
        
        # 检查边界
        if new_sibling_pos < 0 or new_sibling_pos >= len(siblings):
            QMessageBox.information(self, "移动失败", "已经在边界位置")
            return
        
        # 交换位置
        target_index = siblings[new_sibling_pos]
        self.all_data[current_index], self.all_data[target_index] = \
            self.all_data[target_index], self.all_data[current_index]
        
        self.build_table()
        QMessageBox.information(self, "移动成功", f"已{'上移' if direction == -1 else '下移'} '{child_item['name']}'")
    
    def delete_child_item(self, child_item: Dict[str, Any]) -> None:
        """删除子项.
        
        Args:
            child_item: 子项数据
        """
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除 '{child_item['name']}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.all_data.remove(child_item)
            self.build_table()
            QMessageBox.information(self, "删除成功", f"已删除 '{child_item['name']}'")
    
    def show_child_properties(self, child_item: Dict[str, Any]) -> None:
        """显示子项属性.
        
        Args:
            child_item: 子项数据
        """
        QMessageBox.information(
            self, "子项属性", 
            f"名称: {child_item['name']}\n类型: {child_item['data'][1]}\n值: {child_item['value']}\n描述: {child_item['description']}\n父项: {child_item.get('parent', 'N/A')}"
        )
    
    def on_selection_changed(self) -> None:
        """处理选择变化事件.
        
        确保只有子节点可以被选中，父节点不能被选中。
        同时更新第一列自定义控件的选中状态显示。
        不使用缓存，通过遍历所有行来识别选中和失去选中的行。
        """
        selected_items = self.selectedItems()
        
        # 获取当前选中的行索引集合
        current_selected_rows = set()
        for item in selected_items:
            current_selected_rows.add(item.row())
        
        # 遍历所有行，更新第一列自定义控件的选中状态
        for row in range(self.rowCount()):
            custom_widget = self.cellWidget(row, 0)
            if isinstance(custom_widget, CustomCellWidget):
                # 检查当前行是否被选中
                is_row_selected = row in current_selected_rows
                
                # 获取控件当前的选中状态
                was_selected = custom_widget.is_selected
                
                # 如果状态发生变化，进行相应处理
                if is_row_selected and not was_selected:
                    # 行被新选中
                    print(f"行 {row} 被选中")
                    custom_widget.set_selected(True)
                elif not is_row_selected and was_selected:
                    # 行失去选中
                    print(f"行 {row} 失去选中")
                    custom_widget.set_selected(False)
        
        # 检查选中的项目，如果是父节点则清除选择
        for item in selected_items:
            row = item.row()
            if row in self.parent_rows:
                # 清除父节点的选择
                self.clearSelection()
                # 清除选择后，需要再次更新所有控件状态
                for row in range(self.rowCount()):
                    custom_widget = self.cellWidget(row, 0)
                    if isinstance(custom_widget, CustomCellWidget):
                        custom_widget.set_selected(False)
                        print(f"父节点选择被清除，行 {row} 失去选中")
                break


class MainWindow(QMainWindow):
    """主窗口类.
    
    包含带右键菜单的表格控件演示。
    """
    
    def __init__(self):
        """初始化主窗口."""
        super().__init__()
        self.setWindowTitle("TableWidget 右键菜单演示")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建表格
        self.table = ContextMenuTableWidget()
        layout.addWidget(self.table)


def main():
    """主函数."""
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()