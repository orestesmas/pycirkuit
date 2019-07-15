#!/usr/bin/python3
# coding: utf-8
"""
Main program entry point/function
"""
# Copyright (C) 2018-2019 Orestes Mas
# This file is part of PyCirkuit.
#
# PyCirkuit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCirkuit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyCirkuit.  If not, see <https://www.gnu.org/licenses/>.
#

# Standard library imports
import sys
from os.path import isfile

# Third-party imports
from PyQt5.QtCore import QCoreApplication, \
                                            QTranslator, \
                                            QLocale, \
                                            QLibraryInfo
from PyQt5.QtWidgets import QApplication

# Local application imports
from pycirkuit.cliparser import PyCirkuitParser
from pycirkuit.ui.mainwindow import MainWindow
from pycirkuit import __version__

# Resources for translation
from pycirkuit.resources import resources_rc
# Translation function
_translate = QCoreApplication.translate


# Main entry point
def main():
    app = QApplication(sys.argv)
  
    # First try to load the Qt-provided translations (used in some standard dialog strings)
    qtTranslator = QTranslator()
    filename = "qtbase_" + QLocale.system().name().split("_")[0]
    if qtTranslator.load(filename, QLibraryInfo.location(QLibraryInfo.TranslationsPath), suffix=".qm"):
        app.installTranslator(qtTranslator)
    # Then load PyCirkuit translations
    pycirkuitTranslator = QTranslator()
    if pycirkuitTranslator.load(QLocale(), "pycirkuit", ".", ":/translations", ".qm"):
        app.installTranslator(pycirkuitTranslator)
        
    # These two next values are passed to every instance of QSettings everywhere in the app
    QCoreApplication.setOrganizationName("PyCirkuit")
    QCoreApplication.setApplicationName("pycirkuit")
    QCoreApplication.setApplicationVersion(__version__)

    # Parse command line options, deciding if user requested to work interactively (GUI)
    # or to process a list of files in batch mode (CLI)
    # If the former is chosen, this call returns with an eventual file to open in to the GUI
    # Otherwise the call don't return and does the process itself.
    cmdLineParser = PyCirkuitParser(sys.argv)
    fileToOpen = cmdLineParser.parseCmdLine()

    # Start GUI
    my_mainWindow = MainWindow()
    my_mainWindow.show()
    if fileToOpen != None:
        if isfile(fileToOpen):
            my_mainWindow._load_file(fileToOpen)
        else:
            my_mainWindow.on_actionNew_triggered(fileToOpen)
    app.exec()
    
    
if __name__ == "__main__":
    main()
