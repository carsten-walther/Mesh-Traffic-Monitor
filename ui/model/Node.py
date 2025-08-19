#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import typing

from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex


class NodeModel(QAbstractListModel):
    def __init__(self, *args, nodes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.nodes = nodes or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.nodes[index.row()]
        return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.nodes)
