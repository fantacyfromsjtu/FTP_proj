"""FTP服务器模块"""

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from server.core.user_management import load_users
from server.config import SERVER_CONFIG
from server.core.logging import logger


def start_ftp_server():
    """
    启动FTP服务器
    """
    # 初始化用户认证
    authorizer = DummyAuthorizer()

    # 加载用户数据
    users = load_users(SERVER_CONFIG["USERS_FILE"])
    for user in users:
        # 添加用户
        authorizer.add_user(
            user["username"],
            user["password"],
            user["home_dir"],
            perm=user["permissions"],
        )
        logger.info(f"用户已加载: {user['username']}")

    # 设置匿名用户
    if SERVER_CONFIG.get("ALLOW_ANONYMOUS", False):
        anonymous_dir = SERVER_CONFIG.get("ANONYMOUS_DIR", "/")
        authorizer.add_anonymous(anonymous_dir, perm="elr")  # 仅允许读取

    # 配置FTP处理器
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = SERVER_CONFIG.get("BANNER", "欢迎访问自定义FTP服务器")

    # 启动FTP服务器
    server = FTPServer((SERVER_CONFIG["HOST"], SERVER_CONFIG["PORT"]), handler)
    logger.info(
        f"FTP服务器已启动，地址：{SERVER_CONFIG['HOST']}，端口：{SERVER_CONFIG['PORT']}"
    )
    server.serve_forever()
