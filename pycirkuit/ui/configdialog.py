# -*- coding: utf-8 -*-
"""
Module implementing configDialog.
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
import os

# Third-party imports
from PyQt5.QtCore import pyqtSlot, Qt, QSize, QDir, QSettings, QCoreApplication
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

# Local application imports
from pycirkuit.ui.Ui_configdialog import Ui_ConfigDialog
from pycirkuit.exceptions import PyCirkuitError
# Translation function
_translate = QCoreApplication.translate

class ConfigDialog(QDialog, Ui_ConfigDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        # Hack to center items in QListView
        for i in range(0, self.listWidget.count()):
            self.listWidget.item(i).setSizeHint(QSize(132, 80))
            self.listWidget.item(i).setTextAlignment(Qt.AlignCenter)
        
        # Persistent settings
        settings = QSettings() 
        # Extract stored path to Circuit Macros
        cmStoredPath = settings.value("General/cmPath", "")
        if cmStoredPath == "":
            # emit signal manually as setting an empty text doesn't really changes the text (it is already empty)
            self.cmPath.textChanged.emit("")
        else:
            self.cmPath.setText(cmStoredPath)

        # Extract stored path to LaTeX template file
        # defaultPath = QDir.homePath() + "/Plantilles/cm_tikz.ckt"
        storedLatexTemplateFile = settings.value("General/templatePath", "")
        if storedLatexTemplateFile == "":
            # emit signal manually as setting an empty text doesn't really changes the text (it is already empty)
            self.templateFile.textChanged.emit("")
        else:
            self.templateFile.setText(storedLatexTemplateFile)
    
    
    @pyqtSlot()
    def accept(self):
        settings = QSettings()
        try:
            if not os.path.isdir(self.cmPath.text()):
                message =_translate("MessageBox", "The path to the Circuit Macros location is not valid. Please enter a valid one.", "")
                extraInfo = _translate("MessageBox", "Or, cancel the settings dialog and PyCirkuit will download and install the Circuit Macros when needed.", "")
                raise PyCirkuitError(message, moreInfo=extraInfo)
            if not os.path.isfile(self.templateFile.text()):
                raise PyCirkuitError(_translate("MessageBox", "The path to the LaTeX template does not point to a valid file. Please enter a correct one.", ""))
        except PyCirkuitError as err:
            # Open MessageBox and inform user
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle(err.title)
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(str(err))
            msgBox.setInformativeText(err.moreInfo)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.exec()
            return
        settings.setValue("General/cmPath", self.cmPath.text())
        settings.setValue("General/templatePath", self.templateFile.text())
        settings.sync()
        QDialog.accept(self)
        
    @pyqtSlot()
    def reject(self):
        QDialog.reject(self)
        
        
    @pyqtSlot(int)
    def on_listWidget_currentRowChanged(self, currentRow):
        """
        Slot documentation goes here.
        
        @param currentRow DESCRIPTION
        @type int
        """
        self.stackedWidget.setCurrentIndex(currentRow)
    
    @pyqtSlot()
    def on_toolButtonCMPath_clicked(self):
        """
        Slot documentation goes here.
        """
        fdlg = QFileDialog(self)
        fdlg.setWindowTitle(_translate("ConfigDialog", "Circuit Macros Location", "File Dialog Title"))
        fdlg.setDirectory(self.cmPath.text())
        fdlg.setFileMode(QFileDialog.Directory)
        fdlg.setOptions(QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog | QFileDialog.ReadOnly)
        fdlg.setViewMode(QFileDialog.Detail)
        fdlg.setFilter(QDir.Dirs | QDir.Hidden)
        if fdlg.exec():
            newPath = fdlg.selectedFiles()
            self.cmPath.setText(newPath[0])
        fdlg.close()

    
    @pyqtSlot()
    def on_toolButtonTemplatePath_clicked(self):
        """
        Slot documentation goes here.
        """
        fdlg = QFileDialog(self)
        fdlg.setWindowTitle(_translate("ConfigDialog", "Latex Template Location", "File Dialog Title"))
        fdlg.setDirectory(os.path.dirname(self.templateFile.text()))
        fdlg.setFileMode(QFileDialog.ExistingFile)
        fdlg.setOptions(QFileDialog.DontUseNativeDialog | QFileDialog.ReadOnly)
        fdlg.setViewMode(QFileDialog.Detail)
        fdlg.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot | QDir.Hidden)
        if fdlg.exec():
            newPath = fdlg.selectedFiles()
            self.templateFile.setText(newPath[0])
        fdlg.close()


    @pyqtSlot(str)
    def on_cmPath_textChanged(self, newText):
        if  os.path.isdir(newText):
            self.cmPath.setStyleSheet("background-color: {white};".format(white = "rgb(255, 255, 255)"))
        else:
            self.cmPath.setStyleSheet("background-color: {reddish};".format(reddish = "rgb(255, 230, 230)"))


    @pyqtSlot(str)
    def on_templateFile_textChanged(self, newText):
        if  os.path.isfile(newText):
            self.templateFile.setStyleSheet("background-color: {white};".format(white = "rgb(255, 255, 255)"))
        else:
            self.templateFile.setStyleSheet("background-color: {reddish};".format(reddish = "rgb(255, 230, 230)"))
