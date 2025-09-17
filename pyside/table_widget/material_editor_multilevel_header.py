#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
材料编辑器Demo - 多级表头版本
实现Thickness下包含Value、+Tol、-Tol三个子列的效果
"""

import sys
from typing import List, Dict, Any, Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QCheckBox, QLabel,
    QFrame, QSizePolicy, 
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPalette, QColor, QPainter, QMouseEvent



class MultiLevelHeaderView(QHeaderView):
    """
    多级表头视图
    实现Thickness下包含Value、+Tol、-Tol三个子列的效果
    """
    
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setDefaultSectionSize(80)
        # 设置表头的最小高度
        self.setMinimumHeight(80)
    
    def sizeHint(self):
        """返回表头的建议尺寸"""
        size = super().sizeHint()
        # 设置表头高度为60像素，足够显示双层表头
        size.setHeight(80)
        return size
        
    def paintSection(self, painter: QPainter, rect, logicalIndex):
        """绘制表头区域"""
        painter.save()
        
        # 设置字体和颜色
        font = QFont("Segoe UI", 9, QFont.Bold)
        painter.setFont(font)
        painter.setPen(Qt.white)
        
        # 根据列索引绘制不同的表头内容
        if logicalIndex == 0:
            # Used列 - 单级表头
            painter.fillRect(rect, QColor(45, 45, 45))
            painter.setPen(QColor(85, 85, 85))
            painter.drawRect(rect)
            painter.setPen(Qt.white)
            painter.drawText(rect, Qt.AlignCenter, "Used")
        elif logicalIndex == 1:
            # Name列 - 单级表头
            painter.fillRect(rect, QColor(45, 45, 45))
            painter.setPen(QColor(85, 85, 85))
            painter.drawRect(rect)
            painter.setPen(Qt.white)
            painter.drawText(rect, Qt.AlignCenter, "Name")
        elif logicalIndex == 2:
            # Material Type列 - 单级表头
            painter.fillRect(rect, QColor(45, 45, 45))
            painter.setPen(QColor(85, 85, 85))
            painter.drawRect(rect)
            painter.setPen(Qt.white)
            painter.drawText(rect, Qt.AlignCenter, "Material Type")
        elif logicalIndex in [3, 4, 5]:  # Thickness组合列 - 双级表头
            # 计算上下两部分的矩形区域
            main_rect = rect.adjusted(0, 0, 0, -rect.height()//2)
            sub_rect = rect.adjusted(0, rect.height()//2, 0, 0)
            
            # 绘制整个区域的背景
            painter.fillRect(rect, QColor(45, 45, 45))
            
            # 绘制边框 - 避免在主标题区域绘制左右竖线
            painter.setPen(QColor(85, 85, 85))
            
            # 绘制顶部边框线
            painter.drawLine(rect.left(), rect.top(), rect.right(), rect.top())
            # 绘制底部边框线
            painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())
            
            # 只在第一列和最后一列绘制左右边框线
            if logicalIndex == 3:  # 第一列，绘制左边框
                painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())
            elif logicalIndex == 5:  # 最后一列，绘制右边框
                painter.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())
            
            # 绘制子标题区域的左右边框（用于分隔子列）
            if logicalIndex in [4, 5]:  # 中间列和最后列绘制左边框分隔子列
                painter.drawLine(rect.left(), sub_rect.top(), rect.left(), sub_rect.bottom())
            
            # 绘制子标题文字
            painter.setPen(Qt.white)
            if logicalIndex == 3:
                painter.drawText(sub_rect, Qt.AlignCenter, "Value")
            elif logicalIndex == 4:
                painter.drawText(sub_rect, Qt.AlignCenter, "(+)Tol.")
            elif logicalIndex == 5:
                painter.drawText(sub_rect, Qt.AlignCenter, "(-)Tol.")
            
            # 绘制主标题 - 只在中间列绘制以实现居中效果
            if logicalIndex == 4:
                # 在中间列绘制主标题文字
                painter.setPen(Qt.white)
                painter.drawText(main_rect, Qt.AlignCenter, "Thickness(um)")
            
            # 绘制水平分隔线（分隔主标题和子标题）
            painter.setPen(QColor(85, 85, 85))
            painter.drawLine(rect.left(), main_rect.bottom(), rect.right(), main_rect.bottom())
        
        painter.restore()


class MaterialTableWidget(QTableWidget):
    """
    材料表格组件
    实现多级表头效果
    """
    
    # 信号定义
    material_selection_changed = Signal(int, bool)  # 材料选择状态变更信号
    material_data_changed = Signal()  # 材料数据变更信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_style()
        # self._connect_signals()
        
    def _setup_ui(self):
        """初始化UI设置"""
        # 设置表格基本属性
        # self.setAlternatingRowColors(True)
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.setGridStyle(Qt.SolidLine)
        
        # # 使用自定义多级表头
        # multi_header = MultiLevelHeaderView(Qt.Horizontal, self)
        # self.setHorizontalHeader(multi_header)
        
        # # 设置垂直表头不可见
        # self.verticalHeader().setVisible(False)
        
        # # 设置字体
        # font = QFont()
        # font.setPointSize(9)
        # font.setFamily("Segoe UI")
        # self.setFont(font)
        
        # # 设置行高
        # self.verticalHeader().setDefaultSectionSize(25)
        
        # # 设置表头高度以容纳两级标题
        # self.horizontalHeader().setFixedHeight(50)

        # 打开鼠标追踪，否则 mouseMoveEvent 只有按下时才会触发
        self.setMouseTracking(True)

        # 默认选择整行
        # self.setSelectionBehavior(QTableWidget.SelectRows)

        # 当前悬浮的行号
        self._hover_row = -1
    
    def mouseMoveEvent(self, event: QMouseEvent):
        row = self.rowAt(event.pos().y())
        if row != self._hover_row:  # 如果移动到了新行
            old_hover_row = self._hover_row
            self._hover_row = row
            # 只清除之前悬浮行的背景
            if old_hover_row >= 0:
                self._clear_row_background(old_hover_row)
            # 设置新悬浮行的背景
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
            # 处理普通item
            item = self.item(row, c)
            if item and not item.isSelected():  # 不覆盖选中状态
                item.setBackground(QColor("#505050"))  # 使用深色主题的悬浮颜色
            
            # 处理cellWidget（如复选框）
            widget = self.cellWidget(row, c)
            if widget:
                widget.setStyleSheet(f"background-color: #505050;")

    def _clear_hover_background(self):
        """清除所有行的悬浮背景（用于leaveEvent）"""
        for r in range(self.rowCount()):
            self._clear_row_background(r)
    
    def _clear_row_background(self, row: int):
        """清除指定行的背景"""
        if row < 0:
            return
        for c in range(self.columnCount()):
            # 清除普通item背景
            item = self.item(row, c)
            if item and not item.isSelected():
                item.setBackground(QColor("#3c3c3c"))  # 恢复深色主题的默认背景色
            
            # 清除cellWidget背景
            widget = self.cellWidget(row, c)
            if widget:
                widget.setStyleSheet("background-color: transparent;")
        
    def _setup_style(self):
        """设置深色主题样式"""
        self.setStyleSheet("""
            QTableWidget {
                color: #ffffff;
                gridline-color: #555555;
                selection-background-color: #4a4a4a;
                alternate-background-color: #404040;
            }
            

            
            QTableWidget::item:selected {
                background-color: #4a4a4a;
            }
            

            
            QCheckBox {
                background-color: transparent;
                color: #ffffff;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            
            QCheckBox::indicator:unchecked {
                background-color: #3c3c3c;
                border: 1px solid #666666;
            }
            
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border: 1px solid #0078d4;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEzLjUgNEw2IDExLjVMMi41IDgiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
        """)
        
    def _connect_signals(self):
        """连接信号槽"""
        self.itemChanged.connect(self._on_item_changed)
        
    def _on_item_changed(self, item: QTableWidgetItem):
        """数据项变更事件"""
        self.material_data_changed.emit()
    
    def _on_checkbox_toggled(self, row: int, checked: bool):
        """复选框状态变更事件"""
        self.material_selection_changed.emit(row, checked)
    
    def set_material_data(self, materials: List[Dict[str, Any]]) -> bool:
        """
        设置材料数据的主要接口
        
        Args:
            materials: 材料数据列表，每个字典包含材料信息
            格式: [
                {
                    'used': True/False,
                    'name': '材料名称',
                    'material_type': '材料类型',
                    'thickness_value': '厚度数值',
                    'thickness_pos_tol': '厚度(+)Tol.',
                    'thickness_neg_tol': '厚度(-)Tol.'
                },
                ...
            ]
            
        Returns:
            bool: 设置是否成功
        """
        try:
            if not materials:
                return False
            
            # 设置表格尺寸 - 6列：Used, Name, Material Type, Value, (+)Tol., (-)Tol.
            self.setRowCount(len(materials))
            self.setColumnCount(6)
            
            # 不设置水平表头标签，因为我们使用自定义绘制
            
            # 填充数据
            for row_idx, material in enumerate(materials):
                # Used列 - 复选框
                checkbox = QCheckBox()
                checkbox.setChecked(material.get('used', False))
                checkbox.toggled.connect(lambda checked, r=row_idx: self._on_checkbox_toggled(r, checked))
                
                # 创建一个居中的widget来放置复选框
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                
                self.setCellWidget(row_idx, 0, checkbox_widget)
                
                # Name列
                name_item = QTableWidgetItem(str(material.get('name', 'XXXXX')))
                name_item.setFlags(name_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 1, name_item)
                
                # Material Type列
                type_item = QTableWidgetItem(str(material.get('material_type', 'XXXX')))
                type_item.setFlags(type_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 2, type_item)
                
                # Thickness Value列
                value_item = QTableWidgetItem(str(material.get('thickness_value', 'XXXX')))
                value_item.setFlags(value_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 3, value_item)
                
                # Thickness (+)Tol.列
                pos_tol_item = QTableWidgetItem(str(material.get('thickness_pos_tol', 'XXXX')))
                pos_tol_item.setFlags(pos_tol_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 4, pos_tol_item)
                
                # Thickness (-)Tol.列
                neg_tol_item = QTableWidgetItem(str(material.get('thickness_neg_tol', 'XXXX')))
                neg_tol_item.setFlags(neg_tol_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 5, neg_tol_item)
            
            # 调整列宽
            self.setColumnWidth(0, 60)   # Used列
            self.setColumnWidth(1, 120)  # Name列
            self.setColumnWidth(2, 120)  # Material Type列
            self.setColumnWidth(3, 80)   # Thickness Value列
            self.setColumnWidth(4, 80)   # Thickness (+)Tol.列
            self.setColumnWidth(5, 80)   # Thickness (-)Tol.列
            # 设置cell背景
            for r in range(self.rowCount()):
                for c in range(self.columnCount()):
                    item = self.item(r, c)
                    if item:
                        item.setBackground(QColor("#3c3c3c"))
            
            return True
            
        except Exception as e:
            print(f"设置材料数据失败: {e}")
            return False
    
    def get_material_data(self) -> List[Dict[str, Any]]:
        """
        获取当前所有材料数据
        
        Returns:
            List[Dict]: 材料数据列表
        """
        try:
            materials = []
            
            for row in range(self.rowCount()):
                # 获取复选框状态
                checkbox_widget = self.cellWidget(row, 0)
                checkbox = checkbox_widget.findChild(QCheckBox)
                used = checkbox.isChecked() if checkbox else False
                
                # 获取其他列数据
                material = {
                    'used': used,
                    'name': self.item(row, 1).text() if self.item(row, 1) else '',
                    'material_type': self.item(row, 2).text() if self.item(row, 2) else '',
                    'thickness_value': self.item(row, 3).text() if self.item(row, 3) else '',
                    'thickness_pos_tol': self.item(row, 4).text() if self.item(row, 4) else '',
                    'thickness_neg_tol': self.item(row, 5).text() if self.item(row, 5) else ''
                }
                
                materials.append(material)
            
            return materials
            
        except Exception as e:
            print(f"获取材料数据失败: {e}")
            return []
    
    def add_material(self, material: Dict[str, Any] = None) -> bool:
        """
        添加新材料行
        
        Args:
            material: 材料数据字典，如果为None则添加默认数据
            
        Returns:
            bool: 添加是否成功
        """
        try:
            if material is None:
                material = {
                    'used': False,
                    'name': 'XXXXX',
                    'material_type': 'XXXX',
                    'thickness_value': 'XXXX',
                    'thickness_pos_tol': 'XXXX',
                    'thickness_neg_tol': 'XXXX'
                }
            
            # 获取当前材料数据
            current_materials = self.get_material_data()
            current_materials.append(material)
            
            # 重新设置数据
            return self.set_material_data(current_materials)
            
        except Exception as e:
            print(f"添加材料失败: {e}")
            return False
    
    def remove_selected_materials(self) -> bool:
        """
        删除选中的材料行
        
        Returns:
            bool: 删除是否成功
        """
        try:
            # 获取当前材料数据
            materials = self.get_material_data()
            
            # 过滤掉选中的材料
            filtered_materials = [m for m in materials if not m['used']]
            
            # 重新设置数据
            return self.set_material_data(filtered_materials)
            
        except Exception as e:
            print(f"删除材料失败: {e}")
            return False


class MaterialEditorWindow(QMainWindow):
    """
    材料编辑器主窗口
    """
    
    def __init__(self):
        super().__init__()
        self.material_table = None
        self._setup_ui()
        self._setup_demo_data()
        
    def _setup_ui(self):
        """初始化UI"""
        self.setWindowTitle("Stack Material Editor - Multi-Level Header")
        self.setGeometry(100, 100, 900, 700)
        
        # 设置深色主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #666666;
                padding: 6px 12px;
                border-radius: 3px;
                font-size: 9pt;
            }
            
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            
            QPushButton:pressed {
                background-color: #363636;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 9pt;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建标题
        title_label = QLabel("Stack Material Editor - Multi-Level Header")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建按钮
        self.btn_refresh = QPushButton("Refresh")
        self.btn_add = QPushButton("Add Material")
        self.btn_remove = QPushButton("Remove Selected")
        self.btn_clear = QPushButton("Clear All")
        
        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_remove)
        button_layout.addWidget(self.btn_clear)
        button_layout.addStretch()
        
        # 材料统计标签
        self.materials_label = QLabel("Materials: XXXX")
        button_layout.addWidget(self.materials_label)
        
        # 创建材料表格
        self.material_table = MaterialTableWidget()
        
        # 创建底部按钮
        bottom_layout = QHBoxLayout()
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancel")
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_ok)
        bottom_layout.addWidget(self.btn_cancel)
        
        # 添加到主布局
        main_layout.addWidget(title_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.material_table)
        main_layout.addLayout(bottom_layout)
        
        # 连接信号
        self._connect_signals()
    
    def _connect_signals(self):
        """连接信号槽"""
        self.btn_refresh.clicked.connect(self._refresh_materials)
        self.btn_add.clicked.connect(self._add_material)
        self.btn_remove.clicked.connect(self._remove_selected)
        self.btn_clear.clicked.connect(self._clear_all)
        self.btn_ok.clicked.connect(self._on_ok)
        self.btn_cancel.clicked.connect(self._on_cancel)
        
        # 连接表格信号
        self.material_table.material_selection_changed.connect(self._on_selection_changed)
        self.material_table.material_data_changed.connect(self._update_materials_count)
    
    def _setup_demo_data(self):
        """设置演示数据"""
        demo_materials = []
        
        # 创建20行演示数据
        for i in range(20):
            material = {
                'used': i < 6,  # 前6行选中
                'name': 'XXXXX',
                'material_type': 'XXXX',
                'thickness_value': 'XXXX',
                'thickness_pos_tol': 'XXXX',
                'thickness_neg_tol': 'XXXX'
            }
            demo_materials.append(material)
        
        self.material_table.set_material_data(demo_materials)
        self._update_materials_count()
    
    def _refresh_materials(self):
        """刷新材料列表"""
        print("刷新材料列表")
        self._update_materials_count()
    
    def _add_material(self):
        """添加新材料"""
        success = self.material_table.add_material()
        if success:
            print("添加材料成功")
            self._update_materials_count()
    
    def _remove_selected(self):
        """删除选中的材料"""
        success = self.material_table.remove_selected_materials()
        if success:
            print("删除选中材料成功")
            self._update_materials_count()
    
    def _clear_all(self):
        """清空所有材料"""
        self.material_table.set_material_data([])
        print("清空所有材料")
        self._update_materials_count()
    
    def _update_materials_count(self):
        """更新材料数量显示"""
        count = self.material_table.rowCount()
        self.materials_label.setText(f"Materials: {count:04d}")
    
    def _on_selection_changed(self, row: int, checked: bool):
        """材料选择状态变更"""
        print(f"材料 {row+1} 选择状态: {checked}")
    
    def _on_ok(self):
        """确定按钮"""
        materials = self.material_table.get_material_data()
        selected_count = sum(1 for m in materials if m['used'])
        print(f"确定 - 共 {len(materials)} 个材料，选中 {selected_count} 个")
    
    def _on_cancel(self):
        """取消按钮"""
        print("取消")
        self.close()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 创建主窗口
    window = MaterialEditorWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()