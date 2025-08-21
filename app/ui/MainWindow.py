from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow

from app.ui.views import NodeListView
from app.ui.widgets import MenuBar, ToolBar, StatusBar, ConnectDialog
from app.utilities.AppConfig import AppConfig
from app.utilities.Interface import Interface


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.interface = Interface()
        self.initUi()

    def initUi(self) -> None:
        self.setWindowTitle(AppConfig().load()['app']['name'])
        self.resize(350, 700)

        self.createMenuBar()
        self.createToolBar()
        self.createStatusBar()
        self.setCentralWidget(NodeListView(self))

    def createMenuBar(self) -> None:
        self.setMenuBar(MenuBar(self))

    def createToolBar(self) -> None:
        toolbar = ToolBar(self)
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setOrientation(Qt.Orientation.Horizontal)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        toolbar.add_button("Connect", "connect.svg", self.connect)
        # toolbar.add_button("Disconnect", "disconnect.svg", self.disconnect)

        toolbar.add_separator()

        toolbar.add_button("Log", "console.svg", self.toggle_log_view)
        toolbar.add_button("Traffic", "list.svg", self.toggle_packet_view)

        toolbar.add_spacer()

        toolbar.add_button("Help", "help.svg", self.toggle_help_view)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def createStatusBar(self) -> None:
        self.setStatusBar(StatusBar(self))

    def connect(self) -> None:
        if not self.interface.running:
            dlg = ConnectDialog(self)
            if dlg.exec():
                _type = dlg.type_combo.currentText().lower()
                _port = dlg.port_combo.currentText()
                _host = dlg.host_line.text()
                _addr = dlg.addr_combo.currentText()

                self.interface.connect(connection_type=_type, port=_port, host=_host, addr=_addr)
                # self.topbar.actions_call["Connect"].setVisible(False)
                # self.topbar.actions_call["Disconnect"].setVisible(True)

    def disconnect(self) -> None:
        if self.interface.running:
            self.interface.disconnect()
            # self.topbar.actions_call["Disconnect"].setVisible(False)
            # self.topbar.actions_call["Connect"].setVisible(True)

    def toggle_log_view(self) -> None:
        # if self.log_table_view.isHidden():
        #     self.log_table_view.show()
        #     self.topbar.actions_call["Log"].setChecked(True)
        # else:
        #     self.log_table_view.hide()
        #     self.topbar.actions_call["Log"].setChecked(False)
        pass

    def toggle_packet_view(self) -> None:
        pass

    def toggle_help_view(self) -> None:
        print("help")
