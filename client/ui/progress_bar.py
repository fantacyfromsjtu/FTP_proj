from PyQt5.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
    """
    文件传输进度条。
    """

    def __init__(self):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(100)

    def update_progress(self, value):
        """
        更新进度条的值。
        :param value: 当前进度（0-100）
        """
        self.setValue(value)
