#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
材料编辑器Demo
实现类似Stack Material Editor的表格界面效果
"""

import sys
from typing import List, Dict, Any, Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QCheckBox, QLabel,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPalette, QColor


class MaterialTableWidget(QTableWidget):
    """
    材料表格组件
    实现类似Stack Material Editor的界面效果
    """
    
    # 信号定义
    material_selection_changed = Signal(int, bool)  # 材料选择状态变更信号
    material_data_changed = Signal()  # 材料数据变更信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_style()
        self._connect_signals()
        
    def _setup_ui(self):
        """初始化UI设置"""
        # 设置表格基本属性
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setGridStyle(Qt.SolidLine)
        
        # 设置表头
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        
        # 设置字体
        font = QFont()
        font.setPointSize(9)
        font.setFamily("Segoe UI")
        self.setFont(font)
        
        # 设置行高
        self.verticalHeader().setDefaultSectionSize(25)
        
    def _setup_style(self):
        """设置深色主题样式"""
        self.setStyleSheet("""
            QTableWidget {
                background-color: #3c3c3c;
                color: #ffffff;
                gridline-color: #555555;
                selection-background-color: #4a4a4a;
                alternate-background-color: #404040;
            }
            
            QTableWidget::item {
                padding: 4px;
                border: none;
            }
            
            QTableWidget::item:selected {
                background-color: #4a4a4a;
            }
            
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 6px;
                border: 1px solid #555555;
                font-weight: bold;
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
                    'value': '数值',
                    'thickness_pos': '厚度(+)Tol.',
                    'thickness_neg': '厚度(-)Tol.'
                },
                ...
            ]
            
        Returns:
            bool: 设置是否成功
        """
        try:
            if not materials:
                return False
            
            # 设置表头
            headers = ['Used', 'Name', 'Material Type', 'Value', 
                      'Thickness(um)', '(+)Tol.', '(-)Tol.']
            
            # 设置表格尺寸
            self.setRowCount(len(materials))
            self.setColumnCount(len(headers))
            self.setHorizontalHeaderLabels(headers)
            
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
                
                # Value列
                value_item = QTableWidgetItem(str(material.get('value', 'XXXX')))
                value_item.setFlags(value_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 3, value_item)
                
                # Thickness列
                thickness_item = QTableWidgetItem(str(material.get('thickness', 'XXXX')))
                thickness_item.setFlags(thickness_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 4, thickness_item)
                
                # (+)Tol.列
                pos_tol_item = QTableWidgetItem(str(material.get('thickness_pos', 'XXXX')))
                pos_tol_item.setFlags(pos_tol_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 5, pos_tol_item)
                
                # (-)Tol.列
                neg_tol_item = QTableWidgetItem(str(material.get('thickness_neg', 'XXXX')))
                neg_tol_item.setFlags(neg_tol_item.flags() | Qt.ItemIsEditable)
                self.setItem(row_idx, 6, neg_tol_item)
            
            # 调整列宽
            self.setColumnWidth(0, 60)   # Used列
            self.setColumnWidth(1, 120)  # Name列
            self.setColumnWidth(2, 120)  # Material Type列
            self.setColumnWidth(3, 80)   # Value列
            self.setColumnWidth(4, 100)  # Thickness列
            self.setColumnWidth(5, 80)   # (+)Tol.列
            self.setColumnWidth(6, 80)   # (-)Tol.列
            
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
                    'value': self.item(row, 3).text() if self.item(row, 3) else '',
                    'thickness': self.item(row, 4).text() if self.item(row, 4) else '',
                    'thickness_pos': self.item(row, 5).text() if self.item(row, 5) else '',
                    'thickness_neg': self.item(row, 6).text() if self.item(row, 6) else ''
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
                    'value': 'XXXX',
                    'thickness': 'XXXX',
                    'thickness_pos': 'XXXX',
                    'thickness_neg': 'XXXX'
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
        self.setWindowTitle("Stack Material Editor")
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
        title_label = QLabel("Stack Material Editor")
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
                'value': 'XXXX',
                'thickness': 'XXXX',
                'thickness_pos': 'XXXX',
                'thickness_neg': 'XXXX'
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