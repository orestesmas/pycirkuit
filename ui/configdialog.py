# -*- coding: utf-8 -*-

"""
Module implementing configDialog.
"""

import os
from PyQt5.QtCore import pyqtSlot,\
                         QDir,\
                         QSettings
from PyQt5.QtWidgets import QDialog,\
                            QFileDialog
from .Ui_configdialog import Ui_configDialog

#FIXME: El diàleg encara deixa introduir (manualment) paths inexistents, i només desa els paths a la configuració si els escollim via botó
# - Una solució és no deixar editar manualment els paths, però és poc elegant/intuïtiu
# - Una altra via seria convertir la QLineEdit en un QComboBox. Potser funciona.
#WARNING: - Els botons potser s'haurien de dir "Navega" (Browse)...
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
        storedLatexTemplateFile = settings.value("General/latexTemplateFile", "")
        if storedLatexTemplateFile == "":
            # emit signal manually as setting an empty text doesn't really changes the text (it is already empty)
            self.templateFile.textChanged.emit("")
        else:
            self.templateFile.setText(storedLatexTemplateFile)
    
    
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
            settings = QSettings()
            newPath = fdlg.selectedFiles()
            self.cmPath.setText(newPath[0])
            settings.setValue("General/cmPath", self.cmPath.text())
            settings.sync()
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
            settings = QSettings()
            newPath = fdlg.selectedFiles()
            self.templateFile.setText(newPath[0])
            settings.setValue("General/latexTemplateFile", self.templateFile.text())
            settings.sync()
        fdlg.close()


    @pyqtSlot(str)
    def on_cmPath_textChanged(self, newText):
        if  os.path.exists(newText):
            self.cmPath.setStyleSheet("background-color: {blanc};".format(blanc = "rgb(255, 255, 255)"))
        else:
            self.cmPath.setStyleSheet("background-color: {vermell};".format(vermell = "rgb(255, 230, 230)"))


    @pyqtSlot(str)
    def on_templateFile_textChanged(self, newText):
        if  os.path.exists(newText):
            self.templateFile.setStyleSheet("background-color: {blanc};".format(blanc = "rgb(255, 255, 255)"))   # verd = rgb(230, 255, 230)
        else:
            self.templateFile.setStyleSheet("background-color: {vermell};".format(vermell = "rgb(255, 230, 230)"))
