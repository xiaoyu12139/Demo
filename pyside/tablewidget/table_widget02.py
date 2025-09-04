import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QHeaderView
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPalette, QColor, QPainter

class HoverTableWidget(QTableWidget):
    """支持鼠标悬停高亮行的表格控件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_hover_row = -1
        self.original_colors = {}  # 存储原始背景色
        
        # 启用鼠标跟踪
        self.setMouseTracking(True)
        
        # 设置表格样式
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        
        # 设置表头
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        
    def enterEvent(self, event):
        """鼠标进入表格区域"""
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """鼠标离开表格区域"""
        super().leaveEvent(event)
        # 清除悬停高亮
        self.clear_hover_highlight()
        
    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 用于跟踪当前悬停行"""
        super().mouseMoveEvent(event)
        
        # 获取鼠标位置对应的行
        row = self.rowAt(event.position().toPoint().y())
        print(f"鼠标移动到行: {row}")  # 调试信息
        
        if row >= 0 and row != self.current_hover_row:
            # 清除之前的高亮
            self.clear_hover_highlight()
            # 设置新的高亮
            self.set_hover_highlight(row)
        elif row < 0:
            # 鼠标不在任何行上，清除高亮
            self.clear_hover_highlight()
            
    def clear_hover_highlight(self):
        """清除悬停高亮效果"""
        if self.current_hover_row >= 0:
            # 恢复原始背景色
            for col in range(self.columnCount()):
                item = self.item(self.current_hover_row, col)
                if item and self.current_hover_row in self.original_colors:
                    original_color = self.original_colors[self.current_hover_row].get(col)
                    if original_color:
                        item.setBackground(original_color)
                    else:
                        # 恢复默认背景
                        item.setBackground(QColor())
            
            self.current_hover_row = -1
            
    def set_hover_highlight(self, row):
        """设置悬停高亮效果 - 整行高亮"""
        if row < 0 or row >= self.rowCount():
            return
            
        self.current_hover_row = row
        print(f"设置行 {row} 高亮")  # 调试信息
        
        # 保存原始颜色
        if row not in self.original_colors:
            self.original_colors[row] = {}
            
        # 设置高亮颜色 - 使用更明显的颜色
        highlight_color = QColor(255, 255, 0, 180)  # 半透明黄色
        
        # 对整行的所有列设置高亮背景色
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                # 保存原始背景色
                self.original_colors[row][col] = item.data(Qt.BackgroundRole)
                # 使用setData方法设置背景色，这样更可靠
                item.setData(Qt.BackgroundRole, highlight_color)
                print(f"设置单元格 ({row}, {col}) 背景色为黄色")  # 调试信息

class TableWidget02Demo(QMainWindow):
    """表格悬停高亮演示主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Widget 02 - 鼠标悬停高亮行演示")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建表格
        self.table = HoverTableWidget()
        layout.addWidget(self.table)
        
        # 初始化表格数据
        self.setup_table()
        
    def setup_table(self):
        """设置表格数据"""
        # 设置表格大小
        self.table.setRowCount(10)
        self.table.setColumnCount(4)
        
        # 设置表头
        headers = ["姓名", "年龄", "职业", "城市"]
        self.table.setHorizontalHeaderLabels(headers)
        
        # 添加示例数据
        sample_data = [
            ["张三", "25", "软件工程师", "北京"],
            ["李四", "30", "产品经理", "上海"],
            ["王五", "28", "UI设计师", "深圳"],
            ["赵六", "35", "项目经理", "广州"],
            ["钱七", "26", "前端开发", "杭州"],
            ["孙八", "32", "后端开发", "成都"],
            ["周九", "29", "测试工程师", "西安"],
            ["吴十", "27", "运维工程师", "南京"],
            ["郑十一", "31", "数据分析师", "武汉"],
            ["王十二", "24", "实习生", "重庆"]
        ]
        
        # 填充数据
        for row, row_data in enumerate(sample_data):
            for col, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
        
        # 调整列宽
        self.table.resizeColumnsToContents()
        
        # 设置表格样式 - 移除可能干扰悬停效果的样式
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #3daee9;
                color: white;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 8px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
        """)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = TableWidget02Demo()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()