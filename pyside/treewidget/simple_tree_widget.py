#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的TreeWidget演示
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import QSize


class SimpleTreeWidgetDemo(QMainWindow):
    """简单的TreeWidget演示"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简单TreeWidget演示")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建TreeWidget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("项目")
        
        # 设置图标大小
        self.tree_widget.setIconSize(QSize(200, 12))
        self.tree_widget.setRootIsDecorated(False)

        
        # 设置样式，使用相对路径引用本地SVG文件
        self.tree_widget.setStyleSheet("""
        QTreeView::branch:closed:has-children {
    image: none;
}
QTreeView::branch:open:has-children {
    image: none;
}
        """)
        
        # 加根节点
        root1 = QTreeWidgetItem(self.tree_widget, ["文件夹1"])
        root1.addChild(QTreeWidgetItem(["文件1.txt"]))
        root1.addChild(QTreeWidgetItem(["文件2.txt"]))
        
        root2 = QTreeWidgetItem(self.tree_widget, ["文件夹2"])
        root2.addChild(QTreeWidgetItem(["文件3.txt"]))
        root2.addChild(QTreeWidgetItem(["文件4.txt"]))
        
        layout.addWidget(self.tree_widget)


def main():
    app = QApplication(sys.argv)
    window = SimpleTreeWidgetDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()