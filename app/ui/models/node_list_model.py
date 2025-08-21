import typing

from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex


class NodeListModel(QAbstractListModel):
    def __init__(self, *args, items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.items[index.row()]
        return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items)
