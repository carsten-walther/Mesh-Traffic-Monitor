import typing
from datetime import datetime

from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex


class LogTableModel(QAbstractTableModel):
    def __init__(self, items=None):
        super().__init__()
        self.headers = ['Timestamp', 'Level', 'Message']
        self.items = items or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            value = self.items[index.row()][index.column()]
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            return value

        return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items[0]) if self.items else len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        pass
