from datetime import datetime, timezone
from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtWidgets import QListView

from app.ui.models import NodeListModel
from app.ui.views.NodeStyledItemDelegate import NodeStyledItemDelegate
from app.utilities.NodeInfo import NodeInfo


class NodeListView(QListView):
    def __new__(cls, parent):
        model = NodeListModel()

        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)

        def on_node_discovered(node: NodeInfo):
            model.items.append(node)
            model.layoutChanged.emit()

        parent.interface.node_discovered.connect(on_node_discovered)

        list_view = QListView()
        list_view.setSpacing(2)
        list_view.setModel(proxy)
        list_view.setWordWrap(True)
        list_view.setMinimumWidth(390)
        list_view.setMinimumHeight(500)
        list_view.setUniformItemSizes(True)
        list_view.setAlternatingRowColors(True)
        list_view.setItemDelegate(NodeStyledItemDelegate(list_view))

        return list_view