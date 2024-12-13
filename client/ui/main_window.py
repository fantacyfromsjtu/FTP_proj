import os
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QFileDialog,
)
from client.ui.file_browser import FileBrowser
from client.ui.progress_bar import ProgressBar
from client.core.ftp_client import FTPClient


class MainWindow(QMainWindow):
    """
    主窗口类，支持浏览和操作 FTP 文件。
    """

    def __init__(self, server_ip, username, password):
        super().__init__()
        self.setWindowTitle("FTP Client")
        self.setGeometry(100, 100, 800, 600)

        self.ftp_client = FTPClient(server_ip, username, password)
        self.current_directory = "/"  # 记录当前目录
        self.progress_bar = ProgressBar()
        self.file_browser = FileBrowser()

        self.init_ui()
        self.bind_events()
        self.connect_to_server()

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


    def bind_events(self):
        """
        绑定事件和信号。
        """
        self.file_browser.refresh_button.clicked.connect(self.refresh_file_list)
        self.file_browser.download_button.clicked.connect(self.download_file)
        self.file_browser.upload_button.clicked.connect(self.upload_file)

        # 绑定导航信号
        self.file_browser.navigate_to_sub_directory.connect(self.go_to_sub_directory)
        self.file_browser.navigate_to_parent_directory.connect(self.go_to_parent_directory)

    def connect_to_server(self):
        """
        连接到 FTP 服务器。
        """
        if self.ftp_client.connect():
            QMessageBox.information(self, "成功", "连接到 FTP 服务器成功！")
            self.refresh_file_list()
        else:
            QMessageBox.critical(self, "错误", "无法连接到 FTP 服务器！")
            self.close()

    def refresh_file_list(self):
        """
        刷新文件列表。
        """
        try:
            files = self.ftp_client.list_files()
            self.file_browser.update_file_list(
                files, include_parent=self.current_directory != "/"
            )
        except Exception as e:
            QMessageBox.critical(self, "错误", f"刷新文件列表失败: {e}")

    def go_to_sub_directory(self, directory):
        """
        进入子目录。
        """
        try:
            self.ftp_client.ftp.cwd(directory)
            self.current_directory = (
                f"{self.current_directory.rstrip('/')}/{directory}".rstrip("/")
            )
            self.refresh_file_list()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法进入目录 {directory}: {e}")

    def go_to_parent_directory(self):
        """
        返回上级目录。
        """
        try:
            self.ftp_client.ftp.cwd("..")
            self.current_directory = (
                "/".join(self.current_directory.split("/")[:-1]) or "/"
            )
            self.refresh_file_list()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法返回上级目录: {e}")

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
                self.ftp_client.ftp.size(
                    selected_item
                )  # 如果能获取文件大小，说明是文件
                local_file_path = os.path.join(save_path, selected_item)
                self.ftp_client.download_file(
                    selected_item, local_file_path, self.progress_bar.update_progress
                )
                QMessageBox.information(
                    self, "成功", f"文件 {selected_item} 下载成功！"
                )
            except Exception:
                local_dir_path = os.path.join(
                    save_path, selected_item
                )  # 如果失败，说明是文件夹
                self.ftp_client.download_directory(
                    selected_item, local_dir_path, self.progress_bar.update_progress
                )
                QMessageBox.information(
                    self, "成功", f"文件夹 {selected_item} 下载成功！"
                )
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

        remote_path = f"{self.current_directory}/{os.path.basename(file_path)}"  # 基于当前目录计算路径

        try:
            if os.path.isdir(file_path):
                self.ftp_client.upload_directory(
                    file_path, remote_path, self.progress_bar.update_progress
                )
                QMessageBox.information(self, "成功", f"文件夹 {file_path} 上传成功！")
            else:
                self.ftp_client.upload_file(
                    file_path, remote_path, self.progress_bar.update_progress
                )
                QMessageBox.information(self, "成功", f"文件 {file_path} 上传成功！")
            self.refresh_file_list()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"上传失败: {e}")
