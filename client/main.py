import sys

import os
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PyQt5.QtWidgets import QApplication
from client.ui.main_window import MainWindow
from client.ui.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 显示登录窗口
    login_window = LoginWindow()
    if login_window.exec_() == LoginWindow.Accepted:
        # 登录成功后启动主窗口
        server_ip = login_window.server_ip.text()
        username = login_window.username_input.text()
        password = login_window.password_input.text()

        main_window = MainWindow(server_ip, username, password)
        main_window.show()

    sys.exit(app.exec_())
