import json
from server.core.user_management import hash_password


def encrypt_existing_passwords(file_path):
    """
    加密用户文件中未加密的明文密码
    :param file_path: 用户数据文件路径
    """
    try:
        with open(file_path, "r") as f:
            users = json.load(f)

        updated = False
        for user in users:
            if not user["password"].startswith("$2b$"):  # 检查是否未加密
                user["password"] = hash_password(user["password"])
                updated = True
                print(f"用户 {user['username']} 的密码已加密。")

        if updated:
            with open(file_path, "w") as f:
                json.dump(users, f, indent=4)
            print("所有密码已加密并更新到文件。")
        else:
            print("所有密码均已加密，无需更新。")
    except FileNotFoundError:
        print(f"用户文件未找到：{file_path}")


if __name__ == "__main__":
    encrypt_existing_passwords("./server/users.json")
