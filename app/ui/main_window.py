from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QTabWidget

from .views.log_table_view import LogTableView
from .views.nodes_list_view import NodesListView
from .views.packet_table_view import PacketTableView
from .widgets.connect_dialog import ConnectionDialog
from .widgets.menubar import MenuBar
from .widgets.toolbar import ToolBar
from .widgets.statusbar import StatusBar
from ..utils.config import AppConfig
from ..utils.interface import Interface


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.interface = Interface()

        self.topbar = None
        self.packet_table_view = None
        self.log_table_view = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(AppConfig().load()['app']['name'])
        self.resize(int(AppConfig().load()['window']['width']), int(AppConfig().load()['window']['height']))
        self.center()

        self.create_toolbars()
        self.setMenuBar(MenuBar(self))
        self.setStatusBar(StatusBar(self))

        self.packet_table_view = PacketTableView(self)
        self.log_table_view = LogTableView(self)

        # Zentrales Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Hauptlayout (horizontal)
        main_layout = QHBoxLayout(central_widget)

        # Splitter für die Hauptaufteilung
        splitter = QSplitter(Qt.Orientation.Horizontal)
        #splitter.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(splitter)

        list_widget = NodesListView(self)
        list_widget.setMinimumWidth(200)
        list_widget.setMaximumWidth(400)
        splitter.addWidget(list_widget)

        right_widget = QWidget()
        right_widget.setMinimumWidth(400)
        right_layout = QVBoxLayout(right_widget)

        # Splitter für vertikale Aufteilung (Tabs oben, TableView unten)
        vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        #vertical_splitter.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(vertical_splitter)

        # Tab-Widget oben
        tab_widget = QTabWidget(self)

        # Tab 1: Übersicht
        tab1 = QWidget(tab_widget)
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(self.packet_table_view)
        tab_widget.addTab(tab1, "Packets")

        vertical_splitter.addWidget(tab_widget)
        vertical_splitter.addWidget(self.log_table_view)

        splitter.addWidget(right_widget)
        splitter.adjustSize()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    def create_toolbars(self) -> None:
        self.topbar = ToolBar(self, orientation=Qt.Orientation.Vertical,
                                style=Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
                                icon_size=(16, 16))
        self.topbar.setMovable(False)

        self.topbar.add_button("Connect", "connect.svg", self.connect)
        self.topbar.add_button("Disconnect", "disconnect.svg", self.disconnect, False)
        self.topbar.add_separator()
        self.topbar.add_button("Log", "console.svg", self.toggle_log, True, True)
        self.topbar.actions_call["Log"].setChecked(True)
        self.topbar.add_spacer()
        self.topbar.add_button("Help", "help.svg", self.help)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.topbar)

    def connect(self) -> None:
        if not self.interface.running:
            dlg = ConnectionDialog(self)
            if dlg.exec():

                _type = dlg.type_combo.currentText().lower()
                _port = dlg.port_combo.currentText()
                _host = dlg.host_line.text()
                _addr = dlg.addr_combo.currentText()

                self.interface.connect(connection_type=_type, port=_port, host=_host, addr=_addr)
                self.topbar.actions_call["Connect"].setVisible(False)
                self.topbar.actions_call["Disconnect"].setVisible(True)

    def disconnect(self) -> None:
        if self.interface.running:
            self.interface.disconnect()
            self.topbar.actions_call["Disconnect"].setVisible(False)
            self.topbar.actions_call["Connect"].setVisible(True)

    def toggle_log(self):
        if self.log_table_view.isHidden():
            self.log_table_view.show()
            self.topbar.actions_call["Log"].setChecked(True)
        else:
            self.log_table_view.hide()
            self.topbar.actions_call["Log"].setChecked(False)

    def help(self, state) -> None:
        print("help", state)
