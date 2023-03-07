from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTreeWidgetItem,
    QSizePolicy,
    QAbstractItemView,
    QAbstractScrollArea,
    QFrame,
    QTreeWidget
)
from PyQt6.QtGui import QIcon, QPixmap
from ..tools.communication import Communicate


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


class TasksManagerAddItemWidget(QWidget):

    """Класс, описывающий виджет кнопки добавления нового элемента в список.
    Наследует QWidget.
    """

    def __init__(self, parent=None, communicate=Communicate()):
        """Конструктор класса TasksManagerAddItemWidget.

        Args:
            parent:
                виджет-родитель, по умолчанию None.
            communicate:
                объект класса Communicate с описанием сигналов.
        """
        super(TasksManagerAddItemWidget, self).__init__(parent)
        self.signals = communicate
        self.h_box_layout = QHBoxLayout(self)
        self.add_button = QPushButton(self)
        add_icon = QIcon()
        add_icon.addPixmap(QPixmap('icons/widget_icons/add_icon.png'))
        self.add_button.setIcon(add_icon)
        self.h_box_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.signals.create_file.emit)


class TasksManagerItemWidget(QFrame):

    """Класс, описывающий кастомный виджет для отображения задачи парсинга.
    Наследует QFrame.
    """

    # список существующих объектов TaskManagerItemWidget
    objects = []

    def __init__(self, parent=None, communicate=Communicate()):
        """Конструктор класса TasksManagerItemWidget.

        Args:
            parent:
                виджет-родитель, по умолчанию None
            communicate:
                объект класса Communicate с описанием сигналов
        """
        super(TasksManagerItemWidget, self).__init__(parent)
        self.signals = communicate
        self.setLayout(QHBoxLayout())
        self.task_data = QTreeWidget(self)
        self.task_data.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.delete_button = QPushButton(self)
        delete_img = QIcon()
        delete_img.addPixmap(QPixmap(r'icons/widget_icons/delete-icon.png'))
        self.delete_button.setIcon(delete_img)
        self.delete_button.clicked.connect(self.send_delete_signal)
        self.add_item()
        self.task_name = ''
        self.task_data.setStyleSheet("border: none")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setLineWidth(15)
        self.layout().addWidget(self.task_data)
        self.layout().addWidget(self.delete_button)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_data(self, name, links):
        """Метод, создающий в виджете древовидную структуру QTreeWidgetItem с информацией о задаче.

        Args:
            name:
                имя задачи
            links:
                ссылки для парсинга
        """
        self.task_name = name
        header = QTreeWidgetItem(self.task_data)
        header.setText(0, 'Parsing links')
        self.task_data.setHeaderLabel(name)
        self.task_data.setColumnCount(1)
        for link in links:
            self.task_data.insertTopLevelItem(0, QTreeWidgetItem(header, [link]))

    def send_delete_signal(self):
        """Метод, посылающий сигнал удаления элемента из списка с его индексом и именем задачи."""
        row = TasksManagerItemWidget.delete_item(self)
        self.signals.delete_item.emit(row + 1, self.task_name)

    def delete_item(self):
        """Метод, удаляющий экземпляр из списка objects.

        Returns:
            index:
                индекс удаленного экземпляра.
        """
        index = TasksManagerItemWidget.objects.index(self)
        TasksManagerItemWidget.objects.pop(index)
        return index

    def add_item(self):
        """Метод, добавляющий созданный экземпляр в список объектов objects."""
        TasksManagerItemWidget.objects.append(self)
