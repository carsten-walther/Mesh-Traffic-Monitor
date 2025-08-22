from PyQt6.QtCore import QSettings, QByteArray
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from app.ui.views import LogTableView
from app.utilities.AppConfig import AppConfig


class LogWindow(QWidget):
    def __init__(self, interface) -> None:
        super().__init__()
        self.interface = interface

        self.settings = QSettings(AppConfig().load()['app']['name'], "Log")
        self.readSettings()

        self.initUi()

    def initUi(self) -> None:
        self.setWindowTitle("Log")
        self.setMinimumSize(800, 200)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(LogTableView(self))
        self.setLayout(layout)

    def writeSettings(self):
        self.settings.setValue("geometry", self.saveGeometry())

    def readSettings(self):
        self.restoreGeometry(self.settings.value("geometry", QByteArray()))

    def closeEvent(self, event):
        self.writeSettings()
        super().closeEvent(event)
        event.accept()
