from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QGuiApplication


class ThemeManager(QObject):
    theme_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = self.detect_theme()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.on_color_scheme_changed)

    @staticmethod
    def detect_theme() -> str:
        scheme = QGuiApplication.styleHints().colorScheme()
        if scheme == Qt.ColorScheme.Dark:
            return "dark"
        return "light"

    def on_color_scheme_changed(self) -> None:
        new_theme = self.detect_theme()
        if new_theme != self.theme:
            self.theme = new_theme
            self.theme_changed.emit()
