from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox


class FileBrowser(QWidget):
    """
    文件浏览器组件。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.file_list = QListWidget()
        self.refresh_button = QPushButton("刷新文件列表")
        self.download_button = QPushButton("下载选中文件")
        self.upload_button = QPushButton("上传文件")

        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.upload_button)

        self.setLayout(self.layout)

    def update_file_list(self, files):
        """
        更新文件列表。
        :param files: 文件列表
        """
        self.file_list.clear()
        self.file_list.addItems(files)

    def get_selected_file(self):
        """
        获取用户选择的文件。
        :return: 文件名或 None
        """
        selected_items = self.file_list.selectedItems()
        return selected_items[0].text() if selected_items else None
