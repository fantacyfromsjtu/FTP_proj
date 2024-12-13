from ftplib import FTP
import ftplib
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

    def upload_directory(self, local_dir, remote_dir, progress_callback=None):
        """
        递归上传本地文件夹到远程 FTP 服务器。
        :param local_dir: 本地文件夹路径
        :param remote_dir: 远程目标文件夹路径
        :param progress_callback: 更新进度条的回调函数
        """
        try:
            # 在 FTP 服务器上创建目标目录
            try:
                self.ftp.mkd(remote_dir)
                print(f"创建远程目录: {remote_dir}")
            except Exception:
                print(f"远程目录 {remote_dir} 已存在，继续上传")

            # 遍历本地文件夹内容
            for item in os.listdir(local_dir):
                local_path = os.path.join(local_dir, item)
                remote_path = f"{remote_dir}/{item}"

                if os.path.isdir(local_path):
                    # 如果是子文件夹，递归上传
                    print(f"发现文件夹: {local_path}")
                    self.upload_directory(local_path, remote_path, progress_callback)
                else:
                    # 如果是文件，直接上传
                    print(f"发现文件: {local_path}")
                    self.upload_file(local_path, remote_path, progress_callback)

            print(f"文件夹 {local_dir} 上传完成")
        except Exception as e:
            print(f"上传文件夹失败: {e}")
            raise

    def download_file(self, remote_filename, local_path, progress_callback=None):
        """
        下载文件到本地。
        :param remote_filename: 远程文件名
        :param local_path: 本地文件路径
        :param progress_callback: 更新进度条的回调函数
        """
        try:
            print(f"正在下载文件: {remote_filename}")

            # 切换到二进制模式
            self.ftp.voidcmd("TYPE I")  # 设置 FTP 传输模式为二进制

            # 确保本地路径的父目录存在
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            with open(local_path, "wb") as f:
                file_size = self.ftp.size(remote_filename)

                def handle_progress(block):
                    # 写入文件块
                    f.write(block)
                    # 更新进度
                    if progress_callback:
                        progress_callback(f.tell() * 100 / file_size)

                # 下载文件
                self.ftp.retrbinary(
                    f"RETR {remote_filename}", callback=handle_progress, blocksize=1024
                )

            print(f"文件 {remote_filename} 下载完成")
        except Exception as e:
            print(f"下载文件失败: {e}")
            raise


    def download_directory(self, remote_dir, local_dir, progress_callback=None):
        """
        递归下载远程文件夹到本地。
        :param remote_dir: 远程文件夹路径
        :param local_dir: 本地文件夹路径
        :param progress_callback: 更新进度条的回调函数
        """
        try:
            # 创建本地目录
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
                print(f"创建本地目录: {local_dir}")

            # 获取远程目录内容
            file_list = self.ftp.nlst(remote_dir)  # 列出远程目录中的所有文件和子目录
            print(f"远程目录 {remote_dir} 包含: {file_list}")

            for item in file_list:
                remote_path = (
                    f"{remote_dir}/{item}"
                    if not remote_dir.endswith("/")
                    else f"{remote_dir}{item}"
                )
                local_path = os.path.join(local_dir, os.path.basename(item))

                try:
                    # 判断是文件还是文件夹
                    self.ftp.cwd(remote_path)  # 尝试进入远程子文件夹
                    print(f"发现文件夹: {remote_path}")
                    # 如果是文件夹，递归调用
                    self.download_directory(remote_path, local_path, progress_callback)
                    self.ftp.cwd("..")  # 返回上一级目录
                except Exception:
                    # 如果不能进入，说明是文件，直接下载
                    print(f"发现文件: {remote_path}")
                    self.download_file(remote_path, local_path, progress_callback)

            print(f"文件夹 {remote_dir} 下载完成")
        except Exception as e:
            print(f"下载文件夹失败: {e}")
            raise

    def close(self):
        """
        关闭与 FTP 的连接。
        """
        self.ftp.quit()
