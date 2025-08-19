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
        painter.save()
        
        # 绘制背景
        painter.fillRect(rect, Qt.lightGray)
        
        # 绘制边框
        painter.setPen(Qt.black)
        painter.drawRect(rect)
        
        # 检查绘制所有表头section的状态
        self._check_all_sections()
        
        # 首先隐藏所有复选框，避免错位显示
        for checkbox in self.checkboxes.values():
            checkbox.hide()
        
        # 如果这一列需要复选框，则定位复选框控件
        if logicalIndex in self.checkbox_columns:
            checkbox = self.checkboxes[logicalIndex]
            
            # 设置复选框位置 - 直接基于绘制区域rect计算位置
            checkbox_size = 20
            
            # 检查rect是否有效且在可见区域内
            if rect.width() > checkbox_size + 10 and rect.x() >= 0:
                checkbox_x = rect.x() + 5
                checkbox_y = rect.y() + (rect.height() - checkbox_size) // 2
                
                # 确保复选框完全在rect范围内
                if checkbox_x + checkbox_size <= rect.x() + rect.width():
                    checkbox.setGeometry(checkbox_x, checkbox_y, checkbox_size, checkbox_size)
                    checkbox.show()
                else:
                    checkbox.hide()
            else:
                checkbox.hide()
            
            # 绘制文本（在复选框右侧）
            text = f"Column {logicalIndex}"
            text_rect = QRect(rect.x() + 30, rect.y(), rect.width() - 30, rect.height())
            
            # 设置文本颜色和字体
            painter.setPen(Qt.black)
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        else:
            # 绘制默认文本
            text = f"Header {logicalIndex}"
            painter.setPen(Qt.black)
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, text)
        
        painter.restore()
    
    def _check_all_sections(self) -> None:
        """检查所有表头section的状态
        
        确保所有section的复选框状态和显示都是正确的
        """
        # 遍历所有可见的section
        for i in range(self.count()):
            logical_index = self.logicalIndex(i)
            
            # 检查该section是否应该有复选框
            if logical_index in self.checkbox_columns:
                checkbox = self.checkboxes.get(logical_index)
                if checkbox:
                    # 确保复选框存在且状态正确
                    expected_state = self.checkbox_states.get(logical_index, False)
                    if checkbox.isChecked() != expected_state:
                        checkbox.setChecked(expected_state)
                        
                    # 获取section的几何信息
                    section_pos = self.sectionPosition(logical_index)
                    section_size = self.sectionSize(logical_index)
                    
                    # 检查section是否在可见区域内
                    viewport_rect = self.viewport().rect()
                    if section_pos >= 0 and section_pos < viewport_rect.width():
                        # section可见，但复选框位置将在paintSection中具体设置
                        pass
    
    def _on_checkbox_changed(self, column: int, state: int) -> None:
        """复选框状态改变回调
        
        Args:
            column: 列索引
            state: 复选框状态
        """
        is_checked = state == Qt.CheckState.Checked.value
        self.checkbox_states[column] = is_checked
        print(f"Column {column} checkbox changed to: {is_checked}")
    
    def trigger_repaint(self) -> None:
        """手动触发表头重绘
      print(f"显示复选框 - Section {logical_index}: pos=({checkbox_x}, {checkbox_y}), size={ch ckbox_size}")
                        e     
        提供多种重绘方式：
        1. update() - 异步重绘，性能较好
        2. r        print(f"隐藏复选框 - Section {logicap_index}: section_size={aection_sizi} 太小")
                    elsent() - 立即重绘，性能较差但立即生效
        3. viewpor)
                        print(f"隐藏复选框 - Section {logical_index}: section_pos={section_pos} 不在可见区域"t().update() - 重绘视口区域
        """
        # 方法1：异步更新（推荐）
        QWidget.update(self)  # 明确调用QWidget的update方法
        
        # 方法2：立即重绘（可选，取消注释使用）
        # self.repaint()
        
        # 方法3：更新视口（可选，取消注释使用）
        # self.viewport().update()
        
        print("表头重绘已触发")
    
    def trigger_section_repaint(self, logical_index: int) -> None:
        """手动触发指定section的重绘
        
        Args:
            logical_index: 要重绘的section的逻辑索引
        """
        # 获取指定section的几何区域
        section_pos = self.sectionPosition(logical_index)
        section_size = self.sectionSize(logical_index)
        
        if section_pos >= 0 and section_size > 0:
            # 计算section的矩形区域
            if self.orientation() == Qt.Horizontal:
                section_rect = QRect(section_pos, 0, section_size, self.height())
            else:
                section_rect = QRect(0, section_pos, self.width(), section_size)
            
            # 更新指定区域 - 使用QWidget的update方法
            QWidget.update(self, section_rect)
            print(f"Section {logical_index} 重绘已触发")
        else:
            print(f"Section {logical_index} 不可见或无效")
    


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
        
        # 添加重绘控制按钮
        self.add_repaint_controls(frame_layout)
        
        # 添加示例数据
        self.add_sample_data()
        
        # 设置样式
        self.setup_styles()
    
    def add_repaint_controls(self, layout: QVBoxLayout) -> None:
        """添加重绘控制按钮
        
        Args:
            layout: 要添加按钮的布局
        """
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 全表头重绘按钮
        repaint_all_btn = QPushButton("重绘整个表头")
        repaint_all_btn.clicked.connect(self.on_repaint_all_clicked)
        button_layout.addWidget(repaint_all_btn)
        
        # 重绘指定section按钮
        repaint_section_btn = QPushButton("重绘Section 1")
        repaint_section_btn.clicked.connect(lambda: self.on_repaint_section_clicked(1))
        button_layout.addWidget(repaint_section_btn)
        
        # 立即重绘按钮
        repaint_immediate_btn = QPushButton("立即重绘")
        repaint_immediate_btn.clicked.connect(self.on_repaint_immediate_clicked)
        button_layout.addWidget(repaint_immediate_btn)
        
        # 重绘视口按钮
        repaint_viewport_btn = QPushButton("重绘视口")
        repaint_viewport_btn.clicked.connect(self.on_repaint_viewport_clicked)
        button_layout.addWidget(repaint_viewport_btn)
        
        # 添加到主布局
        layout.addLayout(button_layout)
    
    def on_repaint_all_clicked(self) -> None:
        """全表头重绘按钮点击事件"""
        print("=== 触发全表头重绘 ===")
        self.custom_header.trigger_repaint()
    
    def on_repaint_section_clicked(self, section: int) -> None:
        """指定section重绘按钮点击事件
        
        Args:
            section: section索引
        """
        print(f"=== 触发Section {section}重绘 ===")
        self.custom_header.trigger_section_repaint(section)
    
    def on_repaint_immediate_clicked(self) -> None:
        """立即重绘按钮点击事件"""
        print("=== 触发立即重绘 ===")
        self.custom_header.repaint()
        print("立即重绘完成")
    
    def on_repaint_viewport_clicked(self) -> None:
        """重绘视口按钮点击事件"""
        print("=== 触发视口重绘 ===")
        self.custom_header.viewport().update()
        print("视口重绘已触发")
    
    def setup_table(self):
        """设置表格基本属性"""
        # 设置表格大小
        self.table_widget.setRowCount(5)
        self.table_widget.setColumnCount(4)
        
        # 设置表头
        headers = ["姓名", "年龄", "职业", "城市"]
        # self.table_widget.setHorizontalHeaderLabels(headers)
        
        # 使用自定义表头
        self.custom_header = CustomHeaderView(Qt.Horizontal, self.table_widget)
        self.table_widget.setHorizontalHeader(self.custom_header)
    
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