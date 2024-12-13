import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QApplication,
    QMessageBox,
    QDialog,
    QFileDialog,
)
from client.ui.file_browser import FileBrowser
from client.ui.progress_bar import ProgressBar
from client.config.settings import FTP_DEFAULT_HOST
from client.ui.login_window import LoginWindow  # 导入 LoginWindow
from client.core.ftp_client import FTPClient  # 导入 FTPClient


class MainWindow(QMainWindow):
    """
    主窗口类，负责整体界面管理。
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FTP Client")
        self.setGeometry(100, 100, 800, 600)

        self.username = None
        self.password = None
        self.ftp_client = None
        self.progress_bar = ProgressBar()
        self.file_browser = FileBrowser()

        self.init_ui()
        self.bind_events()

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

        # 如果登录成功（exec_() 返回 QDialog.Accepted），则连接到服务器
        if login_window.exec_() == QDialog.Accepted:
            print("登录成功")
            # 从登录窗口获取用户名和密码
            self.username = login_window.username_input.text()
            self.password = login_window.password_input.text()
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
            self.refresh_file_list()
        else:
            QMessageBox.critical(self, "错误", "无法连接到 FTP 服务器！")

    def bind_events(self):
        """
        绑定按钮事件。
        """
        self.file_browser.refresh_button.clicked.connect(self.refresh_file_list)
        self.file_browser.download_button.clicked.connect(self.download_file)
        self.file_browser.upload_button.clicked.connect(self.upload_file)

    def refresh_file_list(self):
        """
        刷新文件列表。
        """
        if self.ftp_client:
            try:
                files = self.ftp_client.list_files()
                self.file_browser.update_file_list(files)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"刷新文件列表失败: {e}")
        else:
            QMessageBox.warning(self, "警告", "尚未连接到 FTP 服务器！")

    def download_file(self):
        """
        下载选中的文件或文件夹。
        """
        selected_item = self.file_browser.get_selected_file()
        if not selected_item:
            QMessageBox.warning(self, "警告", "请先选择一个文件或文件夹！")
            return

        save_path = QFileDialog.getExistingDirectory(self, "选择保存文件夹")
        if not save_path:
            return  # 用户取消选择

        try:
            # 判断是文件还是文件夹
            try:
                # 如果能获取文件大小，说明是文件
                self.ftp_client.ftp.size(selected_item)
                local_file_path = os.path.join(save_path, selected_item)
                self.ftp_client.download_file(
                    selected_item, local_file_path, self.progress_bar.update_progress
                )
                QMessageBox.information(self, "成功", f"文件 {selected_item} 下载成功！")
            except Exception:
                # 如果获取文件大小失败，说明是文件夹
                local_dir_path = os.path.join(save_path, selected_item)
                self.ftp_client.download_directory(
                    selected_item, local_dir_path, self.progress_bar.update_progress
                )
                QMessageBox.information(self, "成功", f"文件夹 {selected_item} 下载成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"下载失败: {e}")


    def upload_file(self):
        """
        上传文件或文件夹到 FTP 服务器。
        """
        file_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if not file_path:
            return  # 用户未选择任何文件或文件夹

        remote_path = f"/{os.path.basename(file_path)}"  # 远程目标路径

        try:
            if os.path.isdir(file_path):
                # 如果是文件夹，调用 upload_directory 方法
                self.ftp_client.upload_directory(
                    file_path, remote_path, self.progress_bar.update_progress
                )
                QMessageBox.information(self, "成功", f"文件夹 {file_path} 上传成功！")
            else:
                # 如果是文件，调用 upload_file 方法
                self.ftp_client.upload_file(
                    file_path, remote_path, self.progress_bar.update_progress
                )
                QMessageBox.information(self, "成功", f"文件 {file_path} 上传成功！")

            self.refresh_file_list()  # 上传成功后刷新文件列表
        except Exception as e:
            QMessageBox.critical(self, "错误", f"上传失败: {e}")
