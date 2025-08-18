#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from datetime import datetime

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QTextEdit, QTableWidget, \
    QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt6.uic.Compiler.qtproxies import QtGui


class LogWindow(QWidget):
    def __init__(self, settings, interface):
        super().__init__()

        self.settings = settings
        self.interface = interface
        self.interface.log_message.connect(self.on_log_message)

        self.update_timer = QTimer()
        self.update_timer.start()
        self.update_timer.timeout.connect(self.update_log_table)

        self.log_debug_cb = None
        self.log_info_cb = None
        self.log_error_cb = None

        self.log_table = None
        self.log_data = []

        self.init_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Log Level:"))

        self.log_debug_cb = QCheckBox("DEBUG")
        self.log_debug_cb.setChecked(self.settings.config.getboolean('log', 'debug'))
        self.log_debug_cb.stateChanged.connect(self.on_log_debug_cb)
        filter_layout.addWidget(self.log_debug_cb)

        self.log_info_cb = QCheckBox("INFO")
        self.log_info_cb.setChecked(self.settings.config.getboolean('log', 'info'))
        self.log_info_cb.stateChanged.connect(self.on_log_info_cb)
        filter_layout.addWidget(self.log_info_cb)

        self.log_error_cb = QCheckBox("ERROR")
        self.log_error_cb.setChecked(self.settings.config.getboolean('log', 'error'))
        self.log_error_cb.stateChanged.connect(self.on_log_error_cb)
        filter_layout.addWidget(self.log_error_cb)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.log_table.setHorizontalHeaderLabels(['Timestamp', 'Level', 'Message'])
        layout.addWidget(self.log_table)

        header = self.log_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.setLayout(layout)
        self.setWindowTitle("Log")
        self.resize(800, 300)
        self.center()

    def on_log_debug_cb(self, s):
        self.settings.config.set('log', 'debug', str(s == Qt.CheckState.Checked.value))
        self.settings.write()

    def on_log_info_cb(self, s):
        self.settings.config.set('log', 'info', str(s == Qt.CheckState.Checked.value))
        self.settings.write()

    def on_log_error_cb(self, s):
        self.settings.config.set('log', 'error', str(s == Qt.CheckState.Checked.value))
        self.settings.write()

    def on_log_message(self, level: str, message: str):
        self.log_data.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'level': level,
            'message': message
        })

        if len(self.log_data) > 1000:
            self.log_data = self.log_data[-1000:]

    def update_log_table(self):
        recent_logs = self.log_data[-100:]
        self.log_table.setRowCount(len(recent_logs))

        for i, log in enumerate(reversed(recent_logs)):
            self.log_table.setItem(i, 0, QTableWidgetItem(log.get('timestamp')))
            self.log_table.setItem(i, 1, QTableWidgetItem(log.get('level')))
            self.log_table.setItem(i, 2, QTableWidgetItem(log.get('message')))

            if log.get('level') == 'DEBUG':
                self.log_table.item(i, 1).setBackground(QColor(109, 129, 150))
            elif log.get('level') == 'INFO':
                self.log_table.item(i, 1).setBackground(QColor(186, 142, 35))
            elif log.get('level') == 'ERROR':
                self.log_table.item(i, 1).setBackground(QColor(155, 17, 30))