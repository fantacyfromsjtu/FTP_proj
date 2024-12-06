import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication
from client.ui.file_browser import FileBrowser
from client.ui.progress_bar import ProgressBar
from client.core.ftp_client import FTPClient
from client.config.settings import (
    FTP_DEFAULT_HOST,
    FTP_DEFAULT_USERNAME,
    FTP_DEFAULT_PASSWORD,
)


class MainWindow(QMainWindow):
    """
    主窗口类，负责整体界面管理。
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FTP Client")
        self.setGeometry(100, 100, 800, 600)

        self.ftp_client = None
        self.progress_bar = ProgressBar()
        self.file_browser = FileBrowser()

        self.init_ui()

    def init_ui(self):
        """
        初始化用户界面。
        """
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.file_browser)
        layout.addWidget(self.progress_bar)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def connect_to_server(self):
        """
        连接到 FTP 服务器。
        """
        self.ftp_client = FTPClient(
            FTP_DEFAULT_HOST, FTP_DEFAULT_USERNAME, FTP_DEFAULT_PASSWORD
        )
        self.ftp_client.connect()
