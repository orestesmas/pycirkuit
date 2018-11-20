#!/usr/bin/python3
# coding: utf-8

from PyQt5.QtWidgets import QApplication
from ui.mainwindow import MainWindow


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    my_mainWindow = MainWindow()
    my_mainWindow.show()
    sys.exit(app.exec_())
