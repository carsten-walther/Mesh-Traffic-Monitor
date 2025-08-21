from PyQt6.QtCore import Qt, QRect, QModelIndex
from PyQt6.QtGui import QPainter, QFont, QColor
from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from app.utils.node import Node


class NodeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        node: Node = index.data(Qt.ItemDataRole.UserRole)
        if not node:
            super().paint(painter, option, index)
            return

        painter.save()

        # Hintergrund zeichnen (für Selektion/Hover)
        self.parent().style().drawPrimitive(
            self.parent().style().PrimitiveElement.PE_PanelItemViewItem,
            option, painter, self.parent()
        )

        # Textbereich definieren
        text_rect = option.rect.adjusted(8, 3, -8, -3)

        # Schriftarten definieren
        title_font = QFont(option.font)
        title_font.setBold(True)
        title_font.setPointSize(option.font.pointSize() + 1)

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
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, node.long_name)

        # Short Name und Hardware in derselben Zeile
        painter.setFont(detail_font)
        painter.setPen(detail_color)
        info_y = title_rect.bottom() + 1
        info_text = f"{node.short_name} • {node.hardware}"
        info_rect = QRect(text_rect.left(), info_y, text_rect.width(), 14)
        painter.drawText(info_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, info_text)

        # Status-Informationen in der nächsten Zeile
        status_y = info_rect.bottom() + 1
        status_parts = []

        if node.battery_level is not None:
            status_parts.append(f"🔋 {node.battery_level}%")
        if node.snr is not None:
            status_parts.append(f"SNR: {node.snr}dB")
        if node.rssi is not None:
            status_parts.append(f"RSSI: {node.rssi}dBm")

        if status_parts:
            painter.setFont(small_font)
            status_text = " • ".join(status_parts)
            status_rect = QRect(text_rect.left(), status_y, text_rect.width(), 14)
            painter.drawText(status_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, status_text)

        # Zeitstempel (rechts ausgerichtet)
        time_text = node.last_seen.strftime('%H:%M:%S')
        time_rect = QRect(text_rect.right() - 80, text_rect.top(), 80, 16)
        painter.setFont(small_font)
        painter.drawText(time_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, time_text)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        return option.rect.size().expandedTo(QRect(0, 0, 200, 45).size())
