import os


def check_local_file(path):
    """
    检查文件是否存在。
    :param path: 文件路径
    :return: True 或 False
    """
    return os.path.exists(path)


def create_local_directory(path):
    """
    创建本地目录（如果不存在）。
    :param path: 目录路径
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created: {path}")
