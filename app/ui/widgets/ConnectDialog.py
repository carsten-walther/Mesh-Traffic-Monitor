import serial.tools.list_ports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QDialog, QDialogButtonBox, QFormLayout
from meshtastic.ble_interface import BLEInterface


class ConnectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.type_label = None
        self.type_combo = None
        self.port_label = None
        self.port_combo = None
        self.host_label = None
        self.host_line = None
        self.addr_label = None
        self.addr_combo = None

        self.init_ui()

        self.add_type_combo_items()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        layout = QVBoxLayout()

        info_text = QLabel("Please select connection type for your node.")

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        self.type_label = QLabel('Type', form_widget)
        form_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.type_label)

        self.type_combo = QComboBox()
        self.type_combo.setCurrentIndex(2)
        self.type_combo.currentIndexChanged.connect(self.on_type_combo_changed)
        form_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.type_combo)

        self.port_label = QLabel('Port', form_widget)
        self.port_label.hide()
        form_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.port_label)

        self.port_combo = QComboBox()
        self.port_combo.hide()
        form_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.port_combo)

        self.host_label = QLabel('Hostname', form_widget)
        self.host_label.hide()
        form_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.host_label)

        self.host_line = QLineEdit("192.168.178.72")
        self.host_line.setPlaceholderText("meshtastic.local")
        self.host_line.hide()
        form_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.host_line)

        self.addr_label = QLabel('Address', form_widget)
        self.addr_label.hide()
        form_layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.addr_label)

        self.addr_combo = QComboBox()
        self.addr_combo.hide()
        form_layout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.addr_combo)

        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(info_text)
        layout.addWidget(form_widget)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.setWindowTitle("Connect")
        # self.resize(300, 200)
        self.setModal(True)
        self.center()
        self.show()

    def on_type_combo_changed(self, value):
        if value == 1:
            self.add_port_combo_items()

            self.port_label.show()
            self.port_combo.show()
            self.host_label.hide()
            self.host_line.hide()
            self.addr_label.hide()
            self.addr_combo.hide()
        elif value == 2:
            self.port_label.hide()
            self.port_combo.hide()
            self.host_label.show()
            self.host_line.show()
            self.addr_label.hide()
            self.addr_combo.hide()
        elif value == 3:
            self.add_addr_combo_items()

            self.port_label.hide()
            self.port_combo.hide()
            self.host_label.hide()
            self.host_line.hide()
            self.addr_label.show()
            self.addr_combo.show()

    def add_type_combo_items(self):
        self.type_combo.clear()
        self.type_combo.addItem("")
        self.type_combo.addItem("Serial")
        self.type_combo.addItem("Tcp")
        self.type_combo.addItem("Ble")

    def add_port_combo_items(self):
        self.port_combo.clear()
        self.port_combo.addItem("")
        for port in serial.tools.list_ports.comports():
            self.port_combo.addItem(f"{port.device}")
        if self.port_combo.count() == 0:
            self.port_combo.addItem("No ports found")

    def add_addr_combo_items(self):
        self.addr_combo.clear()
        self.addr_combo.addItem("")
        for device in BLEInterface.scan():
            self.addr_combo.addItem(f"{device.address}")
        if self.addr_combo.count() == 0:
            self.addr_combo.addItem("No devices found")
