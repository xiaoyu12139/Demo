import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableView, QHeaderView, QPushButton, QSpinBox, QLabel,
    QComboBox, QTextEdit
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QFont

class SimpleIndentTableModel(QAbstractTableModel):
    """简单的表格模型，支持多种缩进方法"""
    
    def __init__(self):
        super().__init__()
        self.data_list = [
            ["项目1", "描述1", "值1"],
            ["项目2", "描述2", "值2"],
            ["项目3", "描述3", "值3"],
            ["项目4", "描述4", "值4"],
            ["项目5", "描述5", "值5"]
        ]
        self.headers = ["名称", "描述", "值"]
        
        # 存储每个单元格的缩进级别
        self.indent_levels = {}
        
        # 当前使用的缩进方法
        self.indent_method = "spaces"  # spaces, html, unicode
        
    def set_indent_level(self, row, column, level):
        """设置指定单元格的缩进级别"""
        self.indent_levels[(row, column)] = level
        index = self.index(row, column)
        self.dataChanged.emit(index, index)
        
    def get_indent_level(self, row, column):
        """获取指定单元格的缩进级别"""
        return self.indent_levels.get((row, column), 0)
        
    def set_indent_method(self, method):
        """设置缩进方法"""
        self.indent_method = method
        # 刷新所有数据
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount()-1, self.columnCount()-1))
        
    def rowCount(self, parent=QModelIndex()):
        return len(self.data_list)
        
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
        
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
            
        row, col = index.row(), index.column()
        
        if role == Qt.DisplayRole:
            original_text = self.data_list[row][col]
            indent_level = self.get_indent_level(row, col)
            
            if indent_level == 0:
                return original_text
                
            # 根据不同方法添加缩进
            if self.indent_method == "spaces":
                # 方法1：使用空格字符
                indent = "  " * indent_level  # 每级缩进2个空格
                return indent + original_text
                
            elif self.indent_method == "unicode":
                # 方法2：使用Unicode空白字符
                indent = "\u2003" * indent_level  # 使用em空格
                return indent + original_text
                
            elif self.indent_method == "html":
                # 方法3：使用HTML格式（需要在视图中启用富文本）
                indent_px = indent_level * 20
                return f'<span style="margin-left: {indent_px}px;">{original_text}</span>'
                
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignLeft | Qt.AlignVCenter
            
        return None
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None
        
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole and index.isValid():
            self.data_list[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False
        
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

class TableViewDemo07(QMainWindow):
    """TableView缩进演示 - 简单方法"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TableView 文本缩进演示 - 简单方法")
        self.setGeometry(100, 100, 900, 700)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建表格模型和视图
        self.model = SimpleIndentTableModel()
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        
        # 设置表格属性
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        
        # 创建控制面板
        control_panel = self.create_control_panel()
        
        # 创建说明文本
        info_text = self.create_info_text()
        
        # 添加到布局
        layout.addWidget(control_panel)
        layout.addWidget(self.table_view)
        layout.addWidget(info_text)
        
        # 初始化示例数据
        self.init_examples()
        
    def create_control_panel(self):
        """创建控制面板"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        
        # 行选择
        layout.addWidget(QLabel("行:"))
        self.row_spin = QSpinBox()
        self.row_spin.setRange(0, self.model.rowCount() - 1)
        layout.addWidget(self.row_spin)
        
        # 列选择
        layout.addWidget(QLabel("列:"))
        self.col_spin = QSpinBox()
        self.col_spin.setRange(0, self.model.columnCount() - 1)
        layout.addWidget(self.col_spin)
        
        # 缩进级别
        layout.addWidget(QLabel("缩进级别:"))
        self.indent_spin = QSpinBox()
        self.indent_spin.setRange(0, 10)
        layout.addWidget(self.indent_spin)
        
        # 缩进方法选择
        layout.addWidget(QLabel("缩进方法:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(["空格字符", "Unicode空白", "HTML样式"])
        self.method_combo.currentTextChanged.connect(self.on_method_changed)
        layout.addWidget(self.method_combo)
        
        # 应用按钮
        apply_btn = QPushButton("应用缩进")
        apply_btn.clicked.connect(self.apply_indent)
        layout.addWidget(apply_btn)
        
        # 清除按钮
        clear_btn = QPushButton("清除所有缩进")
        clear_btn.clicked.connect(self.clear_all_indents)
        layout.addWidget(clear_btn)
        
        # 示例按钮
        example_btn = QPushButton("应用示例")
        example_btn.clicked.connect(self.init_examples)
        layout.addWidget(example_btn)
        
        layout.addStretch()
        return panel
        
    def create_info_text(self):
        """创建说明文本"""
        info = QTextEdit()
        info.setMaximumHeight(150)
        info.setReadOnly(True)
        info.setHtml("""
        <h3>三种简单的缩进实现方法：</h3>
        <ul>
        <li><b>空格字符：</b>在文本前添加普通空格，简单但可能因字体而异</li>
        <li><b>Unicode空白：</b>使用Unicode em空格(\u2003)，宽度更一致</li>
        <li><b>HTML样式：</b>使用HTML的margin-left样式，精确控制像素</li>
        </ul>
        <p><b>优点：</b>实现简单，无需自定义委托</p>
        <p><b>缺点：</b>空格方法可能不够精确，HTML方法需要富文本支持</p>
        """)
        return info
        
    def on_method_changed(self, text):
        """缩进方法改变时的处理"""
        method_map = {
            "空格字符": "spaces",
            "Unicode空白": "unicode", 
            "HTML样式": "html"
        }
        method = method_map.get(text, "spaces")
        self.model.set_indent_method(method)
        
    def apply_indent(self):
        """应用缩进设置"""
        row = self.row_spin.value()
        col = self.col_spin.value()
        level = self.indent_spin.value()
        
        self.model.set_indent_level(row, col, level)
        print(f"已设置第{row}行第{col}列的缩进级别为{level}")
        
    def clear_all_indents(self):
        """清除所有缩进"""
        self.model.indent_levels.clear()
        self.model.dataChanged.emit(
            self.model.index(0, 0), 
            self.model.index(self.model.rowCount()-1, self.model.columnCount()-1)
        )
        print("已清除所有缩进")
        
    def init_examples(self):
        """初始化示例缩进"""
        # 清除现有缩进
        self.model.indent_levels.clear()
        
        # 设置示例缩进
        examples = [
            (0, 0, 0),  # 第0行第0列，无缩进
            (1, 0, 1),  # 第1行第0列，1级缩进
            (2, 0, 2),  # 第2行第0列，2级缩进
            (3, 0, 1),  # 第3行第0列，1级缩进
            (4, 0, 3),  # 第4行第0列，3级缩进
            (1, 1, 1),  # 第1行第1列，1级缩进
            (2, 1, 2),  # 第2行第1列，2级缩进
        ]
        
        for row, col, level in examples:
            self.model.set_indent_level(row, col, level)
            
        print("已应用示例缩进")

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    window = TableViewDemo07()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()