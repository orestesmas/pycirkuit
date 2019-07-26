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
import sys, os, inspect, platform
from os.path import isfile

# Third-party imports
from PyQt5.QtCore import QCoreApplication, \
                         QTranslator, \
                         QLocale, \
                         QLibraryInfo, \
                         QSettings
from PyQt5.QtWidgets import QApplication

# Local application imports
from pycirkuit.tools.cliparser import PyCirkuitParser
from pycirkuit.ui.mainwindow import MainWindow
from pycirkuit import __version__

# Resources for translation
from pycirkuit.resources import resources_rc
# Translation function
_translate = QCoreApplication.translate

# Function to ensure meaningful settings
def _check_settings():
    """
    Check if config file is empty (deleted, first run, etc.) and if so, set reasonable default values
    """
    settings = QSettings()
    # Start updating the "General" section
    settings.beginGroup("General")
    # Import ourselves
    import pycirkuit
    # Find absolute application's path
    applicationPath = os.path.dirname(inspect.getfile(pycirkuit))
    # Check app version
    storedVersion = settings.value("Version", "")
    if (storedVersion == ""):
        settings.setValue("Version", pycirkuit.__version__)
    elif (storedVersion < pycirkuit.__version__):
        #TODO: If upgrading we can remove the unnecessary entries, rename others, etc.
        pass
    elif (storedVersion > pycirkuit.__version__):
        #TODO: Handle downgrading, perhaps raising an exception, showing warning, etc.
        pass
    # Check the stored path to LaTeX templates
    if (settings.value("templatePath",  "") == ""):
        # Add the relative path where the default template is located
        templatePath = os.path.normpath(os.path.join(applicationPath, 'templates/cm_tikz.tpl'))
        settings.setValue("templatePath", templatePath)
    # Check Circuit Macros path
    from pycirkuit.tools.circuitmacrosmanager import CircuitMacrosManager
    if (settings.value("cmPath",  "") == ""):
        CM = CircuitMacrosManager()
        settings.setValue("cmPath", CM.default_CMPath())
    # Check the stored path to the built-in examples
    if (settings.value("examplesPath",  "") == ""):
        # Add the relative path where the examples are located
        examplesPath = os.path.normpath(os.path.join(applicationPath, 'examples'))
        settings.setValue("examplesPath", examplesPath)
    # Check last working dir (from where the files to be opened are taken)
    # This one will be initially the same as the examples path. Later on, the user actions will change it.
    if (settings.value("lastWD",  "") == ""):
        # Add the relative path where the examples are located
        examplesPath = os.path.normpath(os.path.join(applicationPath, 'examples'))
        settings.setValue("lastWD", examplesPath)
    # Check the stored path to built-in documentation
    if (settings.value("docPath",  "") == ""):
        # Add the relative path where the examples are located
        docPath = os.path.normpath(os.path.join(applicationPath, 'doc'))
        settings.setValue("docPath", docPath)
    settings.endGroup()   # Finished updating the "General" section
    # Begin updating the "Export" section
    settings.beginGroup("Export")
    settings.setValue("exportTIKZ", settings.value("exportTIKZ", True, type=bool))
    settings.setValue("exportPDF", settings.value("exportPDF", False, type=bool))
    settings.setValue("exportPNG", settings.value("exportPNG", False, type=bool))
    settings.setValue("exportJPEG", settings.value("exportJPEG", False, type=bool))
    settings.setValue("exportDPI", settings.value("exportDPI", 150, type=int))
    settings.setValue("exportQuality", settings.value("exportQuality", 80, type=int))
    settings.endGroup()  # Finished updating the "Export" section
    
    # Save settings for other object's use
    settings.sync()

# Main entry point
def main():
    if ("DESKTOP_SESSION" in os.environ) or (platform.system() == 'Windows'):
        app = QApplication(sys.argv)
    else:
        app = QCoreApplication(sys.argv)
  
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

    # Ensure meaningful settings
    _check_settings()
    
    # Parse command line options, deciding if user requested to work interactively (GUI)
    # or to process a list of files in batch mode (CLI)
    # If the former is chosen, this call returns with an eventual file to open in to the GUI
    # Otherwise the call don't return and does the process itself.
    cmdLineParser = PyCirkuitParser(sys.argv)
    fileToOpen = cmdLineParser.parseCmdLine()

    # Start GUI
    if not isinstance(app, QApplication):
        sys.exit(_translate("CommandLine", "No desktop environment available.", ""))
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
