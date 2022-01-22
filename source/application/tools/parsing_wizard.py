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
        self.tasks_list = TasksList(parent=self.existing_tasks_window, communicate=self.signals)
        self.ui = WizardSecondPageUi()
        self.ui.setupUi(self)
        self.connect_slots()

    def get_parsing_targets(self):
        urls = self.ui.UserUrls.toPlainText().split()
        urls = Extractor.get_links(urls)
        return urls

    def create_task(self):
        dialog = QInputDialog()
        dialog_window = QWidget()
        dialog.setWindowTitle('New parsing task')
        invalid_names = glob('parsing_tasks/*.ini')
        invalid_names = [os.path.basename(name) for name in invalid_names]
        name, ok = dialog.getText(dialog_window, 'Parsing wizard', 'Enter name of task')
        if len(name) == 0 or f'{name}.ini' in invalid_names:
            self.msg_window.setText('Invalid name')
            self.msg_window.setWindowTitle('Name error')
            self.msg_window.exec()
            return
        if ok:
            self.show()
            self.signals.write_task.emit(name)

    def write_task(self, task_name):
        """TODO"""
        settings = QSettings(f'parsing_tasks/{task_name}.ini', QSettings.Format.IniFormat)
        settings.setValue('task_name', task_name)
        data = self.get_parsing_targets()
        settings.beginWriteArray('links')
        if self.signals.links_got:
            for i in range(len(data)):
                settings.setArrayIndex(i)
                settings.setValue("links", data[i])
            settings.endArray()
            settings.sync()

    def write_links(self):
        """TODO"""

    def delete_task(self):
        """"TODO"""

    def show_tasks(self):
        """TODO"""
        tasks = self.read_tasks()
        for task in tasks:
            self.tasks_list.add_item(task['name'], task['links'])
        self.tasks_list.show()

    def read_tasks(self):
        """TODO"""
        files = glob('parsing_tasks/*.ini')
        tasks = []
        for file in files:
            settings = QSettings(file, QSettings.Format.IniFormat)
            task_name = file
            links = settings.value('links', [], str)
            print(links)
            tasks.append(dict(name=task_name, links=links))
        return tasks

    def connect_slots(self):
        self.signals.write_task.connect(self.write_task)
        self.ui.OkButton.clicked.connect(self.signals.links_got.emit)
        self.ui.OkButton.clicked.connect(self.close)
        self.ui.CancelButton.clicked.connect(self.close)
