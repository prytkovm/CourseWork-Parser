from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6.QtCore import Qt, QThreadPool
from .tools.settings_wizard import SettingsWizard
from .tools.links_extractor import LinksExtractor
from .tools.parsing_wizard import ParsingWizard
from .tools.parsing_worker import ParsingWorker
from .tools.communication import Communicate
from .tools.file_browser import FileDialog
from .tools.csv_reader import CsvReader
from .tools.csv_writer import CsvWriter
from .ui.mainwindow import MainWindowUI
from datetime import date
from glob import glob
import logging
import sys


class App:
    """Класс, описыващий приложение."""

    def __init__(self):
        """Конструктор класса App."""
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.main_window = QMainWindow()
        self.msg_window = QMessageBox()
        self.msg_window.setIcon(QMessageBox.Icon.Warning)
        self.msg_window.setWindowTitle('Message')
        self.msg_window.setText('Something went wrong.\n'
                                'See logs for more information')
        self.main_window_ui = MainWindowUI()
        self.main_window_ui.setupUi(self.main_window)
        self.settings_wizard = SettingsWizard()
        self.signals = Communicate()
        self.parsing_wizard = ParsingWizard(communicate=self.signals)
        self.file_browser = FileDialog()
        self.connect_slots()
        logging.basicConfig(
            filename='../app_log.log',
            filemode='w',
            format='%(asctime)s, %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.ERROR
        )
        self.logger = logging.getLogger(__name__)
        self.parsing_thread = QThreadPool()
        if self.settings_wizard.autoparse_enabled():
            self.auto_parse()

    def init_parsing(self):
        """Метод для инициализации процесса парсинга, отключает слоты ParsingWizard во избежание коллизий при ручном
        конфигурировании задачи парсинга. Вызывается при совершении пользователем действия start parsing.
        """
        self.parsing_wizard.disable_files_operations()
        self.parsing_wizard.urls_get_window.show()
        self.signals.links_got.connect(self.start_parsing)

    def start_parsing(self, urls):
        """Метод, запускающий процесс парсинга после получения ссылок.

        Args:
            urls:
                полученные ссылки.
        """
        self.parsing_wizard.urls_get_window.close()
        urls = LinksExtractor.get_relevant(urls)
        # Создаем задачу
        worker = ParsingWorker(
            communicate=self.signals,
            urls=urls
        )
        # Кидаем задачу в отдельный поток
        self.parsing_thread.start(worker)

    def auto_parse(self):
        """Метод, запускающий процесс автопарсинга."""
        self.parsing_wizard.disable_files_operations()
        self.parsing_thread.clear()
        tasks = self.parsing_wizard.read_tasks()
        urls_set = []
        for task in tasks:
            urls = LinksExtractor.get_relevant(task['links'])
            urls_set.append(urls)
        worker = ParsingWorker(
            communicate=self.signals,
            urls=urls_set,
            auto_parse=True
        )
        self.parsing_thread.start(worker)

    def show_parsed_data(self, from_auto_parse):
        """Метод, отображающий спарсенные данные в таблице.
        Вызывается пи получении сигнала parsing_finished.

        Args:
            from_auto_parse:
                флаг, показывающий откуда юыли получены данные,
                True - даннные получены автопарсингом,
                False - данные получены ручным конфигурированием парсера.
        """
        self.parsing_wizard.enable_files_operations()
        try:
            if from_auto_parse:
                data = CsvReader.merge_files(glob(f'parsed_data/{date.today()}/auto/*.csv'))
            else:
                data = CsvReader.merge_files(glob(f'parsed_data/{date.today()}/*.csv'))
            if data is not None:
                self.set_table_data(data)
        except Exception as error:
            self.logger.error(error)
            self.msg_window.show()
            return

    def stop_parsing(self):
        """Метод, останавливающий парсинг, посылает сигнал stop_parsing."""
        self.signals.stop_parsing.emit()

    def read_csv(self):
        """Метод, считывающий данные из csv файла, выбранного пользователем и отображающий их в таблице.
        Вызывается при совершении пользователем действия open file.
        """
        try:
            path_to_file = self.file_browser.show_file_open_dialog()
            if path_to_file is None:
                return
            data = CsvReader.read_file(path_to_file)
            if data is not None:
                self.set_table_data(data)
        except Exception as error:
            self.logger.error(error)
            self.msg_window.show()
            return

    def write_csv(self):
        """Метод, записывающий данные в csv файл, выбранный пользователем.
        Вызывается при совершении пользователем действия export file.
        """
        try:
            path_to_file = self.file_browser.show_file_save_dialog()
            if path_to_file is None:
                return
            rows = self.main_window_ui.tableWidget.rowCount()
            columns = self.main_window_ui.tableWidget.columnCount()
            header = []
            for i in range(columns):
                header_item = self.main_window_ui.tableWidget.horizontalHeaderItem(i).data(Qt.ItemDataRole.DisplayRole)
                header.append(header_item)
            header = (','.join(header) + '\n').encode('utf_8')
            data = []
            for i in range(rows):
                table_row = []
                for j in range(columns):
                    cell = self.main_window_ui.tableWidget.item(i, j).text()
                    table_row.append(f'"{cell}"')
                table_row = (','.join(table_row) + '\n').encode('utf_8')
                data.append(table_row)
            CsvWriter.write(path_to_file, header, data)
        except Exception as error:
            self.logger.error(error)
            self.msg_window.show()
            return

    def set_table_data(self, data):
        """Метод, отображающий данные в таблице tableWidget главного окна.

        Args:
            data:
                данные для отображения, тип - Pandas DataFrame.
        """
        rows_count = len(data.index)
        columns_count = len(data.columns)
        self.main_window_ui.tableWidget.setColumnCount(columns_count)
        self.main_window_ui.tableWidget.setRowCount(rows_count)
        self.main_window_ui.tableWidget.setHorizontalHeaderLabels(data.columns)
        for i in range(rows_count):
            for j in range(columns_count):
                item = QTableWidgetItem(str(data.iat[i, j]))
                self.main_window_ui.tableWidget.setItem(i, j, item)
        self.main_window_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.main_window_ui.tableWidget.setEnabled(True)
        self.main_window_ui.tableWidget.setVisible(True)

    def enable_stop_button(self):
        """Метод, делающий кнопку остановки парсинга доступной пользователю для взаимодействия."""
        self.main_window_ui.actionStopParsing.setEnabled(True)

    def disable_stop_button(self):
        """Метод, делающий кнопку остановки парсинга недоступной пользователю для взаимодействия."""
        self.main_window_ui.actionStopParsing.setEnabled(False)

    def enable_start_button(self):
        """Метод, делающий кнопку начала парсинга доступной пользователю для взаимодействия."""
        self.main_window_ui.actionStartParsing.setEnabled(True)

    def disable_start_button(self):
        """Метод, делающий кнопку начала парсинга недоступной пользователю для взаимодействия."""
        self.main_window_ui.actionStartParsing.setEnabled(False)

    def show_loading_logo(self):
        """Метод, отображающий логотип загрузки, вызывается при получении сигнала parsing_started."""
        self.main_window_ui.label.setEnabled(True)
        self.main_window_ui.label.setVisible(True)
        self.main_window_ui.tableWidget.setVisible(False)
        self.main_window_ui.tableWidget.setEnabled(False)
        self.main_window_ui.movie.start()

    def hide_loading_logo(self):
        """Метод, скрывающий логотип загрузки, вызывается при получении сигнала parsing_finished."""
        self.main_window_ui.movie.stop()
        self.main_window_ui.label.setEnabled(False)
        self.main_window_ui.label.setVisible(False)
        self.main_window_ui.tableWidget.setEnabled(True)
        self.main_window_ui.tableWidget.setVisible(True)

    def show_settings_window(self):
        """Метод, отображающий окно настроек, вызывается при совершении пользователем действия open settings."""
        self.settings_wizard.show()

    def send_to_statusbar(self, text):
        """Метод, отображающий текст в статус-баре главного окна приложения.

        Args:
            text:
                строка, текст для отображения.
        """
        self.main_window_ui.statusbar.showMessage(text, 1500)

    def connect_slots(self):
        """Метод, подключающий слоты приложения."""
        self.main_window_ui.actionOpenSettings.triggered.connect(self.show_settings_window)
        self.main_window_ui.actionOpenFile.triggered.connect(self.read_csv)
        self.main_window_ui.actionExport.triggered.connect(self.write_csv)
        self.main_window_ui.actionStartParsing.triggered.connect(self.init_parsing)
        self.main_window_ui.actionStopParsing.triggered.connect(self.stop_parsing)
        self.main_window_ui.actionShowTasks.triggered.connect(self.parsing_wizard.show_tasks)
        self.main_window_ui.actionStartParsing.hovered.connect(
            lambda text='Start parsing process': self.send_to_statusbar(text)
        )
        self.main_window_ui.actionStopParsing.hovered.connect(
            lambda text='Stop parsing process': self.send_to_statusbar(text)
        )
        self.main_window_ui.actionOpenSettings.hovered.connect(
            lambda text='Configure parser': self.send_to_statusbar(text)
        )
        self.signals.parsing_started.connect(self.show_loading_logo)
        self.signals.parsing_started.connect(self.disable_start_button)
        self.signals.parsing_started.connect(self.enable_stop_button)
        self.signals.parsing_finished.connect(self.hide_loading_logo)
        self.signals.parsing_finished.connect(self.disable_stop_button)
        self.signals.parsing_finished.connect(self.enable_start_button)
        self.signals.parsing_finished.connect(self.show_parsed_data)

    def run(self):
        """Метод, запускающий приложение."""
        self.main_window.show()
        sys.exit(self.app.exec())
