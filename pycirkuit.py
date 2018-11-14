# coding: utf-8
import sys
import os
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTemporaryDir
from PyQt5.QtCore import QStandardPaths
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
            f.close()

    def textCanviat(self):
        if self.ui.textEdit.toPlainText() == "":
            self.ui.pushButton.setEnabled(False)
        else:
            self.ui.pushButton.setEnabled(True)

    def processa(self):
        # Primer deso la feina no desada
        with open(self.lastFilename,'w') as f:
            f.write(self.ui.textEdit.toPlainText())
            f.close()
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
            tmpFile.close()
        # Li passo les M4 per convertir-ho a pic
        try:
            command = "m4 -I /home/orestes/.local/share/cirkuit/circuit_macros pgf.m4 {baseName}.ckt > {baseName}.pic".format(baseName=tmpFileBaseName)
            retcode = subprocess.call(command, shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode)
            else:
                print("Child returned", retcode)
        except OSError as e:
            print("Execution failed:", e)
        # passar-li el dpic per convertir-ho a tikzs
        try:
            retcode = subprocess.call("dpic -g {baseName}.pic > {baseName}.tikz".format(baseName=tmpFileBaseName), shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode)
            else:
                print("Child returned", retcode)
        except OSError as e:
            print("Execution failed:", e)
        # Ara genero la imatge passant pel LaTeX
        with open("{baseName}.tikz".format(baseName=tmpFileBaseName),'r') as f:
            source = f.read()
            dest = self.plantilla.replace('%%SOURCE%%',source,1)
            print(dest)
            with open('{baseName}.tex'.format(baseName=tmpFileBaseName),'w') as g:
                g.write(dest)
                g.write('\n')
                g.close()
            retcode = subprocess.call("pdflatex --output-directory {tmpDir} {baseName}.tex".format(tmpDir=tmpDir, baseName=tmpFileBaseName), shell=True)
            retcode = subprocess.call("pdftoppm {baseName}.pdf -png > {baseName}.png".format(baseName=tmpFileBaseName), shell=True)
        imatge = QPixmap("{baseName}.png".format(baseName=tmpFileBaseName))
        self.ui.imatge.setPixmap(imatge)

app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
