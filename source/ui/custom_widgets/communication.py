from PyQt6.QtCore import pyqtSignal, QObject, QSettings


class Communicate(QObject):

    """Класс содержит описание кастомных сигналов, используемых для общения между различными модулями"""

    # Сигнал, сообщающий классу TasksList об удалении элемента из списка, посылает индекс удаляемого объекта
    delete_item = pyqtSignal(int)
    # Сигнал, сообщающий классу TasksList о добавлении нового элемента в список
    add_item = pyqtSignal()
    write_task = pyqtSignal(str)
    links_got = pyqtSignal(str, QSettings, list)
