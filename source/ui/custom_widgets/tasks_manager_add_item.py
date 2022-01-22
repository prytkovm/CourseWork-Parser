from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from ui.custom_widgets.communication import Communicate


class TasksManagerAddItemWidget(QWidget):

    def __init__(self, parent=None, communicate=Communicate()):
        super(TasksManagerAddItemWidget, self).__init__(parent)
        self.signals = communicate
        self.h_box_layout = QHBoxLayout(self)
        self.add_button = QPushButton(self)
        add_icon = QIcon()
        add_icon.addPixmap(QPixmap(r'ui/custom_widgets/widget_icons/add_icon.png'))
        self.add_button.setIcon(add_icon)
        self.h_box_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.send_add_item_signal)

    def send_add_item_signal(self):
        self.signals.add_item.emit()


# if __name__ == '__main__':
#     import sys
#     from PyQt6.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     w = TasksManagerAddItemWidget()
#     w.show()
#     sys.exit(app.exec())
