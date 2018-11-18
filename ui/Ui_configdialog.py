# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/orestes/Devel/Software/pycirkuit/ui/configdialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_configDialog(object):
    def setupUi(self, configDialog):
        configDialog.setObjectName("configDialog")
        configDialog.resize(697, 490)
        self.verticalLayout = QtWidgets.QVBoxLayout(configDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(configDialog)
        self.listWidget.setMaximumSize(QtCore.QSize(128, 16777215))
        self.listWidget.setIconSize(QtCore.QSize(96, 84))
        self.listWidget.setMovement(QtWidgets.QListView.Static)
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/config.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.horizontalLayout.addWidget(self.listWidget)
        self.stackedWidget = QtWidgets.QStackedWidget(configDialog)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Panel)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page1 = QtWidgets.QWidget()
        self.page1.setObjectName("page1")
        self.pushButton = QtWidgets.QPushButton(self.page1)
        self.pushButton.setGeometry(QtCore.QRect(140, 190, 99, 40))
        self.pushButton.setObjectName("pushButton")
        self.stackedWidget.addWidget(self.page1)
        self.page2 = QtWidgets.QWidget()
        self.page2.setObjectName("page2")
        self.radioButton = QtWidgets.QRadioButton(self.page2)
        self.radioButton.setGeometry(QtCore.QRect(160, 150, 117, 28))
        self.radioButton.setObjectName("radioButton")
        self.stackedWidget.addWidget(self.page2)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(configDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(configDialog)
        self.stackedWidget.setCurrentIndex(1)
        self.closeButton.clicked.connect(configDialog.accept)
        self.listWidget.currentRowChanged['int'].connect(self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(configDialog)
        configDialog.setTabOrder(self.listWidget, self.pushButton)
        configDialog.setTabOrder(self.pushButton, self.closeButton)
        configDialog.setTabOrder(self.closeButton, self.radioButton)

    def retranslateUi(self, configDialog):
        _translate = QtCore.QCoreApplication.translate
        configDialog.setWindowTitle(_translate("configDialog", "Config Dialog"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("configDialog", "General"))
        item = self.listWidget.item(1)
        item.setText(_translate("configDialog", "Un altre"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("configDialog", "PushButton"))
        self.radioButton.setText(_translate("configDialog", "RadioB&utton"))
        self.closeButton.setText(_translate("configDialog", "Close"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    configDialog = QtWidgets.QDialog()
    ui = Ui_configDialog()
    ui.setupUi(configDialog)
    configDialog.show()
    sys.exit(app.exec_())

