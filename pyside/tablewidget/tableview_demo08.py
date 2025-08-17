import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableView, QHeaderView, QPushButton, QSpinBox, QLabel,
    QStyledItemDelegate, QStyleOptionViewItem, QComboBox, QTextEdit, QStyle
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QRect
from PySide6.QtGui import QPainter, QFont, QFontMetrics, QColor

class IndentedTextDelegate(QStyledItemDelegate):
    """缩进文本委托"""
    
    def __init__(self, indent_width=20, parent=None):
        super().__init__(parent)
        self.indent_width = indent_width
        
    def paint(self, painter, option, index):
        painter.save()
        
        # 获取原始矩形
        rect = option.rect
        
        # 绘制背景
        if option.state & QStyle.State_Selected:
            painter.fillRect(rect, option.palette.highlight())
            painter.setPen(option.palette.highlightedText().color())
        else:
            painter.fillRect(rect, option.palette.base())
            painter.setPen(option.palette.text().color())
            
        # 设置字体
        font = option.font
        painter.setFont(font)
        
        # 获取文本
        text = index.data(Qt.DisplayRole)
        if text:
            # 创建缩进后的矩形
            indented_rect = QRect(
                rect.x() + self.indent_width,
                rect.y(),
                rect.width() - self.indent_width,
                rect.height()
            )
            
            # 绘制文本
            painter.drawText(indented_rect, Qt.AlignLeft | Qt.AlignVCenter, str(text))
            
        painter.restore()

class ColoredTextDelegate(QStyledItemDelegate):
    """彩色文本委托"""
    
    def __init__(self, text_color=QColor(255, 0, 0), parent=None):
        super().__init__(parent)
        self.text_color = text_color
        
    def paint(self, painter, option, index):
        painter.save()
        
        # 获取原始矩形
        rect = option.rect
        
        # 绘制背景
        if option.state & QStyle.State_Selected:
            painter.fillRect(rect, option.palette.highlight())
        else:
            painter.fillRect(rect, option.palette.base())
            
        # 设置字体和颜色
        font = option.font
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(self.text_color)
        
        # 获取文本
        text = index.data(Qt.DisplayRole)
        if text:
            painter.drawText(rect, Qt.AlignCenter, str(text))
            
        painter.restore()

class BorderDelegate(QStyledItemDelegate):
    """边框委托"""
    
    def __init__(self, border_color=QColor(0, 0, 255), parent=None):
        super().__init__(parent)
        self.border_color = border_color
        
    def paint(self, painter, option, index):
        painter.save()
        
        # 绘制默认内容
        super().paint(painter, option, index)
        
        # 绘制边框
        painter.setPen(self.border_color)
        painter.drawRect(option.rect.adjusted(0, 0, -1, -1))
        
        painter.restore()

class TableModel(QAbstractTableModel):
    """表格数据模型"""
    
    def __init__(self):
        super().__init__()
        self.data_list = [
            ["普通行1", "数据1", "值1"],
            ["缩进行1", "数据2", "值2"],
            ["彩色行1", "数据3", "值3"],
            ["边框行1", "数据4", "值4"],
            ["普通行2", "数据5", "值5"],
            ["缩进行2", "数据6", "值6"],
            ["彩色行2", "数据7", "值7"],
            ["边框行2", "数据8", "值8"],
        ]
        self.headers = ["名称", "描述", "值"]
        
    def rowCount(self, parent=QModelIndex()):
        return len(self.data_list)
        
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
        
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
            
        if role == Qt.DisplayRole:
            return self.data_list[index.row()][index.column()]
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

