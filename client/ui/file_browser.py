from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget


class FileBrowser(QWidget):
    """
    文件浏览器组件。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.file_list = QListWidget()
        self.refresh_button = QPushButton("Refresh")
        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.refresh_button)
        self.setLayout(self.layout)
