'''文件系统操作模块'''
# server/core/file_system.py

import os


def create_directory(path):
    """
    创建目录
    :param path: 目录路径
    """
    if not os.path.exists(path):
        os.makedirs(path)


def delete_file(path):
    """
    删除文件
    :param path: 文件路径
    """
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


def delete_directory(path):
    """
    删除目录
    :param path: 目录路径
    """
    if os.path.exists(path) and os.path.isdir(path):
        os.rmdir(path)
