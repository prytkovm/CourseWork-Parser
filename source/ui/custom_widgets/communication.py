from PyQt6.QtCore import pyqtSignal, QObject


class Communicate(QObject):

    """Класс содержит описание кастомных сигналов, используемых для общения между различными модулями"""

    # Сигнал, сообщающий классу TasksList об удалении элемента из списка, посылает индекс удаляемого объекта
    delete_item = pyqtSignal(int, str)
    delete_file = pyqtSignal(str)
    # Сигнал, сообщающий классу TasksList о добавлении нового элемента в список
    add_item = pyqtSignal()
    links_got = pyqtSignal(list)
