from datetime import datetime, timezone
from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtWidgets import QListView

from app.ui.models import NodeListModel
from app.ui.views.NodeStyledItemDelegate import NodeStyledItemDelegate
from app.utils.node import Node


class NodeListView(QListView):
    def __new__(cls, parent):
        model = NodeListModel()

        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)

        def on_node_discovered(node: Node):
            model.items.append(node)
            model.layoutChanged.emit()

        parent.interface.node_discovered.connect(on_node_discovered)

        node = Node(
            node_id="!1234567890",
            short_name="Shortname",
            long_name="Longname",
            hardware="Hardware",
            last_seen=datetime.now(timezone.utc),
            battery_level=96,
            position = (52.8405709,13.7687769, 134)
        )
        on_node_discovered(node)

        list_view = QListView()
        # list_view.setSpacing(2)
        list_view.setModel(proxy)
        # list_view.setWordWrap(True)
        # list_view.setUniformItemSizes(False)
        # list_view.setAlternatingRowColors(True)
        list_view.setItemDelegate(NodeStyledItemDelegate(list_view))

        return list_view