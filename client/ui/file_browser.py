from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal

class FileBrowser(QWidget):
    """
    文件浏览器组件，支持双击进入子目录和返回上级目录。
    """
    navigate_to_sub_directory = pyqtSignal(str)  # 进入子目录信号
    navigate_to_parent_directory = pyqtSignal()  # 返回上级目录信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.file_list = QListWidget()
        self.refresh_button = QPushButton("刷新文件列表")
        self.download_button = QPushButton("下载选中文件")
        self.upload_button = QPushButton("上传文件")
        self.create_button = QPushButton("创建文件夹")
        self.delete_button = QPushButton("删除")
        self.rename_button = QPushButton("重命名")

        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.upload_button)
        

        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.rename_button)

        self.setLayout(self.layout)

        # 信号绑定
        self.file_list.itemDoubleClicked.connect(self.on_item_double_clicked)

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
