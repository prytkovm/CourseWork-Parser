from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtGui import QIcon, QPixmap
from ui.custom_widgets.communication import Communicate


class TasksManagerItemWidget(QWidget):

    objects = []

    def __init__(self, parent=None, communicate=Communicate()):
        super(TasksManagerItemWidget, self).__init__(parent)
        self.signals = communicate
        self.h_box_layout = QHBoxLayout(self)
        self.combobox = QComboBox(self)
        self.h_box_layout.addWidget(self.combobox)
        self.delete_button = QPushButton(self)
        delete_img = QIcon()
        delete_img.addPixmap(QPixmap(r'ui/custom_widgets/widget_icons/delete-icon.png'))
        self.delete_button.setIcon(delete_img)
        self.h_box_layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.send_delete_signal)
        self.add_item()

    def set_data(self, name, data):
        self.combobox.addItem(name, *data)

    def send_delete_signal(self):
        row = TasksManagerItemWidget.delete_item(self)
        self.signals.delete_item.emit(row + 1)

    def delete_item(self):
        index = TasksManagerItemWidget.objects.index(self)
        TasksManagerItemWidget.objects.pop(index)
        return index

    def add_item(self):
        TasksManagerItemWidget.objects.append(self)

#
# if __name__ == '__main__':
#     import sys
#     from PyQt6.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     w = TasksManagerItemWidget()
#     w.show()
#     print(type(w.get_id()))
#     # print(type(id(w)))
#     # print(id(w))
#     sys.exit(app.exec())
