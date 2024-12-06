import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QMessageBox
from client.ui.file_browser import FileBrowser
from client.ui.progress_bar import ProgressBar
from client.config.settings import FTP_DEFAULT_HOST
from client.ui.login_window import LoginWindow  # 导入 LoginWindow


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

        # 弹出登录窗口
        self.show_login_window()

    def show_login_window(self):
        """
        显示登录窗口，并等待用户输入。
        """
        login_window = LoginWindow(self)  # 创建登录窗口实例

        # 如果登录成功（accept() 返回 True），则连接到服务器
        if login_window.exec_() == QDialog.Accepted:
            self.connect_to_server()
        else:
            # 如果用户关闭了窗口或者登录失败，退出应用
            QApplication.quit()

    def connect_to_server(self):
        """
        连接到 FTP 服务器。
        """
        self.ftp_client = FTPClient(FTP_DEFAULT_HOST, self.username, self.password)
        if self.ftp_client.connect():
            QMessageBox.information(self, "成功", "连接到 FTP 服务器成功！")
        else:
            QMessageBox.critical(self, "错误", "无法连接到 FTP 服务器！")
