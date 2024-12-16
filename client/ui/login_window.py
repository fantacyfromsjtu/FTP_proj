from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
)
from client.core.ftp_client import FTPClient
import hashlib


class LoginWindow(QDialog):
    """
    登录窗口类，负责输入服务器IP、用户名和密码。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FTP 登录")
        self.setGeometry(100, 100, 300, 200)

        # 输入框和按钮
        self.server_ip = QLineEdit(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("登录", self)
        self.login_button.clicked.connect(self.on_login)

        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;")

        self.init_ui()

    def init_ui(self):
        """
        初始化登录窗口界面。
        """
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("服务器IP:", self.server_ip)
        form_layout.addRow("用户名:", self.username_input)
        form_layout.addRow("密码:", self.password_input)

        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def on_login(self):
        """
        登录按钮点击事件处理。
        """
        server_ip = self.server_ip.text()
        username = self.username_input.text()
        password = self.password_input.text()

        # 将密码进行哈希处理
        hashed_password = self.hash_password(password)

        # 尝试连接和登录
        if self.authenticate(server_ip, username, hashed_password):
            self.accept()  # 登录成功
        else:
            self.error_label.setText("用户名或密码错误！")

    def hash_password(self, password):
        """
        对密码进行哈希处理。
        """
        # 这里模拟简单哈希处理，真实系统可以使用更复杂的算法
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def authenticate(self, server_ip, username, hashed_password):
        """
        验证用户名和密码是否正确。
        """
        try:
            ftp_client = FTPClient(server_ip, username, hashed_password)
            return ftp_client.connect()  # 使用哈希密码尝试登录
        except Exception as e:
            print(f"登录失败: {e}")
            return False
