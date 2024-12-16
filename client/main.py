import hashlib
import sys

import os
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PyQt5.QtWidgets import QApplication
from client.ui.main_window import MainWindow
from client.ui.login_window import LoginWindow


def hash_password(password):
    """
    使用 SHA256 对密码进行哈希处理
    :param password: 明文密码
    :return: 哈希后的密码
    
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 显示登录窗口
    login_window = LoginWindow()
    if login_window.exec_() == LoginWindow.Accepted:
        # 登录成功后启动主窗口
        server_ip = login_window.server_ip.text()
        username = login_window.username_input.text()
        password = login_window.password_input.text()

        # 对密码进行哈希处理
        hashed_password = hash_password(password)

        # 将哈希后的密码传递给 MainWindow
        main_window = MainWindow(server_ip, username, hashed_password)
        main_window.show()

    sys.exit(app.exec_())
