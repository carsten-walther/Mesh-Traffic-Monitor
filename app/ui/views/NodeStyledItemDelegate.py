from PyQt6.QtCore import Qt, QRect, QModelIndex, QSize
from PyQt6.QtGui import QPainter, QFont, QColor
from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from app.utilities.NodeInfo import NodeInfo


class NodeStyledItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        node: NodeInfo = index.data(Qt.ItemDataRole.UserRole)
        if not node:
            super().paint(painter, option, index)
            return

        painter.save()

        # Hintergrund zeichnen (für Selektion/Hover)
        self.parent().style().drawPrimitive(
            self.parent().style().PrimitiveElement.PE_PanelItemViewItem,
            option,
            painter,
            self.parent()
        )

        # Kreis für Icon zeichnen (links vom Text)
        circle_size = 45  # Durchmesser des Kreises
        circle_margin = 10  # Abstand vom Rand
        circle_x = option.rect.left() + circle_margin
        circle_y = option.rect.top() + (option.rect.height() - circle_size) // 2  # Vertikal zentriert
        circle_rect = QRect(circle_x, circle_y, circle_size, circle_size)

        # Farbe basierend auf node_id generieren (konsistent für gleiche Node)
        circle_color = self.get_node_color(node.user.shortName)

        # Kreis zeichnen
        painter.setBrush(circle_color)
        painter.setPen(Qt.PenStyle.NoPen)  # Kein Rand
        painter.drawEllipse(circle_rect)

        # Shortname im Kreis zentrieren
        painter.setPen(QColor(255, 255, 255))  # Weiße Schrift
        circle_font = QFont(option.font)
        circle_font.setBold(True)
        circle_font.setPointSize(option.font.pointSize())
        painter.setFont(circle_font)
        painter.drawText(circle_rect, Qt.AlignmentFlag.AlignCenter, node.user.shortName)

        # Textbereich definieren
        text_rect = option.rect.adjusted(65, 5, -5, -5)

        # Schriftarten definieren
        title_font = QFont(option.font)
        title_font.setPointSize(option.font.pointSize() + 2)
        title_font.setBold(True)

        detail_font = QFont(option.font)
        detail_font.setPointSize(option.font.pointSize() - 1)

        small_font = QFont(option.font)
        small_font.setPointSize(option.font.pointSize() - 2)

        # Farben definieren
        text_color = option.palette.color(option.palette.ColorGroup.Normal, option.palette.ColorRole.Text)
        detail_color = QColor(text_color)
        detail_color.setAlpha(180)

        # Titel zeichnen (Long Name)
        painter.setFont(title_font)
        painter.setPen(text_color)
        title_rect = QRect(text_rect.left(), text_rect.top(), text_rect.width(), 16)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, node.user.longName)

        # Hardware in derselben Zeile
        painter.setFont(detail_font)
        painter.setPen(detail_color)
        info_y = title_rect.bottom() + 5
        info_text = node.user.hwModel
        info_rect = QRect(text_rect.left(), info_y, text_rect.width(), 14)
        painter.drawText(info_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, info_text)

        # Status-Informationen in drei Spalten aufteilen
        status_y = info_rect.bottom() + 5
        status_parts = []

        if node.deviceMetrics.batteryLevel is not None:
            status_parts.append(f"Battery: {node.deviceMetrics.batteryLevel}%")
        if node.snr is not None:
            status_parts.append(f"SNR: {node.snr}dB")
        if node.hopsAway is not None:
            status_parts.append(f"Hops Away: {node.hopsAway}")

        if status_parts:
            painter.setFont(small_font)

            # Drei gleich breite Spalten erstellen
            col_width = text_rect.width() // 3

            # Linke Spalte (linksbündig)
            if len(status_parts) > 0:
                left_rect = QRect(text_rect.left(), status_y, col_width, 14)
                painter.drawText(left_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                                 status_parts[0])

            # Mittlere Spalte (zentriert)
            if len(status_parts) > 1:
                center_rect = QRect(text_rect.left() + col_width, status_y, col_width, 14)
                painter.drawText(center_rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
                                 status_parts[1])

            # Rechte Spalte (rechtsbündig)
            if len(status_parts) > 2:
                right_rect = QRect(text_rect.left() + 2 * col_width, status_y, col_width, 14)
                painter.drawText(right_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
                                 status_parts[2])

        time_text = node.lastHeard.strftime('%H:%M:%S')
        time_rect = QRect(text_rect.right() - 80, text_rect.top(), 80, 16)

        painter.setFont(small_font)
        painter.drawText(time_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, time_text)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        return QSize(-1, 65)

    # Bessere Farbverteilung (hellere, freundlichere Farben)
    def get_node_color(self, node_id: str) -> QColor:
        import hashlib
        color_hash = hashlib.md5(node_id.encode()).hexdigest()

        # HSV-Farbmodell für gleichmäßigere Farben verwenden
        hue = int(color_hash[0:2], 16) * 360 // 256  # Farbton 0-360
        saturation = 180 + (int(color_hash[2:4], 16) % 75)  # Sättigung 180-255
        value = 180 + (int(color_hash[4:6], 16) % 75)  # Helligkeit 180-255

        color = QColor()
        color.setHsv(hue, saturation, value)

        return color