from ftplib import FTP
import os


class FTPClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ftp = None

    def connect(self):
        """
        连接到 FTP 服务器并进行身份验证。
        """
        print("尝试连接到 FTP 服务器")
        # print("username, password",self.username, self.password)
        try:
            # 连接到 FTP 服务器
            self.ftp = FTP()
            self.ftp.connect(self.host,2121)

            # 尝试登录
            self.ftp.login(self.username, self.password)
            print("登录成功")
            return True  # 登录成功
        except Exception as e:
            print(f"登录失败: {e}")
            self.ftp = None  # 连接失败，ftp 设置为 None
            return False  # 登录失败

    def quit(self):
        """
        退出 FTP 连接
        """
        if self.ftp:
            try:
                self.ftp.quit()
                print("已断开连接")
            except Exception as e:
                print(f"退出连接失败: {e}")
        else:
            print("没有活跃的 FTP 连接")

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
        try:
            # 切换到二进制模式
            self.ftp.voidcmd("TYPE I")  # 设置 FTP 传输模式为二进制

            with open(local_path, "wb") as f:
                file_size = self.ftp.size(remote_filename)

                def handle_progress(block):
                    # 写入文件块
                    f.write(block)
                    # 更新进度
                    if progress_callback:
                        progress_callback(f.tell() * 100 / file_size)

                # 传递 handle_progress 作为唯一的回调函数
                self.ftp.retrbinary(
                    f"RETR {remote_filename}", callback=handle_progress, blocksize=1024
                )

            print(f"文件 {remote_filename} 下载完成")
        except Exception as e:
            print(f"下载文件失败: {e}")
            raise

    def close(self):
        """
        关闭与 FTP 的连接。
        """
        self.ftp.quit()
