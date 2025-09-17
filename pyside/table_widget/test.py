import sys
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QColor, QMouseEvent
from PySide6.QtCore import Qt


class HoverTableWidget(QTableWidget):
    def __init__(self, rows, cols, parent=None):
        super().__init__(rows, cols, parent)

        # 打开鼠标追踪，否则 mouseMoveEvent 只有按下时才会触发
        self.setMouseTracking(True)

        # 默认选择整行
        self.setSelectionBehavior(QTableWidget.SelectRows)

        # 当前悬浮的行号
        self._hover_row = -1

    def mouseMoveEvent(self, event: QMouseEvent):
        row = self.rowAt(event.pos().y())
        if row != self._hover_row:  # 如果移动到了新行
            self._clear_hover_background()
            self._hover_row = row
            self._set_hover_background(row)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        """鼠标移出表格时清除悬浮效果"""
        self._clear_hover_background()
        self._hover_row = -1
        super().leaveEvent(event)

    def _set_hover_background(self, row: int):
        if row < 0:
            return
        for c in range(self.columnCount()):
            item = self.item(row, c)
            if item and not item.isSelected():  # 不覆盖选中状态
                item.setBackground(QColor("#E0F0FF"))

    def _clear_hover_background(self):
        for r in range(self.rowCount()):
            for c in range(self.columnCount()):
                item = self.item(r, c)
                if item and not item.isSelected():
                    item.setBackground(Qt.white)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    table = HoverTableWidget(10, 3)
    table.setWindowTitle("QTableWidget 悬浮高亮示例")

    # 填充数据
    for r in range(10):
        for c in range(3):
            table.setItem(r, c, QTableWidgetItem(f"Row {r}, Col {c}"))

    table.resize(400, 300)
    table.show()

    sys.exit(app.exec())
