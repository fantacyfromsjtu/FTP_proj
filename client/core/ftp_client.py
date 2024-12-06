from ftplib import FTP
import os


class FTPClient:
    """
    FTP 客户端类，封装与 FTP 服务器的通信功能。
    """

    def __init__(self, host, username, password):
        """
        初始化 FTP 客户端。
        :param host: FTP 服务器地址
        :param username: 用户名
        :param password: 密码
        """
        self.ftp = FTP()
        self.host = host
        self.username = username
        self.password = password

    def connect(self):
        """
        连接到 FTP 服务器并登录。
        """
        try:
            self.ftp.connect(self.host, 21)
            self.ftp.login(self.username, self.password)
            print(f"Connected to {self.host}")
        except Exception as e:
            print(f"Connection error: {e}")

    def list_files(self):
        """
        列出当前目录的文件和文件夹。
        :return: 文件列表
        """
        try:
            return self.ftp.nlst()
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def upload_file(self, local_path, remote_filename, progress_callback=None):
        """
        上传本地文件到 FTP 服务器。
        :param local_path: 本地文件路径
        :param remote_filename: 远程文件名
        :param progress_callback: 更新进度条的回调函数
        """
        with open(local_path, "rb") as f:
            file_size = os.path.getsize(local_path)

            def handle_progress(block):
                if progress_callback:
                    progress_callback(f.tell() * 100 / file_size)

            self.ftp.storbinary(
                f"STOR {remote_filename}", f, 1024, callback=handle_progress
            )

    def download_file(self, remote_filename, local_path, progress_callback=None):
        """
        下载文件到本地。
        :param remote_filename: 远程文件名
        :param local_path: 本地文件路径
        :param progress_callback: 更新进度条的回调函数
        """
        with open(local_path, "wb") as f:
            file_size = self.ftp.size(remote_filename)

            def handle_progress(block):
                if progress_callback:
                    progress_callback(f.tell() * 100 / file_size)

            self.ftp.retrbinary(
                f"RETR {remote_filename}", f.write, 1024, callback=handle_progress
            )

    def close(self):
        """
        关闭与 FTP 的连接。
        """
        self.ftp.quit()
