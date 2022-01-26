from pandas import read_csv, concat


class CsvReader:

    """Статический класс с описанием методов для чтения csv файлов."""

    @staticmethod
    def read_file(path):
        """Чтение csv файла.

        Args:
            path: путь к csv файлу.

        Returns:
            pandas DataFrame: прочитанные данные.

        Raises:
            Exception: возникла непредвиденная ошибка.
        """
        try:
            data = read_csv(path)
        except ValueError:
            pass
        except Exception as error:
            raise Exception(error)
        return data

    @staticmethod
    def merge_files(paths):
        """Чтение нескольких csv файлов и объединение данных.

        Args:
            paths: список путей к csv файлам.

        Returns:
            pandas DataFrame: прочитанные данные.
            None: pandas не удалось прочитать файл.

        Raises:
             Exception: возникла непредвиденная ошибка.
        """
        data_to_merge = []
        for path in paths:
            try:
                data = read_csv(path, index_col=None, header=0)
                if data is not None:
                    data_to_merge.append(data)
            except ValueError:
                return None
            except Exception as error:
                raise Exception(error)
        try:
            merged_files = concat(data_to_merge, axis=0, ignore_index=True)
        except ValueError:
            return None
        except Exception as error:
            raise Exception(error)
        return merged_files
