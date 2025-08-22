from PyQt6.QtWidgets import QWidget, QVBoxLayout

from app.ui.views.PacketTableView import PacketTableView
from app.utilities.SettingsManager import SettingsManager


class PacketWindow(QWidget):
    def __init__(self, interface) -> None:
        super().__init__()
        self.interface = interface
        self.readSettings()
        self.initUi()

    def initUi(self) -> None:
        self.setWindowTitle("Packet")
        self.setMinimumSize(800, 300)

        layout = QVBoxLayout()

        layout.addWidget(PacketTableView(self))
        self.setLayout(layout)

    def writeSettings(self):
        SettingsManager().save_window_state("Packet", self.saveGeometry())

    def readSettings(self):
        geometry, windowState = SettingsManager().read_window_state("Packet")
        self.restoreGeometry(geometry)

    def closeEvent(self, event):
        self.writeSettings()
        super().closeEvent(event)
        event.accept()
