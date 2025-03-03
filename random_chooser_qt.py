import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLabel, QPushButton,
                             QLineEdit, QListWidget, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
import random
import json
import os

class RandomChooserQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("随机选择工具")
        self.setMinimumSize(600, 700)
        self.resize(800, 800)
        
        # 设置窗口图标
        try:
            self.setWindowIcon(QIcon("icon.ico"))
        except:
            pass
        
        # 存储选项的列表
        self.options = []
        
        # 设置默认保存路径
        self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_options")
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        
        # 创建主窗口部件和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.create_widgets()
        self.setup_styles()
    
    def create_widgets(self):
        # 标题区域
        title_layout = QVBoxLayout()
        title_label = QLabel("随机选择工具", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        
        subtitle_label = QLabel("告别选择困难症", self)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Microsoft YaHei", 10))
        subtitle_label.setStyleSheet("color: #666666;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        self.main_layout.addLayout(title_layout)
        
        # 输入区域
        input_layout = QHBoxLayout()
        self.option_entry = QLineEdit(self)
        self.option_entry.setFont(QFont("Microsoft YaHei", 13))
        self.option_entry.setPlaceholderText("输入选项...")
        self.option_entry.returnPressed.connect(self.add_option)
        
        add_button = QPushButton("添加选项", self)
        add_button.setFont(QFont("Microsoft YaHei", 11))
        add_button.clicked.connect(self.add_option)
        
        input_layout.addWidget(self.option_entry)
        input_layout.addWidget(add_button)
        self.main_layout.addLayout(input_layout)
        
        # 选项列表区域
        list_label = QLabel("当前选项列表", self)
        list_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.main_layout.addWidget(list_label)
        
        self.options_list = QListWidget(self)
        self.options_list.setFont(QFont("Microsoft YaHei", 12))
        self.main_layout.addWidget(self.options_list)
        
        # 操作按钮区域
        buttons_layout = QHBoxLayout()
        
        delete_button = QPushButton("删除选项", self)
        clear_button = QPushButton("清空所有", self)
        save_button = QPushButton("保存选项", self)
        load_button = QPushButton("加载选项", self)
        
        for button in [delete_button, clear_button, save_button, load_button]:
            button.setFont(QFont("Microsoft YaHei", 10))
            buttons_layout.addWidget(button)
        
        delete_button.clicked.connect(self.delete_option)
        clear_button.clicked.connect(self.clear_options)
        save_button.clicked.connect(self.save_options)
        load_button.clicked.connect(self.load_options)
        
        self.main_layout.addLayout(buttons_layout)
        
        # 随机选择区域
        choose_button = QPushButton("随机选择", self)
        choose_button.setFont(QFont("Microsoft YaHei", 15, QFont.Bold))
        choose_button.setFixedHeight(60)
        choose_button.clicked.connect(self.choose_random)
        self.main_layout.addWidget(choose_button)
        
        # 结果显示区域
        result_label = QLabel("结果", self)
        result_label.setFont(QFont("Microsoft YaHei", 12))
        result_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(result_label)
        
        self.result_display = QLabel("等待选择...", self)
        self.result_display.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        self.result_display.setAlignment(Qt.AlignCenter)
        self.result_display.setFixedHeight(80)
        self.main_layout.addWidget(self.result_display)
        
        # 状态栏
        self.statusBar().setFont(QFont("Microsoft YaHei", 9))
        self.update_status()
    
    def setup_styles(self):
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                color: white;
                min-width: 80px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton[text="添加选项"] {
                background-color: #4CAF50;
            }
            QPushButton[text="删除选项"] {
                background-color: #f44336;
            }
            QPushButton[text="清空所有"] {
                background-color: #ff9800;
            }
            QPushButton[text="保存选项"] {
                background-color: #2196F3;
            }
            QPushButton[text="加载选项"] {
                background-color: #9c27b0;
            }
            QPushButton[text="随机选择"] {
                background-color: #3f51b5;
                font-size: 16px;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #a6d4fa;
                color: black;
            }
            QLabel[text="结果"] {
                margin-top: 10px;
            }
            #result_display {
                background-color: #e0e0e0;
                border-radius: 4px;
                padding: 10px;
            }
        """)
    
    def add_option(self):
        option = self.option_entry.text().strip()
        if option:
            self.options.append(option)
            self.options_list.addItem(option)
            self.option_entry.clear()
            self.update_status()
        else:
            QMessageBox.warning(self, "警告", "请输入有效的选项!")
    
    def delete_option(self):
        current_item = self.options_list.currentItem()
        if current_item:
            row = self.options_list.row(current_item)
            self.options_list.takeItem(row)
            self.options.pop(row)
            self.update_status()
        else:
            QMessageBox.information(self, "提示", "请先选择要删除的选项!")
    
    def clear_options(self):
        # 创建确认对话框并设置中文按钮文本
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("确认清空")
        msg_box.setText("确定要清空所有选项吗？")
        msg_box.setIcon(QMessageBox.Question)
        
        # 添加"是"和"否"按钮
        yes_button = msg_box.addButton("是", QMessageBox.YesRole)
        no_button = msg_box.addButton("否", QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        
        # 显示对话框并获取结果
        msg_box.exec_()
        reply = msg_box.clickedButton()
        if reply == yes_button:
            # 清空列表控件
            self.options_list.clear()
            # 清空选项列表
            self.options.clear()
            # 清空结果显示
            self.result_display.setText("等待选择...")
            # 更新状态栏
            self.update_status()
    
    def choose_random(self):
        if not self.options:
            QMessageBox.information(self, "提示", "请先添加一些选项!")
            return
        
        self.animation_count = 10
        self.choose_animation()
    
    def choose_animation(self):
        if self.animation_count > 0:
            random_option = random.choice(self.options)
            self.result_display.setText(random_option)
            delay = int(100 * (1 + (10-self.animation_count)/5))
            self.animation_count -= 1
            QTimer.singleShot(delay, self.choose_animation)
        else:
            final_choice = random.choice(self.options)
            self.result_display.setText(final_choice)
            self.statusBar().showMessage(f"已选择: {final_choice} | 选项数量: {len(self.options)}")
    
    def save_options(self):
        if not self.options:
            QMessageBox.warning(self, "警告", "没有选项可保存!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "保存选项列表",
            self.save_path,
            "JSON文件 (*.json)"
        )
        
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({"options": self.options}, f, ensure_ascii=False, indent=2)
            
            self.statusBar().showMessage(f"已保存 | 选项数量: {len(self.options)}")
    
    def load_options(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "加载选项列表",
            self.save_path,
            "JSON文件 (*.json)"
        )
        
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                if "options" in data and isinstance(data["options"], list):
                    self.options_list.clear()
                    self.options.clear()
                    
                    for option in data["options"]:
                        self.options.append(option)
                        self.options_list.addItem(option)
                    
                    self.update_status()
                    QMessageBox.information(self, "成功", f"已加载 {len(self.options)} 个选项")
                else:
                    QMessageBox.critical(self, "错误", "文件格式不正确!")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载文件时出错: {str(e)}")
    
    def update_status(self):
        self.statusBar().showMessage(f"就绪 | 选项数量: {len(self.options)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RandomChooserQt()
    window.show()
    sys.exit(app.exec_())