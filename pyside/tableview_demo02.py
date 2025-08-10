#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 TableView Demo with QFrame

这个演示程序创建了一个包含QFrame的窗口，QFrame中内嵌一个TableView，
实现了类似Gerber文件配置界面的功能，包括树形结构和复选框。

Features:
- 深色主题界面
- QFrame容器中的TableView
- 树形结构展开/折叠
- 多列复选框
- 自定义样式

Author: AI Assistant
Date: 2024
Version: 1.0
"""

import sys
import os
from typing import List, Optional, Any, Union, Dict, Set, Tuple
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QTableWidget, QTableWidgetItem, QFrame, QHeaderView,
    QStyledItemDelegate, QStyle, QStyleOptionViewItem, 
    QStyleOptionButton, QAbstractItemView, QCheckBox, QLabel,
    QLineEdit, QComboBox
)
from PySide6.QtCore import (
    Qt, QModelIndex, QRect, QEvent
)
from PySide6.QtGui import QFont, QPalette, QPainter, QMouseEvent, QIcon, QPixmap
from PySide6.QtSvg import QSvgRenderer


class ExpandableTableWidget(QTableWidget):
    """可展开的表格组件.
    
    这个类继承自QTableWidget，实现了点击父行展开/折叠子行的功能。
    支持Surface等父项的展开折叠，以及复选框功能。
    """
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化可展开表格.
        
        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self.expanded_rows: Set[str] = set()  # 记录已展开的父行名称集合
        self.setup_table()  # 设置表格基本属性
        self.setup_data()   # 设置表格数据
        self.cellClicked.connect(self.on_cell_clicked)  # 连接单元格点击信号
    
    def create_icon_label(self, svg_path: str, size: Tuple[int, int] = (16, 16)) -> QLabel:
        """创建SVG图标标签.
        
        Args:
            svg_path: SVG文件路径
            size: 图标大小
            
        Returns:
            QLabel: 包含SVG图标的标签
        """
        label = QLabel()
        if os.path.exists(svg_path):
            renderer = QSvgRenderer(svg_path)
            pixmap = QPixmap(size[0], size[1])
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # label.setStyleSheet("background: transparent; border: none;")
        return label
    
    def setup_table(self) -> None:
        """设置表格基本属性."""
        # 设置列数和表头
        self.setColumnCount(9)  # 9列：Gerber名称 + 8个配置列
        headers = [
            'Gerber',                    # 第0列：Gerber文件名称
            'Undefined\nline width',     # 第1列：未定义线宽（输入框）
            'Mirror',                    # 第2列：镜像（复选框）
            'Negative',                  # 第3列：负片（复选框）
            'Fill thermal',              # 第4列：填充热焊盘（复选框）
            'Delete unused pads',        # 第5列：删除未使用焊盘（复选框）
            'Rotate',                    # 第6列：旋转角度（下拉框）
            'Offset X',                  # 第7列：X偏移（输入框）
            'Offset Y'                   # 第8列：Y偏移（输入框）
        ]
        self.setHorizontalHeaderLabels(headers)
        
        # 设置表格属性
        self.setSortingEnabled(False)  # 禁用排序功能
        self.setAlternatingRowColors(True)  # 启用交替行颜色
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)  # 选择单个项目
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # 单选模式
        self.verticalHeader().setVisible(False)  # 隐藏行号
        self.horizontalHeader().setSectionsClickable(False)  # 禁用列头点击
        
        # 设置字体
        font = QFont()
        font.setPointSize(9)  # 设置字体大小为9pt
        self.setFont(font)
    
    def setup_data(self) -> None:
        """设置表格数据.
        
        数据结构说明：
        - name: 行的唯一标识名称
        - type: 行类型 ('parent'=父行, 'child'=子行, 'normal'=普通行)
        - parent: 子行所属的父行名称（仅child类型需要）
        - data: 9列数据 [名称, 线宽, 镜像, 负片, 填充热焊盘, 删除未使用焊盘, 旋转, X偏移, Y偏移]
        - hidden: 9列隐藏控制 [False, False, False, False, False, False, False, False, False] (True=隐藏控件)
        """
        # 定义所有数据（包含父行、子行和普通行）
        self.all_data: List[Dict[str, Any]] = [
            # Surface父行及其子行
            {'name': 'Surface', 'type': 'parent', 'data': ['Surface', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, True, True, False, False, False, False, False]},
            {'name': 'Track/Surface', 'type': 'child', 'parent': 'Surface', 'data': ['  Track/Surface', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, True, True, False, False, False, False, False]},
            {'name': 'Via/Surface', 'type': 'child', 'parent': 'Surface', 'data': ['  Via/Surface', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, True, True, False, False, False, False, False]},
            {'name': 'Pad/Surface', 'type': 'child', 'parent': 'Surface', 'data': ['  Pad/Surface', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, True, True, False, False, False, False, False]},
            {'name': 'Copper/Surface', 'type': 'child', 'parent': 'Surface', 'data': ['  Copper/Surface', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, True, True, False, False, False, False, False]},
            
            # Signal父行及其子行
            {'name': 'Signal', 'type': 'parent', 'data': ['Signal', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Signal_Layer1', 'type': 'child', 'parent': 'Signal', 'data': ['  Signal_Layer1', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Signal_Layer2', 'type': 'child', 'parent': 'Signal', 'data': ['  Signal_Layer2', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            
            # Gnd父行及其子行
            {'name': 'Gnd', 'type': 'parent', 'data': ['Gnd', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Gnd_Layer1', 'type': 'child', 'parent': 'Gnd', 'data': ['  Gnd_Layer1', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Gnd_Layer2', 'type': 'child', 'parent': 'Gnd', 'data': ['  Gnd_Layer2', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            
            # Soldermask父行及其子行
            {'name': 'Soldermask', 'type': 'parent', 'data': ['Soldermask', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Soldermask_Top', 'type': 'child', 'parent': 'Soldermask', 'data': ['  Soldermask_Top', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Soldermask_Bottom', 'type': 'child', 'parent': 'Soldermask', 'data': ['  Soldermask_Bottom', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            
            # Pastemask父行及其子行
            {'name': 'Pastemask', 'type': 'parent', 'data': ['Pastemask', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Pastemask_Top', 'type': 'child', 'parent': 'Pastemask', 'data': ['  Pastemask_Top', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Pastemask_Bottom', 'type': 'child', 'parent': 'Pastemask', 'data': ['  Pastemask_Bottom', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            
            # Silkscreen父行及其子行
            {'name': 'Silkscreen', 'type': 'parent', 'data': ['Silkscreen', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Silkscreen_Top', 'type': 'child', 'parent': 'Silkscreen', 'data': ['  Silkscreen_Top', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Silkscreen_Bottom', 'type': 'child', 'parent': 'Silkscreen', 'data': ['  Silkscreen_Bottom', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            
            # Assembly父行及其子行
            {'name': 'Assembly', 'type': 'parent', 'data': ['Assembly', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Assembly_Top', 'type': 'child', 'parent': 'Assembly', 'data': ['  Assembly_Top', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Assembly_Bottom', 'type': 'child', 'parent': 'Assembly', 'data': ['  Assembly_Bottom', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            
            # 其他独立行（无子项的普通行）
            {'name': 'Base', 'type': 'normal', 'data': ['Base', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]},
            {'name': 'Outline', 'type': 'normal', 'data': ['Outline', '1.000', False, False, False, False, '0', '0.000', '0.000'], 'hidden': [False, False, False, False, False, False, False, False, False]}
        ]
        
        # 初始化表格显示
        self.refresh_table()
    
    def refresh_table(self) -> None:
        """刷新表格显示.
        
        根据当前展开状态重新构建表格内容。
        只显示父行、普通行和已展开父行的子行。
        """
        # 清空表格内容
        self.setRowCount(0)
        
        # 筛选可见行：父行、普通行 + 已展开父行的子行
        visible_rows: List[Dict[str, Any]] = []
        for item in self.all_data:
            if item['type'] == 'parent' or item['type'] == 'normal':
                # 父行和普通行始终可见
                visible_rows.append(item)
            elif item['type'] == 'child' and item['parent'] in self.expanded_rows:
                # 子行仅在其父行展开时可见
                visible_rows.append(item)
        
        # 设置表格行数
        self.setRowCount(len(visible_rows))
        
        # 逐行填充数据
        for row, item in enumerate(visible_rows):
            data = item['data']  # 获取当前行的9列数据
            hidden = item.get('hidden', [False] * 9)  # 获取当前行的隐藏控制，默认全部显示
            
            # === 第一列：构建复合控件（展开图标 + 复选框 + 文本） ===
            # 创建主容器widget
            cell_widget = QWidget()
            cell_widget.setStyleSheet("QWidget { background: transparent; border: none; }")
            cell_layout = QVBoxLayout(cell_widget)
            cell_layout.setContentsMargins(5, 2, 5, 2)  # 设置边距
            cell_layout.setSpacing(0)
            
            # 创建水平布局容器，用于排列：展开图标 + 复选框 + 文本
            h_widget = QWidget()
            h_widget.setStyleSheet("QWidget { background: transparent; border: none; }")
            h_layout = QHBoxLayout(h_widget)
            h_layout.setContentsMargins(0, 0, 0, 0)
            h_layout.setSpacing(5)  # 控件间距5像素
            
            # 1. 添加展开图标（仅parent行显示，放在最前面）
            if item['type'] == 'parent':
                # 根据展开状态选择对应的SVG图标
                if item['name'] in self.expanded_rows:
                    icon_path = os.path.join(os.path.dirname(__file__), 'hide.svg')  # 展开状态：显示收起图标
                else:
                    icon_path = os.path.join(os.path.dirname(__file__), 'show.svg')  # 收起状态：显示展开图标
                
                icon_label = self.create_icon_label(icon_path, (12, 12))  # 创建12x12像素的图标
                h_layout.addWidget(icon_label)
            
            # 2. 添加复选框（所有行都有，位于展开图标之后）
            checkbox = QCheckBox()
            checkbox.setChecked(False)  # 默认未选中状态
            checkbox.setStyleSheet("""
                QCheckBox {
                    margin: 0px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            h_layout.addWidget(checkbox)
            
            # 3. 添加文本标签（显示Gerber文件名称）
            text_label = QLabel(data[0])  # data[0]是第一列的文本内容
            text_label.setStyleSheet("color: #ffffff; background: transparent; border: none;")
            text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            h_layout.addWidget(text_label)
            h_layout.addStretch()  # 添加弹性空间，使内容左对齐
            
            # 将水平布局添加到主布局中
            cell_layout.addWidget(h_widget)
            # 将整个复合控件设置到表格的第一列
            self.setCellWidget(row, 0, cell_widget)
            
            # === 其他列：根据列类型和隐藏控制设置不同的控件 ===
            for col in range(1, 9):
                if hidden[col]:  # 如果该列被标记为隐藏，则不创建控件
                    # 设置为空的表格项，显示原始数据
                    item_widget = QTableWidgetItem(str(data[col]))
                    self.setItem(row, col, item_widget)
                elif col == 1 or col == 7 or col == 8:  
                    # 第1列（线宽）、第7列（X偏移）、第8列（Y偏移）：使用文本输入框
                    line_edit = QLineEdit(str(data[col]))
                    # 注释的样式代码可用于自定义外观
                    # line_edit.setStyleSheet("""
                    #     QLineEdit {
                    #         background-color: #2d2d2d;
                    #         border: 1px solid #555555;
                    #         border-radius: 2px;
                    #         padding: 2px;
                    #         color: #ffffff;
                    #     }
                    #     QLineEdit:focus {
                    #         border-color: #0078d4;
                    #     }
                    # """)
                    self.setCellWidget(row, col, line_edit)
                    
                elif 2 <= col <= 5:  
                    # 第2-5列（镜像、负片、填充热焊盘、删除未使用焊盘）：使用复选框
                    checkbox = QCheckBox()
                    checkbox.setChecked(data[col])  # 根据数据设置选中状态
                    # 注释的样式代码可用于自定义外观
                    # checkbox.setStyleSheet("""
                    #     QCheckBox {
                    #         margin: auto;
                    #     }
                    #     QCheckBox::indicator {
                    #         width: 16px;
                    #         height: 16px;
                    #     }
                    # """)
                    self.setCellWidget(row, col, checkbox)
                    
                elif col == 6:  
                    # 第6列（旋转角度）：使用下拉框
                    combo_box = QComboBox()
                    combo_box.addItems(['0', '90', '180', '270'])  # 添加旋转角度选项
                    combo_box.setCurrentText(str(data[col]))  # 设置当前选中值
                    # 注释的样式代码可用于自定义外观
                    # combo_box.setStyleSheet("""
                    #     QComboBox {
                    #         background-color: #2d2d2d;
                    #         border: 1px solid #555555;
                    #         border-radius: 2px;
                    #         padding: 2px;
                    #         color: #ffffff;
                    #     }
                    #     QComboBox:focus {
                    #         border-color: #0078d4;
                    #     }
                    #     QComboBox::drop-down {
                    #         border: none;
                    #     }
                    #     QComboBox QAbstractItemView {
                    #         background-color: #3c3c3c;
                    #         color: #ffffff;
                    #         selection-background-color: #0078d4;
                    #     }
                    # """)
                    self.setCellWidget(row, col, combo_box)
        
        # === 设置列宽 ===
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 第一列固定宽度
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # 第二列固定宽度
        
        # 设置各列的具体宽度（像素）
        self.setColumnWidth(0, 150)  # Gerber文件名列
        self.setColumnWidth(1, 80)   # 未定义线宽列
        self.setColumnWidth(2, 60)   # 镜像列
        self.setColumnWidth(3, 70)   # 负片列
        self.setColumnWidth(4, 80)   # 填充热焊盘列
        self.setColumnWidth(5, 120)  # 删除未使用焊盘列
        self.setColumnWidth(6, 60)   # 旋转角度列
        self.setColumnWidth(7, 70)   # X偏移列
        self.setColumnWidth(8, 70)   # Y偏移列
    
    def on_cell_clicked(self, row: int, column: int) -> None:
        """处理单元格点击事件.
        
        仅处理第一列的点击，用于展开/折叠父行。
        点击父行时切换其展开状态，点击其他行无效果。
        
        Args:
            row: 被点击的行索引
            column: 被点击的列索引
        """
        # 只处理第一列的点击事件（展开/折叠功能）
        if column == 0:
            # 重新构建当前可见行列表（与refresh_table中的逻辑一致）
            visible_rows: List[Dict[str, Any]] = []
            for item in self.all_data:
                if item['type'] == 'parent' or item['type'] == 'normal':
                    visible_rows.append(item)
                elif item['type'] == 'child' and item['parent'] in self.expanded_rows:
                    visible_rows.append(item)
            
            # 检查点击的行是否为有效的父行
            if row < len(visible_rows):
                clicked_item = visible_rows[row]
                if clicked_item['type'] == 'parent':
                    parent_name = clicked_item['name']
                    # 切换展开状态：已展开则收起，未展开则展开
                    if parent_name in self.expanded_rows:
                        self.expanded_rows.remove(parent_name)  # 收起
                    else:
                        self.expanded_rows.add(parent_name)     # 展开
                    # 刷新表格显示以反映状态变化
                    self.refresh_table()






class GerberConfigWindow(QMainWindow):
    """Gerber配置主窗口类.
    
    这个类创建并管理Gerber文件配置的用户界面。
    包含一个QFrame容器，其中内嵌TableView组件。
    """
    
    def __init__(self) -> None:
        """初始化主窗口."""
        super().__init__()
        self.init_ui()
        self.setup_model()
    
    def init_ui(self) -> None:
        """初始化用户界面."""
        self.setWindowTitle('Gerber Configuration')
        self.setGeometry(100, 100, 1000, 600)
        
        # 设置深色主题样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QFrame {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QTableWidget {
                background-color: #3c3c3c;
                alternate-background-color: #454545;
                color: #ffffff;
                gridline-color: #555555;
                selection-background-color: #0078d4;
                border: none;
            }
            QTableWidget::item {
                padding: 4px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                padding: 4px;
                border: 1px solid #555555;
                font-weight: bold;
            }
            QHeaderView::section:horizontal {
                border-top: none;
            }
            QHeaderView::section:vertical {
                border-left: none;
            }
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                background-color: #2d2d2d;
                border: 1px solid #555555;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border-color: #0078d4;
            }
            QCheckBox::indicator:checked:pressed {
                background-color: #106ebe;
            }
            QScrollBar:vertical {
                background-color: #404040;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #606060;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #707070;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建QFrame容器
        self.frame = QFrame()
        # self.frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        
        # 创建QFrame内的布局
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        
        # 创建可展开表格
        self.table_widget = ExpandableTableWidget()
        
        # 将表格添加到QFrame布局中
        frame_layout.addWidget(self.table_widget)
        
        # 将QFrame添加到主布局中
        main_layout.addWidget(self.frame)
    
    def setup_model(self) -> None:
        """设置数据模型."""
        # 表格已经在init_ui中创建并设置了数据
        pass


def main() -> None:
    """主函数."""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    window = GerberConfigWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()