import sys

from PyQt6.QtWidgets import QApplication

from .ui.main_window import MainWindow
from .utils.config import AppConfig


def run() -> int:
    app: QApplication = QApplication(sys.argv)
    AppConfig()

    window: MainWindow = MainWindow()
    window.show()
    return sys.exit(app.exec())
