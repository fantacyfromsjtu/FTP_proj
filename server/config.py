"""服务器配置"""

SERVER_CONFIG = {
    "HOST": "0.0.0.0",  # 允许所有 IP 连接，或者可以使用具体 IP 地址
    "PORT": 2121,  # FTP 服务端口
    "USERS_FILE": "./server/users.json",  # 用户数据文件路径
    "LOG_FILE": "./server/ftp_server.log",  # 日志文件路径
    "ALLOW_ANONYMOUS": False,  # 是否允许匿名用户
    "ANONYMOUS_DIR": "./",  # 匿名用户的根目录
    "BANNER": "欢迎使用 FTP 服务器！",  # 自定义欢迎语
}
