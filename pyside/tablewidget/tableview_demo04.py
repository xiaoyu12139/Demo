import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, 
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class TreeTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup_table()
        self.populate_data()
        self.setup_connections()
        
    def setup_table(self):
        """设置表格基本属性"""
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["名称", "类型", "描述"])
        
        # 设置表格样式
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        
    def populate_data(self):
        """填充表格数据"""
        # 生成大量测试数据
        data = []
        
        # 定义父分类
        parent_categories = [
            ("项目管理", "项目相关功能"),
            ("用户管理", "用户相关功能"),
            ("系统设置", "系统配置功能"),
            ("数据管理", "数据处理功能"),
            ("报表统计", "报表生成功能"),
            ("权限控制", "权限管理功能"),
            ("日志管理", "日志记录功能"),
            ("备份恢复", "数据备份功能"),
            ("监控告警", "系统监控功能"),
            ("接口管理", "API接口功能")
        ]
        
        # 子功能模板
        child_templates = [
            "创建", "编辑", "删除", "查看", "导入", "导出", "复制", "移动",
            "搜索", "筛选", "排序", "分页", "批量操作", "详情查看", "历史记录",
            "权限设置", "状态管理", "配置管理", "模板管理", "规则设置"
        ]
        
        row_index = 0
        
        # 为每个父分类生成子项，确保总数达到1000行
        children_per_parent = 999  # 每个父分类99个子项，10个父分类共990个子项，加上10个父项=1000行
        
        for i, (parent_name, parent_desc) in enumerate(parent_categories):
            # 添加父行
            data.append((parent_name, "分类", parent_desc, True, -1))
            parent_row_index = row_index
            row_index += 1
            
            # 为当前父分类生成子项
            for j in range(children_per_parent):
                template_index = j % len(child_templates)
                child_name = f"  {child_templates[template_index]}{parent_name}_{j+1:03d}"
                child_desc = f"{child_templates[template_index]}{parent_name}的具体功能_{j+1}"
                data.append((child_name, "功能", child_desc, False, parent_row_index))
                row_index += 1
        
        self.setRowCount(len(data))
        self.parent_rows = []  # 存储父行索引
        self.child_rows = {}   # 存储每个父行对应的子行索引
        
        for row, (name, type_val, desc, is_parent, parent_idx) in enumerate(data):
            # 创建表格项
            name_item = QTableWidgetItem(name)
            type_item = QTableWidgetItem(type_val)
            desc_item = QTableWidgetItem(desc)
            
            # 设置父行样式
            if is_parent:
                font = QFont()
                font.setBold(True)
                name_item.setFont(font)
                type_item.setFont(font)
                desc_item.setFont(font)
                
                # 添加展开/折叠图标
                name_item.setData(Qt.UserRole, "expanded")
                self.parent_rows.append(row)
                self.child_rows[row] = []
            else:
                # 记录子行
                if parent_idx in self.child_rows:
                    self.child_rows[parent_idx].append(row)
            
            self.setItem(row, 0, name_item)
            self.setItem(row, 1, type_item)
            self.setItem(row, 2, desc_item)
            
    def setup_connections(self):
        """设置信号连接"""
        self.cellClicked.connect(self.on_cell_clicked)
        
    def on_cell_clicked(self, row, column):
        """处理单元格点击事件"""
        if row in self.parent_rows:
            self.toggle_children(row)
            
    def toggle_children(self, parent_row):
        """切换子行的显示/隐藏状态"""
        if parent_row not in self.child_rows:
            return
            
        # 获取当前状态
        name_item = self.item(parent_row, 0)
        current_state = name_item.data(Qt.UserRole)
        
        # 切换状态
        if current_state == "expanded":
            # 隐藏子行
            for child_row in self.child_rows[parent_row]:
                self.setRowHidden(child_row, True)
            name_item.setData(Qt.UserRole, "collapsed")
            # 更新父行文本，添加展开指示符
            current_text = name_item.text()
            if not current_text.startswith("▶ "):
                name_item.setText("▶ " + current_text)
        else:
            # 显示子行
            for child_row in self.child_rows[parent_row]:
                self.setRowHidden(child_row, False)
            name_item.setData(Qt.UserRole, "expanded")
            # 更新父行文本，添加折叠指示符
            current_text = name_item.text()
            if current_text.startswith("▶ "):
                name_item.setText(current_text[2:])
            if not current_text.startswith("▼ "):
                name_item.setText("▼ " + name_item.text())
                
    def expand_all(self):
        """展开所有父行"""
        for parent_row in self.parent_rows:
            name_item = self.item(parent_row, 0)
            if name_item.data(Qt.UserRole) == "collapsed":
                self.toggle_children(parent_row)
                
    def collapse_all(self):
        """折叠所有父行"""
        for parent_row in self.parent_rows:
            name_item = self.item(parent_row, 0)
            if name_item.data(Qt.UserRole) == "expanded":
                self.toggle_children(parent_row)
                
    def insert_row_at(self, position, name, type_val, desc, is_parent=False, parent_idx=-1):
        """在指定位置插入新行，并更新索引"""
        # 插入新行
        self.insertRow(position)
        
        # 创建新的表格项
        name_item = QTableWidgetItem(name)
        type_item = QTableWidgetItem(type_val)
        desc_item = QTableWidgetItem(desc)
        
        if is_parent:
            font = QFont()
            font.setBold(True)
            name_item.setFont(font)
            type_item.setFont(font)
            desc_item.setFont(font)
            name_item.setData(Qt.UserRole, "expanded")
            name_item.setText("▼ " + name)
        
        self.setItem(position, 0, name_item)
        self.setItem(position, 1, type_item)
        self.setItem(position, 2, desc_item)
        
        # 更新所有索引
        self.update_indices_after_insert(position, is_parent, parent_idx)
        
    def update_indices_after_insert(self, insert_position, is_parent, parent_idx):
        """插入行后更新所有相关索引"""
        # 更新父行索引列表
        updated_parent_rows = []
        for parent_row in self.parent_rows:
            if parent_row >= insert_position:
                updated_parent_rows.append(parent_row + 1)
            else:
                updated_parent_rows.append(parent_row)
        
        # 如果插入的是父行，添加到父行列表
        if is_parent:
            updated_parent_rows.append(insert_position)
            updated_parent_rows.sort()
        
        self.parent_rows = updated_parent_rows
        
        # 更新子行索引字典
        updated_child_rows = {}
        for parent_row, children in self.child_rows.items():
            # 更新父行索引
            new_parent_row = parent_row + 1 if parent_row >= insert_position else parent_row
            
            # 更新子行索引
            updated_children = []
            for child_row in children:
                if child_row >= insert_position:
                    updated_children.append(child_row + 1)
                else:
                    updated_children.append(child_row)
            
            updated_child_rows[new_parent_row] = updated_children
        
        # 如果插入的是父行，初始化其子行列表
        if is_parent:
            updated_child_rows[insert_position] = []
        # 如果插入的是子行，添加到对应父行的子行列表
        elif parent_idx != -1:
            # 找到更新后的父行索引
            updated_parent_idx = parent_idx + 1 if parent_idx >= insert_position else parent_idx
            if updated_parent_idx in updated_child_rows:
                updated_child_rows[updated_parent_idx].append(insert_position)
                updated_child_rows[updated_parent_idx].sort()
        
        self.child_rows = updated_child_rows
        
    def add_test_row(self):
        """测试方法：在第一个父行下添加一个新的子行"""
        if self.parent_rows:
            first_parent = self.parent_rows[0]
            # 在第一个父行的第一个子行位置插入新行
            insert_position = first_parent + 10000
            self.insert_row_at(
                insert_position,
                "  新插入的测试功能",
                "功能",
                "这是一个测试插入的功能",
                is_parent=False,
                parent_idx=first_parent
            )
            print(f"在位置 {insert_position} 插入新行")
            print(f"父行索引: {self.parent_rows}")
            print(f"子行索引: {self.child_rows}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TableWidget 父子行演示")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建按钮
        button_layout = QVBoxLayout()
        
        expand_btn = QPushButton("展开所有")
        collapse_btn = QPushButton("折叠所有")
        test_insert_btn = QPushButton("测试插入行")
        
        button_layout.addWidget(expand_btn)
        button_layout.addWidget(collapse_btn)
        button_layout.addWidget(test_insert_btn)
        
        # 创建表格
        self.table = TreeTableWidget()
        
        # 连接按钮信号
        expand_btn.clicked.connect(self.table.expand_all)
        collapse_btn.clicked.connect(self.table.collapse_all)
        test_insert_btn.clicked.connect(self.table.add_test_row)
        
        # 添加到主布局
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        
        # 初始化时添加展开指示符
        self.init_parent_indicators()
        
    def init_parent_indicators(self):
        """初始化父行指示符"""
        for parent_row in self.table.parent_rows:
            name_item = self.table.item(parent_row, 0)
            current_text = name_item.text()
            if not current_text.startswith("▼ "):
                name_item.setText("▼ " + current_text)

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()