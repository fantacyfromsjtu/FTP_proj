"""记录服务器运行日志和用户操作。"""

import logging
from server.config import SERVER_CONFIG


def setup_logger():
    """
    配置日志记录器
    """
    logging.basicConfig(
        filename=SERVER_CONFIG["LOG_FILE"],  # 日志文件路径
        level=logging.INFO,  # 日志级别
        format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
        encoding="utf-8",  # 设置日志文件编码为 UTF-8
    )
    return logging.getLogger("FTPServer")


logger = setup_logger()
