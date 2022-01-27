from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QSizePolicy, QFrame
from PyQt6.QtGui import QIcon, QPixmap
from application.tools.communication import Communicate


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
