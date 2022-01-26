class CsvWriter:

    @staticmethod
    def create_csv(path, header, data):
        try:
            with open(path, 'wb') as csv:
                csv.write(header)
                csv.writelines(data)
        except Exception as e:
            print(str(e))
            return

