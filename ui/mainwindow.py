# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(716, 604)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/AppIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.imatge = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.imatge.sizePolicy().hasHeightForWidth())
        self.imatge.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.imatge.setFont(font)
        self.imatge.setAutoFillBackground(False)
        self.imatge.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 0, 0);")
        self.imatge.setText("")
        self.imatge.setAlignment(QtCore.Qt.AlignCenter)
        self.imatge.setObjectName("imatge")
        self.verticalLayout.addWidget(self.imatge)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 716, 36))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAbout_PyCirkuit = QtWidgets.QAction(MainWindow)
        self.actionAbout_PyCirkuit.setObjectName("actionAbout_PyCirkuit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_PyCirkuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyCirkuit - by Orestes Mas"))
        self.pushButton.setText(_translate("MainWindow", "Processa!"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionAbout_PyCirkuit.setText(_translate("MainWindow", "&About PyCirkuit"))

import resources
