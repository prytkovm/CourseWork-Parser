from PyQt6 import QtCore, QtGui, QtWidgets


class SettingsWindowUi:

    """Класс, описывающий UI мастера настроек."""

    def setupUi(self, SettingsWindow):
        """Метод, создающий объекты виджета в соответствующих контейнерах окна SettingsWindow.

        Args:
            SettingsWindow:
                окно, тип QWidget.
        """
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(294, 112)
        self.gridLayout = QtWidgets.QGridLayout(SettingsWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.AutoParse = QtWidgets.QCheckBox(SettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.AutoParse.setFont(font)
        self.AutoParse.setObjectName("AutoParse")
        self.verticalLayout.addWidget(self.AutoParse)
        self.UseProxies = QtWidgets.QCheckBox(SettingsWindow)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.UseProxies.setFont(font)
        self.UseProxies.setObjectName("UseProxies")
        self.verticalLayout.addWidget(self.UseProxies)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(67, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OkButton = QtWidgets.QPushButton(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OkButton.sizePolicy().hasHeightForWidth())
        self.OkButton.setSizePolicy(sizePolicy)
        self.OkButton.setObjectName("OkButton")
        self.horizontalLayout.addWidget(self.OkButton)
        self.CancelButton = QtWidgets.QPushButton(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CancelButton.sizePolicy().hasHeightForWidth())
        self.CancelButton.setSizePolicy(sizePolicy)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        """Метод, устанавливающий текст и заголовки виджетов."""
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Settings"))
        self.AutoParse.setText(_translate("SettingsWindow", "Automatically start parsing on startup"))
        self.UseProxies.setText(_translate("SettingsWindow", "Use proxies"))
        self.OkButton.setText(_translate("SettingsWindow", "OK"))
        self.CancelButton.setText(_translate("SettingsWindow", "Cancel"))
