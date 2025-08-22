from PyQt6.QtWidgets import QWidget, QVBoxLayout

from app.ui.views import LogTableView
from app.utilities.SettingsManager import SettingsManager


class LogWindow(QWidget):
    def __init__(self, interface) -> None:
        super().__init__()
        self.interface = interface
        self.readSettings()
        self.initUi()

    def initUi(self) -> None:
        self.setWindowTitle("Log")
        self.setMinimumSize(800, 200)

        layout = QVBoxLayout()

        layout.addWidget(LogTableView(self))
        self.setLayout(layout)

    def writeSettings(self):
        SettingsManager().save_window_state("Log", self.saveGeometry())

    def readSettings(self):
        geometry, windowState = SettingsManager().read_window_state("Log")
        self.restoreGeometry(geometry)

    def closeEvent(self, event):
        self.writeSettings()
        super().closeEvent(event)
        event.accept()
