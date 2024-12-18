"""服务器主入口"""

import sys
import os
import argparse

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # 添加项目根目录到 sys.path

from server.core.ftp_server import start_ftp_server
from server.core.logging import logger
from server.config import SERVER_CONFIG
from server.core.user_management import add_user, load_users


def configure_server(args):
    """
    根据命令行参数配置服务器。
    """
    if args.port:
        SERVER_CONFIG["PORT"] = args.port
    if args.path:
        SERVER_CONFIG["ANONYMOUS_DIR"] = args.path
    if args.allow_anonymous:
        SERVER_CONFIG["ALLOW_ANONYMOUS"] = True
    else:
        SERVER_CONFIG["ALLOW_ANONYMOUS"] = False

    logger.info(f"服务器配置：{SERVER_CONFIG}")


def manage_users(args):
    """
    根据命令行参数管理用户。
    """
    if args.add_user:
        username, password, home_dir, permissions = args.add_user
        add_user(username, password, home_dir, permissions)
        logger.info(f"用户 {username} 已添加。")
        print(f"用户 {username} 已成功添加。")
    elif args.list_users:
        users = load_users(SERVER_CONFIG["USERS_FILE"])
        print("\n当前用户列表：")
        for user in users:
            print(f"用户名: {user['username']}")
            print(f"  根目录: {user['home_dir']}")
            print(f"  权限: {user['permissions']}\n")


def parse_arguments():
    """
    定义并解析命令行参数。
    """
    parser = argparse.ArgumentParser(
        description="启动 FTP 服务器并管理配置",
        formatter_class=argparse.RawTextHelpFormatter,  # 支持多行格式化输出
    )

    # 服务器配置参数
    parser.add_argument("--port", type=int, help="设置 FTP 服务器端口（默认 2121）")
    parser.add_argument("--path", type=str, help="设置 FTP 根路径（仅匿名访问有效）")
    parser.add_argument(
        "--allow-anonymous", action="store_true", help="允许匿名访问（默认关闭）"
    )

    # 用户管理参数
    parser.add_argument(
        "--add-user",
        nargs=4,
        metavar=("USERNAME", "PASSWORD", "HOME_DIR", "PERMISSIONS"),
        help=(
            "添加用户，需提供以下参数：\n"
            "  USERNAME: 用户名\n"
            "  PASSWORD: 用户密码\n"
            "  HOME_DIR: 用户根目录\n"
            "  PERMISSIONS: 用户权限\n"
            "\n权限字符说明：\n"
            "  e - 进入子目录（Enter Directory）\n"
            "  l - 列出文件和目录（List）\n"
            "  r - 读取文件（Read）\n"
            "  a - 附加文件数据（Append Data）\n"
            "  d - 删除文件或目录（Delete）\n"
            "  f - 重命名文件或目录（Rename）\n"
            "  m - 创建子目录（Make Directory）\n"
            "  w - 写入文件（Write）\n"
            "\n示例:\n"
            "  --add-user admin admin123 /ftp/admin elradfmw"
        ),
    )
    parser.add_argument("--list-users", action="store_true", help="列出所有用户")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # 配置服务器
    configure_server(args)

    # 用户管理
    if args.add_user or args.list_users:
        manage_users(args)
    else:
        # 启动服务器
        try:
            logger.info("FTP服务器启动中...")
            print("FTP服务器,启动!")
            start_ftp_server()
        except Exception as e:
            logger.error(f"FTP服务器启动失败：{e}")
            print(f"FTP服务器启动失败：{e}")
