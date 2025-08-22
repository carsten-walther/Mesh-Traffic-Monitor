import io
import os
import folium

from PyQt6.QtCore import QSettings, QByteArray, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from app.utilities.AppConfig import AppConfig
from app.utilities.NodeInfo import NodeInfo


class MapWindow(QWidget):
    def __init__(self, interface) -> None:
        super().__init__()
        self.interface = interface

        self.settings = QSettings(AppConfig().load()['app']['name'], "Map")
        self.readSettings()

        self.web_view = None

        self.initUi()

        self.nodes = {}
        self.interface.node_discovered.connect(self.add_node)
        self.update_map()

    def initUi(self) -> None:
        self.setWindowTitle(f"{AppConfig().load()['app']['name']} - Map")
        self.setMinimumSize(800, 300)

        layout = QVBoxLayout()

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)

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

    def update_map(self):
        """Aktualisiert die Karte mit allen bekannten Nodes"""
        # Standard-Standort (Deutschland Mitte) falls keine Nodes vorhanden
        center_lat, center_lon = 51.1657, 10.4515

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

        # Folium Karte erstellen
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=8,
            tiles='OpenStreetMap.Mapnik'
        )

        for node in self.nodes.values():
            if (node.position and
                    node.position.latitude and node.position.longitude and
                    node.position.latitude != 0 and node.position.longitude != 0):
                color = self.get_node_color(node)

                popup_html = f"""
                <div>
                    <h4>{node.user.longName}</h4>
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

                folium.CircleMarker(
                    location=[node.position.latitude, node.position.longitude],
                    radius=8,
                    popup=folium.Popup(popup_html, max_width=350),
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                    weight=2,
                    tooltip=f"{node.user.longName} ({node.user.shortName})"
                ).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.web_view.setHtml(data.getvalue().decode())

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
