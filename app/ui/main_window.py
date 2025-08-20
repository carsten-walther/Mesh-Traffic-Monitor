from datetime import datetime

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTableView, QAbstractItemView, QHeaderView, QVBoxLayout, \
    QSplitter, QListWidget, QTabWidget, QLabel

from .models.log_table_model import LogTableModel
from .models.packet_table_model import PacketTableModel
from .widgets.connect_dialog import ConnectionDialog
from .widgets.menubar import MenuBar
from .widgets.toolbar import ToolBar
from .widgets.statusbar import StatusBar
from ..utils.config import AppConfig
from ..utils.interface import Interface
from ..utils.packet import Packet


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.interface = Interface()
        self.interface.packet_received.connect(self.on_packet_received)
        self.interface.log_message.connect(self.on_log_message)

        self.packet_table_model = PacketTableModel()
        self.packet_table_model_proxy = QSortFilterProxyModel()

        self.log_table_model = LogTableModel()
        self.log_table_model_proxy = QSortFilterProxyModel()

        self.topbar = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(AppConfig().load()['app']['name'])
        self.resize(int(AppConfig().load()['window']['width']), int(AppConfig().load()['window']['height']))
        self.center()

        self.create_toolbars()
        self.setMenuBar(MenuBar(self))
        self.setStatusBar(StatusBar(self))

        # Zentrales Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Hauptlayout (horizontal)
        main_layout = QHBoxLayout(central_widget)

        # Splitter für die Hauptaufteilung
        splitter = QSplitter(Qt.Orientation.Horizontal)
        #splitter.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(splitter)

        list_widget = QListWidget()
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
        tab_widget = QTabWidget()

        # Tab 1: Übersicht
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        #tab1_layout.setContentsMargins(0, 0, 0, 0)
        tab1_layout.addWidget(self.create_packet_table())
        tab_widget.addTab(tab1, "Packets")

        vertical_splitter.addWidget(tab_widget)
        vertical_splitter.addWidget(self.create_log_table())

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
        self.topbar.add_spacer()
        self.topbar.add_button("Help", "help.svg", self.help)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.topbar)

    def create_packet_table(self):
        self.packet_table_model_proxy.setSourceModel(self.packet_table_model)

        table = QTableView()
        table.setModel(self.packet_table_model_proxy)
        table.setSortingEnabled(True)
        table.setWordWrap(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = table.horizontalHeader()
        for i in range(0, header.count()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        # TableView properties
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        return table

    def create_log_table(self):
        self.log_table_model_proxy.setSourceModel(self.log_table_model)

        table = QTableView()
        table.setMinimumHeight(100)
        table.setMaximumHeight(150)
        table.setModel(self.log_table_model_proxy)
        table.setSortingEnabled(True)
        table.setWordWrap(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = table.horizontalHeader()
        for i in range(0, header.count()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        # TableView properties
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        return table

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

    def help(self, state) -> None:
        print("help", state)

    def on_packet_received(self, packet: Packet):
        self.packet_table_model.items.append((
            packet.rx_time, packet.from_node, packet.to_node, packet.port_number,
            packet.rx_snr, packet.rx_rssi, packet.hop_limit, packet.hop_start,
            packet.payload
        ))
        self.packet_table_model.layoutChanged.emit()

    def on_log_message(self, level: str, message: str):
        self.log_table_model.items.append((datetime.now(), level, message))
        self.log_table_model.layoutChanged.emit()
