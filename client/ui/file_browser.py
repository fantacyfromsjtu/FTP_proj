from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QMessageBox,
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QPalette


class FileBrowser(QWidget):
    """
    文件浏览器组件，支持双击进入子目录和返回上级目录。
    """

    navigate_to_sub_directory = pyqtSignal(str)  # 进入子目录信号
    navigate_to_parent_directory = pyqtSignal()  # 返回上级目录信号

    def __init__(self, parent=None):
        super().__init__(parent)

        # 主布局分为左右两部分
        self.main_layout = QHBoxLayout()

        # 左侧文件列表
        self.file_list = QListWidget()
        self.main_layout.addWidget(self.file_list, 3)

        # 右侧按钮布局
        self.button_layout = QVBoxLayout()

        self.refresh_button = QPushButton("刷新文件列表")
        self.download_button = QPushButton("下载选中文件")
        self.upload_button = QPushButton("上传文件")
        self.create_button = QPushButton("创建文件夹")
        self.delete_button = QPushButton("删除")
        self.rename_button = QPushButton("重命名")

        # 设置按钮颜色
        self.set_button_styles()

        # 按钮添加到布局
        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addWidget(self.download_button)
        self.button_layout.addWidget(self.upload_button)
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.rename_button)
        self.button_layout.addStretch()  # 添加弹性空间

        self.main_layout.addLayout(self.button_layout, 1)
        self.setLayout(self.main_layout)

        # 信号绑定
        self.file_list.itemDoubleClicked.connect(self.on_item_double_clicked)

    def set_button_styles(self):
        """设置按钮的颜色样式"""
        # 刷新按钮 - 蓝色
        self.set_button_style(self.refresh_button, "#87CEEB")

        # 下载按钮 - 绿色
        self.set_button_style(self.download_button, "#32CD32")

        # 上传按钮 - 浅紫色
        self.set_button_style(self.upload_button, "#DA70D6")

        # 创建文件夹按钮 - 黄色
        self.set_button_style(self.create_button, "#FFD700")

        # 删除按钮 - 红色
        self.set_button_style(self.delete_button, "#FF4500")

        # 重命名按钮 - 灰色
        self.set_button_style(self.rename_button, "#D3D3D3")

    def set_button_style(self, button, color):
        """为按钮设置背景颜色"""
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color};
                color: black;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #B0E0E6;  /* 提供悬停效果 */
            }}
            """
        )

    def update_file_list(self, files, include_parent=False):
        """
        更新文件列表。
        :param files: 文件列表
        :param include_parent: 是否包含返回上级目录的 ".." 选项
        """
        self.file_list.clear()
        if include_parent:
            self.file_list.addItem("..")  # 添加上级目录选项
        self.file_list.addItems(files)

    def get_selected_file(self):
        """
        获取用户选择的文件。
        :return: 文件名或 None
        """
        selected_items = self.file_list.selectedItems()
        return selected_items[0].text() if selected_items else None

    def on_item_double_clicked(self, item):
        """
        双击事件处理。
        """
        text = item.text()
        if text == "..":
            self.navigate_to_parent_directory.emit()
        else:
            self.navigate_to_sub_directory.emit(text)
