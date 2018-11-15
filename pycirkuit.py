# coding: utf-8
import sys
import os
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap,QCursor
from PyQt5.QtCore import QTemporaryDir,QStandardPaths,Qt
import mainwindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Inicialització de la IGU
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.obreFitxer)
        self.ui.pushButton.clicked.connect(self.processa)
        self.ui.textEdit.textChanged.connect(self.textCanviat)
        self.needSaving = False
        
        #TODO: gestionar-ho via configuració, per fer-ho permanent. Inicialitzar-ho amb un String desat
        # Last Working Directory (to be persistent)
        cfgPath = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        self.cfgFile = cfgPath + "/pycirkuitrc"
        self.lastWD = "."
        self.lastFilename = ""
        
        #TODO: gestionar la ubicació de les plantilles via configuració
        self.plantilla = ""
        with open('/home/orestes/Devel/Software/pycirkuit/cm_tikz.ckt','r') as f:
            self.plantilla = f.read()

    def obreFitxer(self):
        # Presento el diàleg de càrrega de fitxer
        fitxer, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Títol",self.lastWD,"*.ckt")
        # Ara que tinc la ruta al fitxer complet, n'extrec el directori i me'l deso
        #TODO: Check for valid path (could be a broken link) os.path.exists(path)
        fitxer = os.path.normpath(fitxer)
        self.lastWD,self.lastFilename = os.path.split(fitxer)
        # Change system working dir to target's dir
        os.chdir(self.lastWD)
        with open(self.lastFilename,'r') as f:
            txt = f.read()
            self.ui.textEdit.setPlainText(txt)

    def textCanviat(self):
        if self.ui.textEdit.toPlainText() == "":
            self.ui.pushButton.setEnabled(False)
        else:
            self.ui.pushButton.setEnabled(True)
            self.needSaving = True

    def processa(self):
        # Primer deso la feina no desada
        if self.needSaving:
            with open(self.lastFilename,'w') as f:
                f.write(self.ui.textEdit.toPlainText())
                #TODO: Podria haver-hi un eror en desar el fitxer, aleshores no s'hauria de posar needSaving a False...
                self.needSaving = False
                self.ui.pushButton.setEnabled(False)
        # Creo un directori temporal únic per desar fitxers temporals
        # Si no puc (rar) utilitzo el directori del fitxer font
        d = QTemporaryDir()
        if d.isValid():
            tmpDir = d.path()
        else:
            tmpDir = self.lastWD
        # Sintetitzo un nom de fitxer temporal per desar els fitxers intermedis
        tmpFileBaseName = tmpDir + "/cirkuit_tmp"
        with open("{baseName}.ckt".format(baseName=tmpFileBaseName),'w') as tmpFile:
            tmpFile.write(self.ui.textEdit.toPlainText())
        errMsg = ""
        try:
            # PAS 0: Canvio el cursor momentàniament
            app.setOverrideCursor(QCursor(Qt.WaitCursor))
            # PAS 1: Li passo les M4: .CKT -> .PIC
            command = "m4 -I /home/orestes/.local/share/cirkuit/circuit_macros pgf.m4 {baseName}.ckt > {baseName}.pic".format(baseName=tmpFileBaseName)
            retcode = subprocess.call(command, shell=True)
            if retcode != 0:
                errMsg = "Error en M4: Conversió .CKT -> .PIC"
                raise OSError(errMsg)
            
            # PAS 2: Li passo el dpic: .PIC -> .TIKZ
            command = "dpic -g {baseName}.pic > {baseName}.tikz".format(baseName=tmpFileBaseName)
            retcode = subprocess.call(command, shell=True)
            if retcode != 0:
                errMsg = "Error en DPIC: Conversió .PIC -> .TIKZ"
                raise OSError(errMsg)
            
            # PAS 3: Li passo el PDFLaTeX: .TIKZ -> .PDF
            # Primer haig d'incloure el codi .TIKZ en una plantilla adient
            with open("{baseName}.tikz".format(baseName=tmpFileBaseName),'r') as f, \
                 open('{baseName}.tex'.format(baseName=tmpFileBaseName),'w') as g:
                source = f.read()
                dest = self.plantilla.replace('%%SOURCE%%',source,1)
                # print(dest)
                g.write(dest)
                g.write('\n')
            command = "pdflatex -interaction=batchmode -halt-on-error -file-line-error -output-directory {tmpDir} {baseName}.tex".format(tmpDir=tmpDir, baseName=tmpFileBaseName)
            retcode = subprocess.call(command, shell=True)
            if retcode != 0:
                errMsg = "Error en PDFLaTeX: Conversió .TIKZ -> .PDF"
                raise OSError(errMsg)
            
            # PAS 4: Converteixo el PDF a imatge bitmap per visualitzar-la: .PDF -> .PNG
            command = "pdftoppm {baseName}.pdf -png > {baseName}.png".format(baseName=tmpFileBaseName)
            retcode = subprocess.call(command, shell=True)
            if retcode != 0:
                errMsg = "Error en PDFTOPPM: Conversió .PDF -> .PNG"
                raise OSError(errMsg)
        except OSError as e:
            print("Execution failed:", e)
            self.ui.imatge.setText("Error!")
        else:
            imatge = QPixmap("{baseName}.png".format(baseName=tmpFileBaseName))
            self.ui.imatge.setPixmap(imatge)
        finally:
            app.restoreOverrideCursor()

app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
