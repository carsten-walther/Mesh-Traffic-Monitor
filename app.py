#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging
import sys

from PyQt6.QtWidgets import QApplication

from src.Interface import Interface
from src.Settings import Settings
from ui.MainWindow import MainWindow

# https://github.com/pdxlocations/Meshtastic-Python-Examples/blob/main/print-packets.py

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    app = QApplication(sys.argv)
    settings = Settings()
    interface = Interface()
    main_window = MainWindow(settings, interface)

    logging.info(f"Mesh-Traffic-Monitor started")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()