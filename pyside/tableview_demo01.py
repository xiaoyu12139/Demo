#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PySide6 Gerber配置表格演示程序.

这个模块实现了一个类似于PCB设计软件中Gerber文件配置界面的表格组件。
主要用于演示如何使用PySide6创建具有复选框功能的表格视图。

主要功能:
    - 显示Gerber文件列表和配置选项
    - 支持多种输出格式的复选框选择（Layer View、Gerber、IPC2581、PDF）
    - 文件名编辑功能
    - 添加和删除文件行
    - 深色主题UI设计
    - 配置保存和取消操作

典型用法示例:
    python tableview_demo.py

Author: AI Assistant
Date: 2024
Version: 1.0
"""

import sys
from typing import List, Optional, Any, Union
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QTableView, QPushButton, QHeaderView,
    QMessageBox, QCheckBox, QStyledItemDelegate, QStyle,
    QStyleOptionViewItem, QStyleOptionButton
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QRect, QEvent
from PySide6.QtGui import QFont, QPalette, QPainter, QMouseEvent


class CheckBoxDelegate(QStyledItemDelegate):
    """自定义复选框委托，用于实现复选框的居中显示.
    
    这个委托类重写了paint方法来自定义复选框的绘制位置，
    确保复选框在单元格中居中显示。
    """
    
    def __init__(self, parent=None):
        """初始化复选框代理.
        
        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self.mouse_press_index = None  # 记录鼠标按下时的索引
    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """自定义绘制复选框.
        
        Args:
            painter: 绘制器对象
            option: 绘制选项
            index: 模型索引
        """
        # 获取复选框样式选项
        checkbox_style_option = self.parent().style().subElementRect(
            QStyle.SubElement.SE_CheckBoxIndicator, option, self.parent()
        )
        
        # 计算居中位置
        checkbox_rect = QRect(
            option.rect.x() + (option.rect.width() - checkbox_style_option.width()) // 2,
            option.rect.y() + (option.rect.height() - checkbox_style_option.height()) // 2,
            checkbox_style_option.width(),
            checkbox_style_option.height()
        )
        
        # 绘制背景
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        
        # 创建复选框样式选项
        checkbox_option = QStyleOptionButton()
        checkbox_option.rect = checkbox_rect
        checkbox_option.state = QStyle.StateFlag.State_Enabled
        
        # 根据数据设置复选框状态
        check_state = index.data(Qt.ItemDataRole.CheckStateRole)
        if check_state == Qt.CheckState.Checked:
            checkbox_option.state |= QStyle.StateFlag.State_On
        else:
            checkbox_option.state |= QStyle.StateFlag.State_Off
            
        # 绘制复选框
        self.parent().style().drawControl(
            QStyle.ControlElement.CE_CheckBox, checkbox_option, painter, self.parent()
        )
    
    def editorEvent(self, event: QEvent, model: QAbstractTableModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:
        """处理复选框的点击事件.
        
        Args:
            event: 事件对象
            model: 数据模型
            option: 绘制选项
            index: 模型索引
            
        Returns:
            事件是否被处理
        """
        # 检查是否是鼠标按下事件
        if event.type() == QEvent.Type.MouseButtonPress and isinstance(event, QMouseEvent):
            # 记录鼠标按下时的索引
            cell_rect = option.rect
            click_pos = event.position().toPoint()
            
            # 检查鼠标按下是否在单元格区域内
            if cell_rect.contains(click_pos):
                self.mouse_press_index = index
        
        # 检查是否是鼠标抬起事件
        elif event.type() == QEvent.Type.MouseButtonRelease and isinstance(event, QMouseEvent):
            # 检查鼠标抬起时的位置
            cell_rect = option.rect
            click_pos = event.position().toPoint()
            
            # 只有在同一个单元格内完成点击操作时才切换状态
            if (cell_rect.contains(click_pos) and 
                self.mouse_press_index is not None and 
                self.mouse_press_index == index):
                # 切换复选框状态（每次点击都切换，包括双击的两次）
                current_state = index.data(Qt.ItemDataRole.CheckStateRole)
                new_state = Qt.CheckState.Unchecked if current_state == Qt.CheckState.Checked else Qt.CheckState.Checked
                model.setData(index, new_state, Qt.ItemDataRole.CheckStateRole)
            
            # 清除记录的按下索引
            self.mouse_press_index = None
        
        return super().editorEvent(event, model, option, index)


class GerberTableModel(QAbstractTableModel):
    """Gerber配置表格数据模型.
    
    这个类继承自QAbstractTableModel，用于管理Gerber文件配置数据。
    支持文件名编辑和多种输出格式的复选框选择功能。
    
    Attributes:
        headers (List[str]): 表格列标题列表
        table_data (List[List[Union[str, bool]]]): 表格数据，每行包含[文件名, Layer View状态, Gerber状态, IPC2581状态, PDF状态]
    """
    
    def __init__(self, data: Optional[List[List[Union[str, bool]]]] = None) -> None:
        """初始化Gerber表格模型.
        
        Args:
            data: 初始表格数据。如果为None，将使用默认的Gerber文件数据。
                数据格式: [文件名, Layer View选中状态, Gerber选中状态, IPC2581选中状态, PDF选中状态]
        """
        super().__init__()
        self.headers: List[str] = ['Gerber Name', 'Layer View', 'Gerber', 'IPC2581', 'PDF']
        # 数据格式: [文件名, Layer View选中状态, Gerber选中状态, IPC2581选中状态, PDF选中状态]
        self.table_data: List[List[Union[str, bool]]] = data or [
            ['Top_Copper.gbr', True, True, True, True],
            ['Bottom_Copper.gbr', True, True, True, True],
            ['Top_Soldermask.gbr', True, True, True, True],
            ['Bottom_Soldermask.gbr', True, True, True, True],
            ['Top_Silkscreen.gbr', True, True, True, True],
            ['Bottom_Silkscreen.gbr', True, True, True, True],
            ['Drill_File.drl', True, True, True, True],
            ['Outline.gbr', True, True, True, True],
        ]
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """返回表格行数.
        
        Args:
            parent: 父索引，对于表格模型通常不使用
            
        Returns:
            表格数据的行数
        """
        return len(self.table_data)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """返回表格列数.
        
        Args:
            parent: 父索引，对于表格模型通常不使用
            
        Returns:
            表格列数
        """
        return len(self.headers)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        """返回指定索引和角色的数据.
        
        Args:
            index: 数据索引
            role: 数据角色，如DisplayRole、CheckStateRole等
            
        Returns:
            根据角色返回相应的数据，如果无效则返回None
        """
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        
        if role == Qt.DisplayRole:
            if col == 0:  # Gerber Name列显示文件名
                return self.table_data[row][col]
            else:  # 复选框列不显示文本
                return None
        
        if role == Qt.ItemDataRole.CheckStateRole:
            if col > 0:  # 复选框列返回选中状态
                return Qt.CheckState.Checked if self.table_data[row][col] else Qt.CheckState.Unchecked
            else:
                return None
        
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Optional[str]:
        """返回表头数据.
        
        Args:
            section: 表头节索引
            orientation: 方向（水平或垂直）
            role: 数据角色
            
        Returns:
            表头文本，如果无效则返回None
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            else:
                return str(section + 1)
        return None
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """返回指定索引的项目标志.
        
        Args:
            index: 项目索引
            
        Returns:
            项目标志的组合，定义项目的交互行为
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        
        if index.column() == 0:  # Gerber Name列可编辑
            flags |= Qt.ItemFlag.ItemIsEditable
        else:  # 复选框列可选中
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        
        return flags
    
    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        """设置指定索引的数据.
        
        Args:
            index: 数据索引
            value: 要设置的值
            role: 数据角色
            
        Returns:
            如果数据设置成功返回True，否则返回False
        """
        if not index.isValid():
            return False
        
        row = index.row()
        col = index.column()
        
        if role == Qt.EditRole and col == 0:  # 编辑文件名
            self.table_data[row][col] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True
        
        if role == Qt.ItemDataRole.CheckStateRole and col > 0:  # 复选框状态改变
            self.table_data[row][col] = value == Qt.CheckState.Checked
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.CheckStateRole])
            return True
        
        return False
    
    def insertRow(self, row: int, parent: QModelIndex = QModelIndex()) -> bool:
        """在指定位置插入新行.
        
        Args:
            row: 插入位置
            parent: 父索引
            
        Returns:
            插入成功返回True
        """
        self.beginInsertRows(parent, row, row)
        self.table_data.insert(row, ['New_File.gbr', True, True, True, True])
        self.endInsertRows()
        return True
    
    def removeRow(self, row: int, parent: QModelIndex = QModelIndex()) -> bool:
        """删除指定行.
        
        Args:
            row: 要删除的行索引
            parent: 父索引
            
        Returns:
            删除成功返回True，否则返回False
        """
        if 0 <= row < len(self.table_data):
            self.beginRemoveRows(parent, row, row)
            del self.table_data[row]
            self.endRemoveRows()
            return True
        return False


