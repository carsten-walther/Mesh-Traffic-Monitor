from PyQt6.QtCore import QSettings, QByteArray
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from app.ui.views.PacketTableView import PacketTableView
from app.utilities.AppConfig import AppConfig


class PacketWindow(QWidget):
    def __init__(self, interface) -> None:
        super().__init__()
        self.interface = interface

        self.settings = QSettings(AppConfig().load()['app']['name'], "Packet")
        self.readSettings()

        self.initUi()

    def initUi(self) -> None:
        self.setWindowTitle(f"{AppConfig().load()['app']['name']} - Packet")
        self.setMinimumSize(800, 600)

        layout = QHBoxLayout()
        layout.addWidget(PacketTableView(self))
        self.setLayout(layout)

    def writeSettings(self):
        self.settings.setValue("geometry", self.saveGeometry())

    def readSettings(self):
        self.restoreGeometry(self.settings.value("geometry", QByteArray()))

    def closeEvent(self, event):
        self.writeSettings()
        super().closeEvent(event)
        event.accept()
