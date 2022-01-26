from PyQt6.QtWidgets import QWidget, QInputDialog, QMessageBox, QVBoxLayout
from PyQt6.QtCore import QSettings, Qt
from application.tools.links_extractor import LinksExtractor
from application.tools import Communicate
from ui import ParsingWizardUi
from ui import TasksList
from glob import glob
import os


class ParsingWizard:

    """Класс, описывающий мастер парсинга."""

    def __init__(self, communicate=Communicate()):
        """Конструктор класса ParsingWizard.

        Args:
             communicate: объект класса Communicate с описанием сигналов.
        """
        self.urls_get_window = QWidget()
        self.urls_get_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.existing_tasks_window = QWidget()
        self.existing_tasks_window.setLayout(QVBoxLayout())
        self.existing_tasks_window.setAutoFillBackground(True)
        self.existing_tasks_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.signals = communicate
        self.msg_window = QMessageBox()
        # Виджет списка задач
        self.tasks_list = TasksList(parent=self.existing_tasks_window, communicate=self.signals)
        self.existing_tasks_window.layout().addWidget(self.tasks_list)
        self.existing_tasks_window.setWindowTitle('Parsing tasks')
        self.msg_window.setIcon(QMessageBox.Icon.Warning)
        self.get_links_window = ParsingWizardUi()
        self.get_links_window.setupUi(self.urls_get_window)
        self.connect_slots()

    def write_task(self, links):
        """Метод для записи задачи парсинга в файл, вызывается, когда получен сигнал links_got.

        Args:
            links: ссылки для парсинга для записи в файл.
        """
        task_name = self.get_task_name()
        if task_name is not None:
            settings = QSettings(f'parsing_tasks/{task_name}.ini', QSettings.Format.IniFormat)
            settings.setValue('task_name', task_name)
            settings.beginWriteArray('links')
            for i in range(len(links)):
                settings.setArrayIndex(i)
                settings.setValue("links", links[i])
            settings.endArray()
            settings.sync()
            self.add_task(
                dict(
                    name=task_name,
                    links=links
                )
            )
        else:
            return

    def get_task_name(self):
        """Получение от пользователя имени сохраняемой задачи."""
        dialog = QInputDialog()
        dialog_window = QWidget()
        dialog.setWindowTitle('New parsing task')
        name, ok = dialog.getText(dialog_window, 'Parsing wizard', 'Enter name of task')
        if ok:
            invalid_names = glob('parsing_tasks/*.ini')
            invalid_names = [os.path.basename(name).strip('.ini') for name in invalid_names]
            if len(name) == 0 or name in invalid_names:
                self.msg_window.setText('Invalid name')
                self.msg_window.setWindowTitle('Name error')
                self.msg_window.show()
                return
            return name
        return

    def get_links(self):
        """Получение от пользователя ссылок для парсинга,
        вызывается при получении сигнала нажатия на кнопку Ok в окне получения ссылок.
        Посылает сигнал links_got по окончании выполнения.
        """
        urls = self.get_links_window.UserUrls.toPlainText().split()
        urls = LinksExtractor.get_links(urls)
        self.signals.links_got.emit(urls)
        self.get_links_window.UserUrls.clear()

    def read_tasks(self):
        """Метод, осуществляющий чтение ранее сохраненных задач из файлов.

        Returns:
            tasks: список словарей в формате {Имя задачи, ссылки}.
        """
        files = glob('parsing_tasks/*.ini')
        tasks = []
        for file in files:
            settings = QSettings(file, QSettings.Format.IniFormat)
            task_name = os.path.basename(file).strip('.ini')
            size = settings.beginReadArray('links')
            links = [None for _ in range(size)]
            for i in range(size):
                settings.setArrayIndex(i)
                links[i] = settings.value('links')
            settings.endArray()
            tasks.append(dict(name=task_name, links=links))
        return tasks

    def show_tasks(self):
        """Метод, отображающий окно, визуализирующее задачи для парсинга."""
        tasks = self.read_tasks()
        for task in tasks:
            self.add_task(task)
        self.existing_tasks_window.show()

    def add_task(self, task):
        """Метод, добавляющий задачу в виджет списка задач.

        Args:
            task: словарь с ключами name - имя задачи,
            links: список ссылок для парсинга(строки).
        """
        self.tasks_list.add_item(task['name'], task['links'])

    def delete_task(self, task):
        """Метод, удаляющий файл с задачей.

        Args:
            task: имя задачи, строка.

        Raises:
            Exception: возникла непредвиденная ошибка.
        """
        try:
            os.remove(f'parsing_tasks/{task}.ini')
        except Exception as error:
            raise Exception(error)

    def enable_files_operations(self):
        """Метод, используемый для переподключения слотов, отключаемых методом disable_files_operations."""
        try:
            self.signals.create_file.connect(self.urls_get_window.show)
            self.signals.links_got.connect(self.write_task)
            self.signals.delete_file.connect(self.delete_task)
        except Exception:
            pass

    def disable_files_operations(self):
        """Метод, используемый для отключения слотов во избежание коллизий при ручной конфигурации парсинга."""
        try:
            self.signals.links_got.disconnect()
            self.signals.create_file.disconnect()
            self.signals.delete_file.disconnect()
        except Exception:
            pass

    def connect_slots(self):
        """Метод, подключающий слоты ParsingWizard."""
        self.get_links_window.OkButton.clicked.connect(self.get_links)
        self.signals.create_file.connect(self.urls_get_window.show)
        self.signals.links_got.connect(self.write_task)
        self.signals.delete_file.connect(self.delete_task)
        self.get_links_window.OkButton.clicked.connect(self.urls_get_window.close)
        self.get_links_window.CancelButton.clicked.connect(self.urls_get_window.close)
