import io
import folium

from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSettings, QByteArray
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMenu, QWidget, QVBoxLayout

from app.utilities.AppConfig import AppConfig
from app.utilities.NodeInfo import NodeInfo


class MapWindow(QWidget):
    def __init__(self, interface) -> None:
        super().__init__()
        self.interface = interface

        self.settings = QSettings(AppConfig().load()['app']['name'], "Map")
        self.readSettings()

        self.webView = None
        self.highlighted_node = None

        self.initUi()

        self.nodes = {}
        self.interface.node_discovered.connect(self.add_node)
        self.update_map()

    def initUi(self) -> None:
        self.setWindowTitle("Map")
        self.setMinimumSize(800, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.webView = QWebEngineView()
        layout.addWidget(self.webView)

        self.setLayout(layout)

        # Kontext-Menü für MapWindow aktivieren
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_map_context_menu)

    def writeSettings(self) -> None:
        self.settings.setValue("geometry", self.saveGeometry())

    def readSettings(self) -> None:
        self.restoreGeometry(self.settings.value("geometry", QByteArray()))

    def closeEvent(self, event) -> None:
        self.writeSettings()
        super().closeEvent(event)
        event.accept()

    def add_node(self, node_info: NodeInfo) -> None:
        self.nodes[node_info.user.id] = node_info
        self.update_map()

    def highlight_node(self, node: NodeInfo):
        """Hebt einen bestimmten Node auf der Karte hervor"""
        self.highlighted_node = node
        self.update_map()

        # Fenster in den Vordergrund bringen
        self.raise_()
        self.activateWindow()

    def clear_highlight(self):
        """Entfernt die Hervorhebung von allen Nodes"""
        self.highlighted_node = None
        self.update_map()

    def show_map_context_menu(self, position):
        """Zeigt Kontext-Menü für die Karte an"""

        if not self.highlighted_node:
            return  # Kein Menü anzeigen wenn kein Node hervorgehoben ist

        menu = QMenu(self)

        clear_action = QAction("Clear Highlight", menu)
        clear_action.triggered.connect(self.clear_highlight)
        menu.addAction(clear_action)

        # Menü an der Cursor-Position anzeigen
        global_pos = self.mapToGlobal(position)
        menu.exec(global_pos)

    def update_map(self):
        """Aktualisiert die Karte mit allen bekannten Nodes"""
        # Standard-Standort (Deutschland Mitte) falls keine Nodes vorhanden
        center_lat, center_lon = 51.1657, 10.4515
        zoom_level = 10

        # Wenn Nodes vorhanden sind, Zentrum basierend auf Nodes berechnen
        if self.nodes:
            valid_positions = []
            for node in self.nodes.values():
                if (node.position and
                        node.position.latitude and node.position.longitude and
                        node.position.latitude != 0 and node.position.longitude != 0):
                    valid_positions.append((node.position.latitude, node.position.longitude))

            if valid_positions:
                center_lat = sum(pos[0] for pos in valid_positions) / len(valid_positions)
                center_lon = sum(pos[1] for pos in valid_positions) / len(valid_positions)

        # Wenn ein Node hervorgehoben werden soll, auf diesen zentrieren
        if (self.highlighted_node and
                self.highlighted_node.position and
                self.highlighted_node.position.latitude and
                self.highlighted_node.position.longitude):
            center_lat = self.highlighted_node.position.latitude
            center_lon = self.highlighted_node.position.longitude
            zoom_level = 15  # Näher heranzoomen für hervorgehobenen Node

        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_level,
            tiles='OpenStreetMap.Mapnik'
        )

        for node in self.nodes.values():
            if (node.position and
                    node.position.latitude and node.position.longitude and
                    node.position.latitude != 0 and node.position.longitude != 0):

                # Prüfen ob dies der hervorgehobene Node ist
                is_highlighted = (self.highlighted_node and
                                  node.user.id == self.highlighted_node.user.id)

                color = self.get_node_color(node)
                radius = 12 if is_highlighted else 8  # Größerer Radius für hervorgehobenen Node
                weight = 4 if is_highlighted else 2  # Dickerer Rand für hervorgehobenen Node

                popup_html = f"""
                <div>
                    <h4>{node.user.longName}{'<br><span style="color: red;">📍 HIGHLIGHTED</span>' if is_highlighted else ''}</h4>
                    <p>
                        <b>ID:</b> {node.user.id}<br>
                        <b>Short Name:</b> {node.user.shortName}<br>
                        <b>Hardware:</b> {node.user.hwModel or 'Unknown'}<br>
                        <b>SNR:</b> {node.snr if node.snr else 'N/A'} dB<br>
                        <b>Hops Away:</b> {node.hopsAway if node.hopsAway else 'N/A'}<br>
                        <b>Battery:</b> {node.deviceMetrics.batteryLevel if node.deviceMetrics and node.deviceMetrics.batteryLevel else 'N/A'}%<br>
                        <b>Last Heard:</b> {node.lastHeard.strftime('%Y-%m-%d %H:%M:%S') if node.lastHeard else 'Never'}
                    </p>
                </div>
                """

                marker = folium.CircleMarker(
                    location=[node.position.latitude, node.position.longitude],
                    radius=radius,
                    popup=folium.Popup(popup_html, max_width=350),
                    color='red' if is_highlighted else color,  # Rote Farbe für hervorgehobenen Node
                    fill=True,
                    fillColor='red' if is_highlighted else color,
                    fillOpacity=0.9 if is_highlighted else 0.7,  # Stärkere Deckkraft
                    weight=weight,
                    tooltip=f"{'🎯 ' if is_highlighted else ''}{node.user.longName} ({node.user.shortName})"
                )

                marker.add_to(m)

                # Für hervorgehobenen Node zusätzlich einen Pulsing-Effekt hinzufügen
                if is_highlighted:
                    # Äußerer Kreis für Pulsing-Effekt
                    folium.CircleMarker(
                        location=[node.position.latitude, node.position.longitude],
                        radius=20,
                        color='red',
                        fill=False,
                        weight=1,
                        opacity=0.5
                    ).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

    def get_node_color(self, node: NodeInfo) -> str:
        from datetime import datetime, timedelta
        if node.lastHeard:
            time_diff = datetime.now() - node.lastHeard
            if time_diff < timedelta(minutes=30):
                return 'green'
            elif time_diff < timedelta(hours=2):
                return 'orange'
            else:
                return 'red'
        else:
            return 'gray'
