from PyQt6.QtCore import Qt, QSize, QSettings, QByteArray
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from app.ui.LogWindow import LogWindow
from app.ui.MapWindow import MapWindow
from app.ui.PacketWindow import PacketWindow
from app.ui.views import NodeListView
from app.ui.widgets import MenuBar, ToolBar, StatusBar, ConnectDialog
from app.utilities.AppConfig import AppConfig
from app.utilities.Interface import Interface


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.interface = Interface()

        self.packetWindow = PacketWindow(interface=self.interface)
        self.mapWindow = MapWindow(interface=self.interface)
        self.logWindow = LogWindow(interface=self.interface)

        self.settings = QSettings(AppConfig().load()['app']['name'], "Main")
        self.readSettings()

        self.toolbar = None

        self.initUi()
        self.restoreWindowStates()

    def initUi(self) -> None:
        self.setWindowTitle(f"{AppConfig().load()['app']['name']}")
        self.setMinimumSize(400, 700)

        self.createToolBar()
        self.createMenuBar()
        self.createStatusBar()

        widget = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        nodeList = NodeListView(self)
        layout.addWidget(nodeList)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def writeSettings(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        self.settings.setValue("logWindowVisible", self.logWindow.isVisible())
        self.settings.setValue("packetWindowVisible", self.packetWindow.isVisible())
        self.settings.setValue("mapWindowVisible", self.mapWindow.isVisible())

    def readSettings(self):
        self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        self.restoreState(self.settings.value("windowState", QByteArray()))

    def restoreWindowStates(self):
        if self.settings.value("logWindowVisible", False, type=bool):
            self.logWindow.show()
            self.toolbar.actions_call["Log"].setChecked(True)

        if self.settings.value("packetWindowVisible", False, type=bool):
            self.packetWindow.show()
            self.toolbar.actions_call["Packets"].setChecked(True)

        if self.settings.value("mapWindowVisible", False, type=bool):
            self.mapWindow.show()
            self.toolbar.actions_call["Map"].setChecked(True)

    def closeEvent(self, event):
        self.writeSettings()
        super().closeEvent(event)
        event.accept()

    def createMenuBar(self) -> None:
        self.setMenuBar(MenuBar(self))

    def createToolBar(self) -> None:
        self.toolbar = ToolBar(self)
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setOrientation(Qt.Orientation.Horizontal)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.toolbar.add_button("Connect", "connect.svg", self.connect)
        # self.toolbar.add_button("Disconnect", "disconnect.svg", self.disconnect)

        self.toolbar.add_separator()

        self.toolbar.add_button("Packets", "packets.svg", self.togglePacketWindow, True, True)
        self.toolbar.add_button("Map", "map.svg", self.toggleMapWindow, True, True)

        self.toolbar.add_separator()

        self.toolbar.add_button("Log", "log.svg", self.toggleLogWindow, True, True)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

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

    def toggleLogWindow(self) -> None:
        if self.logWindow.isVisible():
            self.logWindow.hide()
            self.toolbar.actions_call["Log"].setChecked(False)
        else:
            self.logWindow.show()
            self.toolbar.actions_call["Log"].setChecked(True)

    def togglePacketWindow(self) -> None:
        if self.packetWindow.isVisible():
            self.packetWindow.hide()
            self.toolbar.actions_call["Packets"].setChecked(False)
        else:
            self.packetWindow.show()
            self.toolbar.actions_call["Packets"].setChecked(True)

    def toggleMapWindow(self) -> None:
        if self.mapWindow.isVisible():
            self.mapWindow.hide()
            self.toolbar.actions_call["Map"].setChecked(False)
        else:
            self.mapWindow.show()
            self.toolbar.actions_call["Map"].setChecked(True)