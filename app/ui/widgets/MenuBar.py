from PyQt6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        file_menu = self.addMenu("&File")
        file_menu.addAction(self.parent().toolbar.actions_call["Connect"]) # type: ignore

        edit_menu = self.addMenu("&Edit")

        view_menu = self.addMenu("&View")
        view_menu.addAction(self.parent().toolbar.actions_call["Log"]) # type: ignore
        view_menu.addAction(self.parent().toolbar.actions_call["Packets"]) # type: ignore
        view_menu.addAction(self.parent().toolbar.actions_call["Map"]) # type: ignore