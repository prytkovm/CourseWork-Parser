from PyQt6 import QtCore, QtGui, QtWidgets


class ParsingWizardUi:

    """Класс, описывающий UI мастера парсинга."""

    def setupUi(self, Window):
        """Метод, создающий объекты виджета в соответствующих контейнерах окна Window.

        Args:
             Window:
                окно, тип QWidget.
        """
        Window.setObjectName("SecondPage")
        Window.resize(436, 411)
        self.gridLayout = QtWidgets.QGridLayout(Window)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Window)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.UserUrls = QtWidgets.QPlainTextEdit(Window)
        self.UserUrls.setObjectName("UserUrls")
        self.gridLayout.addWidget(self.UserUrls, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(209, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CancelButton = QtWidgets.QPushButton(Window)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.OkButton = QtWidgets.QPushButton(Window)
        self.OkButton.setObjectName("OkButton")
        self.horizontalLayout.addWidget(self.OkButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        """Метод, устанавливающий текст и заголовки виджетов."""
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("SecondPage", "Parsing wizard"))
        self.label.setText(_translate("SecondPage", "Insert your urls to pages:"))
        self.CancelButton.setText(_translate("SecondPage", "Cancel"))
        self.OkButton.setText(_translate("SecondPage", "OK"))
