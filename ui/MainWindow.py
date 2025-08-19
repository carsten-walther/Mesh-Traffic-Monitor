#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from PyQt6.QtCore import QSize, Qt, QSortFilterProxyModel
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolBar, QMessageBox, QTableView, QAbstractItemView, \
    QHeaderView

from ui.ConnectionDialog import ConnectionDialog
from ui.LogWindow import LogWindow
from ui.model.Packet import PacketModel
from src.Packet import Packet


class MainWindow(QMainWindow):
    def __init__(self, settings, interface):
        super().__init__()

        self.settings = settings
        self.interface = interface
        self.interface.packet_received.connect(self.on_packet_received)

        self.log_window = LogWindow(settings=self.settings, interface=self.interface)

        self.connect_action = None
        self.nodes_action = None
        self.log_action = None

        self.model_packet = PacketModel()
        self.model_packet_proxy = QSortFilterProxyModel()

        self.init_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.model_packet_proxy.setSourceModel(self.model_packet)

        table = QTableView()
        table.setModel(self.model_packet_proxy)
        table.setSortingEnabled(True)
        table.setWordWrap(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = table.horizontalHeader()
        for i in range(0, header.count()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        main_layout.addWidget(table)


        self.create_toolbar()
        self.create_menu()

        self.statusBar().showMessage("Ready")

        self.setWindowTitle("Mesh Traffic Monitor")
        self.resize(1280, 800)
        self.center()
        self.show()

    def create_toolbar(self):
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        self.connect_action = QAction(QIcon("assets/icon-connect.svg"), "&Connect", self)
        self.connect_action.setStatusTip("Connect node")
        self.connect_action.triggered.connect(self.on_connect_action_clicked)
        toolbar.addAction(self.connect_action)

        toolbar.addSeparator()

        self.nodes_action = QAction(QIcon("assets/icon-list.svg"), "&Nodes", self)
        self.nodes_action.setStatusTip("Open Node list")
        self.nodes_action.triggered.connect(self.on_nodes_action_clicked)
        toolbar.addAction(self.nodes_action)

        toolbar.addSeparator()

        self.log_action = QAction(QIcon("assets/icon-log.svg"), "&Log", self)
        self.log_action.setStatusTip("Open console")
        self.log_action.triggered.connect(self.on_log_action_clicked)
        toolbar.addAction(self.log_action)

        toolbar.addSeparator()

    def create_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(self.connect_action)

        view_menu = menu.addMenu("&View")
        view_menu.addAction(self.log_action)
        view_menu.addAction(self.nodes_action)

    def on_connect_action_clicked(self, s):
        if not self.interface.running:
            dlg = ConnectionDialog(self)
            if dlg.exec():

                _type = dlg.type_combo.currentText().lower()
                _port = dlg.port_combo.currentText()
                _host = dlg.host_line.text()
                _addr = dlg.addr_combo.currentText()

                self.settings.config.set('interface', 'type', _type)
                self.settings.config.set('interface', 'port', _port)
                self.settings.config.set('interface', 'host', _host)
                self.settings.config.set('interface', 'addr', _addr)
                self.settings.write()

                if not self.interface.running:
                    self.interface.connect(connection_type=_type, port=_port, host=_host, addr=_addr)
                    self.connect_action.setIcon(QIcon("assets/icon-disconnect.svg"))
                    self.connect_action.setText("&Disconnect")
                    self.connect_action.setStatusTip("Disconnect node")
        else:
            self.interface.disconnect()
            self.connect_action.setIcon(QIcon("assets/icon-connect.svg"))
            self.connect_action.setText("&Connect")
            self.connect_action.setStatusTip("Connect node")

    def on_nodes_action_clicked(self, s):
        print("click", s)

    def on_log_action_clicked(self, checked):
        if self.log_window.isVisible():
            self.log_window.hide()
        else:
            self.log_window.show()

    def on_packet_received(self, packet: Packet):
        self.model_packet.items.append((
            packet.rx_time, packet.from_node, packet.to_node, packet.port_number,
            packet.rx_snr, packet.rx_rssi, packet.hop_limit, packet.hop_start,
            packet.payload
        ))
        self.model_packet.layoutChanged.emit()

    def closeEvent(self, event):
        if self.interface.running:
            self.interface.disconnect()
        event.accept()
