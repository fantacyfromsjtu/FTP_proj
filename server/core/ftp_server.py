"""FTP服务器模块"""
# server/core/ftp_server.py

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from server.core.user_management import load_users
from server.config import SERVER_CONFIG


def start_ftp_server():
    """启动FTP服务器"""
    # 初始化用户认证
    authorizer = DummyAuthorizer()

    # 加载用户数据
    users = load_users(SERVER_CONFIG["USERS_FILE"])
    for user in users:
        # 假设这里不直接验证密码，而是配置用户权限
        authorizer.add_user(
            user["username"],
            user["password"],  # 哈希密码
            user["home_dir"],
            perm=user["permissions"],
        )

    # 设置匿名用户
    authorizer.add_anonymous("/", perm="elr")  # 仅读权限

    # 设置FTP处理器
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "欢迎访问自定义FTP服务器"  # 自定义欢迎语

    # 启动FTP服务器
    server = FTPServer((SERVER_CONFIG["HOST"], SERVER_CONFIG["PORT"]), handler)
    print(
        f"FTP服务器已启动，地址：{SERVER_CONFIG['HOST']}，端口：{SERVER_CONFIG['PORT']}"
    )
    server.serve_forever()


if __name__ == "__main__":
    start_ftp_server()
