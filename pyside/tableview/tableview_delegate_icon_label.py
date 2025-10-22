"""
TableView + Delegate 示例：在委托的 paint 中把带 icon 的 QLabel 渲染到单元格右侧。

运行：python tableview_delegate_icon_label.py
"""
from typing import Optional, List
import os

from PySide6.QtCore import Qt, QRect, QPoint, QTimer, QModelIndex
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QLabel,
    QStyle,
    QStyleOption,
    QMenu,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem


class IconLabelDelegate(QStyledItemDelegate):
    """在每个单元格右侧绘制一个包含图标的 QLabel。

    如果提供 icon_path，则使用该图标；否则退回到样式的标准下拉箭头图标。
    """

    def __init__(self, icon_path: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.icon: Optional[QIcon] = QIcon(icon_path) if icon_path else None

    def paint(self, painter, option: QStyleOptionViewItem, index) -> None:
        """在单元格右侧绘制包含图标的 QLabel，并保留文本区域。
        
        本方法首先缩小文本绘制区域，为右侧图标预留固定宽度；随后根据提供的自定义图标或
        样式的标准下拉箭头生成一个 QLabel 的位图，绘制到单元格右侧的图标区域。
        
        Args:
            painter (QPainter): 用于绘制单元格内容的画笔对象。
            option (QStyleOptionViewItem): 项视图的样式选项，包含矩形、状态等信息。
            index (QModelIndex): 当前单元格对应的模型索引。
        
        Returns:
            None: 直接在传入的 painter 上完成绘制，不返回任何值。
        
        Notes:
            - 图标区域宽度与行高相关，取 min(24, 行高)。
            - 若提供的自定义图标不可用，则回退到 QStyle.SP_ArrowDown 标准图标。
            - 使用 QLabel.grab() 生成位图以避免在委托环境中直接渲染 QWidget 的潜在问题。
        """
        # 保留默认绘制，但缩小文本区域，给右侧图标预留空间
        rect = option.rect
        icon_w = min(24, rect.height())
        text_opt = QStyleOptionViewItem(option)
        text_opt.rect = rect.adjusted(0, 0, -icon_w, 0)
        super().paint(painter, text_opt, index)

        # 图标区域：单元格右侧，宽度 icon_w
        icon_rect = QRect(rect.x() + rect.width() - icon_w, rect.y(), icon_w, rect.height())
        style = option.widget.style() if option.widget else QApplication.style()

        # 选择图标：优先自定义，其次标准箭头
        icon = self.icon if (self.icon and not self.icon.isNull()) else style.standardIcon(QStyle.SP_ArrowDown)

        painter.save()
        # 不再严格裁剪或平移，直接生成 QLabel 的位图并绘制到目标区域
        if icon and not icon.isNull():
            pm_icon = icon.pixmap(16, 16)
            label = QLabel()
            label.setAttribute(Qt.WA_TranslucentBackground, True)
            label.setStyleSheet("background: transparent; border: none;")
            label.setFixedSize(icon_rect.size())
            label.setAlignment(Qt.AlignCenter)
            label.setScaledContents(False)
            label.setPixmap(pm_icon)
            label.ensurePolished()
            # 生成标签的位图并绘制到单元格右侧区域
            pm_label = label.grab()
            x = icon_rect.x() + (icon_rect.width() - pm_label.width()) // 2
            y = icon_rect.y() + (icon_rect.height() - pm_label.height()) // 2
            painter.drawPixmap(x, y, pm_label)
        else:
            # 回退：绘制标准箭头原语
            arrow_opt = QStyleOption()
            arrow_opt.rect = icon_rect
            arrow_opt.state = option.state
            style.drawPrimitive(QStyle.PE_IndicatorArrowDown, arrow_opt, painter, option.widget)
        painter.restore()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TableView Delegate Icon Label Demo")
        self.resize(680, 420)

        self.view = QTableView(self)
        self.setCentralWidget(self.view)

        # 简单模型：三列若干行
        headers: List[str] = ["名称", "类型", "描述"]
        data: List[List[str]] = [
            ["Item 1", "Option A", "示例数据 1"],
            ["Item 2", "Option B", "示例数据 2"],
            ["Item 3", "Option C", "示例数据 3"],
            ["Item 4", "Option A", "示例数据 4"],
            ["Item 5", "Option B", "示例数据 5"],
        ]
        model = QStandardItemModel(len(data), len(headers), self)
        model.setHorizontalHeaderLabels(headers)
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                it = QStandardItem(str(val))
                it.setEditable(True)
                if c == 1:
                    it.setTextAlignment(Qt.AlignCenter)
                model.setItem(r, c, it)
        self.view.setModel(model)

        # 行高统一
        row_h = 32
        self.view.verticalHeader().setDefaultSectionSize(row_h)
        for r in range(model.rowCount()):
            self.view.setRowHeight(r, row_h)

        # 给第 2 列设置委托，在单元格右侧绘制图标
        base_dir = os.path.dirname(__file__)
        icon_path = os.path.abspath(os.path.join(base_dir, "..", "table_widget", "select.svg"))
        delegate = IconLabelDelegate(icon_path=icon_path, parent=self.view)
        self.view.setItemDelegateForColumn(1, delegate)

        # 交互与外观
        header = self.view.horizontalHeader()
        header.setStretchLastSection(False)
        header.setMinimumSectionSize(100)
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        # 启用自定义右键菜单，并让位置跟随鼠标
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.on_context_menu)
        self.view.setStyleSheet(
            "QTableView { background-color: #f5f7fa; gridline-color: #d0d7de; } "
            "QHeaderView::section { border: none; border-right: 1px solid #d0d7de; border-bottom: none; } "
        )

        # 初始适配列宽
        QTimer.singleShot(0, self._fit_columns)

    def _fit_columns(self):
        vw = self.view.viewport().width()
        cols = self.view.model().columnCount()
        # 简单分配：前两列固定最小值，最后一列占剩余
        min_w = 140
        for c in range(cols - 1):
            self.view.setColumnWidth(c, min_w)
        self.view.setColumnWidth(cols - 1, max(min_w, vw - (cols - 1) * min_w))

    def on_context_menu(self, pos: QPoint) -> None:
        """在鼠标位置显示表格右键菜单，并选中鼠标所在行。

        Args:
            pos (QPoint): 由 QTableView 发出的 viewport 坐标。
        """
        # 根据鼠标位置选中该行
        index = self.view.indexAt(pos)
        if index.isValid():
            self.view.selectRow(index.row())

        # 将视口坐标映射为全局坐标，确保菜单跟随鼠标
        global_pos = self.view.viewport().mapToGlobal(pos)

        # 构造菜单
        menu = QMenu(self)
        # 菜单样式：消除选中项圆角与菜单矩形之间的颜色不一致问题
        # 做法：item 默认透明；选中时使用主题高亮色并取消圆角，让高亮色充满整行
        menu.setStyleSheet(
            """
            QMenu {
                background-color: palette(Base);
                border: 1px solid #d0d7de;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                background-color: transparent;
                color: palette(WindowText);
                padding: 6px 12px;
                border-radius: 0; /* 取消圆角，避免与菜单圆角之间出现颜色不一致的过渡区 */
            }
            QMenu::item:selected {
                background-color: palette(Highlight);
                color: palette(HighlightedText);
                border-radius: 0; /* 选中项充满整行的矩形区域，颜色一致 */
            }
            QMenu::item:disabled {
                color: #9aa0a6;
            }
            QMenu::separator {
                height: 1px;
                background: #e5e7eb;
                margin: 6px 8px;
            }
            """
        )
        act_copy = menu.addAction("复制该行文本")
        act_delete = menu.addAction("删除该行")

        chosen = menu.exec(global_pos)
        if chosen == act_copy and index.isValid():
            model = self.view.model()
            r = index.row()
            cols = model.columnCount()
            values = [str(model.index(r, c).data() or "") for c in range(cols)]
            QApplication.clipboard().setText("\t".join(values))
        elif chosen == act_delete and index.isValid():
            self.view.model().removeRow(index.row())


def main():
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()