# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

# Standard library imports
import sys
import os
import subprocess
from shutil import copyfile

# Third-party imports
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets, QtGui

# Local application imports
from .Ui_mainwindow import Ui_MainWindow
from .configdialog import configDialog
#FIXME: Els imports relatius no són bons.
# Cal mirar-se la resposta de l'usuari np8 a https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
sys.path.append("..")
from circuitmacrosmanager import CircuitMacrosManager


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
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # La icona de l'aplicació és al fitxer de recursos
        icon = QtGui.QIcon(":/icons/AppIcon")
        self.setWindowIcon(icon)

        # Connect signals with slots
        #NOTE: Is NOT necessary to MANUALLY connect most signals to slots, as 
        # pyuic5 calls QtCore.QMetaObject.connectSlotsByName in Ui_configdialog.py
        # do do such connections AUTOMATICALLY (so connecting them manually triggers slots twice)

        # Properties regarding the present open file
        self.lastFilename = ""
        self.needSaving = False
 
        # Set up a temporary directory to save intermediate files
        self.tmpDir = QtCore.QTemporaryDir()


    def closeEvent(self,  event):
        self.tmpDir.remove()
        super(QtWidgets.QMainWindow, self).closeEvent(event)


    @pyqtSlot()
    def on_processButton_clicked(self):
        # Comprovo si tinc totes les aplicacions necessàries correctament instal·lades
        if not self.check_programs():
            return
        
        # Comprovo si tenim les Circuit Macros a la carpeta especificada als Settings
        if not self.check_circuit_macros():
            return
        
        # Comprovo si el fitxer de plantilla existeix i és vàlid
        if not self.check_templates():
            return

        # Començo: Primer deso la feina no desada
        if self.needSaving:
            try:
                f = open(self.lastFilename,'w', encoding='UTF-8')
                f.write(self.sourceText.toPlainText())
            except OSError as e:
                errMsg = "S'ha produït un error en desar el fitxer font: " + e.strerror + ".\n\n"
                errMsg += "No es pot processar el circuit."
                QtWidgets.QMessageBox.critical(self, "Error crític",  errMsg)
                return
            else:
                self.needSaving = False
                self.processButton.setEnabled(False)
            finally:
                f.close()

        # Instantiate a settings object to load config values. At this point the config have valid entries, so don't test much
        settings = QtCore.QSettings()
        cmPath = settings.value("General/cmPath") 
        # Sintetitzo un nom de fitxer temporal per desar els fitxers intermedis
        tmpFileBaseName = self.tmpDir .path()+ "/cirkuit_tmp"
        with open("{baseName}.ckt".format(baseName=tmpFileBaseName), 'w') as tmpFile:
            tmpFile.write(self.sourceText.toPlainText())
        errMsg = ""
        try:
            # PAS 0: Canvio el cursor momentàniament
            app = QtWidgets.QApplication.instance()
            app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            # PAS 1: Li passo les M4: .CKT -> .PIC
            # La crida subprocess.run() és molt interessant
            # el 'check=False' fa que no salti una excepció si l'ordre falla, atès que ja la llanço jo després
            # amb un missatge més personalitzat
            command = "m4 -I {cmPath} pgf.m4 {baseName}.ckt > {baseName}.pic".format(cmPath=cmPath,  baseName=tmpFileBaseName)
            result = subprocess.run(command, shell=True, check=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            if result.returncode != 0:
                errMsg = "Error en M4: Conversió .CKT -> .PIC\n"
                errMsg += result.stdout.decode()
                raise OSError(errMsg)

            # PAS 2: Li passo el dpic: .PIC -> .TIKZ
            command = "dpic -g {baseName}.pic > {baseName}.tikz".format(baseName=tmpFileBaseName)
            result = subprocess.run(command, shell=True, check=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            if result.returncode != 0:
                errMsg = "Error en DPIC: Conversió .PIC -> .TIKZ\n"
                errMsg += result.stdout.decode()
                raise OSError(errMsg)

            # PAS 3: Li passo el PDFLaTeX: .TIKZ -> .PDF
            # Primer haig d'incloure el codi .TIKZ en una plantilla adient
            latexTemplateFile = settings.value("General/latexTemplateFile")
            templateCode = ""
            with open("{templateFile}".format(templateFile=latexTemplateFile), 'r') as template:
                templateCode = template.read()        
            with open("{baseName}.tikz".format(baseName=tmpFileBaseName), 'r') as f, \
                     open('{baseName}.tex'.format(baseName=tmpFileBaseName), 'w') as g:
                source = f.read()
                dest = templateCode.replace('%%SOURCE%%', source, 1)
                g.write(dest)
                g.write('\n')
            command = "pdflatex -interaction=batchmode -halt-on-error -file-line-error -output-directory {tmpDir} {baseName}.tex".format(tmpDir=self.tmpDir.path(), baseName=tmpFileBaseName)
            result = subprocess.run(command, shell=True, check=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            if result.returncode != 0:
                errMsg = "Error en PDFLaTeX: Conversió .TIKZ -> .PDF\n"
                ###### TODO: NO-PORTABLE!! Només funciona en entorns on existeixi el GREP
                ###### Es pot mirar d'usar el mòdul "re" (regular expressions) de python, però és complicadot
                ###### El que he après fins ara és:
                ###### 1) Cal passar -interaction=nonstopmode al pdflatex perquè tregui el log per STDOUT
                ###### 2) Cal muntar-se una cadena que faci d'expressió regular quelcom del tipus "^{baseName}.tex:[0-9]+:"
                ###### 3) Potser cal escapar caràcters d'aquesta cadena amb re.escape()
                ###### 4) potser usar re.search(regexp.log) o re.match(regexp,log) per cercar. "log" és result.stdout.decode('UTF-8')
                ###### 5) En acabat encara caldria recuperar 2 línies de context posterior per tal de saber l'error
                # Explorem el LOG de LaTeX amb el GREP extern per saber l'error
                # (amb l'opció -file-line-error el format del missatge és fitxer:línia:error)
                # Opcions del grep-> -A 2: 2 línies de context posterior, -m 1: només 1 concordança, -a: ascii text (no binari)
                command = 'grep -A 2 -m 1 -a --color=always "^{baseName}.tex:" {baseName}.log'.format(baseName=tmpFileBaseName)
                result = subprocess.run(command, shell=True, check=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                if result.returncode == 0:
                    errMsg += result.stdout.decode()
                else:
                    errMsg += "No s'ha pogut determinar l'error del LaTeX"
                raise OSError(errMsg)

            # PAS 4: Converteixo el PDF a imatge bitmap per visualitzar-la: .PDF -> .PNG
            command = "pdftoppm {baseName}.pdf -png > {baseName}.png".format(baseName=tmpFileBaseName)
            result = subprocess.run(command, shell=True, check=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            if result.returncode != 0:
                errMsg = "Error en PDFTOPPM: Conversió .PDF -> .PNG\n"
                errMsg += result.stdout.decode()
                raise OSError(errMsg)
        except OSError as e:
            print("Execution failed:", e)
            self.imatge.setText("Error!")
            # TODO: Es podria posar el missatge d'error al mateix widget on surt la imatge...
        else:
            imatge = QtGui.QPixmap("{baseName}.png".format(baseName=tmpFileBaseName))
            self.imatge.setPixmap(imatge)
            # If all went well and we have a generated image, we can 
            self.exportButton.setEnabled(True)
        finally:
            app.restoreOverrideCursor()

  
    @pyqtSlot()
    def on_exportButton_clicked(self):
        settings = QtCore.QSettings()
        lastWD = settings.value("General/lastWD")
        src = "{srcFile}".format(srcFile=self.tmpDir .path()+ "/cirkuit_tmp.tikz")
        dst = "{dstFile}".format(dstFile=lastWD+'/'+self.lastFilename.partition('.')[0]+".tikz")
        try:    
            if os.path.exists(dst):
                msgBox = QtWidgets.QMessageBox(self)
                msgBox.setWindowTitle("Avís")
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText("Ja existeix un fitxer de nom «{filename}» al directori de treball.".format(filename=self.lastFilename.partition('.')[0]+".tikz"))
                msgBox.setInformativeText("Voleu sobreescriure'l?")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                saveAsButton = msgBox.addButton("Desa com a...",  QtWidgets.QMessageBox.AcceptRole)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
                response = msgBox.exec()
                # Overwrite
                if response == QtWidgets.QMessageBox.Yes:
                    copyfile(src, dst)
                    self.exportButton.setEnabled(False)
                # Save with another name (and ask for it first)
                if (response == QtWidgets.QMessageBox.NoButton) and (msgBox.clickedButton() == saveAsButton):
                    fdlg = QtWidgets.QFileDialog(self)
                    fdlg.setWindowTitle("Enter a file to save into")
                    fdlg.setDirectory(dst)
                    fdlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
                    fdlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
                    fdlg.setViewMode(QtWidgets.QFileDialog.Detail)
                    fdlg.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files )
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
            print("Export failed:", e)
    
    
    @pyqtSlot()
    def on_sourceText_textChanged(self):
        if self.sourceText.toPlainText() == "":
            self.processButton.setEnabled(False)
        else:
            self.processButton.setEnabled(True)
            self.needSaving = True
        self.exportButton.setEnabled(False)


    @pyqtSlot()
    def on_actionOpen_triggered(self):
        # Instantiate a settings object
        settings = QtCore.QSettings()
        
        # Presento el diàleg de càrrega de fitxer
        fdlg = QtWidgets.QFileDialog(self)
        fdlg.setWindowTitle("Open Source File")
        fdlg.setDirectory(settings.value("General/lastWD",  ""))
        fdlg.setNameFilters(["PyCirkuit files (*.ckt)",  "TeX files (*.tex)",  "Any files (*)"])
        fdlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        fdlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog | QtWidgets.QFileDialog.ReadOnly)
        fdlg.setViewMode(QtWidgets.QFileDialog.Detail)
        fdlg.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
        fitxer = ""
        if fdlg.exec():
            fitxer = fdlg.selectedFiles()[0]
        fdlg.close()
        
        # Comprovo que no he premut 'Cancel' a la dialog box...
        if fitxer != "":
            # Comprovo que el fitxer no sigui un enllaç trencat
            fitxer = os.path.normpath(fitxer)
            if os.path.exists(fitxer):
                lastWD, self.lastFilename = os.path.split(fitxer)
                # Change system working dir to target's dir
                os.chdir(lastWD)
                settings.setValue("General/lastWD", lastWD)
                settings.sync()
                with open(self.lastFilename, 'r') as f:
                    txt = f.read()
                    self.sourceText.setPlainText(txt)
                    self.setWindowTitle("PyCirkuit - {filename}".format(filename=self.lastFilename))
                    self.on_processButton_clicked()


    @pyqtSlot()
    def on_actionAbout_triggered(self):
        """
        Slot documentation goes here.
        """
        txt = "Copyright (c) 2018 Orestes Mas\n\n"\
                 "PyCirkuit is a compiler/renderer of circuit diagrams written using the Dwight Aplevich's 'Circuit Macros'.\n"\
                 "Being written in python, the code and ideas are largely based on 'cirkuit' C++ program, by Matteo Agostinelli.\n"
        QtWidgets.QMessageBox.about(self,  "About PyCirkuit",  txt)

    
    @pyqtSlot()
    def on_actionPreferences_triggered(self):
        """
        Slot documentation goes here.
        """
        cfgDlg = configDialog()
        cfgDlg.exec()


    def check_programs(self):
        programs = (
            {"progName": "m4",  "errMsg": "processador de macros «M4»"},
            {"progName": "dpic",  "errMsg": "compilador de llenguatge «PIC»"},
            {"progName": "pdflatex",  "errMsg": "programa pdfLaTeX"},
            {"progName": "pdftoppm",  "errMsg": "conversor d'imatges PDF a PNG"},
        )
        execPath = os.get_exec_path()
        for p in programs:
            for testPath in execPath:
                if os.path.exists(testPath + "/{progName}".format(progName=p["progName"])):
                    print("Found: {prg}\n".format(prg=p["progName"]))
                    break
            else:
                txt  = "No s'ha trobat el {msg}!\n\n"
                txt += "Assegureu-vos de tenir aquesta aplicació correctament instal·lada i l'executable «{execName}» al PATH.\n\n"
                txt += "No es pot processar el circuit."
                txt  = txt.format(msg=p["errMsg"],  execName=p["progName"])
                QtWidgets.QMessageBox.critical(self, "Error crític",  txt)
                return False
        return True


    def check_circuit_macros(self):
        settings = QtCore.QSettings()
        cmPath = settings.value("General/cmPath",  "")
        if os.path.exists(cmPath + "/libcct.m4"):
            return True
        else:
            txt  = "No s'han trobat les «Circuit Macros»!\n\n"
            txt += "Voleu provar de cercar-les i instal·lar-les automàticament?"
            response = QtWidgets.QMessageBox.question(self, "Error",  txt,  defaultButton = QtWidgets.QMessageBox.Yes)
            result = False
            if response == QtWidgets.QMessageBox.Yes:
                try:
                    app = QtWidgets.QApplication.instance()
                    app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
                    cmMgr = CircuitMacrosManager(self)
                    cmMgr.download_latest()
                    cmMgr.unpack_circuit_macros()
                    result = True
                except:
                    pass
                finally:
                    app.restoreOverrideCursor()
            else:
                txt  = "No s'han trobat les «Circuit Macros»!\n\n"
                txt += "Si us plau, indiqueu-ne la ruta correcta als arranjaments.\n\n"
                txt += "No es pot processar el circuit."
                QtWidgets.QMessageBox.critical(self, "Error crític",  txt)
            return result

    
    def check_templates(self):
        pass
        settings = QtCore.QSettings()
        template = settings.value("General/latexTemplateFile",  "")
        if os.path.exists(template):
            with open(template, 'r') as t:
                templateCode = t.read()
                if "%%SOURCE%%" in templateCode:
                    return True
                else:
                    txt  = "La plantilla LaTeX especificada no sembla vàlida!\n\n"
                    txt += "Si us plau, indiqueu-ne una de correcta als arranjaments.\n\n"
                    txt += "No es pot processar el circuit."
                    QtWidgets.QMessageBox.critical(self, "Error crític",  txt)
                    return False
        else:
            txt  = "No s'ha trobat la plantilla LaTeX!\n\n"
            txt += "Si us plau, indiqueu-ne la ruta correcta als arranjaments.\n\n"
            txt += "No es pot processar el circuit."
            QtWidgets.QMessageBox.critical(self, "Error crític",  txt)
            return False

