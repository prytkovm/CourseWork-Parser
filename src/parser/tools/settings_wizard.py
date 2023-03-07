from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import QWidget
from ..ui.settings_window import SettingsWindowUi


class SettingsWizard:

    """Класс, описывающий менеджер настроек приложения."""

    def __init__(self):
        """Конструктор класса SettingsWizard."""
        self.window = QWidget()
        self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui = SettingsWindowUi()
        self.ui.setupUi(self.window)
        self.settings = QSettings('parser_config.ini', QSettings.Format.IniFormat)
        self.ui.OkButton.clicked.connect(self.save_settings)
        self.ui.CancelButton.clicked.connect(self.close)
        self.read_settings()

    def show(self):
        """Метод, отображающий окно настроек."""
        self.read_settings()
        self.window.show()

    def close(self):
        """Метод, закрывающий окно настроек."""
        self.window.close()
        self.settings.sync()

    def save_settings(self):
        """Метод, сохраняющий настройки в файл parser_config.ini."""
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
        """Метод, считывающий настройки из файла parser_config.ini."""
        if self.settings.value('auto_parse', type=bool):
            self.ui.AutoParse.setChecked(True)
        else:
            self.ui.AutoParse.setChecked(False)
        if self.settings.value('proxy_enabled', type=bool):
            self.ui.UseProxies.setChecked(True)
        else:
            self.ui.UseProxies.setChecked(False)

    def autoparse_enabled(self):
        """Метод, получающий значение из настроек, отвечающее за автопарсинг при запуске.

        Returns:
             True: автопарсинг включен,
             False: автопарсинг выключен.
        """
        return self.settings.value('auto_parse', type=bool)
