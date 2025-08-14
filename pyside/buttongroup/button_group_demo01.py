import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QRadioButton, QButtonGroup, QLabel, QPushButton
)
from PySide6.QtCore import Qt

class ButtonGroupDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QButtonGroup 单选按钮演示")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 添加标题标签
        title_label = QLabel("请选择一个选项：")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # 创建按钮组
        self.button_group = QButtonGroup()
        
        # 创建四个单选按钮
        self.radio1 = QRadioButton("选项 1 - 红色")
        self.radio2 = QRadioButton("选项 2 - 绿色")
        self.radio3 = QRadioButton("选项 3 - 蓝色")
        self.radio4 = QRadioButton("选项 4 - 黄色")
        
        # 将单选按钮添加到按钮组
        self.button_group.addButton(self.radio1, 1)
        self.button_group.addButton(self.radio2, 2)
        self.button_group.addButton(self.radio3, 3)
        self.button_group.addButton(self.radio4, 4)
        
        # 设置默认选中第一个
        self.radio1.setChecked(True)
        
        # 创建单选按钮布局
        radio_layout = QVBoxLayout()
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        radio_layout.addWidget(self.radio4)
        
        # 添加一些样式
        for radio in [self.radio1, self.radio2, self.radio3, self.radio4]:
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 14px;
                    padding: 5px;
                    margin: 2px;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)
        
        main_layout.addLayout(radio_layout)
        
        # 添加分隔线
        main_layout.addSpacing(20)
        
        # 创建状态显示标签
        self.status_label = QLabel("当前选中：选项 1 - 红色")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2E86AB;
                background-color: #F5F5F5;
                padding: 10px;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.status_label)
        
        # 添加按钮来获取选中状态
        button_layout = QHBoxLayout()
        
        get_selection_btn = QPushButton("获取选中项")
        get_selection_btn.clicked.connect(self.get_selection)
        
        clear_selection_btn = QPushButton("清除选择")
        clear_selection_btn.clicked.connect(self.clear_selection)
        
        test_disable_btn = QPushButton("测试禁用")
        test_disable_btn.clicked.connect(self.test_disable_radio)
        
        button_layout.addWidget(get_selection_btn)
        button_layout.addWidget(clear_selection_btn)
        button_layout.addWidget(test_disable_btn)
        
        main_layout.addLayout(button_layout)
        
        # 连接信号
        self.button_group.buttonClicked.connect(self.on_button_clicked)
        
        # 添加弹性空间
        main_layout.addStretch()
        
    def on_button_clicked(self, button):
        """当按钮被点击时的回调函数"""
        button_id = self.button_group.id(button)
        button_text = button.text()
        
        self.status_label.setText(f"当前选中：{button_text}")
        print(f"选中了按钮 ID: {button_id}, 文本: {button_text}")
        
    def get_selection(self):
        """获取当前选中的按钮"""
        checked_button = self.button_group.checkedButton()
        if checked_button:
            button_id = self.button_group.checkedId()
            button_text = checked_button.text()
            print(f"当前选中的按钮 ID: {button_id}, 文本: {button_text}")
            
            # 更新状态标签
            self.status_label.setText(f"当前选中：{button_text}")
        else:
            print("没有选中任何按钮")
            self.status_label.setText("没有选中任何按钮")
            
    def clear_selection(self):
        """清除所有选择"""
        # 注意：QButtonGroup 默认情况下不允许取消所有选择
        # 如果需要允许无选择状态，需要设置 setExclusive(False)
        checked_button = self.button_group.checkedButton()
        if checked_button:
            # 临时设置为非互斥模式
            self.button_group.setExclusive(False)
            checked_button.setChecked(False)
            # 恢复互斥模式
            self.button_group.setExclusive(True)
            
            self.status_label.setText("没有选中任何按钮")
            print("已清除所有选择")
            
    def test_disable_radio(self):
        # """测试禁用指定的radio button"""
        self.radio1.setEnabled(False)

        # # 循环禁用/启用不同的radio button进行测试
        # radios = [self.radio1, self.radio2, self.radio3, self.radio4]
        
        # # 检查当前哪些按钮被禁用
        # disabled_radios = [radio for radio in radios if not radio.isEnabled()]
        
        # if not disabled_radios:
        #     # 如果没有禁用的按钮，禁用第二个按钮（选项2）
        #     self.radio2.setEnabled(False)
        #     self.status_label.setText("已禁用：选项 2 - 绿色")
        #     print("测试：禁用了选项 2 - 绿色")
        # elif len(disabled_radios) == 1:
        #     # 如果有一个禁用的按钮，再禁用第四个按钮
        #     self.radio4.setEnabled(False)
        #     self.status_label.setText("已禁用：选项 2 - 绿色 和 选项 4 - 黄色")
        #     print("测试：禁用了选项 2 - 绿色 和 选项 4 - 黄色")
        # else:
        #     # 如果有多个禁用的按钮，重新启用所有按钮
        #     for radio in radios:
        #         radio.setEnabled(True)
        #     self.status_label.setText("所有选项已重新启用")
        #     print("测试：重新启用了所有选项")
            
        # # 输出当前状态信息
        # enabled_count = sum(1 for radio in radios if radio.isEnabled())
        # disabled_count = len(radios) - enabled_count
        # print(f"当前状态：{enabled_count}个按钮可用，{disabled_count}个按钮被禁用")
        
        # # 检查当前选中的按钮是否被禁用
        # checked_button = self.button_group.checkedButton()
        # if checked_button and not checked_button.isEnabled():
        #     print("警告：当前选中的按钮已被禁用！")
        #     # 自动选择第一个可用的按钮
        #     for radio in radios:
        #         if radio.isEnabled():
        #             radio.setChecked(True)
        #             self.status_label.setText(f"自动选择：{radio.text()}")
        #             print(f"自动选择了第一个可用按钮：{radio.text()}")
        #             break

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #FFFFFF;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 14px;
            border-radius: 4px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
    """)
    
    window = ButtonGroupDemo()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()