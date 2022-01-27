from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QSizePolicy, QAbstractItemView, QAbstractScrollArea
from ui.custom_widgets.tasks_manager_item import TasksManagerItemWidget
from ui.custom_widgets.tasks_manager_add_item import TasksManagerAddItemWidget
from application.tools.communication import Communicate


class TasksList(QListWidget):

    """Класс, описывающий кастомный виджет для отображения задач парсинга в виде списка.
    Наследует QListWidget.
    """

    def __init__(self, parent=None, communicate=Communicate()):
        """Конструктор класса TasksList.

        Args:
            parent:
                виджет-родитель, по умолчанию None.
            communicate:
                объект класса Communicate с описанием сигналов.
        """
        super(TasksList, self).__init__(parent)
        self.signals = communicate
        # виджет-кнопка для добавления новой задачи
        self.add_button = TasksManagerAddItemWidget(parent=self, communicate=self.signals)
        widget_item = QListWidgetItem(self)
        widget_item.setSizeHint(self.add_button.sizeHint())
        self.addItem(widget_item)
        self.signals.delete_item.connect(self.delete_item)
        self.setItemWidget(widget_item, self.add_button)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tasks_names = []
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        if parent is not None:
            if parent.layout() is not None:
                parent.layout().addWidget(self)

    def add_item(self, name, data):
        """Метод, используемый для добавления новой задачи в список.

        Args:
            name:
                имя задачи.
            data:
                информация о задаче, в данном случае список ссылок.
        """
        if name not in self.tasks_names:
            new_item = TasksManagerItemWidget(parent=self, communicate=self.signals)
            new_item.set_data(name, data)
            self.tasks_names.append(name)
            widget_item = QListWidgetItem(self)
            widget_item.setSizeHint(new_item.sizeHint())
            self.addItem(widget_item)
            self.setItemWidget(widget_item, new_item)

    def delete_item(self, item_id, item_name):
        """Метод, вызываемый при получении сигнала delete_item. Посылает сигнал delete_file с именем задачи.

        Args:
            item_id:
                индекс удаляемого объекта.
            item_name:
                имя удаляемой задачи.
        """
        self.takeItem(item_id)
        self.tasks_names.remove(item_name)
        self.signals.delete_file.emit(item_name)
