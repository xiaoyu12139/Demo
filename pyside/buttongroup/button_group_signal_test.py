import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QRadioButton, QButtonGroup, QLabel, QPushButton,
    QTextEdit, QSplitter
)
from PySide6.QtCore import Qt

class ButtonGroupSignalTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QButtonGroup 信号测试 - 禁用状态下的行为")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧控制面板
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # 添加标题
        title_label = QLabel("QButtonGroup 信号测试")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        left_layout.addWidget(title_label)
        
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
        
        # 添加单选按钮到布局
        radio_group = QWidget()
        radio_layout = QVBoxLayout(radio_group)
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        radio_layout.addWidget(self.radio4)
        
        left_layout.addWidget(radio_group)
        
        # 控制按钮
        control_layout = QVBoxLayout()
        
        # 禁用/启用按钮
        disable_btn = QPushButton("禁用选项2")
        disable_btn.clicked.connect(self.toggle_radio2)
        control_layout.addWidget(disable_btn)
        
        # 清空日志按钮
        clear_log_btn = QPushButton("清空日志")
        clear_log_btn.clicked.connect(self.clear_log)
        control_layout.addWidget(clear_log_btn)
        
        # 测试不同信号按钮
        test_signals_btn = QPushButton("切换信号类型")
        test_signals_btn.clicked.connect(self.toggle_signal_type)
        control_layout.addWidget(test_signals_btn)
        
        left_layout.addLayout(control_layout)
        
        # 当前信号类型显示
        self.signal_type_label = QLabel("当前使用信号: buttonClicked")
        self.signal_type_label.setStyleSheet("font-weight: bold; color: blue; margin: 10px;")
        left_layout.addWidget(self.signal_type_label)
        
        left_layout.addStretch()
        
        # 右侧日志面板
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        log_title = QLabel("信号触发日志:")
        log_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(log_title)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                background-color: #f8f8f8;
                border: 1px solid #ccc;
            }
        """)
        right_layout.addWidget(self.log_text)
        
        # 添加到分割器
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 500])
        
        # 信号连接状态
        self.current_signal = "buttonClicked"
        self.connect_signals()
        
        # 初始日志
        self.log("程序启动，当前使用 buttonClicked 信号")
        self.log("提示：禁用按钮后测试不同信号的行为差异")
        
    def connect_signals(self):
        """连接当前选择的信号类型"""
        # 断开所有现有连接
        try:
            self.button_group.buttonClicked.disconnect()
            self.button_group.buttonPressed.disconnect()
            self.button_group.buttonReleased.disconnect()
            self.button_group.buttonToggled.disconnect()
        except:
            pass
        
        # 根据当前信号类型连接相应的信号
        if self.current_signal == "buttonClicked":
            self.button_group.buttonClicked.connect(self.on_button_clicked)
        elif self.current_signal == "buttonPressed":
            self.button_group.buttonPressed.connect(self.on_button_pressed)
        elif self.current_signal == "buttonReleased":
            self.button_group.buttonReleased.connect(self.on_button_released)
        elif self.current_signal == "buttonToggled":
            self.button_group.buttonToggled.connect(self.on_button_toggled)
    
    def log(self, message):
        """添加日志消息"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.log_text.append(f"[{timestamp}] {message}")
        
    def on_button_clicked(self, button):
        """buttonClicked 信号处理"""
        button_id = self.button_group.id(button)
        button_text = button.text()
        enabled = button.isEnabled()
        self.log(f"🖱️ buttonClicked: ID={button_id}, 文本='{button_text}', 启用={enabled}")
        
    def on_button_pressed(self, button):
        """buttonPressed 信号处理"""
        button_id = self.button_group.id(button)
        button_text = button.text()
        enabled = button.isEnabled()
        self.log(f"⬇️ buttonPressed: ID={button_id}, 文本='{button_text}', 启用={enabled}")
        
    def on_button_released(self, button):
        """buttonReleased 信号处理"""
        button_id = self.button_group.id(button)
        button_text = button.text()
        enabled = button.isEnabled()
        self.log(f"⬆️ buttonReleased: ID={button_id}, 文本='{button_text}', 启用={enabled}")
        
    def on_button_toggled(self, button, checked):
        """buttonToggled 信号处理"""
        button_id = self.button_group.id(button)
        button_text = button.text()
        enabled = button.isEnabled()
        self.log(f"🔄 buttonToggled: ID={button_id}, 文本='{button_text}', 选中={checked}, 启用={enabled}")
        
    def toggle_radio2(self):
        """切换选项2的启用状态"""
        current_state = self.radio2.isEnabled()
        self.radio2.setEnabled(not current_state)
        
        action = "启用" if not current_state else "禁用"
        self.log(f"🔧 手动{action}了选项2")
        
        # 更新按钮文本
        sender = self.sender()
        if sender:
            sender.setText("启用选项2" if current_state else "禁用选项2")
            
        # 如果禁用的是当前选中的按钮，自动选择其他按钮
        if not self.radio2.isEnabled() and self.radio2.isChecked():
            self.radio1.setChecked(True)
            self.log("⚠️ 当前选中的按钮被禁用，自动选择选项1")
    
    def toggle_signal_type(self):
        """切换信号类型"""
        signal_types = ["buttonClicked", "buttonPressed", "buttonReleased", "buttonToggled"]
        current_index = signal_types.index(self.current_signal)
        next_index = (current_index + 1) % len(signal_types)
        self.current_signal = signal_types[next_index]
        
        self.connect_signals()
        self.signal_type_label.setText(f"当前使用信号: {self.current_signal}")
        self.log(f"🔄 切换到信号: {self.current_signal}")
        
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        self.log(f"📝 日志已清空，当前信号: {self.current_signal}")

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
            min-width: 120px;
            margin: 2px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QRadioButton {
            font-size: 14px;
            padding: 5px;
            margin: 2px;
        }
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
        }
        QRadioButton:disabled {
            color: #888888;
        }
    """)
    
    window = ButtonGroupSignalTest()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()