class TableViewDemo08(QMainWindow):
    """TableView行级自定义委托演示"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TableView Demo 08 - 行级自定义委托")
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建表格模型和视图
        self.model = TableModel()
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        
        # 设置表格属性
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setRowHeight(0, 40)  # 设置行高
        
        # 创建不同的委托
        self.indent_delegate = IndentedTextDelegate(30)
        self.colored_delegate = ColoredTextDelegate(QColor(255, 0, 0))
        self.border_delegate = BorderDelegate(QColor(0, 0, 255))
        
        # 创建控制面板
        control_panel = self.create_control_panel()
        
        # 创建说明文本
        info_text = self.create_info_text()
        
        # 添加到布局
        layout.addWidget(control_panel)
        layout.addWidget(self.table_view)
        layout.addWidget(info_text)
        
        # 初始化委托设置
        self.init_delegates()
        
    def create_control_panel(self):
        """创建控制面板"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        
        # 行选择
        layout.addWidget(QLabel("行:"))
        self.row_spin = QSpinBox()
        self.row_spin.setRange(0, self.model.rowCount() - 1)
        layout.addWidget(self.row_spin)
        
        # 委托类型选择
        layout.addWidget(QLabel("委托类型:"))
        self.delegate_combo = QComboBox()
        self.delegate_combo.addItems(["默认", "缩进", "彩色", "边框"])
        layout.addWidget(self.delegate_combo)
        
        # 应用按钮
        apply_btn = QPushButton("应用委托")
        apply_btn.clicked.connect(self.apply_delegate)
        layout.addWidget(apply_btn)
        
        # 清除按钮
        clear_btn = QPushButton("清除所有委托")
        clear_btn.clicked.connect(self.clear_all_delegates)
        layout.addWidget(clear_btn)
        
        # 重置示例按钮
        reset_btn = QPushButton("重置示例")
        reset_btn.clicked.connect(self.init_delegates)
        layout.addWidget(reset_btn)
        
        layout.addStretch()
        return panel
        
    def create_info_text(self):
        """创建说明文本"""
        info = QTextEdit()
        info.setMaximumHeight(120)
        info.setReadOnly(True)
        info.setHtml("""
        <h3>行级自定义委托演示：</h3>
        <ul>
        <li><b>缩进委托：</b>为指定行添加左边距缩进效果</li>
        <li><b>彩色委托：</b>为指定行设置红色粗体文本</li>
        <li><b>边框委托：</b>为指定行添加蓝色边框</li>
        </ul>
        <p><b>使用方法：</b>选择行号和委托类型，点击"应用委托"按钮</p>
        """)
        return info
        
    def apply_delegate(self):
        """应用委托到指定行"""
        row = self.row_spin.value()
        delegate_type = self.delegate_combo.currentText()
        
        # 应用新委托
        if delegate_type == "缩进":
            delegate = self.indent_delegate
        elif delegate_type == "彩色":
            delegate = self.colored_delegate
        elif delegate_type == "边框":
            delegate = self.border_delegate
        else:
            delegate = None
            
        # 为指定行设置委托
        self.table_view.setItemDelegateForRow(row, delegate)
                
        print(f"已为第{row}行应用{delegate_type}委托")
        
    def clear_all_delegates(self):
        """清除所有自定义委托"""
        for row in range(self.model.rowCount()):
            self.table_view.setItemDelegateForRow(row, None)
        print("已清除所有自定义委托")
        
    def init_delegates(self):
        """初始化委托设置"""
        # 清除所有委托
        self.clear_all_delegates()
        
        # 设置示例委托
        delegate_settings = [
            (1, self.indent_delegate),   # 第1行使用缩进委托
            (2, self.colored_delegate),  # 第2行使用彩色委托
            (3, self.border_delegate),   # 第3行使用边框委托
            (5, self.indent_delegate),   # 第5行使用缩进委托
            (6, self.colored_delegate),  # 第6行使用彩色委托
            (7, self.border_delegate),   # 第7行使用边框委托
        ]
        
        for row, delegate in delegate_settings:
            if row < self.model.rowCount():
                self.table_view.setItemDelegateForRow(row, delegate)
                    
        print("已初始化示例委托设置")

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    window = TableViewDemo08()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()