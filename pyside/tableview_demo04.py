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
        
        button_layout.addWidget(expand_btn)
        button_layout.addWidget(collapse_btn)
        
        # 创建表格
        self.table = TreeTableWidget()
        
        # 连接按钮信号
        expand_btn.clicked.connect(self.table.expand_all)
        collapse_btn.clicked.connect(self.table.collapse_all)
        
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