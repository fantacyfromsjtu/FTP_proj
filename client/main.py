import sys
import os
from PyQt5.QtWidgets import QApplication
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # 添加项目根目录到 sys.path
from client.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
