import json
import bcrypt
from server.config import SERVER_CONFIG


def hash_password(password):
    """
    使用 bcrypt 对密码进行哈希处理
    :param password: 明文密码
    :return: 哈希后的密码
    """
    salt = bcrypt.gensalt()  # 生成盐
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password, hashed_password):
    """
    验证输入密码是否匹配哈希值
    :param plain_password: 明文密码
    :param hashed_password: 哈希后的密码
    :return: 匹配返回 True，否则返回 False
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def load_users(file_path):
    """
    从文件加载用户数据
    :param file_path: 用户数据文件路径
    :return: 用户列表
    """
    try:
        with open(file_path, "r") as f:
            users = json.load(f)
            for user in users:
                # 检查是否有未加密的明文密码
                if not user["password"].startswith("$2b$"):
                    print(f"警告：用户 {user['username']} 的密码未加密！")
            return users
    except FileNotFoundError:
        print(f"用户文件未找到：{file_path}，请创建 users.json 文件")
        return []


def save_users(users, file_path):
    """
    保存用户数据到文件
    :param users: 用户列表
    :param file_path: 文件路径
    """
    with open(file_path, "w") as f:
        json.dump(users, f, indent=4)


def add_user(username, password, home_dir, permissions):
    """
    添加新用户
    :param username: 用户名
    :param password: 明文密码（会被加密）
    :param home_dir: 用户根目录
    :param permissions: 用户权限
    """
    users = load_users(SERVER_CONFIG["USERS_FILE"])
    hashed_password = hash_password(password)
    users.append(
        {
            "username": username,
            "password": hashed_password,
            "home_dir": home_dir,
            "permissions": permissions,
        }
    )
    save_users(users, SERVER_CONFIG["USERS_FILE"])
    print(f"用户 {username} 已添加并保存。")
