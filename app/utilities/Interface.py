import logging
import time
from datetime import datetime, timezone
from typing import Optional, Tuple

import meshtastic
import meshtastic.ble_interface
import meshtastic.serial_interface
import meshtastic.tcp_interface
from PyQt6.QtCore import QThread, pyqtSignal
from pubsub import pub

from app.utilities.NodeInfo import NodeInfo, NodeInfoUser, NodeInfoPosition, NodeInfoDeviceMetrics
from app.utilities.Packet import Packet, PacketDecoded


class Interface(QThread):
    node_discovered = pyqtSignal(NodeInfo)
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

            if self.type == 'serial':
                self.interface = meshtastic.serial_interface.SerialInterface(self.port)
                self.log_message.emit("INFO", f"Connecting via {self.type} on {self.port}")
            elif self.type == 'tcp':
                self.interface = meshtastic.tcp_interface.TCPInterface(self.host)
                self.log_message.emit("INFO", f"Connecting via {self.type} on {self.host}")
            elif self.type == 'ble':
                self.interface = meshtastic.ble_interface.BLEInterface(self.addr)
                self.log_message.emit("INFO", f"Connecting via {self.type} on {self.addr}")

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
            logging.error(f"Connection error: {str(e)}")
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
            logging.error(f"Error discovering nodes: {str(e)}")

    def parse_node_info(self, node_id: str, node_data: dict) -> Optional[NodeInfo]:
        try:
            # Sichere Zeitstempel-Konvertierung mit Fallback
            def safe_timestamp(timestamp):
                if timestamp and timestamp != 0:
                    return datetime.fromtimestamp(timestamp)
                return None

            nodeInfo = NodeInfo(
                num=int(node_data.get('num', 0)),
                user=NodeInfoUser(
                    id=node_data.get('user', {}).get('id', 'Unknown'),
                    longName=node_data.get('user', {}).get('longName', 'Unknown'),
                    shortName=node_data.get('user', {}).get('shortName', 'Unknown'),
                    macaddr=node_data.get('user', {}).get('macaddr'),
                    hwModel=node_data.get('user', {}).get('hwModel'),
                    role=node_data.get('user', {}).get('role'),
                    publicKey=node_data.get('user', {}).get('publicKey'),
                    isUnmessagable=node_data.get('user', {}).get('isUnmessagable'),
                ),
                position=NodeInfoPosition(
                    latitudeI=node_data.get('position', {}).get('latitudeI'),
                    longitudeI=node_data.get('position', {}).get('longitudeI'),
                    altitude=node_data.get('position', {}).get('altitude'),
                    time=safe_timestamp(node_data.get('position', {}).get('time')),
                    locationSource=node_data.get('position', {}).get('locationSource'),
                    latitude=node_data.get('position', {}).get('latitude'),
                    longitude=node_data.get('position', {}).get('longitude'),
                ),
                deviceMetrics=NodeInfoDeviceMetrics(
                    batteryLevel=node_data.get('deviceMetrics', {}).get('batteryLevel'),
                    voltage=node_data.get('deviceMetrics', {}).get('voltage'),
                    channelUtilization=node_data.get('deviceMetrics', {}).get('channelUtilization'),
                    airUtilTx=node_data.get('deviceMetrics', {}).get('airUtilTx'),
                    uptimeSeconds=node_data.get('deviceMetrics', {}).get('uptimeSeconds'),
                ),
                snr=node_data.get('snr'),
                lastHeard=safe_timestamp(node_data.get('lastHeard')),
                hopsAway=node_data.get('hopsAway'),
            )

            return nodeInfo

        except Exception as e:
            self.log_message.emit("ERROR", f"Error parsing node info: {str(e)}")
            logging.error(f"Error parsing node info: {str(e)}")
            return None

    def connection_established(self):
        self.log_message.emit("INFO", f"Connection established")

    def connection_lost(self):
        self.log_message.emit("INFO", f"Connection lost")

    def node_updated(self):
        self.log_message.emit("INFO", f"Node updated")

    def process_packet(self, packet: dict):
        try:
            # Sichere Konvertierung für optionale Integer-Werte
            def safe_int(value):
                if value is not None:
                    return int(value)
                return None

            # Sichere Zeitstempel-Konvertierung
            rx_time = packet.get('rxTime')
            if rx_time and rx_time != 0:
                rx_time_dt = datetime.fromtimestamp(rx_time, timezone.utc)
            else:
                rx_time_dt = datetime.now(timezone.utc)

            packetData = Packet(
                id=int(packet.get('id', 0)),
                nodeFrom=packet.get('from', 'Unknown'),
                fromId=packet.get('fromId', 'Unknown'),
                nodeTo=packet.get('to', 'Unknown'),
                toId=packet.get('toId', 'Unknown'),
                decoded=PacketDecoded(
                    portnum=packet.get('decoded', {}).get('portnum', 'Unknown'),
                    payload=packet.get('decoded', {}).get('payload', ''),
                    text=packet.get('decoded', {}).get('text', ''),
                    bitfield=safe_int(packet.get('decoded', {}).get('bitfield')),
                ),
                rxTime=rx_time_dt,
                rxSnr=float(packet.get('rxSnr', 0.0)),
                rxRssi=int(packet.get('rxRssi', 0)),
                channel=packet.get('channel'),
                wantAck=packet.get('wantAck'),
                hopLimit=safe_int(packet.get('hopLimit')),
                hopStart=safe_int(packet.get('hopStart')),
                publicKey=packet.get('publicKey'),
                pkiEncrypted=packet.get('pkiEncrypted'),
                nextHop=packet.get('nextHop'),
                relayNode=packet.get('relayNode'),
            )

            self.packet_received.emit(packetData)

        except Exception as e:
            self.log_message.emit("ERROR", f"Error processing packet: {str(e)}")
            logging.error(f"Error processing packet: {str(e)}")

    @staticmethod
    def get_node_color(node_id: str) -> Tuple[int, int, int]:
        import hashlib
        color_hash = hashlib.md5(node_id.encode()).hexdigest()

        # HSV-Farbmodell für gleichmäßigere Farben verwenden
        hue = int(color_hash[0:2], 16) * 360 // 256  # Farbton 0-360
        saturation = 180 + (int(color_hash[2:4], 16) % 75)  # Sättigung 180-255
        value = 180 + (int(color_hash[4:6], 16) % 75)  # Helligkeit 180-255

        return hue, saturation, value