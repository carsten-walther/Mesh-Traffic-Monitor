import typing

from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex

from app.utils.node import Node

class NodeListModel(QAbstractListModel):
    def __init__(self, *args, items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid() or index.row() >= len(self.items):
            return None

        node: Node = self.items[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return node.long_name

        elif role == Qt.ItemDataRole.UserRole:
            return node

        elif role == Qt.ItemDataRole.ToolTipRole:
            tooltip = f"ID: {node.node_id}\n"
            tooltip += f"Hardware: {node.hardware}\n"
            tooltip += f"Last seen: {node.last_seen.strftime('%Y-%m-%d %H:%M:%S')}\n"

            if node.position:
                tooltip += f"Position: {node.position[0]:.4f}, {node.position[1]:.4f}\n"
            if node.snr is not None:
                tooltip += f"SNR: {node.snr} dB\n"
            if node.rssi is not None:
                tooltip += f"RSSI: {node.rssi} dBm\n"
            if node.battery_level is not None:
                tooltip += f"Battery: {node.battery_level}%\n"

            return tooltip

        return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items)
