import os

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QToolBar, QWidget, QSizePolicy

from app.ui.theme_manager import ThemeManager


class ToolBar(QToolBar):
    def __init__(self, parent,
                 orientation: Qt.Orientation = Qt.Orientation.Horizontal,
                 style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
                 icon_size: tuple[int, int] = (24, 24)) -> None:
        super().__init__(parent)
        self.actions_call = {}
        self.setOrientation(orientation)
        self.setToolButtonStyle(style)
        self.setIconSize(QSize(icon_size[0], icon_size[1]))

        self.theme_manager = ThemeManager(self)
        self.theme_manager.theme_changed.connect(self.update_icons)
        self.icon_registry = {}

    def add_button(self, text: str, icon: str, trigger_action, visible: bool = True) -> None:
        action = QAction(self.get_icon(icon), text, self)
        action.triggered.connect(trigger_action)
        action.setVisible(visible)
        self.actions_call[text] = action
        self.icon_registry[text] = icon
        self.addAction(action)

    def add_separator(self) -> None:
        separator = QWidget(self)
        separator.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.addWidget(separator)

    def add_spacer(self) -> None:
        separator = QWidget(self)
        separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(separator)

    def update_icons(self) -> None:
        for text, action in self.actions_call.items():
            icon_name = self.icon_registry.get(text)
            if icon_name:
                action.setIcon(self.get_icon(icon_name))

    def get_icon(self, icon: str) -> QIcon:
        path = os.path.join("resources/assets/icons/", f"{self.theme_manager.theme}-theme", icon)
        icon = QIcon(path)
        return icon
