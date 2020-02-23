# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
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
#import sys
import os
from shutil import copyfile

# Third-party imports
from PyQt5.QtCore import pyqtSlot, Qt, QCoreApplication, QSettings,  QFileInfo
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QProgressBar, QFileDialog,  QDialog

# Local application imports
from pycirkuit.ui.Ui_mainwindow import Ui_MainWindow
from pycirkuit.ui.configdialog import ConfigDialog
from pycirkuit.ui.aboutdialog import AboutDialog
from pycirkuit.tools.circuitmacrosmanager import CircuitMacrosManager
from pycirkuit.highlighter import PyCirkuitHighlighter
from pycirkuit.exceptions import *
from pycirkuit.tools.m4 import ToolM4
from pycirkuit.tools.dpic import ToolDpic
from pycirkuit.tools.pdflatex import ToolPdfLaTeX
from pycirkuit.tools.pdftopng import ToolPdfToPng
from pycirkuit.tools.pdftojpg import ToolPdfToJpeg
from pycirkuit.tools.processor import PyCirkuitProcessor
import pycirkuit


# Translation function
_translate = QCoreApplication.translate

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
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
        # This is the translated name for unnamed files
        self._translatedUnnamed = _translate("MainWindow", "unnamed", "Initial name of a new empty file")
        
        # This is to avoid starting the app with buffer marked as "dirty", and hence needing saving
        # This occurs because the "setupUI" method modifies text and hence triggers a textChanged signal
        self.insideConstructor = True
        self.setupUi(self)

        # The app icon is located inside the resource file
        icon = QtGui.QIcon(":/icons/AppIcon")
        self.setWindowIcon(icon)
        
        # A class variable to hold the exporting dir temporarily
        # Set destination dir to the same value of source dir. Defaults to empty.
        settings = QSettings()
        self.lastDstDir = settings.value("General/lastSrcDir", "")

        # Connect signals with slots
        #NOTE: Is NOT necessary to MANUALLY connect most signals to slots, as 
        # pyuic5 calls QtCore.QMetaObject.connectSlotsByName in Ui_configdialog.py
        # do such connections AUTOMATICALLY (so connecting them manually triggers slots twice)
        self.imageViewer.conversion_failed.connect(self._display_error)
        self.imageViewer.image_changed.connect(self._resize_preview)
        self.previewWidget.dockLocationChanged.connect(self._resize_preview)

        # Instantiate a processor object which will perform the actual file processing
        self.processor = PyCirkuitProcessor()

        # Set up the editor
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.sourceText.setFont(font)
        self.highlighter = PyCirkuitHighlighter(self.sourceText.document())
        # Initialize editor contents with a default drawing template
        self.needSaving = False
        self.on_actionNew_triggered()
        
        # Center the window on screen
        self._center()

        # Set up the permanent widgets in status bar
        self.sbProgressBar = QProgressBar()
        self.sbProgressBar.setRange(0, 100)
        self.sbProgressBar.setMaximumHeight(10)
        self.sbProgressBar.setTextVisible(False)
        self.sbProgressBar.setVisible(False)
        self.statusBar.addPermanentWidget(self.sbProgressBar)
        
        # We're quitting constructor
        self.insideConstructor = False


    def _check_export_dir(self, dir):
        fdlg = QtWidgets.QFileDialog(self)
        fdlg.setWindowTitle(_translate("MainWindow", "Enter a writable directory to save into",  "Window Title"))
        fdlg.setDirectory(dir)
        fdlg.setFileMode(QtWidgets.QFileDialog.Directory)
        fdlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog | QtWidgets.QFileDialog.ShowDirsOnly)
        fdlg.setViewMode(QtWidgets.QFileDialog.List)
        while True:
            if fdlg.exec() == QtWidgets.QFileDialog.Accepted:
                newDir = fdlg.selectedFiles()[0]
                #TODO: Check if selected dir is writable
                try:
                    name = os.path.join(newDir, 'test.txt')
                    with open(name, 'w'):
                        pass
                except:
                    pass
                return newDir
            else:
                #Dialog cancelled,  we must return with the dir name unchanged
                break
        return dir


    def _ask_export_file(self, dst):
        fdlg = QtWidgets.QFileDialog(self)
        fdlg.setWindowTitle(_translate("MainWindow", "Enter a file to save into",  "Window Title"))
        fdlg.setDirectory(dst)
        fdlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fdlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
        fdlg.setViewMode(QtWidgets.QFileDialog.Detail)
        fdlg.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files)
        fdlg.selectFile(dst)
        #FIXME: Bad programming style: new format additions are been managed in too many differents places
        filterList = []
        n, e = os.path.splitext(dst)
        if e == '.tikz':
            filterList.append(_translate("MainWindow", "TikZ files (*.tikz)", "File filter"))
        elif e == '.pdf':
            filterList.append(_translate("MainWindow", "PDF files (*.pdf)", "File filter"))
        elif e == '.png':
            filterList.append(_translate("MainWindow", "PNG files (*.png)", "File filter"))
        elif e == '.jpeg':
            filterList.append(_translate("MainWindow", "JPEG files (*.jpeg *.jpg)", "File filter"))
        elif e == '.svg':
            filterList.append(_translate("MainWindow", "SVG files (*.svg)", "File filter"))
        filterList.append(_translate("MainWindow", "Any files (*)", "File filter"))
        fdlg.setNameFilters(filterList)
        if fdlg.exec():
            dst = fdlg.selectedFiles()[0]
        fdlg.close()
        return dst


    def _ask_saving(self):
        # Open MessageBox and inform user
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(_translate("MessageBox", "PyCirkuit - Warning",  "Message Box title"))
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(_translate("MessageBox", "Source file have unsaved changes.", "Message box text"))
        msgBox.setInformativeText(_translate("MessageBox", "Do you want to save them before proceeding?",  "Message Box text"))
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        response = msgBox.exec()
        if response == QtWidgets.QMessageBox.Yes:
            self.actionSave.trigger()


    def _ask_writable_dir(self, offendingDir):
        fdlg = QFileDialog(self)
        fdlg.setWindowTitle(_translate("MainWindow", "Enter new directory", "File Dialog Title"))
        fdlg.setDirectory(offendingDir)
        fdlg.setFileMode(QFileDialog.Directory)
        fdlg.setOptions(QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
        fdlg.setViewMode(QFileDialog.Detail)
        fdlg.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Hidden)
        if fdlg.exec():
            newPath = fdlg.selectedFiles()
        else:
           newPath = None
        fdlg.close()
        return newPath

    def _center(self):
        # Get desktop's geometry
        app = QtWidgets.QApplication.instance()
        desktop = app.desktop()
        deskRect = desktop.screenGeometry(-1)
        # Now get MainWindow's geometry
        winRect = self.frameGeometry()
        # Now translate the window's rectangle so its center coincides with the desktop's one
        winRect.moveCenter(deskRect.center())
        # Finally, move the physical window using the top-left corner coords:
        self.move(winRect.x(), winRect.y())


    def _check_programs(self):
        try:
            # Dictionary using a class as index and a class instance as value
            self.extTools = {
                ToolM4: ToolM4(),
                ToolDpic: ToolDpic(), 
                ToolPdfLaTeX: ToolPdfLaTeX(), 
                ToolPdfToPng: ToolPdfToPng(), 
                ToolPdfToJpeg: ToolPdfToJpeg()
            }
        except PyCktToolNotFoundError as err:
            # Open MessageBox and inform user
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle(err.title)
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText(str(err))
            msgBox.setInformativeText(err.moreInfo)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
            return False
        return True


    def _check_templates(self):
        settings = QSettings()
        template = settings.value("General/templatePath",  "")
        if os.path.exists(template):
            with open(template, 'r') as t:
                templateCode = t.read()
                if "%%SOURCE%%" in templateCode:
                    return True
                else:
                    errMsg  = _translate("MessageBox", "The specified LaTeX template seems invalid!\n\n", "Error message")
                    errMsg += _translate("MessageBox", "Please indicate a correct one in the Settings.\n\n", "Error message")
                    errMsg += _translate("MessageBox", "Cannot generate the preview.", "Error message")
                    error = PyCirkuitError(errMsg)
                    self._display_error(error)
                    return False
        else:
            errMsg  = _translate("MessageBox", "The LaTeX template has not been found!\n\n", "Error message")
            errMsg += _translate("MessageBox", "Please indicate its correct PATH in the Settings.\n\n", "Error message")
            errMsg += _translate("MessageBox", "Cannot generate the preview.", "Error message")
            error = PyCirkuitError(errMsg)
            self._display_error(error)
            return False



    def _ensure_writable_location(self, dstDir):
        while True:
            dstDirInfo = QFileInfo(dstDir)
            if ( dstDirInfo.isDir() and dstDirInfo.isWritable() ):
                return dstDir
            else:
                # Display error messagebox
                msgBox = QtWidgets.QMessageBox(self)
                msgBox.setWindowTitle(_translate("MessageBox", "PyCirkuit - Error",  "Message Box title"))
                msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                msgBox.setText(_translate("MessageBox", "The exporting destination directory is not writable.", "Message box text." ))
                msgBox.setInformativeText(_translate("MessageBox", "Please enter a suitable directory to write into.",  "Message Box text"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.exec()
                # Ask user to choose another directory
                dstDir = self._ask_writable_dir(dstDirInfo.canonicalPath())[0]



    @pyqtSlot(PyCirkuitError)
    def _display_error(self, error):
        # Open MessageBox and inform user
        #TODO: Use this method to display message boxes
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(error.title)
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText(str(error))
        msgBox.setInformativeText(error.moreInfo)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msgBox.exec()


    def _enforce_circuit_macros(self):
        cmMgr = CircuitMacrosManager(self)
        if cmMgr.check_installed():
            return True
        else:
            _cmNotFound  = _translate("MessageBox", "Cannot find the 'Circuit Macros'!\n\n")
            txt = _cmNotFound + _translate("MessageBox", "Do you want to try to search and install them automatically?")
            response = QtWidgets.QMessageBox.question(self, _translate("MessageBox", "PyCirkuit - Warning", "Message Box title"),  txt,  defaultButton=QtWidgets.QMessageBox.Yes)
            result = False
            if response == QtWidgets.QMessageBox.Yes:
                try:
                    self.statusBar.showMessage(_translate("StatusBar", "Downloading and unpacking Circuit Macros", "Status Bar message"))
                    app = QtWidgets.QApplication.instance()
                    app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
                    self.sbProgressBar.setRange(0, 100)
                    self.sbProgressBar.setValue(0)
                    self.sbProgressBar.setVisible(True)
                    cmMgr.download_latest(self.sbProgressBar)
                    cmMgr.unpack_circuit_macros()
                    result = True
                except:
                    pass
                finally:
                    app.restoreOverrideCursor()
                    self.statusBar.clearMessage()
                    self.sbProgressBar.setVisible(False)
            else:
                txt = _cmNotFound + _translate("MessageBox", "Please indicate the correct path to them in the settings dialog.")
                QtWidgets.QMessageBox.critical(self, _translate("MessageBox", "PyCirkuit - Error", "Message Box title"),  txt)
            return result


    @pyqtSlot()
    def _exportSettingsChanged(self):
        self.exportButton.setEnabled(False)
        self.processButton.setEnabled(True)

    def _load_file(self, fileName):
        settings = QSettings()
        # Check that file is not a broken link
        fileName = os.path.normpath(fileName)
        if os.path.isfile(fileName):
            lastSrcDir, filename = os.path.split(fileName)
            # Change system working dir to target's dir
            os.chdir(lastSrcDir)
            # Make new source dir persistent
            settings.setValue("General/lastSrcDir", lastSrcDir)
            settings.sync()
            # Destination dir for saving and exporting will be equal to source dir initially
            self.lastDstDir = lastSrcDir
            with open(filename, 'r') as f:
                txt = f.read()
                self.sourceText.setPlainText(txt)
                self.openedFilename = filename
                self.needSaving = False
                self._modify_title()
                self.on_processButton_clicked()


    def _modify_title(self):
        if self.needSaving:
            title = "PyCirkuit - {filename}*".format(filename=self.openedFilename)
        else:
            title = "PyCirkuit - {filename}".format(filename=self.openedFilename)
        self.setWindowTitle(title)


    @pyqtSlot()
    def _resize_preview(self):
        # First, retrieve the pixmap rect
        rect = self.imageViewer.getRect() 
        # Next, calculate the differences between dock widget and its contents
        extraHeight = self.previewWidget.height() - self.imageViewer.viewport().height()
        extraWidth  = self.previewWidget.width() - self.imageViewer.viewport().width()
        # Then resize the dock widget in a way that acknowledges the size constraints of other widgets
        dockWidgetLocation = self.dockWidgetArea(self.previewWidget)
        if (dockWidgetLocation == Qt.TopDockWidgetArea) or (dockWidgetLocation == Qt.BottomDockWidgetArea):
            self.resizeDocks([self.previewWidget], [rect.height() + extraHeight +2], Qt.Vertical)
        elif (dockWidgetLocation == Qt.LeftDockWidgetArea) or (dockWidgetLocation == Qt.RightDockWidgetArea):
            self.resizeDocks([self.previewWidget], [rect.width() + extraWidth +2], Qt.Horizontal)



    def _save_buffer(self,  dst):
        """ Saves the content of the editing buffer onto disk.
        
        Arguments:
        dst -- the destination directory
        """
        # We decided to handle exceptions
        try:
            with open(dst,'w', encoding='UTF-8') as f:
                f.write(self.sourceText.toPlainText())
        except FileNotFoundError:
            raise
        except PermissionError:
            errMsg = _translate("MessageBox", "Error saving source file: Destination is not writable.\n\n", "Error message")
            errMsg += _translate("MessageBox", "Please select a suitable destination to save into.", "Error message")
            QtWidgets.QMessageBox.critical(self, _translate("MessageBox", "PyCirkuit - Error", "Message Box title"),  errMsg)
            raise
        else:
            # If saving succeeded, write down the export path and file name
            self.lastDstDir, self.openedFilename = os.path.split(dst)
            self.needSaving = False
            self._modify_title()
            self.actionSave.setEnabled(False)


    def closeEvent(self,  event):
        if self.needSaving:
            self._ask_saving()
        super().closeEvent(event)


    @pyqtSlot()
    def on_actionAbout_triggered(self):
        """
        Slot documentation goes here.
        """
        dlg = AboutDialog()
        dlg.exec()


    @pyqtSlot()
    def on_actionCMMan_triggered(self):
        # Search for Circuit Macros PDF manual
        if self._enforce_circuit_macros():
            try:
                cmMgr = CircuitMacrosManager(self)
                cmPath = cmMgr.getManUrl()
                # Open it with the default app. We can do that using Qt or in a mode pythonic way (os.system...)
                # I choose the former because I want Qt to deal with the differences between OSes
                QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(cmPath))
            except PyCktCMManNotFoundError as error:
                QtWidgets.QMessageBox.warning(self, error.title,  str(error))


    @pyqtSlot()
    def on_actionDpicMan_triggered(self):
        try:
            dpic = ToolDpic();
            path = dpic.getManUrl()
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))
        except PyCktDocNotFoundError as err:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle(err.title)
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(str(err))
            msgBox.setInformativeText(err.moreInfo)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()


    @pyqtSlot()
    def on_actionNew_triggered(self, newName=None):
        if self.needSaving:
            self._ask_saving()
        txt = _translate("MainWindow", ".PS\nscale=2.54\ncct_init\n\nl=elen_\n# Enter your drawing code here\n.PE\n",  "Template text. Translate ONLY the commented out text (line starting with '#')")
        self.sourceText.setText(txt)
        if newName == None:
            self.openedFilename = self._translatedUnnamed
            self.needSaving = False
        else:
            settings = QSettings()
            lastSrcDir, filename = os.path.split(newName)
            # Change system working dir to target's dir
            os.chdir(lastSrcDir)
            settings.setValue("General/lastSrcDir", lastSrcDir)
            settings.sync()
            self.openedFilename = filename
            self.needSaving = True
        self._modify_title()
        self.imageViewer.clearImage()


    @pyqtSlot()
    def on_actionOpen_triggered(self):
        if self.needSaving:
            self._ask_saving()
    
        # Instantiate a settings object
        settings = QSettings()

        # Show the 'load file' Dialog
        fdlg = QtWidgets.QFileDialog(self)
        fdlg.setWindowTitle(_translate("MainWindow", "Source File Selection", "File Dialog title"))
        fdlg.setDirectory(settings.value("General/lastSrcDir",  ""))
        fdlg.setNameFilters([
            _translate("MainWindow", "PyCirkuit files (*.ckt)", "File filter text"), 
            _translate("MainWindow", "M4 macro files (*.m4)", "File filter text"),
            _translate("MainWindow", "TeX files (*.tex)", "File filter text"),
            _translate("MainWindow", "Any files (*)", "File filter text")])
        fdlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        fdlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog | QtWidgets.QFileDialog.ReadOnly)
        fdlg.setViewMode(QtWidgets.QFileDialog.Detail)
        fdlg.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
        fitxer = ""
        if fdlg.exec():
            fitxer = fdlg.selectedFiles()[0]
        fdlg.close()

        # Check that user didn't press 'Cancel' on the Dialog Box...
        if fitxer != "":
            self._load_file(fitxer)
    
    
    @pyqtSlot()
    def on_actionPreferences_triggered(self):
        """
        Slot documentation goes here.
        """
        cfgDlg = ConfigDialog()
        cfgDlg.exportSettingsChange.connect(self._exportSettingsChanged)
        cfgDlg.exec()


    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        settings = QSettings()
        lastSrcDir = settings.value("General/lastSrcDir", QtCore.QStandardPaths.displayName(QtCore.QStandardPaths.HomeLocation))
        fdlg = QtWidgets.QFileDialog(self)
        fdlg.setWindowTitle(_translate("MainWindow", "Enter a file to save into", "File Dialog title"))
        fdlg.setDirectory(lastSrcDir)
        fdlg.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files)
        fdlg.setNameFilters([
            _translate("MainWindow", "PyCirkuit files (*.ckt)", "File filter"),
            _translate("MainWindow", "Any files (*)", "File filter")])
        fdlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
        fdlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fdlg.setViewMode(QtWidgets.QFileDialog.Detail)
        fdlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        while (fdlg.exec() == QDialog.Accepted):
            dst = fdlg.selectedFiles()[0]
            try:
                self._save_buffer(dst)
                return
            except PermissionError:
                pass


    @pyqtSlot()
    def on_actionSave_triggered(self):
        # Try to save into the last destination dir used.
        filePath = os.path.join(self.lastDstDir , self.openedFilename)
        # Check empty name
        if (self.openedFilename == self._translatedUnnamed ):
            self.actionSaveAs.trigger()
        else:
            # Try to save. If it fails (non-writable location...), ask for a name.
            try:
                self._save_buffer(filePath)
            except PermissionError:
                self.actionSaveAs.trigger()


    @pyqtSlot()
    def on_exportButton_clicked(self):
        if self.openedFilename == self._translatedUnnamed:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle(_translate("MessageBox", "PyCirkuit - Warning",  "Message Box title"))
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(_translate("MessageBox", "The source file isn't saved yet.", "Message box text."))
            msgBox.setInformativeText(_translate("MessageBox", "Please save the source file somewhere prior to exporting it.",  "Message Box text"))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            response = msgBox.exec()
            return

        # Fetch the formats to save. For now the extensions are fixed
        settings = QSettings()
        toSave = []
        if settings.value("Export/exportTIKZ", type=bool):
            toSave.append("tikz")
        if settings.value("Export/exportSVG", type=bool):
            toSave.append("svg")
        if settings.value("Export/exportPDF", type=bool):
            toSave.append("pdf")
        if settings.value("Export/exportPNG", type=bool):
            toSave.append("png")
        if settings.value("Export/exportJPEG", type=bool):
            toSave.append("jpeg")
        
        # First we must detect if destination dir is writable. If not, ask for another one and update "lastSrcDir" setting (if it's writable)
        self.lastDstDir = self._ensure_writable_location(self.lastDstDir)
        
        # Next we do a loop for every export format requested
        for fileType in toSave:
            src = os.path.join(pycirkuit.__tmpDir__.path(), "cirkuit_tmp") + os.extsep + fileType
            # First try for destination path
            dst = os.path.join(self.lastDstDir, os.path.splitext(self.openedFilename)[0]) + os.extsep + fileType
            success = False
            while not success:
                try:    
                    if os.path.exists(dst):
                        msgBox = QtWidgets.QMessageBox(self)
                        msgBox.setWindowTitle(_translate("MessageBox", "PyCirkuit - Warning",  "Message Box title"))
                        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgBox.setText(_translate("MessageBox", "There's already a file named \"{filename}\" at working directory.", "Message box text. Don't translate '{filename}'").format(filename=self.openedFilename.partition('.')[0]+os.extsep+fileType))
                        msgBox.setInformativeText(_translate("MessageBox", "Do you want to overwrite it?",  "Message Box text"))
                        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                        saveAsButton = msgBox.addButton(_translate("MessageBox", "Save As...",  "Button text"),  QtWidgets.QMessageBox.AcceptRole)
                        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
                        response = msgBox.exec()
                        # Overwrite
                        if response == QtWidgets.QMessageBox.Yes:
                            copyfile(src, dst)
                            success = True
                        # Save with another name/path (and ask for it first)
                        if (response == QtWidgets.QMessageBox.NoButton) and (msgBox.clickedButton() == saveAsButton):
                            dst = self._ask_export_file(dst)
                            self.lastDstDir, f = os.path.split(dst)
                            copyfile(src, dst)
                            success = True
                        # Any other option means user doesn't want to overwrite the file -> Exit
                        break
                    else:
                        copyfile(src, dst)
                        success = True
                except PermissionError as err:
                    msgBox = QtWidgets.QMessageBox(self)
                    msgBox.setWindowTitle(_translate("MessageBox", "PyCirkuit - Error",  "Message Box title"))
                    msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                    msgBox.setText(_translate("MessageBox", "Permission denied writing the file {filename}.", "Message box text. Don't translate '{filename}'").format(filename=err.filename))
                    msgBox.setInformativeText(_translate("MessageBox", "Please try to export again with another name and/or location.",  "Message Box text"))
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    response = msgBox.exec()
                    # Replace dst with the new user-choosed file
                    self.lastDstDir = self._ask_export_file(dst)
                except OSError:
                    msgBox = QtWidgets.QMessageBox(self)
                    msgBox.setWindowTitle(_translate("MessageBox", "PyCirkuit - Error",  "Message Box title"))
                    msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                    msgBox.setText(_translate("MessageBox", "An error has occurred trying to export the file. The error says:", "Message Box text"))
                    msgBox.setInformativeText(err.strerror)
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    response = msgBox.exec()
        # Continue after the 'for' loop. If we are here we've saved successfully all the requested formats, so we can disable the button
        self.exportButton.setEnabled(False)



    @pyqtSlot()
    def on_processButton_clicked(self):
        def writeHeader(tool):
            aux = header.format(toolLongName=self.extTools[tool].longName)
            self.outputText.appendPlainText('\n' + aux)
            self.outputText.appendPlainText("="*len(aux))
                
        def writeOk():
            self.outputText.appendPlainText(_translate("OutputLog", " + No execution errors", "Output log info"))

        # STEP 0: Basic checks for the existence of auxiliary programs/utilities
        # Check if we have all the auxiliary apps correctly installed
        if not self._check_programs():
            return
        # Check if we have the Circuit Macros at the folder specified into the Settings
        if not self._enforce_circuit_macros():
            return
        # Check if the template file exists and is valid
        if not self._check_templates():
            return

        try:
            settings = QSettings()
            # STEP 1: Prepare the Progress Bar
            self.sbProgressBar.setRange(0, 8)
            self.sbProgressBar.setValue(0)
            self.sbProgressBar.setVisible(True)

            # STEP 2: Save current WD and set a new one
            savedWD = os.getcwd()
            os.chdir(pycirkuit.__tmpDir__.path())
            
            # STEP 3: Establish a temporary file base name to store intermediate results
            tmpFileBaseName = "cirkuit_tmp"
            with open("{baseName}.ckt".format(baseName=tmpFileBaseName), 'w') as tmpFile:
                tmpFile.write(self.sourceText.toPlainText())
            
            # STEP 4: Change cursor shape temporarily
            app = QtWidgets.QApplication.instance()
            app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            
            # STEP 5: Clear log text
            self.outputText.clear()
            self.outputText.setPlainText(_translate("OutputLog", ">>>>> Start processing", "Output log info"))
            header = _translate("OutputLog", "Output of {toolLongName}:", "Output log info. Do NOT modify/translate the '{toolLongName}' variable")
 
            # STEP 6: Call M4: .CKT -> .PIC
            self.statusBar.showMessage(_translate("StatusBar", "Converting: Circuit Macros -> PIC", "Status Bar message"))
            writeHeader(ToolM4)
            self.extTools[ToolM4].execute(tmpFileBaseName)
            writeOk()
            self.sbProgressBar.setValue(1)

            # STEP 7a: Call dpic: .PIC -> .TIKZ
            self.statusBar.showMessage(_translate("StatusBar", "Converting: PIC -> TIKZ", "Status Bar message"))
            writeHeader(ToolDpic)
            self.extTools[ToolDpic].execute(tmpFileBaseName, outputType = pycirkuit.Option.TIKZ)
            writeOk()
            self.sbProgressBar.setValue(2)

            # STEP 7b: Call dpic: .PIC -> .SVG
            if settings.value("Export/exportSVG", type=bool):
                self.statusBar.showMessage(_translate("StatusBar", "Converting: PIC -> SVG", "Status Bar message"))
                writeHeader(ToolDpic)
                self.extTools[ToolDpic].execute(tmpFileBaseName, outputType = pycirkuit.Option.SVG)
                writeOk()
                self.sbProgressBar.setValue(3)

            # STEP 8: Call PDFLaTeX: .TIKZ -> .PDF
            # First we have to embed the .TIKZ code inside a suitable template
            self.statusBar.showMessage(_translate("StatusBar", "Converting: TIKZ -> PDF", "Status Bar message"))
            writeHeader(ToolPdfLaTeX)
            self.extTools[ToolPdfLaTeX].execute(tmpFileBaseName)
            writeOk()
            self.sbProgressBar.setValue(4)

            # STEP 9: Call pdftoppm to convert the PDF into a bitmap image to visualize it: .PDF -> .PNG
            self.statusBar.showMessage(_translate("StatusBar", "Converting: PDF -> PNG", "Status Bar message"))
            writeHeader(ToolPdfToPng)
            settings.beginGroup("Export")
            dpi = settings.value("exportDPI", type=int)
            copyfile(tmpFileBaseName+os.extsep+"pdf", tmpFileBaseName+"_display"+os.extsep+"pdf")
            self.extTools[ToolPdfToPng].execute(tmpFileBaseName+"_display", resolution=150)
            if settings.value("exportPNG", type=bool):
                self.extTools[ToolPdfToPng].execute(tmpFileBaseName, resolution=dpi)
            if settings.value("exportJPEG", type=bool):
                q = settings.value("exportQuality", type=int)
                self.extTools[ToolPdfToJpeg].execute(tmpFileBaseName, resolution=dpi, quality=q)
            settings.endGroup()
            writeOk()
            self.sbProgressBar.setValue(5)
            
            # STEP 10: Call pdftoppm to convert the PDF into a JPEG
            settings.beginGroup("Export")
            if settings.value("exportJPEG", type=bool):
                dpi = settings.value("exportDPI", type=int)
                q = settings.value("exportQuality", type=int)
                self.statusBar.showMessage(_translate("StatusBar", "Converting: PDF -> JPEG", "Status Bar message"))
                writeHeader(ToolPdfToPng)
                self.extTools[ToolPdfToJpeg].execute(tmpFileBaseName, resolution=dpi, quality=q)
                writeOk()
                self.sbProgressBar.setValue(6)
            settings.endGroup()
            
            # STEP 10: Visualize the image (can fail)
            self.sbProgressBar.setValue(7)
            self.imageViewer.setImage(tmpFileBaseName+"_display", adjustIGU=True)

        except PyCktToolExecutionError as err:
            self.imageViewer.setText(_translate("MainWindow", "Error!", "Fallback text to be displayed when the image cannot be generated"))
            self.outputText.appendPlainText(err.moreInfo)
            if err.tool == ToolPdfLaTeX:
                with open(tmpFileBaseName+'.log', 'rt') as f:
                    for line in f.readlines():
                        self.outputText.appendPlainText(line)
            self._display_error(err)
        except PyCktImageError as err:
            self.imageViewer.setText(_translate("MainWindow", "Error!", "Fallback text to be displayed when the image cannot be generated"))
            self._display_error(err)
        else:
            # If all went well and we have a generated image, we can 
            self.processButton.setEnabled(False)
            self.exportButton.setEnabled(True)
        finally:
            os.chdir(savedWD)
            self.statusBar.showMessage("")
            self.sbProgressBar.setVisible(False)
            app.restoreOverrideCursor()


    @pyqtSlot()
    def on_sourceText_textChanged(self):
        self.outputText.clear()
        if self.insideConstructor:
            return
        else:
            self.needSaving = True
            self._modify_title()
            self.actionSave.setEnabled(True)
            self.processButton.setEnabled(True)
            self.exportButton.setEnabled(False)
