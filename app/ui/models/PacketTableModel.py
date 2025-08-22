import typing
from datetime import datetime

from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex

from app.utilities.Packet import Packet


class PacketTableModel(QAbstractTableModel):
    def __init__(self, items=None):
        super().__init__()
        self.headers = ['Timestamp', 'From', 'To', 'Relay', 'Port Number', 'SNR', 'RSSI', 'Hop Limit', 'Hop Start']
        self.items = items or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid() or index.row() >= len(self.items):
            return None

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        packet: Packet = self.items[index.row()]
        column = index.column()

        # Mapping der Spalten zu den entsprechenden Packet-Attributen
        if column == 0:  # Timestamp
            return packet.rxTime.strftime("%Y-%m-%d %H:%M:%S")
        elif column == 1:  # From
            return packet.nodeFrom
        elif column == 2:  # To
            return packet.nodeTo
        elif column == 3:  # Payload (hier nehme ich relayNode wie gewünscht)
            return packet.relayNode if packet.relayNode is not None else ""
        elif column == 4:  # Port Number
            return packet.decoded.portnum
        elif column == 5:  # SNR
            return packet.rxSnr
        elif column == 6:  # RSSI
            return packet.rxRssi
        elif column == 7:  # Hop Limit
            return packet.hopLimit if packet.hopLimit is not None else ""
        elif column == 8:  # Hop Start
            return packet.hopStart if packet.hopStart is not None else ""

        return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        pass
