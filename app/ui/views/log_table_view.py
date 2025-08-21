from datetime import datetime

from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtWidgets import QTableView, QAbstractItemView, QHeaderView

from app.ui.models.log_table_model import LogTableModel


class LogTableView(QTableView):
    def __new__(cls, parent):
        model = LogTableModel()

        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)

        def on_log_message(level: str, message: str):
            model.items.append((
                datetime.now(), level, message
            ))
            model.layoutChanged.emit()

        parent.interface.log_message.connect(on_log_message)

        table_view = QTableView()
        table_view.setModel(proxy)
        table_view.setSortingEnabled(True)
        table_view.setWordWrap(True)
        table_view.verticalHeader().setVisible(False)
        table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table_view.setAlternatingRowColors(True)
        table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        header = table_view.horizontalHeader()
        for i in range(0, header.count()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        return table_view
