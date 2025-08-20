import configparser

class AppConfig:
    CONFIG_FILE = "config.ini"

    def __init__(self) -> None:
        self.appConfig = configparser.ConfigParser()
        self.appConfig.read(self.CONFIG_FILE)

    def load(self) -> dict:
        return self.appConfig

    def update(self) -> None:
        with open(self.CONFIG_FILE, "w") as configfile:
            self.appConfig.write(configfile)
