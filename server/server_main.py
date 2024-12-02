# server/server_main.py

from server.core.ftp_server import start_ftp_server
from server.core.logging import logger

if __name__ == "__main__":
    try:
        logger.info("FTP服务器启动中...")
        start_ftp_server()
    except Exception as e:
        logger.error(f"FTP服务器启动失败：{e}")
