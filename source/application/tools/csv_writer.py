class CsvWriter:

    """Статический класс с описанием методов для записи данных в csv файл."""

    @staticmethod
    def write(path, header, data):
        """Запись в csv файл.

        Args:
            path: путь к файлу для записи.
            header: заголовк csv файла.
            data: данные для записи.

        Raises:
            Exception: возникла непредвиденная ошибка.
        """
        try:
            with open(path, 'wb') as csv:
                csv.write(header)
                csv.writelines(data)
        except Exception as error:
            raise Exception(error)
