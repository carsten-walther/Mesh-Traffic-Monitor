from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtWidgets import QListView

from app.ui.models.node_list_model import NodeListModel
from app.utils.node import Node


class NodesListView(QListView):
    def __new__(cls, parent):
        model = NodeListModel()

        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)

        def on_node_discovered(node: Node):
            model.items.append((
                node.node_id
            ))
            model.layoutChanged.emit()

        parent.interface.node_discovered.connect(on_node_discovered)

        list_view = QListView()
        list_view.setModel(proxy)
        list_view.setWordWrap(True)
        list_view.setAlternatingRowColors(True)

        return list_view