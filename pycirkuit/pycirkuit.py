#!/usr/bin/python3
# coding: utf-8
"""
This file is part of PyCirkuit.

PyCirkuit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyCirkuit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyCirkuit.  If not, see <https://www.gnu.org/licenses/>.
"""

# Third-party imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication

# Local application imports
from ui.mainwindow import MainWindow


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # These two next values are passed to every instance of QSettings everywhere in the app
    QCoreApplication.setOrganizationName("UPC")
    QCoreApplication.setApplicationName("pycirkuit")
    my_mainWindow = MainWindow()
    my_mainWindow.show()
    sys.exit(app.exec_())
