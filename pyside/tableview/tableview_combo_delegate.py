"""TableView ComboBox 委托示例。

该模块演示如何在 PySide6 中使用 QStyledItemDelegate，使 QTableView 的单元格在编辑时使用 QComboBox 作为编辑器。

示例窗口（<MainWindow>）包含一个由 QStandardItemModel 支撑的表格视图，其中第二列“类型”使用由 <ComboBoxDelegate> 实现的下拉列表编辑器。

典型用法：
    - 双击第二列单元格以打开下拉框；
    - 选择一个选项，所选值会回写到模型。
"""
# 类型注解
from typing import List, Optional
# PySide 导入
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QStyledItemDelegate,
    QComboBox,
    QWidget,
    QStyleOptionViewItem,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QLabel,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPainter
from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel, QTimer, QEvent, QRect, QPoint
import os


class ComboBoxDelegate(QStyledItemDelegate):
    """使用 QComboBox 作为单元格编辑器的委托。

    该委托将默认编辑器替换为不可编辑的下拉框，并展示一组预定义选项。

    Args:
        items: 要显示在下拉框中的字符串选项列表；若为 None，则默认为 ["Option A", "Option B", "Option C"]。
        parent: 可选的父级窗口部件。
    """

    def __init__(self, items: Optional[List[str]] = None, parent: Optional[QWidget] = None, arrow_icon_path: Optional[str] = None) -> None:
        super().__init__(parent)
        self.items: List[str] = items or ["Option A", "Option B", "Option C"]
        self.arrow_icon_path: Optional[str] = arrow_icon_path
        self.arrow_icon: Optional[QIcon] = QIcon(self.arrow_icon_path) if self.arrow_icon_path else None

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QComboBox:
        """为给定的索引创建编辑器部件。

        创建一个不可编辑的 QComboBox，并填充预定义选项。

        Args:
            parent: 视图提供的编辑器父级窗口部件。
            option: 描述编辑器显示方式的样式选项。
            index: 需要创建编辑器的模型索引。

        Returns:
            QComboBox: 已配置好的下拉框编辑器。
        """
        combo = QComboBox(parent)
        combo.addItems(self.items)
        # 使用非可编辑模式，避免下拉箭头被禁用/点击无效
        combo.setEditable(False)
        # 居中显示下拉项文本（也影响当前项文本的对齐）
        for i in range(combo.count()):
            combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        # 让下拉框编辑器紧贴单元格大小：去掉内部边框与内边距，并允许扩展
        combo.setFrame(False)
        combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        base_style = (
            "QComboBox { border: 0px; padding: 0px; } "
            "QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 20px; margin: 0px; border: none; }"
        )
        if self.arrow_icon_path:
            base_style += (
                f" QComboBox::down-arrow {{ image: url({self.arrow_icon_path}); width: 16px; height: 16px; }}"
            )
        combo.setStyleSheet(base_style)
        combo.setContentsMargins(0, 0, 0, 0)
        # 进入编辑状态后自动打开下拉框，并安装事件过滤器增强可靠性
        combo.setFocusPolicy(Qt.StrongFocus)
        combo.installEventFilter(self)
        QTimer.singleShot(0, combo.showPopup)
        return combo

    def setEditorData(self, editor: QComboBox, index: QModelIndex) -> None:
        """将模型中的数据填充到编辑器中。

        Args:
            editor: 下拉框编辑器部件。
            index: 包含要显示数据的模型索引。
        """
        # 将下拉框选中到与当前值一致的位置；若不存在则临时加入
        value = index.data(Qt.EditRole) or index.data(Qt.DisplayRole)
        if value is None:
            value = ""
        # Select the matching option; if not present, add it temporarily.
        idx = editor.findText(str(value))
        if idx >= 0:
            editor.setCurrentIndex(idx)
        else:
            editor.addItem(str(value))
            editor.setCurrentIndex(editor.findText(str(value)))

    def setModelData(self, editor: QComboBox, model: QAbstractItemModel, index: QModelIndex) -> None:
        """将编辑器当前选择写回到模型。

        Args:
            editor: 下拉框编辑器部件。
            model: 表格的数据模型。
            index: 需要更新的模型索引。
        """
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """
        更新编辑器的位置和大小，使其与单元格矩形对齐。

        Args:
            editor: 需要定位的编辑器部件。
            option: 包含目标矩形的样式选项。
            index: 正在编辑的模型索引。
        """
        editor.setGeometry(option.rect)
        # 使编辑器高度严格等于单元格高度，并应用动态样式确保 QComboBox 不保留内部边距
        rect = option.rect
        editor.setMinimumHeight(rect.height())
        editor.setMaximumHeight(rect.height())
        editor.setGeometry(rect)
        # 修正样式表：移除 QSS 中不支持的 height 属性，规范箭头图标路径为正斜杠
        style = (
            "QComboBox { border: 0px; padding: 0px; margin: 0px; } "
            "QComboBox::drop-down { width: 20px; margin: 0px; padding: 0px; border: 0px; }"
        )
        if self.arrow_icon_path:
            qss_icon = self.arrow_icon_path.replace('\\', '/')
            style += f" QComboBox::down-arrow {{ image: url({qss_icon}); }}"
        editor.setStyleSheet(style)
        editor.updateGeometry()

    def eventFilter(self, obj: QWidget, event) -> bool:
        # 在编辑器获得焦点或显示时打开下拉框，提升弹出可靠性
        if isinstance(obj, QComboBox) and event.type() in (QEvent.FocusIn, QEvent.Show):
            QTimer.singleShot(0, obj.showPopup)
        return super().eventFilter(obj, event)

    def paint(self, painter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        # 仅在“类型”列（索引 1）右侧绘制下拉箭头/图标
        if index.column() != 1:
            return super().paint(painter, option, index)
        rect = option.rect
        arrow_w = min(24, rect.height())
        # 先绘制文本等默认内容，但缩小可用区域，避免与箭头重叠
        textOption = QStyleOptionViewItem(option)
        textOption.rect = rect.adjusted(0, 0, -arrow_w, 0)
        super().paint(painter, textOption, index)
        # 右侧区域用于绘制图标（避免使用 rect.right()+1 导致越界）
        arrowRect = QRect(rect.x() + rect.width() - arrow_w, rect.y(), arrow_w, rect.height())
        style = option.widget.style() if option.widget else QApplication.style()
        # 获取图标（优先使用自定义，其次使用标准样式图标）
        icon = None
        if self.arrow_icon and not self.arrow_icon.isNull():
            icon = self.arrow_icon
        else:
            try:
                icon = style.standardIcon(QStyle.SP_ArrowDown, QStyleOption(), option.widget)
            except Exception:
                icon = None
        painter.save()
        painter.setClipRect(arrowRect)
        if icon and not icon.isNull():
            pm = icon.pixmap(16, 16)
            label = QLabel()
            label.setAttribute(Qt.WA_TranslucentBackground, True)
            label.setStyleSheet("background: transparent; border: none;")
            label.setFixedSize(arrowRect.size())
            label.setAlignment(Qt.AlignCenter)
            label.setScaledContents(False)
            label.setPixmap(pm)
            label.ensurePolished()
            label.render(painter, QPoint(arrowRect.topLeft()))
        else:
            arrowOpt = QStyleOption()
            arrowOpt.rect = arrowRect
            arrowOpt.state = option.state
            style.drawPrimitive(QStyle.PE_IndicatorArrowDown, arrowOpt, painter, option.widget)
        painter.restore()


class MainWindow(QMainWindow):
    """包含 QTableView 的主窗口。

    设置一个包含三列的简单表格，并将组合框委托应用到第二列（“类型”）。
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TableView ComboBox 编辑器示例")
        self.resize(800, 400)

        # 视图：将 QTableView 作为中心部件
        self.view = QTableView(self)
        self.setCentralWidget(self.view)

        # 模型：使用 QStandardItemModel 并填充示例数据
        model: QStandardItemModel = QStandardItemModel(5, 3, self)
        model.setHorizontalHeaderLabels(["名称", "类型", "状态"])
        data = [
            ["条目1", "Option A", "启用"],
            ["条目2", "Option B", "禁用"],
            ["条目3", "Option C", "启用"],
            ["条目4", "Option A", "禁用"],
            ["条目5", "Option B", "启用"],
        ]
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                item = QStandardItem(str(val))
                item.setEditable(True)
                # 第二列（类型列）居中显示
                if c == 1:
                    item.setTextAlignment(Qt.AlignCenter)
                model.setItem(r, c, item)

        self.view.setModel(model)
        # 统一设置 cell 高度（行高），确保编辑器与单元格高度一致
        self._row_height = 32  # 你可以修改为需要的高度（像素）
        vh = self.view.verticalHeader()
        vh.setDefaultSectionSize(self._row_height)
        vh.setMinimumSectionSize(self._row_height)
        for r in range(model.rowCount()):
            self.view.setRowHeight(r, self._row_height)

        # 委托：将第二列（索引 1）使用下拉框编辑器
        base_dir = os.path.dirname(__file__)
        icon_path = os.path.abspath(os.path.join(base_dir, "..", "table_widget", "select.svg"))
        delegate = ComboBoxDelegate(items=["Option A", "Option B", "Option C"], parent=self.view, arrow_icon_path=icon_path)
        self.view.setItemDelegateForColumn(1, delegate)
        # 若要将该委托应用到所有列，请使用：self.view.setItemDelegate(delegate)

        # 交互与外观设置
        self.view.setEditTriggers(QTableView.DoubleClicked | QTableView.SelectedClicked)
        # 禁用“最后一列拉伸”，启用交互式调整，并开启水平滚动，避免右侧列被压缩至不可见
        header = self.view.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setMinimumSectionSize(80)
        # self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # self.view.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        # 为除第 1 列外的所有列设置“运行时最小宽度”并强制约束
        self._min_col_width = 120  # 你可以根据需要调整该值
        header.sectionResized.connect(self._enforce_min_width_except_first)
        # 初始化时也将现有宽度进行一次校正
        for col in range(1, self.view.model().columnCount()):
            if self.view.columnWidth(col) < self._min_col_width:
                self.view.setColumnWidth(col, self._min_col_width)
        self.view.verticalHeader().setVisible(False)
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        # 设置表格背景与网格线颜色，并优化表头边框厚度（避免与网格线叠加显得更粗）
        self.view.setStyleSheet(
            "QTableView { background-color: #f5f7fa; gridline-color: #d0d7de; } "
            "QHeaderView::section { border: none; border-right: 1px solid #d0d7de; border-bottom: none; } "
            "QTableView QTableCornerButton::section { background-color: #f5f7fa; border: none; border-right: 1px solid #d0d7de; }"
        )
        self.view.setShowGrid(True)
        
        # 首次显示后，将各列宽度计算为“刚好充满视口宽度”，并兼顾最小列宽约束
        QTimer.singleShot(0, self._fit_columns_to_viewport_initial)

    def _enforce_min_width_except_first(self, logicalIndex: int, oldSize: int, newSize: int) -> None:
        """在用户拖拽调整列宽时，强制除第 1 列外的所有列不低于设定的最小宽度。

        Args:
            logicalIndex: 被调整的列索引（从 0 开始）。
            oldSize: 调整前的宽度。
            newSize: 调整后的宽度。
        """
        # 第 1 列（索引 0）不受限制
        if logicalIndex == 0:
            return
        # 其余列若小于最小宽度，则回弹到最小宽度
        if newSize < getattr(self, "_min_col_width", 120):
            self.view.horizontalHeader().resizeSection(logicalIndex, getattr(self, "_min_col_width", 120))

    def _fit_columns_to_viewport_initial(self) -> None:
        """在窗口首次显示后，将列宽调整为：第 1 列和最后一列自适应内容，其他列均分剩余空间。

        - 第 1 列（索引 0）与最后一列（索引 column_count-1）使用内容自适应宽度；
        - 中间列均分视口的剩余空间，并遵守设置的最小列宽。
        """
        model = self.view.model()
        if model is None:
            return
        column_count = model.columnCount()
        if column_count <= 0:
            return
        viewport_width = self.view.viewport().width()
        if viewport_width <= 0:
            return

        # 先让第 1 列与最后一列自适应内容
        self.view.resizeColumnToContents(0)
        last_index = column_count - 1
        if last_index != 0:
            self.view.resizeColumnToContents(last_index)

        first_w = self.view.columnWidth(0)
        last_w = self.view.columnWidth(last_index) if last_index >= 0 else 0

        middle_count = max(0, column_count - 2)
        leftover = max(viewport_width - (first_w + last_w), 0)

        if middle_count > 0:
            base = max(1, leftover // middle_count)
            for col in range(1, last_index):
                # 均分剩余空间，并遵守最小列宽
                w = max(base, getattr(self, "_min_col_width", 120))
                self.view.setColumnWidth(col, w)

    def _install_combo_widgets(self, arrow_icon_path: Optional[str] = None) -> None:
        """在“类型”列（索引 1）的每个单元格中嵌入一个永久的 QComboBox。
        - 文本居中
        - 右侧显示下拉箭头图标（由样式表控制）
        - 选择变化时同步回写到模型
        """
        model = self.view.model()
        if not model:
            return
        for r in range(model.rowCount()):
            idx = model.index(r, 1)
            combo = QComboBox(self.view)
            combo.addItems(["Option A", "Option B", "Option C"])
            # 文本居中（包括当前项与下拉项）
            for i in range(combo.count()):
                combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
            combo.setEditable(False)
            combo.setFrame(False)
            combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            combo.setContentsMargins(0, 0, 0, 0)
            # 样式：去边距；右侧下拉按钮宽度 20；指定下拉箭头图标（16x16）
            style = (
                "QComboBox { border: 0px; padding: 0px; } "
                "QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 20px; margin: 0px; border: none; }"
            )
            if arrow_icon_path:
                style += f" QComboBox::down-arrow {{ image: url({arrow_icon_path}); width: 16px; height: 16px; }}"
            combo.setStyleSheet(style)
            # 初始化当前项为模型的显示值
            cur = model.data(idx, Qt.DisplayRole)
            if cur is not None:
                fi = combo.findText(str(cur))
                if fi >= 0:
                    combo.setCurrentIndex(fi)
                else:
                    combo.addItem(str(cur))
                    combo.setCurrentIndex(combo.findText(str(cur)))
            # 同步更改回模型
            def _on_changed(text, _index=idx):
                model.setData(_index, text, Qt.EditRole)
            combo.currentTextChanged.connect(_on_changed)
            # 将 combo 嵌入到视图
            self.view.setIndexWidget(idx, combo)


if __name__ == "__main__":
    import sys
    # 启用高 DPI 像素图，避免高分屏缩放导致的模糊
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())