from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
)
from client.core.ftp_client import FTPClient  # 导入 FTPClient 类
from client.config.settings import FTP_DEFAULT_HOST


class LoginWindow(QDialog):
    """
    登录窗口类，负责输入用户名和密码。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FTP 登录")
        self.setGeometry(400, 200, 300, 200)

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # 隐藏密码输入

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
        username = self.username_input.text()
        password = self.password_input.text()

        if self.authenticate(username, password):
            self.accept()  # 登录成功，关闭登录窗口
        else:
            self.error_label.setText("用户名或密码错误！")

    def authenticate(self, username, password):
        """
        验证用户名和密码是否正确。与服务器进行交互验证。
        """
        # 创建 FTP 客户端对象，并尝试连接到服务器
        ftp_client = FTPClient(FTP_DEFAULT_HOST, username, password)

        # 尝试连接并登录服务器
        if ftp_client.connect():
            return True  # 登录成功
        else:
            return False  # 登录失败
