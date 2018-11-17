# coding: utf-8
import sys
import os
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap,QCursor,QIcon
from PyQt5.QtCore import Qt,QSettings
from PyQt5.QtCore import QTemporaryDir,QDir
from ui import mainwindow
from resources import resources

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # La icona de l'aplicació és al fitxer de recursos
        icon = QIcon(":/icons/AppIcon")
        self.setWindowIcon(icon)
        # Inicialització de la IGU
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.obreFitxer)
        self.ui.pushButton.clicked.connect(self.processa)
        self.ui.textEdit.textChanged.connect(self.textCanviat)
        self.needSaving = False
        
        # Persistent settings
        self.settings = QSettings("UPC","pycirkuit")
        # Last Working Dir
        d = QDir(self.settings.value("General/lastWD","."))
        self.lastWD = d.absolutePath() if d.exists() else QDir.home().path()
        self.lastFilename = ""
        #TODO: gestionar la ubicació de les plantilles via configuració
        self.plantilla = ""
        with open('/home/orestes/Devel/Software/pycirkuit/cm_tikz.ckt','r') as f:
            self.plantilla = f.read()

    def obreFitxer(self):
        # Presento el diàleg de càrrega de fitxer
        fitxer, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Títol",self.lastWD,"*.ckt")
        # Comprovo que no he premut 'Cancel' a la dialog box...
        if fitxer != '':
            # Comprovo que el fitxer no sigui un enllaç trencat
            fitxer = os.path.normpath(fitxer)
            if os.path.exists(fitxer):
                self.lastWD,self.lastFilename = os.path.split(fitxer)
                # Change system working dir to target's dir
                os.chdir(self.lastWD)       
                self.settings.setValue("General/lastWD", self.lastWD)
                self.settings.sync()
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
            with open(self.lastFilename,'w',encoding='UTF-8') as f:
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
            # TODO: Cal que la ubicació de les Circuit_Macros no estigui "hard-coded"
            #
            # La crida subprocess.run() és molt interessant
            # el 'check=False' fa que no salti una excepció si l'ordre falla, atès que ja la llanço jo després
            # amb un missatge més personalitzat
            command = "m4 -I /home/orestes/.local/share/cirkuit/circuit_macros pgf.m4 {baseName}.ckt > {baseName}.pic".format(baseName=tmpFileBaseName)
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
            with open("{baseName}.tikz".format(baseName=tmpFileBaseName),'r') as f, \
                 open('{baseName}.tex'.format(baseName=tmpFileBaseName),'w') as g:
                source = f.read()
                dest = self.plantilla.replace('%%SOURCE%%',source,1)
                g.write(dest)
                g.write('\n')
            command = "pdflatex -interaction=batchmode -halt-on-error -file-line-error -output-directory {tmpDir} {baseName}.tex".format(tmpDir=tmpDir, baseName=tmpFileBaseName)
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
            self.ui.imatge.setText("Error!")
            # TODO: Es podria posar el missatge d'error al mateix widget on surt la imatge...
        else:
            imatge = QPixmap("{baseName}.png".format(baseName=tmpFileBaseName))
            self.ui.imatge.setPixmap(imatge)
        finally:
            app.restoreOverrideCursor()

app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
