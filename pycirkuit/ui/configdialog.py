# -*- coding: utf-8 -*-
"""
Module implementing configDialog.
"""

# Copyright (C) 2018-2026 Orestes Mas
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
from PySide6.QtCore import (
    Slot,
    Qt,
    QSize,
    QDir,
    QSettings,
    QCoreApplication,
    Signal,
)
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

# Local application imports
from pycirkuit.ui.Ui_configdialog import Ui_ConfigDialog
from pycirkuit.exceptions import PyCirkuitError
from pycirkuit.tools.latex import (
    latex_engine_choices,
    default_template_filename,
    DEFAULT_LATEX_ENGINE,
)

# Translation function
_translate = QCoreApplication.translate


class ConfigDialog(QDialog, Ui_ConfigDialog):
    """
    Class documentation goes here.
    """

    exportSettingsChange = Signal()

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
            self.listWidget.item(i).setSizeHint(QSize(128, 80))
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

        # Populate and select the LaTeX engine combo box
        for engineId, displayName in latex_engine_choices():
            self.latexEngine.addItem(displayName, engineId)
        storedEngine = settings.value("General/latexEngine", DEFAULT_LATEX_ENGINE)
        engineIndex = self.latexEngine.findData(storedEngine)
        if engineIndex >= 0:
            self.latexEngine.setCurrentIndex(engineIndex)

        # Extract stored path to LaTeX template file
        # defaultPath = QDir.homePath() + "/Plantilles/cm_tikz.ckt"
        storedLatexTemplateFile = settings.value("General/templatePath", "")
        if storedLatexTemplateFile == "":
            # emit signal manually as setting an empty text doesn't really changes the text (it is already empty)
            self.templateFile.textChanged.emit("")
        else:
            self.templateFile.setText(storedLatexTemplateFile)

        # Settings from the second page "Export"
        settings.beginGroup("Export")
        self.exportTIKZ.setChecked(settings.value("exportTIKZ", type=bool))
        self.exportSVG.setChecked(settings.value("exportSVG", type=bool))
        self.exportPDF.setChecked(settings.value("exportPDF", type=bool))
        self.exportPNG.setChecked(settings.value("exportPNG", type=bool))
        self.exportJPEG.setChecked(settings.value("exportJPEG", type=bool))
        self.exportDPI.setValue(settings.value("exportDPI", type=int))
        self.exportQuality.setValue(settings.value("exportQuality", type=int))
        settings.endGroup()

    def exportSettingsChanged(self):
        settings = QSettings()
        if (
            (
                self.exportTIKZ.isChecked()
                != settings.value("Export/exportTIKZ", type=bool)
            )
            or (
                self.exportSVG.isChecked()
                != settings.value("Export/exportSVG", type=bool)
            )
            or (
                self.exportPDF.isChecked()
                != settings.value("Export/exportPDF", type=bool)
            )
            or (
                self.exportPNG.isChecked()
                != settings.value("Export/exportPNG", type=bool)
            )
            or (
                self.exportJPEG.isChecked()
                != settings.value("Export/exportJPEG", type=bool)
            )
            or (self.exportDPI.value() != settings.value("Export/exportDPI", type=int))
            or (
                self.exportQuality.value()
                != settings.value("Export/exportQuality", type=int)
            )
        ):
            return True
        else:
            return False

    @Slot()
    def accept(self):
        settings = QSettings()
        # General page
        try:
            if not os.path.isdir(self.cmPath.text()):
                message = _translate(
                    "MessageBox",
                    "The path to the Circuit Macros location is not valid. Please enter a valid one.",
                    "",
                )
                extraInfo = _translate(
                    "MessageBox",
                    "Or, cancel the settings dialog and PyCirkuit will download and install the Circuit Macros when needed.",
                    "",
                )
                raise PyCirkuitError(message, moreInfo=extraInfo)
            if not os.path.isfile(self.templateFile.text()):
                raise PyCirkuitError(
                    _translate(
                        "MessageBox",
                        "The path to the LaTeX template does not point to a valid file. Please enter a correct one.",
                        "",
                    )
                )
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
        settings.setValue("General/latexEngine", self.latexEngine.currentData())
        settings.setValue("General/templatePath", self.templateFile.text())
        # Export page
        if self.exportSettingsChanged():
            QMessageBox.information(
                self,
                "PyCirkuit",
                _translate(
                    "MessageBox",
                    "To be able to export with the new settings you have to process the source again.",
                    "",
                ),
            )
            self.exportSettingsChange.emit()
        settings.beginGroup("Export")
        settings.setValue("exportTIKZ", self.exportTIKZ.isChecked())
        settings.setValue("exportSVG", self.exportSVG.isChecked())
        settings.setValue("exportPDF", self.exportPDF.isChecked())
        settings.setValue("exportPNG", self.exportPNG.isChecked())
        settings.setValue("exportJPEG", self.exportJPEG.isChecked())
        settings.setValue("exportDPI", self.exportDPI.value())
        settings.setValue("exportQuality", self.exportQuality.value())
        settings.endGroup()
        # save settings and quit
        settings.sync()
        QDialog.accept(self)

    @Slot()
    def reject(self):
        QDialog.reject(self)

    @Slot(int)
    def on_listWidget_currentRowChanged(self, currentRow):
        """
        Slot documentation goes here.

        @param currentRow DESCRIPTION
        @type int
        """
        self.stackedWidget.setCurrentIndex(currentRow)

    @Slot(int)
    def on_latexEngine_currentIndexChanged(self, index):
        """
        If the current template path still points at one of the bundled
        per-engine default templates, switch it to the new engine's default
        too, so picking an engine doesn't silently leave an incompatible
        template configured. A custom template path (anything else) is left
        untouched.
        """
        newEngineId = self.latexEngine.itemData(index)
        if newEngineId is None:
            return
        currentDir = os.path.dirname(self.templateFile.text())
        currentBasename = os.path.basename(self.templateFile.text())
        knownDefaults = {
            default_template_filename(engineId)
            for engineId, _ in latex_engine_choices()
        }
        if currentBasename in knownDefaults:
            newBasename = default_template_filename(newEngineId)
            self.templateFile.setText(os.path.join(currentDir, newBasename))

    @Slot()
    def on_toolButtonCMPath_clicked(self):
        """
        Slot documentation goes here.
        """
        fdlg = QFileDialog(self)
        fdlg.setWindowTitle(
            _translate("ConfigDialog", "Circuit Macros Location", "File Dialog Title")
        )
        fdlg.setDirectory(self.cmPath.text())
        fdlg.setFileMode(QFileDialog.Directory)
        fdlg.setOptions(
            QFileDialog.ShowDirsOnly
            | QFileDialog.DontUseNativeDialog
            | QFileDialog.ReadOnly
        )
        fdlg.setViewMode(QFileDialog.Detail)
        fdlg.setFilter(QDir.Dirs | QDir.Hidden)
        if fdlg.exec():
            newPath = fdlg.selectedFiles()
            self.cmPath.setText(newPath[0])
        fdlg.close()

    @Slot()
    def on_toolButtonTemplatePath_clicked(self):
        """
        Slot documentation goes here.
        """
        fdlg = QFileDialog(self)
        fdlg.setWindowTitle(
            _translate("ConfigDialog", "Latex Template Location", "File Dialog Title")
        )
        fdlg.setDirectory(os.path.dirname(self.templateFile.text()))
        fdlg.setFileMode(QFileDialog.ExistingFile)
        fdlg.setOptions(QFileDialog.DontUseNativeDialog | QFileDialog.ReadOnly)
        fdlg.setViewMode(QFileDialog.Detail)
        fdlg.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot | QDir.Hidden)
        if fdlg.exec():
            newPath = fdlg.selectedFiles()
            self.templateFile.setText(newPath[0])
        fdlg.close()

    @Slot(str)
    def on_cmPath_textChanged(self, newText):
        if os.path.isdir(newText):
            self.cmPath.setStyleSheet(
                "background-color: {white};".format(white="rgb(255, 255, 255)")
            )
        else:
            self.cmPath.setStyleSheet(
                "background-color: {reddish};".format(reddish="rgb(255, 230, 230)")
            )

    @Slot(str)
    def on_templateFile_textChanged(self, newText):
        if os.path.isfile(newText):
            self.templateFile.setStyleSheet(
                "background-color: {white};".format(white="rgb(255, 255, 255)")
            )
        else:
            self.templateFile.setStyleSheet(
                "background-color: {reddish};".format(reddish="rgb(255, 230, 230)")
            )
