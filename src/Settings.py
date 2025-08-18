#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import configparser


class Settings:
    SETTINGS_FILE = "settings.ini"
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.SETTINGS_FILE)

    def write(self):
        with open(self.SETTINGS_FILE, "w") as configfile:
            self.config.write(configfile)
