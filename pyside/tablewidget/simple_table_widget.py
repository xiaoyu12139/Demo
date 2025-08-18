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
        # self.setSectionsClickable(True)
        # self.setSectionsMovable(False)
        # self.setDefaultSectionSize(120)
        
        # 定义需要复选框的列
        self.checkbox_columns: Set[int] = {1, 2, 3}  # 第1、2、3列有复选框
        
        # 存储复选框状态
        self.checkbox_states: Dict[int, bool] = {}
        for col in self.checkbox_columns:
            self.checkbox_states[col] = False
        
        # 存储复选框区域用于点击检测
        self.checkbox_rects: Dict[int, QRect] = {}
    
    def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
        """绘制表头区域
        
        Args:
            painter: 绘制器
            rect: 绘制区域
            logicalIndex: 逻辑列索引
        """
        painter.save()
        
        # 获取表头文本
        text = self.model().headerData(logicalIndex, self.orientation(), Qt.ItemDataRole.DisplayRole)
        
        # 绘制背景
        painter.fillRect(rect, self.palette().button())
        
        # 绘制边框
        painter.setPen(self.palette().dark().color())
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
        
        # 设置文本颜色
        painter.setPen(self.palette().buttonText().color())
        
        if logicalIndex in self.checkbox_columns:
            # 有复选框的列：绘制复选框和文本
            self._draw_checkbox(painter, rect, logicalIndex)
            # 文本右移为复选框留空间
            text_rect = rect.adjusted(25, 0, 0, 0)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, str(text))
        else:
            # 普通列：居中绘制文本
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(text))
        
        painter.restore()
    
    def _draw_checkbox(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
        """绘制复选框
        
        Args:
            painter: 绘制器
            rect: 表头区域
            logicalIndex: 列索引
        """
        # 复选框参数
        checkbox_size = 16
        margin = 5
        
        # 计算复选框位置
        checkbox_x = rect.left() + margin
        checkbox_y = rect.center().y() - checkbox_size // 2
        checkbox_rect = QRect(checkbox_x, checkbox_y, checkbox_size, checkbox_size)
        
        # 保存复选框区域用于点击检测
        self.checkbox_rects[logicalIndex] = checkbox_rect
        
        # 使用QStyle绘制复选框
        from PySide6.QtWidgets import QStyleOptionButton
        option = QStyleOptionButton()
        option.rect = checkbox_rect
        option.state = QStyle.StateFlag.State_Enabled
        if self.checkbox_states.get(logicalIndex, False):
            option.state |= QStyle.StateFlag.State_On
        else:
            option.state |= QStyle.StateFlag.State_Off
        
        self.style().drawControl(QStyle.ControlElement.CE_CheckBox, option, painter, QCheckBox())
    
    def mousePressEvent(self, event) -> None:
        """处理鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            logical_index = self.logicalIndexAt(event.position().toPoint())
            
            # 检查是否点击了复选框
            if logical_index in self.checkbox_columns:
                checkbox_rect = self.checkbox_rects.get(logical_index)
                if checkbox_rect and checkbox_rect.contains(event.position().toPoint()):
                    # 切换复选框状态
                    self.checkbox_states[logical_index] = not self.checkbox_states.get(logical_index, False)
                    
                    # 通知父组件状态变化
                    if hasattr(self.parent(), 'on_header_checkbox_changed'):
                        self.parent().on_header_checkbox_changed(logical_index, self.checkbox_states[logical_index])
                    
                    # 重绘表头
                    self.viewport().update()
                    return
        
        super().mousePressEvent(event)

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