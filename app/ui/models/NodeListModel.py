import typing

from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex

from app.utilities.NodeInfo import NodeInfo

class NodeListModel(QAbstractListModel):
    def __init__(self, *args, items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid() or index.row() >= len(self.items):
            return None

        node: NodeInfo = self.items[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return node.user.longName

        elif role == Qt.ItemDataRole.UserRole:
            return node

        elif role == Qt.ItemDataRole.ToolTipRole:
            tooltip = f"ID: {node.num}\n"
            tooltip += f"Hardware: {node.user.hwModel}\n"
            tooltip += f"Last seen: {node.lastHeard.strftime('%Y-%m-%d %H:%M:%S')}\n"

            if node.position.latitude and node.position.longitude and node.position.altitude:
                tooltip += f"Position: {node.position.latitude:.4f}, {node.position.longitude:.4f}, {node.position.altitude}m\n"
            if node.snr is not None:
                tooltip += f"SNR: {node.snr}dB\n"
            if node.hopsAway is not None:
                tooltip += f"Hops Away: {node.hopsAway}\n"
            if node.deviceMetrics.batteryLevel is not None:
                tooltip += f"Battery: {node.deviceMetrics.batteryLevel}%\n"

            return tooltip

        return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items)
