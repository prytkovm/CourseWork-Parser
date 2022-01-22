from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from application.tools.settings_wizard import SettingsWizard
from application.tools.parsing_wizard import ParsingWizard
from application.tools.file_browser import FileDialog
from application.tools.csv_reader import CsvReader
from ui.mainwindow import MainWindowUI
import sys


class App:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.main_window_ui = MainWindowUI()
        self.main_window_ui.setupUi(self.main_window)
        self.settings_wizard = SettingsWizard()
        self.parsing_wizard = ParsingWizard()
        self.file_browser = FileDialog()
        self.connect_slots()

    def start_parsing(self):
        self.show_loading_logo()
        self.disable_start_button()
        self.enable_stop_button()

    def stop_parsing(self):
        self.hide_loading_logo()
        self.disable_stop_button()
        self.enable_start_button()

    def read_csv(self):
        try:
            path_to_file = self.file_browser.show_file_open_dialog()
        except Exception:
            return
        try:
            data = CsvReader.read_file(path_to_file)
        except FileNotFoundError:
            return
        self.set_table_data(data)

    def write_csv(self):
        try:
            path_to_file = self.file_browser.show_file_save_dialog()
        except Exception:
            return
        try:
            pass
        except Exception:
            pass

    def set_table_data(self, data):
        rows_count = len(data.index)
        columns_count = len(data.columns)
        self.main_window_ui.tableWidget.setColumnCount(columns_count)
        self.main_window_ui.tableWidget.setRowCount(rows_count)
        self.main_window_ui.tableWidget.setHorizontalHeaderLabels(data.columns)
        for i in range(rows_count):
            for j in range(columns_count):
                self.main_window_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))
        self.main_window_ui.tableWidget.resizeColumnsToContents()
        self.main_window_ui.tableWidget.setEnabled(True)
        self.main_window_ui.tableWidget.setVisible(True)

    def enable_stop_button(self):
        self.main_window_ui.actionStopParsing.setEnabled(True)

    def disable_stop_button(self):
        self.main_window_ui.actionStopParsing.setEnabled(False)

    def enable_start_button(self):
        self.main_window_ui.actionStartParsing.setEnabled(True)

    def disable_start_button(self):
        self.main_window_ui.actionStartParsing.setEnabled(False)

    def show_loading_logo(self):
        self.main_window_ui.label.setEnabled(True)
        self.main_window_ui.label.setVisible(True)
        self.main_window_ui.tableWidget.setVisible(False)
        self.main_window_ui.tableWidget.setEnabled(False)
        self.main_window_ui.movie.start()

    def hide_loading_logo(self):
        self.main_window_ui.movie.stop()
        self.main_window_ui.label.setEnabled(False)
        self.main_window_ui.label.setVisible(False)
        self.main_window_ui.tableWidget.setEnabled(True)
        self.main_window_ui.tableWidget.setVisible(True)

    def show_settings_window(self):
        self.settings_wizard.show()

    def send_to_statusbar(self, text):
        self.main_window_ui.statusbar.showMessage(text, 1500)

    def connect_slots(self):
        self.main_window_ui.actionOpenSettings.triggered.connect(self.show_settings_window)
        self.main_window_ui.actionOpenFile.triggered.connect(self.read_csv)
        self.main_window_ui.actionExport.triggered.connect(self.write_csv)
        self.main_window_ui.actionStartParsing.triggered.connect(self.start_parsing)
        self.main_window_ui.actionStopParsing.triggered.connect(self.stop_parsing)
        # self.main_window_ui.actionCreateNewParsingTask.triggered.connect(
        #     self.parsing_wizard.show
        # )
        # self.main_window_ui.actionManageExistingTasks.triggered.connect(
        #     self.parsing_wizard.show_tasks
        # )

        self.main_window_ui.actionStartParsing.hovered.connect(
            lambda text='Start parsing process': self.send_to_statusbar(text)
        )
        self.main_window_ui.actionStopParsing.hovered.connect(
            lambda text='Stop parsing process': self.send_to_statusbar(text)
        )
        self.main_window_ui.actionOpenSettings.hovered.connect(
            lambda text='Configure parser': self.send_to_statusbar(text)
        )

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec())
