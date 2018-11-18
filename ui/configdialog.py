# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configdialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(752, 562)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(6, 6, 128, 470))
        self.listWidget.setMaximumSize(QtCore.QSize(128, 16777215))
        self.listWidget.setIconSize(QtCore.QSize(96, 84))
        self.listWidget.setMovement(QtWidgets.QListView.Static)
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget.setObjectName("listWidget")
        self.stackedWidget = QtWidgets.QStackedWidget(Dialog)
        self.stackedWidget.setGeometry(QtCore.QRect(140, 6, 421, 361))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Panel)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.pushButton = QtWidgets.QPushButton(self.page)
        self.pushButton.setGeometry(QtCore.QRect(140, 190, 99, 40))
        self.pushButton.setObjectName("pushButton")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.radioButton = QtWidgets.QRadioButton(self.page_2)
        self.radioButton.setGeometry(QtCore.QRect(160, 150, 117, 28))
        self.radioButton.setObjectName("radioButton")
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Config Dialog"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))
        self.radioButton.setText(_translate("Dialog", "RadioB&utton"))

