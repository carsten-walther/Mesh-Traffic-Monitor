from PyQt6.QtCore import QSettings, QByteArray


class SettingsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.settings = QSettings("Meshtastic", "App")

    def save_window_state(self, window_name, geometry, state=None):
        self.settings.beginGroup(window_name)
        self.settings.setValue("geometry", geometry)
        if state:
            self.settings.setValue("state", state)
        self.settings.endGroup()

    def read_window_state(self, window_name):
        self.settings.beginGroup(window_name)
        geometry = self.settings.value("geometry", QByteArray())
        windowState = self.settings.value("windowState", QByteArray())
        self.settings.endGroup()

        return geometry, windowState