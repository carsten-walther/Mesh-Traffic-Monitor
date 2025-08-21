from PyQt6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        file_menu = self.addMenu("&File")
        edit_menu = self.addMenu("&Edit")
        view_menu = self.addMenu("&View")
        help_menu = self.addMenu("&Help")

        # help_menu.addAction(self.parent().topbar.actions_call["Help"])