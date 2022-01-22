from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QSizePolicy, QAbstractItemView
from ui.custom_widgets.tasks_manager_item import TasksManagerItemWidget
from ui.custom_widgets.tasks_manager_add_item import TasksManagerAddItemWidget
from ui.custom_widgets.communication import Communicate


class TasksList(QListWidget):

    def __init__(self, parent=None, communicate=Communicate()):
        super(TasksList, self).__init__(parent)
        self.signals = communicate
        self.add_button = TasksManagerAddItemWidget(parent=self, communicate=self.signals)
        widget_item = QListWidgetItem(self)
        widget_item.setSizeHint(self.add_button.sizeHint())
        self.addItem(widget_item)
        self.signals.add_item.connect(self.add_item)
        self.signals.delete_item.connect(self.delete_item)
        self.setItemWidget(widget_item, self.add_button)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def delete_item(self, item_id):
        """Call methods from ParseWizard"""
        self.takeItem(item_id)

    def add_item(self, name, data):
        """Here must be called methods from ParseWizard UI"""
        new_item = TasksManagerItemWidget(parent=self, communicate=self.signals)
        # new_item.set_text('raz raz raz')
        new_item.set_data(name, data)
        widget_item = QListWidgetItem(self)
        widget_item.setSizeHint(new_item.sizeHint())
        self.addItem(widget_item)
        self.setItemWidget(widget_item, new_item)


# if __name__ == '__main__':
#     import sys
#     from PyQt6.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     w = TasksList()
#     new = TasksManagerItemWidget(parent=w, communicate=w.signals)
#     new.set_text('Big ass')
#     w_item = QListWidgetItem(w)
#     w_item.setSizeHint(new.sizeHint())
#     w.addItem(w_item)
#     w.setItemWidget(w_item, new)
#     w.show()
#     sys.exit(app.exec())
