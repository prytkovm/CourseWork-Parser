import os
from ui.parsing_wizard_ui.pages.second_page import WizardSecondPageUi
from ui.custom_widgets.tasks_list import TasksList
from ui.custom_widgets.communication import Communicate
from application.tools.links_extractor import Extractor
from PyQt6.QtWidgets import QWidget, QInputDialog, QMessageBox
from PyQt6.QtCore import QSettings
from glob import glob


class ParsingWizard(QWidget):

    def __init__(self):
        super(ParsingWizard, self).__init__()
        self.existing_tasks_window = QWidget()
        self.signals = Communicate()
        self.msg_window = QMessageBox()
        self.msg_window.setIcon(QMessageBox.Icon.Warning)
        self.tasks_list = TasksList(communicate=self.signals)
        self.ui = WizardSecondPageUi()
        self.ui.setupUi(self)
        self.connect_slots()

    def write_task(self, links):
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
        else:
            return

    def get_task_name(self):
        dialog = QInputDialog()
        dialog_window = QWidget()
        dialog.setWindowTitle('New parsing task')
        name, ok = dialog.getText(dialog_window, 'Parsing wizard', 'Enter name of task')
        if ok:
            invalid_names = glob('parsing_tasks/*.ini')
            invalid_names = [os.path.basename(name) for name in invalid_names]
            if len(name) == 0 or f'{name}.ini' in invalid_names:
                self.msg_window.setText('Invalid name')
                self.msg_window.setWindowTitle('Name error')
                self.msg_window.exec()
                return
            return name
        return None

    def get_links(self):
        urls = self.ui.UserUrls.toPlainText().split()
        urls = Extractor.get_links(urls)
        self.signals.links_got.emit(urls)

    def read_tasks(self):
        files = glob('parsing_tasks/*.ini')
        tasks = []
        for file in files:
            settings = QSettings(file, QSettings.Format.IniFormat)
            task_name = os.path.basename(file)
            size = settings.beginReadArray('links')
            links = [None for _ in range(size)]
            for i in range(size):
                settings.setArrayIndex(i)
                links[i] = settings.value('links')
            settings.endArray()
            tasks.append(dict(name=task_name, links=links))
        return tasks

    def show_tasks(self):
        """TODO"""
        tasks = self.read_tasks()
        for task in tasks:
            self.tasks_list.add_item(task['name'], task['links'])
        self.tasks_list.show()

    def add_task(self, create_file):
        """TODO"""


    def delete_task(self, delete_file):
        """"TODO"""
        try:
            os.remove(f'parsing_tasks/{delete_file}')
        except Exception as e:
            print(str(e))
            return

    def connect_slots(self):
        self.ui.OkButton.clicked.connect(self.get_links)
        self.signals.create_file.connect(self.add_task)
        self.signals.links_got.connect(self.write_task)
        self.signals.delete_file.connect(self.delete_task)
        self.ui.OkButton.clicked.connect(self.close)
        self.ui.CancelButton.clicked.connect(self.close)
