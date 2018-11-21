# -*- coding: utf-8 -*-

"""
Module implementing configDialog.
"""

from PyQt5.QtCore import pyqtSlot,  QDir,  QFile,  QSettings
from PyQt5.QtWidgets import QDialog,  QFileDialog

from .Ui_configdialog import Ui_configDialog


class configDialog(QDialog, Ui_configDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(configDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Persistent settings
        self.settings = QSettings() 
        # Extract stored path to Circuit Macros
        defaultPath = QDir.homePath() + "/.local/share/cirkuit/circuit_macros"
        cmStoredPath = QDir(self.settings.value("General/cmPath", defaultPath))
        if  not cmStoredPath.exists():
            cmStoredPath = QDir.home()
            self.settings.setValue("General/cmPath",  cmStoredPath.absolutePath())
            self.settings.sync()
        self.cmPath.setText(cmStoredPath.absolutePath())

        # Extract stored path to LaTeX template file
        defaultPath = QDir.homePath() + "/Plantilles/cm_tikz.ckt"
        storedLatexTemplateFile = QFile(self.settings.value("General/latexTemplateFile", defaultPath))
        if  not storedLatexTemplateFile.exists():
            storedLatexTemplateFile = QDir.home()
            self.settings.setValue("General/latexTemplateFile",  storedLatexTemplateFile.fileName())
            self.settings.sync()
        self.templateFile.setText(storedLatexTemplateFile.fileName())
        
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
        fdlg.setWindowTitle("Circuit Macros Location")
        fdlg.setDirectory(self.cmPath.text())
        fdlg.setFileMode(QFileDialog.Directory)
        fdlg.setOptions(QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog | QFileDialog.ReadOnly)
        fdlg.setViewMode(QFileDialog.Detail)
        fdlg.setFilter(QDir.Dirs | QDir.Hidden)
        if fdlg.exec():
            newPath = fdlg.selectedFiles()
            self.cmPath.setText(newPath[0])
            self.settings.setValue("General/cmPath", self.cmPath.text())
            self.settings.sync()
        fdlg.close()

    
    @pyqtSlot()
    def on_toolButtonTemplatePath_clicked(self):
        """
        Slot documentation goes here.
        """
        fdlg = QFileDialog(self)
        fdlg.setWindowTitle("Latex Template Location")
        fdlg.setDirectory(self.templateFile.text())
        fdlg.setFileMode(QFileDialog.ExistingFile)
        fdlg.setOptions(QFileDialog.DontUseNativeDialog | QFileDialog.ReadOnly)
        fdlg.setViewMode(QFileDialog.Detail)
        fdlg.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot | QDir.Hidden)
        if fdlg.exec():
            newPath = fdlg.selectedFiles()
            self.templateFile.setText(newPath[0])
            self.settings.setValue("General/latexTemplateFile", self.templateFile.text())
            self.settings.sync()
        fdlg.close()

