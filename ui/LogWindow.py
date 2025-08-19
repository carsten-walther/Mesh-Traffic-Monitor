#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from datetime import datetime

from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QAbstractItemView, QTableView

from ui.model.Log import LogModel


class LogWindow(QWidget):
    def __init__(self, settings, interface, parent=None):
        super().__init__(parent)

        self.settings = settings
        self.interface = interface
        self.interface.log_message.connect(self.on_log_message)

        self.model_log = LogModel()
        self.model_log_proxy = QSortFilterProxyModel()

        self.init_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        layout = QVBoxLayout()

        self.model_log_proxy.setSourceModel(self.model_log)

        table = QTableView()
        table.setModel(self.model_log_proxy)
        table.setSortingEnabled(True)
        table.setWordWrap(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = table.horizontalHeader()
        for i in range(0, header.count()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        layout.addWidget(table)

        self.setLayout(layout)
        self.setWindowTitle("Log")
        self.resize(800, 300)
        self.center()

    def on_log_message(self, level: str, message: str):
        self.model_log.items.append((datetime.now(), level, message))
        self.model_log.layoutChanged.emit()
