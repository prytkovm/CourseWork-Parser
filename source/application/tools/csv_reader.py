from pandas import read_csv, concat


class CsvReader:

    @staticmethod
    def read_file(path):
        try:
            data = read_csv(path, sep=',')
        except FileNotFoundError:
            raise FileNotFoundError
        return data

    @staticmethod
    def merge_files(paths):
        data_to_merge = []
        for path in paths:
            try:
                data = read_csv(path, index_col=0, header=0)
                data_to_merge.append(data)
            except FileNotFoundError:
                raise FileNotFoundError
        merged_files = concat(data_to_merge, axis=0, ignore_index=True)
        return merged_files
