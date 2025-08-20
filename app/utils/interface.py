import time
from datetime import datetime, timezone
from typing import Optional

import meshtastic
import meshtastic.ble_interface
import meshtastic.serial_interface
import meshtastic.tcp_interface
from PyQt6.QtCore import QThread, pyqtSignal
from pubsub import pub

from .node import Node
from .packet import Packet


class Interface(QThread):
    node_discovered = pyqtSignal(Node)
    packet_received = pyqtSignal(Packet)
    connection_status = pyqtSignal(bool, str)
    log_message = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.interface = None
        self.running = False
        self.type = None
        self.port = None
        self.host = None
        self.addr = None

    def connect(self, connection_type: str, port: str, host: str, addr: str):
        self.type = connection_type
        self.port = port
        self.host = host
        self.addr = addr
        self.start()

    def disconnect(self):
        self.running = False
        if self.interface:
            try:
                self.interface.close()
                self.log_message.emit("INFO", f"Connection closed")
            except:
                pass
        self.wait()

    def run(self):
        try:
            self.running = True
            self.log_message.emit("INFO", f"Connecting via {self.type} on {self.port}{self.host}{self.addr}")

            if self.type == 'serial':
                self.interface = meshtastic.serial_interface.SerialInterface(self.port)
            elif self.type == 'tcp':
                self.interface = meshtastic.tcp_interface.TCPInterface(self.host)
            elif self.type == 'ble':
                self.interface = meshtastic.ble_interface.BLEInterface(self.addr)

            self.connection_status.emit(True, f"Connected")

            def on_connection_established(interface, topic=pub.AUTO_TOPIC):
                self.connection_established()

            pub.subscribe(on_connection_established, "meshtastic.connection.established")

            def on_connection_lost(interface, topic=pub.AUTO_TOPIC):
                self.connection_lost()

            pub.subscribe(on_connection_lost, "meshtastic.connection.lost")

            def on_node_updated(interface, topic=pub.AUTO_TOPIC):
                self.node_updated()

            pub.subscribe(on_node_updated, "meshtastic.node.updated(node=NodeInfo)")

            def on_receive(packet, interface):
                self.process_packet(packet)

            pub.subscribe(on_receive, "meshtastic.receive")

            self.discover_nodes()

            while self.running:
                time.sleep(0.1)

        except Exception as e:
            self.log_message.emit("ERROR", f"Connection error: {str(e)}")
            self.connection_status.emit(False, str(e))

    def discover_nodes(self):
        try:
            if self.interface and hasattr(self.interface, 'nodes'):
                for node_id, node in self.interface.nodes.items():
                    node_info = self.parse_node_info(node_id, node)
                    if node_info:
                        self.node_discovered.emit(node_info)
        except Exception as e:
            self.log_message.emit("ERROR", f"Error discovering nodes: {str(e)}")

    def parse_node_info(self, node_id: str, node_data: dict) -> Optional[Node]:
        try:
            user = node_data.get('user', {})
            position = node_data.get('position', {})
            device_metrics = node_data.get('deviceMetrics', {})

            node_info = Node(
                node_id=node_id,
                short_name=user.get('shortName', f'Node-{node_id[-4:]}'),
                long_name=user.get('longName', f'Unknown Node {node_id}'),
                hardware=user.get('hwModel', 'Unknown'),
                last_seen=datetime.now(timezone.utc),
                battery_level=device_metrics.get('batteryLevel')
            )

            if position.get('latitude') and position.get('longitude'):
                node_info.position = (
                    position['latitude'],
                    position['longitude'],
                    position.get('altitude', 0)
                )

            return node_info

        except Exception as e:
            self.log_message.emit("ERROR", f"Error parsing node info: {str(e)}")
            return None

    def connection_established(self):
        self.log_message.emit("INFO", f"Connection established")

    def connection_lost(self):
        self.log_message.emit("INFO", f"Connection lost")

    def node_updated(self):
        self.log_message.emit("INFO", f"Node updated")

    def process_packet(self, packet: dict):
        try:
            packet_data = Packet(
                from_node=str(packet.get('from', 'Unknown')),
                to_node=str(packet.get('to', 'Unknown')),
                relay_node=str(packet.get('relayNode', 'Unknown')),
                channel=str(packet.get('channel', '')),
                port_number=packet.get('decoded', {}).get('portnum', 'Unknown'),
                payload_size=len(str(packet.get('decoded', {}).get('payload', ''))),
                id=int(packet.get('id', '')),
                rx_time=datetime.fromtimestamp(packet.get('rxTime', 0), timezone.utc) if packet.get('rxTime', None) else datetime.now(timezone.utc),
                from_id=str(packet.get('fromId', '')),
                to_id=str(packet.get('toId', '')),
                rx_snr=packet.get('rxSnr'),
                rx_rssi=packet.get('rxRssi'),
                hop_limit=packet.get('hopLimit'),
                hop_start=packet.get('hopStart'),
                payload=str(packet.get('decoded', {}).get('payload', ''))
            )

            self.packet_received.emit(packet_data)

        except Exception as e:
            self.log_message.emit("ERROR", f"Error processing packet: {str(e)}")
