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
import inspect

# Third-party imports
from PyQt5.QtCore import pyqtSlot,  QCoreApplication
from PyQt5 import QtCore, QtWidgets, QtGui

# Local application imports
from pycirkuit.ui.Ui_mainwindow import Ui_MainWindow
from pycirkuit.configdialog import ConfigDialog
from pycirkuit.ui.aboutdialog import AboutDialog
from pycirkuit.circuitmacrosmanager import CircuitMacrosManager
from pycirkuit.highlighter import PyCirkuitHighlighter
from pycirkuit.tools.tool_base import PyCktToolNotFoundError, PyCktToolExecutionError
from pycirkuit.tools.m4 import ToolM4
from pycirkuit.tools.dpic import ToolDpic
from pycirkuit.tools.pdflatex import ToolPdfLaTeX
from pycirkuit.tools.pdftopng import ToolPdfToPng

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

        # Ensure meaningful default settings
        self._check_settings()
        
        # Connect signals with slots
        #NOTE: Is NOT necessary to MANUALLY connect most signals to slots, as 
        # pyuic5 calls QtCore.QMetaObject.connectSlotsByName in Ui_configdialog.py
        # do such connections AUTOMATICALLY (so connecting them manually triggers slots twice)

        # Set up a temporary directory to save intermediate files
        self.tmpDir = QtCore.QTemporaryDir()

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
        
        # We're quitting constructor
        self.insideConstructor = False




    def _ask_saving(self):
        # Open MessageBox and inform user
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(_translate("MessageBox", "Warning",  "Message Box title"))
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(_translate("MessageBox", "Source file have unsaved changes.", "Message box text"))
        msgBox.setInformativeText(_translate("MessageBox", "Do you want to save them before proceeding?",  "Message Box text"))
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        response = msgBox.exec()
        if response == QtWidgets.QMessageBox.Yes:
            self.actionSave.trigger()


    def _check_programs(self):
        try:
            self.extTools = {
                'm4': ToolM4(),
                'dpic': ToolDpic(), 
                'pdflatex': ToolPdfLaTeX(), 
                'pdftopng': ToolPdfToPng()
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


    def _check_settings(self):
        """
        Check if config file is empty (deleted, first run, etc.) and if so, set reasonable default values
        """
        settings = QtCore.QSettings()
        # Check LaTeX template
        if (settings.value("General/latexTemplateFile",  "") == ""):
            # Import ourselves
            import pycirkuit
            # Find absolute application's path
            templatePath = os.path.dirname(inspect.getfile(pycirkuit))
            # Add the relative path where the default template is located
            templatePath = os.path.join(templatePath, 'templates/cm_tikz.tpl')
            settings.setValue("General/latexTemplateFile", templatePath)
        # Check Circuit Macros path
        if (settings.value("General/cmPath",  "") == ""):
            CM = CircuitMacrosManager()
            settings.setValue("General/cmPath", CM.default_CMPath())


    def _check_templates(self):
        pass
        settings = QtCore.QSettings()
        template = settings.value("General/latexTemplateFile",  "")
        if os.path.exists(template):
            with open(template, 'r') as t:
                templateCode = t.read()
                if "%%SOURCE%%" in templateCode:
                    return True
                else:
                    #TODO: Recode using dynamic methods and "InformativeText"
                    errMsg  = _translate("MessageBox", "The specified LaTeX template seems invalid!\n\n", "Error message")
                    errMsg += _translate("MessageBox", "Please indicate a correct one in the Settings.\n\n", "Error message")
                    errMsg += _translate("MessageBox", "Cannot generate the preview.", "Error message")
                    QtWidgets.QMessageBox.critical(self, _translate("MessageBox", "Critical Error", "Message Box title"),  errMsg)
                    return False
        else:
            #TODO: Recode using dynamic methods and "InformativeText"
            errMsg  = _translate("MessageBox", "The LaTeX template has not been found!\n\n", "Error message")
            errMsg += _translate("MessageBox", "Please indicate its correct PATH in the Settings.\n\n", "Error message")
            errMsg += _translate("MessageBox", "Cannot generate the preview.", "Error message")
            QtWidgets.QMessageBox.critical(self, _translate("MessageBox", "Critical Error", "Message Box title"),  errMsg)
            return False


    def _enforce_circuit_macros(self):
        cmMgr = CircuitMacrosManager(self)
        if cmMgr.check_installed():
            return True
        else:
            _cmNotFound  = _translate("MessageBox", "Cannot find the 'Circuit Macros'!\n\n")
            txt = _cmNotFound + _translate("MessageBox", "Do you want to try to search and install them automatically?")
            response = QtWidgets.QMessageBox.question(self, _translate("MessageBox", "Warning"),  txt,  defaultButton=QtWidgets.QMessageBox.Yes)
            result = False
            if response == QtWidgets.QMessageBox.Yes:
                try:
                    self.statusBar.showMessage(_translate("StatusBar", "Downloading and unpacking Circuit Macros", "Status Bar message"))
                    app = QtWidgets.QApplication.instance()
                    app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
                    cmMgr.download_latest()
                    cmMgr.unpack_circuit_macros()
                    result = True
                except:
                    pass
                finally:
                    app.restoreOverrideCursor()
                    self.statusBar.clearMessage()
            else:
                txt = _cmNotFound + _translate("MessageBox", "Please indicate the correct path to them in the settings dialog.")
                QtWidgets.QMessageBox.critical(self, _translate("MessageBox", "Critical Error"),  txt)
            return result


    def _modify_title(self):
        if self.needSaving:
            title = "PyCirkuit - {filename}*".format(filename=self.openedFilename)
        else:
            title = "PyCirkuit - {filename}".format(filename=self.openedFilename)
        self.setWindowTitle(title)


    def _save_buffer(self,  dst):
        try:
            f = open(dst,'w', encoding='UTF-8')
            f.write(self.sourceText.toPlainText())
        except OSError as e:
            errMsg = _translate("MessageBox", "Error saving source file: ", "Error message") + e.strerror + ".\n\n"
            errMsg += _translate("MessageBox", "Cannot execute command.", "Error message")
            QtWidgets.QMessageBox.critical(self, _translate("MessageBox", "Critical Error", "Message Box title"),  errMsg)
            return
        else:
            settings = QtCore.QSettings()
            lastWD, self.openedFilename = os.path.split(dst)
            os.chdir(lastWD)
            settings.setValue("General/lastWD", lastWD)
            self.needSaving = False
            self._modify_title()
            self.actionSave.setEnabled(False)
        finally:
            f.close()


    def closeEvent(self,  event):
        if self.needSaving:
            self._ask_saving()
        self.tmpDir.remove()
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
            settings = QtCore.QSettings()
            cmPath = os.path.normpath(settings.value("General/cmPath",  ""))
            try:
                import glob
                cmPath = os.path.join(cmPath, "doc")
                candidates = glob.glob(cmPath + os.sep + "*.[pP][dD][fF]")
                if (len(candidates) == 1) and (os.path.isfile(candidates[0])):
                    # Open it with the default app. We can do that using Qt or in a mode pythonic way (os.system...)
                    # I choose the former because I want Qt to deal with the differences between OSes
                    QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(candidates[0]))
                else:
                    errMsg  = _translate("MessageBox", 'Cannot find the "Circuit Macros" documentation.\n\n', "Warning message")
                    errMsg += _translate("MessageBox", "You will have to search for it manually. It should be a PDF file located into {cmPath} folder or one of its subfolders.", "Message Box text. DO NOT translate '{cmPath}' variable.").format(cmPath=cmPath)
                    QtWidgets.QMessageBox.warning(self, _translate("MessageBox", "Error", "Message Box title"),  errMsg)
            except:
                pass


    @pyqtSlot()
    def on_actionDpicMan_triggered(self):
        dpic = ToolDpic();
        try:
            path = dpic.getManUrl()
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://" + path, QtCore.QUrl.TolerantMode))
        except:
            errMsg  = _translate("MessageBox", 'Cannot find the "Dpic" documentation.\n\n', "Warning message")
            errMsg += _translate("MessageBox", "You will have to search for it manually.")
            QtWidgets.QMessageBox.warning(self, _translate("MessageBox", "Error", "Message Box title"),  errMsg)



    @pyqtSlot()
    def on_actionNew_triggered(self):
        if self.needSaving:
            self._ask_saving()
        txt = _translate("MainWindow", ".PS\nscale=2.54\ncct_init\n\nl=elen_\n# Enter your drawing code here\n.PE\n",  "Template text. Translate ONLY the commented out text (line starting with '#')")
        self.sourceText.setText(txt)
        self.openedFilename = self._translatedUnnamed
        self.needSaving = False
        self._modify_title()


    @pyqtSlot()
    def on_actionOpen_triggered(self):
        if self.needSaving:
            self._ask_saving()
    
        # Instantiate a settings object
        settings = QtCore.QSettings()

        # Show the 'load file' Dialog
        fdlg = QtWidgets.QFileDialog(self)
        fdlg.setWindowTitle(_translate("MainWindow", "Source File Selection", "File Dialog title"))
        fdlg.setDirectory(settings.value("General/lastWD",  ""))
        fdlg.setNameFilters([
            _translate("MainWindow", "PyCirkuit files (*.ckt)", "File filter text"), 
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
            # Check that file is not a broken link
            fitxer = os.path.normpath(fitxer)
            if os.path.exists(fitxer):
                lastWD, filename = os.path.split(fitxer)
                # Change system working dir to target's dir
                os.chdir(lastWD)
                settings.setValue("General/lastWD", lastWD)
                settings.sync()
                with open(filename, 'r') as f:
                    txt = f.read()
                    self.sourceText.setPlainText(txt)
                    self.openedFilename = filename
                    self.needSaving = False
                    self._modify_title()
                    self.on_processButton_clicked()


    @pyqtSlot()
    def on_actionPreferences_triggered(self):
        """
        Slot documentation goes here.
        """
        cfgDlg = ConfigDialog()
        cfgDlg.exec()


    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        settings = QtCore.QSettings()
        lastWD = settings.value("General/lastWD", QtCore.QStandardPaths.displayName(QtCore.QStandardPaths.HomeLocation))
        fdlg = QtWidgets.QFileDialog(self)
        fdlg.setWindowTitle(_translate("MainWindow", "Enter a file to save into", "File Dialog title"))
        fdlg.setDirectory(lastWD)
        fdlg.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files)
        fdlg.setNameFilters([
            _translate("MainWindow", "PyCirkuit files (*.ckt)", "File filter"),
            _translate("MainWindow", "Any files (*)", "File filter")])
        fdlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
        fdlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fdlg.setViewMode(QtWidgets.QFileDialog.Detail)
        fdlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        if fdlg.exec():
            dst = fdlg.selectedFiles()[0]
            self._save_buffer(dst)
        fdlg.close()


    @pyqtSlot()
    def on_actionSave_triggered(self):
        settings = QtCore.QSettings()
        lastWD = settings.value("General/lastWD", "")
        filePath = lastWD + "/" + self.openedFilename
        if os.path.isfile(filePath):
            self._save_buffer(filePath)
        else:
            self.actionSaveAs.trigger()


    @pyqtSlot()
    def on_exportButton_clicked(self):
        #TODO: Delegate the export itself to the ToolDpic class. Pass it only the path where the source file is
        settings = QtCore.QSettings()
        lastWD = settings.value("General/lastWD")
        src = "{srcFile}".format(srcFile=self.tmpDir .path()+ "/cirkuit_tmp.tikz")
        dst = "{dstFile}".format(dstFile=lastWD+'/'+self.openedFilename.rpartition('.')[0]+".tikz")
        try:    
            if os.path.exists(dst):
                msgBox = QtWidgets.QMessageBox(self)
                msgBox.setWindowTitle(_translate("MessageBox", "Warning",  "Message Box title"))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(_translate("MessageBox", "There's already a file named \"{filename}\" at working directory.", "Message box text. Don't translate '{filename}'").format(filename=self.openedFilename.partition('.')[0]+".tikz"))
                msgBox.setInformativeText(_translate("MessageBox", "Do you want to overwrite it?",  "Message Box text"))
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                saveAsButton = msgBox.addButton(_translate("MessageBox", "Save As...",  "Button text"),  QtWidgets.QMessageBox.AcceptRole)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
                response = msgBox.exec()
                # Overwrite
                if response == QtWidgets.QMessageBox.Yes:
                    copyfile(src, dst)
                    self.exportButton.setEnabled(False)
                # Save with another name (and ask for it first)
                if (response == QtWidgets.QMessageBox.NoButton) and (msgBox.clickedButton() == saveAsButton):
                    fdlg = QtWidgets.QFileDialog(self)
                    fdlg.setWindowTitle(_translate("MainWindow", "Enter a file to save into",  "Window Title"))
                    fdlg.setDirectory(dst)
                    fdlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
                    fdlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
                    fdlg.setViewMode(QtWidgets.QFileDialog.Detail)
                    fdlg.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files)
                    if fdlg.exec():
                        dst = fdlg.selectedFiles()[0]
                    fdlg.close()
                    copyfile(src, dst)
                    self.exportButton.setEnabled(False)
                # Any other option means user doesn't want to overwrite the file -> Exit
            else:
                copyfile(src, dst)
                self.exportButton.setEnabled(False)
        except OSError as e:
            print(_translate("MainWindow", "Export failed:",  "Error message"), e)


    @pyqtSlot()
    def on_processButton_clicked(self):
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
            # STEP1 : Save current WD and set a new one
            savedWD = os.getcwd()
            os.chdir(self.tmpDir.path())
            
            # STEP 2: Establish a temporary file base name to store intermediate results
            tmpFileBaseName = "cirkuit_tmp"
            with open("{baseName}.ckt".format(baseName=tmpFileBaseName), 'w') as tmpFile:
                tmpFile.write(self.sourceText.toPlainText())
            
            # STEP 3: Change cursor shape temporarily
            app = QtWidgets.QApplication.instance()
            app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

            # STEP 4 Call M4: .CKT -> .PIC
            self.statusBar.showMessage(_translate("StatusBar", "Converting: Circuit Macros -> PIC", "Status Bar message"))
            self.extTools['m4'].execute(tmpFileBaseName)

            # STEP 5: Call dpic: .PIC -> .TIKZ
            self.statusBar.showMessage(_translate("StatusBar", "Converting: PIC -> TIKZ", "Status Bar message"))
            self.extTools['dpic'].execute(tmpFileBaseName)

            # STEP 6: Call PDFLaTeX: .TIKZ -> .PDF
            # First we have to embed the .TIKZ code inside a suitable template
            self.statusBar.showMessage(_translate("StatusBar", "Converting: TIKZ -> PDF", "Status Bar message"))
            self.extTools['pdflatex'].execute(tmpFileBaseName)

            # STEP 7: Call pdftoppm to convert the PDF into a bitmap image to visualize it: .PDF -> .PNG
            self.statusBar.showMessage(_translate("StatusBar", "Converting: PDF -> PNG", "Status Bar message"))
            self.extTools['pdftopng'].execute(tmpFileBaseName)

        except PyCktToolExecutionError as err:
            self.imatge.setText("Error!")
            # Open MessageBox and inform user
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle(err.title)
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText(str(err))
            msgBox.setInformativeText(err.moreInfo)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
        else:
            imatge = QtGui.QPixmap("{baseName}.png".format(baseName=tmpFileBaseName))
            self.imatge.setPixmap(imatge)
            # If all went well and we have a generated image, we can 
            self.processButton.setEnabled(False)
            self.exportButton.setEnabled(True)
        finally:
            os.chdir(savedWD)
            self.statusBar.clearMessage()
            app.restoreOverrideCursor()


    @pyqtSlot()
    def on_sourceText_textChanged(self):
        if self.insideConstructor:
            return
        else:
            self.needSaving = True
            self._modify_title()
            self.actionSave.setEnabled(True)
            self.processButton.setEnabled(True)
            self.exportButton.setEnabled(False)
