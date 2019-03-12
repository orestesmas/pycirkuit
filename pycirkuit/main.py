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

# Third-party imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, QTranslator, QLocale,  QLibraryInfo,  QCommandLineParser

# Local application imports
from pycirkuit.ui.mainwindow import MainWindow
from pycirkuit import __version__, __productname__

# Resources for translation
from pycirkuit.resources import resources_rc

import sys

# The command line parser
def parseCmdLine(app):
    QCoreApplication.setApplicationName(__productname__)
    QCoreApplication.setApplicationVersion(__version__)
    parser = QCommandLineParser()
    parser.setApplicationDescription("""PyCirkuit is a GUI front-end for Circuit Macros by Dwight Aplevich,
which are a set of macros for drawing high-quality line diagrams
to include in TeX, LaTeX, web or similar documents.""")
    parser.addHelpOption()
    parser.addVersionOption()
    parser.process(app)
    
# Main entry point
def main():
    app = QApplication(sys.argv)
    parseCmdLine(app)
  
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
    my_mainWindow = MainWindow()
    my_mainWindow.show()
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
    main()
