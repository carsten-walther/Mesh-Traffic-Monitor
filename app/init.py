import sys

from PyQt6.QtWidgets import QApplication

from app.ui import MainWindow


def run() -> int:
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    return sys.exit(app.exec())
