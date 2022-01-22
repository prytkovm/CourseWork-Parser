from PyQt6.QtWidgets import QFileDialog


class FileDialog(QFileDialog):

    def __init__(self):
        super().__init__()

    def show_file_open_dialog(self):
        try:
            filename = self.getOpenFileName(self, 'Open file', '', 'Csv files(*.csv)')[0]
        except Exception as error:
            raise Exception(str(error))
        return filename

    def show_file_save_dialog(self):
        try:
            filename = self.getSaveFileName(self, 'Save file', '', 'Csv files(*.csv)')[0]
        except Exception as error:
            raise Exception(str(error))
        return filename
