# server/config.py

# 服务器配置
SERVER_CONFIG = {
    "HOST": "0.0.0.0",  # 允许所有 IP 连接，或者可以使用本机的 IP 地址，如 "192.168.x.x"
    "PORT": 2121,  # FTP 服务端口，确保该端口未被占用，且防火墙允许
    "USERS_FILE": "./server/users.json",  # 用户数据文件路径
    "LOG_FILE": "./server/ftp_server.log",  # 日志文件路径
}
