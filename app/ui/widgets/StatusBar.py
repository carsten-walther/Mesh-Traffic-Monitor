from PyQt6.QtWidgets import QStatusBar

from app.utilities.AppConfig import AppConfig


class StatusBar(QStatusBar):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.showMessage(f"Version {AppConfig().load()['app']['version']}")
