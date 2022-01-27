from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from application.tools.communication import Communicate


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
