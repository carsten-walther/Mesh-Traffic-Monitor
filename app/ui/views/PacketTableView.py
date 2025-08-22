from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtWidgets import QTableView, QAbstractItemView, QHeaderView

from app.ui.models.PacketTableModel import PacketTableModel
from app.utilities.Packet import Packet


class PacketTableView(QTableView):
    def __new__(cls, parent):
        model = PacketTableModel()

        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)

        def on_packet_received(packet: Packet):
            model.items.append(packet)
            model.layoutChanged.emit()

        parent.interface.packet_received.connect(on_packet_received)

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
        header.setStretchLastSection(True)

        for i in range(header.count() - 1):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        return table_view