class GerberConfigDemo(QMainWindow):
    """Gerber配置主窗口类.
    
    这个类创建并管理Gerber文件配置的用户界面。
    提供文件管理、复选框配置和保存/取消操作功能。
    
    Attributes:
        table_view (QTableView): 主要的表格视图组件
        model (GerberTableModel): 表格数据模型
        add_button (QPushButton): 添加文件按钮
        delete_button (QPushButton): 删除文件按钮
        save_button (QPushButton): 保存配置按钮
        cancel_button (QPushButton): 取消配置按钮
    """
    
    def __init__(self):
        """初始化主窗口.
        
        按顺序执行UI初始化、模型设置和信号连接。
        """
        super().__init__()
        self.init_ui()
        self.setup_model()
        self.setup_connections()
    
    def init_ui(self):
        """初始化用户界面.
        
        创建并配置所有UI组件，包括窗口设置、样式表、
        表格视图和按钮布局。应用深色主题样式。
        """
        self.setWindowTitle('Gerber use Configuration')
        self.setGeometry(100, 100, 900, 500)
        
        # 设置深色主题样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTableView {
                background-color: #3c3c3c;
                alternate-background-color: #454545;
                color: #ffffff;
                gridline-color: #555555;
                selection-background-color: #0078d4;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建表格视图
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(False)  # 禁用排序
        self.table_view.setAlternatingRowColors(True)  # 交替行颜色
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)  # 选择单个单元格
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)  # 禁用多选，只允许单选
        self.table_view.verticalHeader().setVisible(False)  # 隐藏行号
        self.table_view.horizontalHeader().setSectionsClickable(False)  # 禁用表头点击选择
        
        # 设置字体
        font = QFont()
        font.setPointSize(9)
        self.table_view.setFont(font)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建按钮
        self.add_button = QPushButton('Add File')
        self.delete_button = QPushButton('Remove File')
        self.save_button = QPushButton('Save')
        self.cancel_button = QPushButton('Cancel')
        
        # 添加按钮到布局
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()  # 添加弹性空间
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        # 添加到主布局
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(button_layout)
    
    def setup_model(self):
        """设置数据模型.
        
        创建GerberTableModel实例并将其设置为表格视图的模型。
        配置列宽和表头行为。
        """
        self.model = GerberTableModel()
        self.table_view.setModel(self.model)
        
        # 设置列宽
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Gerber Name列自适应
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # Layer View列固定宽度
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # Gerber列固定宽度
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # IPC2581列固定宽度
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # PDF列固定宽度
        
        # 设置固定列宽
        self.table_view.setColumnWidth(1, 100)
        self.table_view.setColumnWidth(2, 80)
        self.table_view.setColumnWidth(3, 80)
        self.table_view.setColumnWidth(4, 80)
        
        # 为复选框列设置自定义委托以实现居中显示
        checkbox_delegate = CheckBoxDelegate(self.table_view)
        for col in range(1, 5):  # 第1-4列是复选框列
            self.table_view.setItemDelegateForColumn(col, checkbox_delegate)
    
    def setup_connections(self):
        """设置信号连接.
        
        将所有按钮的clicked信号连接到相应的槽函数。
        """
        self.add_button.clicked.connect(self.add_file)
        self.delete_button.clicked.connect(self.delete_file)
        self.save_button.clicked.connect(self.save_config)
        self.cancel_button.clicked.connect(self.cancel_config)
    
    def add_file(self):
        """添加新文件.
        
        在表格末尾插入一行新的Gerber文件数据，
        并自动选中新添加的行。
        """
        row_count = self.model.rowCount()
        self.model.insertRow(row_count)
        
        # 选中新添加的行
        new_index = self.model.index(row_count, 0)
        self.table_view.setCurrentIndex(new_index)
        self.table_view.scrollTo(new_index)
    
    def delete_file(self):
        """删除选中的文件.
        
        删除当前选中的文件行。如果没有选中任何行，
        显示提示信息。删除前会显示确认对话框。
        """
        current_index = self.table_view.currentIndex()
        if current_index.isValid():
            row = current_index.row()
            file_name = self.model.table_data[row][0]
            reply = QMessageBox.question(
                self, 'Confirm Delete', 
                f'Are you sure you want to delete "{file_name}"?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.model.removeRow(row)
        else:
            QMessageBox.information(self, 'Information', 'Please select a file to delete')
    
    def save_config(self):
        """保存配置.
        
        保存当前的Gerber文件配置。显示保存成功的消息，
        并在控制台输出当前配置信息，然后关闭窗口。
        """
        QMessageBox.information(self, 'Save Configuration', 'Configuration saved successfully!')
        print("Current configuration:")
        for i, row_data in enumerate(self.model.table_data):
            print(f"File {i+1}: {row_data}")
        self.close()
    
    def cancel_config(self):
        """取消配置.
        
        取消当前的配置更改。显示确认对话框询问用户
        是否确定要取消，如果确认则关闭窗口。
        """
        reply = QMessageBox.question(
            self, 'Cancel Configuration', 
            'Are you sure you want to cancel? All changes will be lost.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.close()


def main():
    """主函数.
    
    创建QApplication实例，设置应用程序属性，
    创建并显示主窗口，然后启动事件循环。
    
    Returns:
        int: 应用程序退出代码
    """
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName('TableView Demo')
    app.setApplicationVersion('1.0')
    
    # 创建并显示主窗口
    window = GerberConfigDemo()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == '__main__':
    main()