from PyQt6.QtCore import pyqtSignal, QObject


class Communicate(QObject):

    """Класс содержит описание кастомных сигналов, используемых для общения между различными модулями приложения."""

    # Сигнал, сообщающий экземпляру класса TasksList об удалении элемента из списка, посылает индекс удаляемого объекта и имя задачи
    delete_item = pyqtSignal(int, str)
    # Сигнал, сообщающий экземпляру класса ParsingWizard о необходимости удалить файл с задачей, посылает имя задачи
    delete_file = pyqtSignal(str)
    # Сигнал, сообщающий экземпляру класса TasksList о добавлении нового элемента в список
    create_file = pyqtSignal()
    # Сигнал, сообщающий экземплярам классов ParsingWizard и App(сигнал переподключается в зависимости от настроек)
    # о получении ссылок для парсинга от пользователя
    links_got = pyqtSignal(list)
    # Сигнал, сообщающий экземпляру класса ParsingWorker о необходимости прекратить выполнение
    stop_parsing = pyqtSignal()
    # Сигнал, посылаемый экземпляром ParsingWorker и сообщающий экземпляру класса App о начале парсинга
    parsing_started = pyqtSignal()
    # Сигнал, посылаемый экземпляром ParsingWorker и сообщающий экземпляру класса App об окончании парсинга
    parsing_finished = pyqtSignal(bool)
