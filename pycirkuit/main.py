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
from os.path import abspath, isfile
import glob

# Third-party imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, \
                                            QTranslator, \
                                            QLocale, \
                                            QLibraryInfo, \
                                            QCommandLineParser, \
                                            QCommandLineOption

# Local application imports
from pycirkuit.ui.mainwindow import MainWindow
from pycirkuit import __version__

# Resources for translation
from pycirkuit.resources import resources_rc
# Translation function
_translate = QCoreApplication.translate

import sys

# The command line parser
def parseCmdLine(app):
    parser = QCommandLineParser()
    parser.setApplicationDescription(_translate("main", """
PyCirkuit is a GUI front-end for Circuit Macros by Dwight Aplevich,
which are a set of macros for drawing high-quality line diagrams
to be included in TeX, LaTeX, web or similar documents.""", "Commandline help text"))

    # Adding command line options
    options = [
        QCommandLineOption(
            ["batch", "b"],
            "Group of files / directory to process in batch (unattended) mode.",
            "groupFiles"
        ),
        QCommandLineOption(
            ["tikz"],
            "Generates a TiKz from the input file.",
            "outputFile"
        ),
    ]
    # Adding the '-h, --help' option
    parser.addHelpOption()
    # Adding the '-v --version' option
    parser.addVersionOption()
    # Adding the options in the list
    for option in options:
        parser.addOption(option)
    # Allowing one positional argument -- the file to open
    parser.addPositionalArgument(
        _translate("main", "file", "Commandline help text"), 
        _translate("main", "Source drawing file to open")
    )
    # Process the command line options
    parser.process(app)
    print (parser.optionNames())
    # Act upon given arguments
    for option in options:
        if parser.isSet(option):
            optionName = option.names()[0]
            if optionName == "batch":
                print("Option '-b' not yet implemented. Exiting.")
                print("But the files to be processed are:")
                pathSpec =  parser.value(option)
                fileIterator = iter(glob.iglob(pathSpec))
                for file in fileIterator:
                    print(file)
                sys.exit(-1)
            elif optionName == "tikz":
                print ("tikz")
    # Finished test for options. Now test for a filename passed as parameter, or none
    args = parser.positionalArguments()
    N = len(args)
    if N == 0:
        return None
    if N == 1:
        return abspath(args[0])
    else:
        # More than one argument is an error. Display help and exit.
        parser.showHelp(exitCode=-1)
    
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

    # Parse command line options
    fileToOpen = parseCmdLine(app)

    # Start GUI
    my_mainWindow = MainWindow()
    my_mainWindow.show()
    if fileToOpen != None:
        if isfile(fileToOpen):
            my_mainWindow._load_file(fileToOpen)
        else:
            my_mainWindow.on_actionNew_triggered(fileToOpen)
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
    main()
