import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QFrame, QTableWidget, QWidget, QHeaderView, QCheckBox, QStyleOptionButton
)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QFontMetrics
from PySide6.QtWidgets import QStyle

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
        self.setSectionsClickable(True)
        self.setSectionsMovable(False)
        self.setDefaultSectionSize(120)
        
        # 定义需要复选框的列
        self.checkbox_columns: Set[int] = {1, 2, 3}  # 第1、2、3列有复选框
        
        # 存储复选框状态
        self.checkbox_states: Dict[int, bool] = {}
        for col in self.checkbox_columns:
            self.checkbox_states[col] = False
        
        # 存储复选框控件
        self.checkboxes: Dict[int, QCheckBox] = {}
        
        # 创建实际的复选框控件
        for col in self.checkbox_columns:
            checkbox = QCheckBox(self)
            checkbox.setChecked(False)
            checkbox.stateChanged.connect(lambda state, c=col: self._on_checkbox_changed(c, state))
            self.checkboxes[col] = checkbox
    
    def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
        """绘制表头section
        
        Args:
            painter: 绘制器
            rect: 绘制区域
            logicalIndex: 逻辑索引
        """
        # 先绘制默认的表头背景
        super().paintSection(painter, rect, logicalIndex)
        
        # 如果这一列需要复选框，则定位复选框控件
        if logicalIndex in self.checkbox_columns:
            checkbox = self.checkboxes[logicalIndex]
            
            # 设置复选框位置
            checkbox_size = 20
            checkbox_x = rect.x() + 5
            checkbox_y = rect.y() + (rect.height() - checkbox_size) // 2
            checkbox.setGeometry(checkbox_x, checkbox_y, checkbox_size, checkbox_size)
            checkbox.show()
            
            # 绘制文本（在复选框右侧）
            text = f"Column {logicalIndex}"
            text_rect = QRect(rect.x() + 30, rect.y(), rect.width() - 30, rect.height())
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, text)
    
    def _on_checkbox_changed(self, column: int, state: int) -> None:
        """复选框状态改变回调
        
        Args:
            column: 列索引
            state: 复选框状态
        """
        is_checked = state == Qt.CheckState.Checked.value
        self.checkbox_states[column] = is_checked
        print(f"Column {column} checkbox changed to: {is_checked}")
    


class SimpleTableWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简单的Table Widget")
        self.setGeometry(100, 100, 600, 400)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建Frame
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        main_layout.addWidget(self.frame)
        
        # 在Frame中创建布局
        frame_layout = QVBoxLayout(self.frame)
        
        # 创建Table Widget
        self.table_widget = QTableWidget()
        frame_layout.addWidget(self.table_widget)
        
        # 设置表格基本属性
        self.setup_table()
        
        # 添加示例数据
        self.add_sample_data()
        
        # 设置样式
        self.setup_styles()
    
    def setup_table(self):
        """设置表格基本属性"""
        # 设置表格大小
        self.table_widget.setRowCount(5)
        self.table_widget.setColumnCount(4)
        
        # 设置表头
        headers = ["姓名", "年龄", "职业", "城市"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        
        # 使用自定义表头
        custom_header = CustomHeaderView(Qt.Horizontal, self.table_widget)
        self.table_widget.setHorizontalHeader(custom_header)
    
    def add_sample_data(self):
        """添加示例数据"""
        # 示例数据
        data = [
            ["张三", "25", "工程师", "北京"],
            ["李四", "30", "设计师", "上海"],
            ["王五", "28", "产品经理", "广州"],
            ["赵六", "35", "销售", "深圳"],
            ["钱七", "22", "学生", "杭州"]
        ]
        
        # 填充数据到表格
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                from PySide6.QtWidgets import QTableWidgetItem
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)
    
    def setup_styles(self):
        """设置全局样式"""
        checkbox_style = """
        QCheckBox {
            spacing: 5px;
            font-size: 12px;
            color: #333333;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 2px solid #cccccc;
            border-radius: 3px;
            background-color: #ffffff;
        }
        
        QCheckBox::indicator:hover {
            border-color: #4CAF50;
            background-color: #f5f5f5;
        }
        
        QCheckBox::indicator:checked {
            background-color: #4CAF50;
            border-color: #4CAF50;
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
        }
        
        QCheckBox::indicator:checked:hover {
            background-color: #45a049;
            border-color: #45a049;
        }
        
        QCheckBox::indicator:disabled {
            background-color: #f0f0f0;
            border-color: #d0d0d0;
        }
        """
        
        self.setStyleSheet(checkbox_style)


def main():
    app = QApplication(sys.argv)
    window = SimpleTableWidget()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()