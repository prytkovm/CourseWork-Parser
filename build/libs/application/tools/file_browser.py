from PyQt6.QtWidgets import QFileDialog


class FileDialog(QFileDialog):

    """Класс описывающий диалог для получения от пользователя пути к файлам.
    Наследует QFileDialog.
    """

    def show_file_open_dialog(self):
        """Отображение окна для получения пути к открываемому файлу.

        Returns:
            filename - строка, путь к файлу,
            None - пользователь ничего не ввел и закрыл окно.

        Raises:
             Exception: возникла непредвиденная ошибка.
        """
        try:
            filename = self.getOpenFileName(self, 'Open file', '', 'Csv files(*.csv)')[0]
        except Exception as error:
            raise Exception(error)
        if len(filename) != 0:
            return filename
        else:
            return None

    def show_file_save_dialog(self):
        """Отображение окна для получения пути к сохраняемому файлу.

        Returns:
            filename - строка, путь к файлу,
            None - пользователь ничего не ввел и закрыл окно.

        Raises:
            Exception: возникла непредвиденная ошибка.
        """
        try:
            filename = self.getSaveFileName(self, 'Save file', '', 'Csv files(*.csv)')[0]
        except Exception as error:
            raise Exception(error)
        if len(filename) != 0:
            return filename
        else:
            return None
