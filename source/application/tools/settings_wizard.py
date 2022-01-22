from ui.settings_ui.settings_window import SettingsWindowUi
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QWidget


class SettingsWizard:

    """Класс, описывающий менеджер настроек приложения"""

    def __init__(self):
        self.window = QWidget()
        self.ui = SettingsWindowUi()
        self.ui.setupUi(self.window)
        self.settings = QSettings('parser_config.ini', QSettings.Format.IniFormat)
        self.ui.OkButton.clicked.connect(self.save_settings)
        self.ui.CancelButton.clicked.connect(self.close)
        self.read_settings()

    def show(self):
        self.read_settings()
        self.window.show()

    def close(self):
        self.window.close()
        self.settings.sync()

    def save_settings(self):
        self.settings.setValue(
            'auto_parse',
            self.ui.AutoParse.isChecked(),
        )
        self.settings.setValue(
            'proxy_enabled',
            self.ui.UseProxies.isChecked()
        )
        self.settings.sync()
        self.close()

    def read_settings(self):
        if self.settings.value('auto_parse', type=bool):
            self.ui.AutoParse.setChecked(True)
        else:
            self.ui.AutoParse.setChecked(False)
        if self.settings.value('proxy_enabled', type=bool):
            self.ui.UseProxies.setChecked(True)
        else:
            self.ui.UseProxies.setChecked(False)
