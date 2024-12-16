"""文件系统操作模块"""

import os
import shutil


def create_directory(path):
    """
    创建目录
    :param path: 目录路径
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"目录已创建: {path}")


def delete_file(path):
    """
    删除文件
    :param path: 文件路径
    """
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        print(f"文件已删除: {path}")


def delete_directory(path):
    """
    删除目录
    :param path: 目录路径
    """
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)  # 递归删除目录及其内容
        print(f"目录已删除: {path}")
