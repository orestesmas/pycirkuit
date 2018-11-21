#!/usr/bin/python3
# coding: utf-8

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, \
                         QStandardPaths
from ui.mainwindow import MainWindow


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # These two next values are passed to every instance of QSettings everywhere in the app
    QCoreApplication.setOrganizationName("UPC")
    QCoreApplication.setApplicationName("pycirkuit")
    print(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation))
    print(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
    print(QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation))
    my_mainWindow = MainWindow()
    my_mainWindow.show()
    sys.exit(app.exec_())
