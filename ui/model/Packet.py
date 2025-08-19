#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import typing
from datetime import datetime

from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex


class PacketModel(QAbstractTableModel):
    def __init__(self, items=None):
        super().__init__()
        self.headerStrings = ['Timestamp', 'From', 'To', 'Port Number', 'SNR', 'RSSI', 'Hop Limit', 'Hop Start', 'Payload']
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
        return len(self.items[0]) if self.items else len(self.headerStrings)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headerStrings[section]
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        pass
