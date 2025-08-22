from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QListView, QMenu

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
        list_view.setModel(proxy)
        list_view.setWordWrap(True)
        list_view.setUniformItemSizes(True)
        list_view.setAlternatingRowColors(True)
        list_view.setItemDelegate(NodeStyledItemDelegate(list_view))

        list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        list_view.customContextMenuRequested.connect(lambda pos: show_context_menu(list_view, pos, parent))

        return list_view


def show_context_menu(list_view, position, main_window):
    """Zeigt das Kontext-Menü für einen Node an"""
    index = list_view.indexAt(position)
    if not index.isValid():
        return

    node = index.data(Qt.ItemDataRole.UserRole)
    if not node:
        return

    menu = QMenu(list_view)

    # "Show on Map" Aktion
    show_on_map_action = QAction("Show on Map", menu)
    show_on_map_action.triggered.connect(lambda: show_node_on_map(main_window, node))
    menu.addAction(show_on_map_action)

    # Weitere Aktionen können hier hinzugefügt werden
    menu.addSeparator()

    info_action = QAction("Node Information", menu)
    info_action.triggered.connect(lambda: show_node_info(node))
    menu.addAction(info_action)

    # Menü an der Cursor-Position anzeigen
    global_pos = list_view.mapToGlobal(position)
    menu.exec(global_pos)


def show_node_on_map(main_window, node: NodeInfo):
    """Zeigt den Node auf der Karte hervorgehoben an"""
    # MapWindow öffnen falls nicht sichtbar
    if not main_window.mapWindow.isVisible():
        main_window.mapWindow.show()
        main_window.toolbar.actions_call["Map"].setChecked(True)

    # Node auf der Karte hervorheben
    main_window.mapWindow.highlight_node(node)


def show_node_info(node: NodeInfo):
    """Zeigt Node-Informationen in einem Dialog (optional)"""
    from PyQt6.QtWidgets import QMessageBox

    info_text = f"""
Node Information:
─────────────────
Name: {node.user.longName}
Short Name: {node.user.shortName}
ID: {node.user.id}
Hardware: {node.user.hwModel or 'Unknown'}

Position:
  Latitude: {node.position.latitude if node.position.latitude else 'Unknown'}
  Longitude: {node.position.longitude if node.position.longitude else 'Unknown'}
  Altitude: {node.position.altitude if node.position.altitude else 'Unknown'}m

Status:
  SNR: {node.snr if node.snr else 'N/A'} dB
  Hops Away: {node.hopsAway if node.hopsAway else 'N/A'}
  Battery: {node.deviceMetrics.batteryLevel if node.deviceMetrics and node.deviceMetrics.batteryLevel else 'N/A'}%
  Last Heard: {node.lastHeard.strftime('%Y-%m-%d %H:%M:%S') if node.lastHeard else 'Never'}
"""

    msg_box = QMessageBox()
    msg_box.setWindowTitle("Node Information")
    msg_box.setText(info_text)
    msg_box.exec()