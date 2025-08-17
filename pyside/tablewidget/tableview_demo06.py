import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableView, QHeaderView, QPushButton, QSpinBox, QLabel,
    QStyledItemDelegate, QStyleOptionViewItem, QComboBox
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QRect
from PySide6.QtGui import QPainter, QFont, QFontMetrics


class IndentedTextDelegate(QStyledItemDelegate):
    """自定义委托，支持指定文本左边空格宽度"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.indent_widths = {}  # 存储每个单元格的缩进宽度
        
    def set_indent_width(self, row, column, width):
        """设置指定单元格的缩进宽度"""
        self.indent_widths[(row, column)] = width
        
    def get_indent_width(self, row, column):
        """获取指定单元格的缩进宽度"""
        return self.indent_widths.get((row, column), 0)
        
    def paint(self, painter, option, index):
        """自定义绘制方法"""
        if not index.isValid():
            return
            
        # 获取缩进宽度
        indent_width = self.get_indent_width(index.row(), index.column())
        
        # 获取文本
        text = index.data(Qt.DisplayRole)
        if text is None:
            text = ""
            
        # 设置绘制区域
        rect = option.rect
        
        # 绘制背景
        if option.state & QStyleOptionViewItem.State.State_Selected:
            painter.fillRect(rect, option.palette.highlight())
        else:
            painter.fillRect(rect, option.palette.base())
            
        # 设置文本颜色
        if option.state & QStyleOptionViewItem.State.State_Selected:
            painter.setPen(option.palette.highlightedText().color())
        else:
            painter.setPen(option.palette.text().color())
            
        # 设置字体
        font = option.font
        painter.setFont(font)
        
        # 计算文本绘制位置（添加缩进）
        text_rect = QRect(
            rect.left() + indent_width + 5,  # 左边距 + 缩进宽度 + 额外间距
            rect.top(),
            rect.width() - indent_width - 10,  # 减去缩进宽度和间距
            rect.height()
        )
        
        # 绘制文本
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, str(text))
        
        # 如果有缩进，绘制缩进指示线（可选）
        if indent_width > 0:
            painter.setPen(Qt.lightGray)
            painter.drawLine(
                rect.left() + indent_width,
                rect.top(),
                rect.left() + indent_width,
                rect.bottom()
            )

class TableModel(QAbstractTableModel):
    """表格数据模型"""
    
    def __init__(self):
        super().__init__()
        self.headers = ["名称", "类型", "大小", "修改时间"]
        self.data_list = [
            ["文档", "文件夹", "-", "2024-01-15"],
            ["项目报告.docx", "Word文档", "2.5 MB", "2024-01-14"],
            ["数据分析", "文件夹", "-", "2024-01-13"],
            ["销售数据.xlsx", "Excel文档", "1.8 MB", "2024-01-12"],
            ["图表.png", "图片", "856 KB", "2024-01-11"],
            ["源代码", "文件夹", "-", "2024-01-10"],
            ["main.py", "Python文件", "15 KB", "2024-01-09"],
            ["config.json", "JSON文件", "2 KB", "2024-01-08"],
            ["备份", "文件夹", "-", "2024-01-07"],
            ["readme.txt", "文本文件", "5 KB", "2024-01-06"]
        ]
        
    def rowCount(self, parent=QModelIndex()):
        return len(self.data_list)
        
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
        
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
            
        if role == Qt.DisplayRole:
            return self.data_list[index.row()][index.column()]
            
        return None
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.data_list[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False
        
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

class TableViewDemo06(QMainWindow):
    """TableView演示 - 指定单元格左边文本空格宽度"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TableView Demo 06 - 单元格文本缩进控制")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建控制面板
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # 创建表格视图
        self.table_view = QTableView()
        self.model = TableModel()
        self.table_view.setModel(self.model)
        
        # 创建自定义委托
        self.delegate = IndentedTextDelegate()
        self.table_view.setItemDelegate(self.delegate)
        
        # 设置表格属性
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)
        
        # 设置列宽
        header = self.table_view.horizontalHeader()
        header.resizeSection(0, 200)  # 名称列
        header.resizeSection(1, 120)  # 类型列
        header.resizeSection(2, 100)  # 大小列
        
        main_layout.addWidget(self.table_view)
        
        # 初始化一些缩进示例
        self.init_indent_examples()
        
    def create_control_panel(self):
        """创建控制面板"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        
        # 行选择
        layout.addWidget(QLabel("行:"))
        self.row_spinbox = QSpinBox()
        self.row_spinbox.setRange(0, 9)
        self.row_spinbox.setValue(0)
        layout.addWidget(self.row_spinbox)
        
        # 列选择
        layout.addWidget(QLabel("列:"))
        self.column_combobox = QComboBox()
        self.column_combobox.addItems(["名称", "类型", "大小", "修改时间"])
        layout.addWidget(self.column_combobox)
        
        # 缩进宽度
        layout.addWidget(QLabel("缩进宽度:"))
        self.indent_spinbox = QSpinBox()
        self.indent_spinbox.setRange(0, 200)
        self.indent_spinbox.setSuffix(" px")
        self.indent_spinbox.setValue(0)
        layout.addWidget(self.indent_spinbox)
        
        # 应用按钮
        apply_btn = QPushButton("应用缩进")
        apply_btn.clicked.connect(self.apply_indent)
        layout.addWidget(apply_btn)
        
        # 清除按钮
        clear_btn = QPushButton("清除所有缩进")
        clear_btn.clicked.connect(self.clear_all_indents)
        layout.addWidget(clear_btn)
        
        # 预设按钮
        preset_btn = QPushButton("应用预设缩进")
        preset_btn.clicked.connect(self.apply_preset_indents)
        layout.addWidget(preset_btn)
        
        layout.addStretch()
        
        return panel
        
    def apply_indent(self):
        """应用缩进到指定单元格"""
        row = self.row_spinbox.value()
        column = self.column_combobox.currentIndex()
        indent_width = self.indent_spinbox.value()
        
        # 设置缩进
        self.delegate.set_indent_width(row, column, indent_width)
        
        # 刷新表格
        index = self.model.index(row, column)
        self.table_view.update(index)
        
        print(f"已设置第{row}行第{column}列的缩进宽度为{indent_width}px")
        
    def clear_all_indents(self):
        """清除所有缩进"""
        self.delegate.indent_widths.clear()
        self.table_view.viewport().update()
        print("已清除所有缩进")
        
    def apply_preset_indents(self):
        """应用预设的缩进示例"""
        # 清除现有缩进
        self.delegate.indent_widths.clear()
        
        # 设置预设缩进（模拟文件夹结构）
        # 文件夹项目不缩进
        self.delegate.set_indent_width(0, 0, 0)   # 文档 (文件夹)
        self.delegate.set_indent_width(1, 0, 20)  # 项目报告.docx (文件)
        self.delegate.set_indent_width(2, 0, 0)   # 数据分析 (文件夹)
        self.delegate.set_indent_width(3, 0, 20)  # 销售数据.xlsx (文件)
        self.delegate.set_indent_width(4, 0, 20)  # 图表.png (文件)
        self.delegate.set_indent_width(5, 0, 0)   # 源代码 (文件夹)
        self.delegate.set_indent_width(6, 0, 20)  # main.py (文件)
        self.delegate.set_indent_width(7, 0, 20)  # config.json (文件)
        self.delegate.set_indent_width(8, 0, 0)   # 备份 (文件夹)
        self.delegate.set_indent_width(9, 0, 20)  # readme.txt (文件)
        
        # 刷新表格
        self.table_view.viewport().update()
        print("已应用预设缩进（模拟文件夹结构）")
        
    def init_indent_examples(self):
        """初始化一些缩进示例"""
        # 设置一些初始缩进作为演示
        self.delegate.set_indent_width(1, 0, 15)  # 第2行第1列缩进15px
        self.delegate.set_indent_width(3, 0, 15)  # 第4行第1列缩进15px
        self.delegate.set_indent_width(4, 0, 15)  # 第5行第1列缩进15px
        self.delegate.set_indent_width(6, 0, 15)  # 第7行第1列缩进15px
        self.delegate.set_indent_width(7, 0, 15)  # 第8行第1列缩进15px
        self.delegate.set_indent_width(9, 0, 15)  # 第10行第1列缩进15px

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QTableView {
            gridline-color: #d0d0d0;
            background-color: white;
            alternate-background-color: #f8f8f8;
            selection-background-color: #3daee9;
            border: 1px solid #c0c0c0;
        }
        QTableView::item {
            padding: 5px;
            border: none;
        }
        QTableView::item:selected {
            background-color: #3daee9;
            color: white;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            padding: 8px;
            border: 1px solid #c0c0c0;
            font-weight: bold;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 14px;
            border-radius: 4px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QSpinBox, QComboBox {
            padding: 5px;
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            background-color: white;
        }
        QLabel {
            font-weight: bold;
            color: #333;
        }
    """)
    
    window = TableViewDemo06()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()