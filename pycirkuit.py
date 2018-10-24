# coding: utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import mainwindow
import subprocess
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.obreFitxer)
        self.ui.pushButton.clicked.connect(self.processa)
        self.ui.textEdit.textChanged.connect(self.textCanviat)
        self.plantilla = ""
        with open('/home/orestes/Devel/Software/pycirkuit/cm_tikz.ckt','r') as f:
            self.plantilla = f.read()

    def obreFitxer(self):
        fitxer, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Títol",".","*.ckt")
        with open(fitxer,'r') as f:
            txt = f.read()
            self.ui.textEdit.setPlainText(txt)

    def textCanviat(self):
        if self.ui.textEdit.toPlainText() == "":
            self.ui.pushButton.setEnabled(False)
        else:
            self.ui.pushButton.setEnabled(True)

    def processa(self):
        # Creo un fitxer temporal per desar això
        tmpfile = open("tmp.ckt",'w')
        tmpfile.write(self.ui.textEdit.toPlainText())
        tmpfile.close()
        # Li passo les M4 per convertir-ho a pic
        try:
            command = "m4 -I /home/orestes/.local/share/cirkuit/circuit_macros pgf.m4 tmp.ckt > tmp.pic"
            retcode = subprocess.call(command, shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode)
            else:
                print("Child returned", retcode)
        except OSError as e:
            print("Execution failed:", e)
        # passar-li el dpic per conveertir-ho a tikzs
        try:
            retcode = subprocess.call("dpic -g tmp.pic > tmp.tikz", shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode)
            else:
                print("Child returned", retcode)
        except OSError as e:
            print("Execution failed:", e)
        # Ara genero la imatge passant pel LaTeX
        with open("tmp.tikz",'r') as f:
            source = f.read()
            dest = self.plantilla.replace('%%SOURCE%%',source,1)
            print(dest)
            with open('tmp.tex','w') as g:
                g.write(dest)
                g.write('\n')
                g.close()
            retcode = subprocess.call("pdflatex tmp.tex", shell=True)
            retcode = subprocess.call("pdftoppm tmp.pdf -png > tmp.png", shell=True)
        imatge = QPixmap("tmp.png")
        self.ui.imatge.setPixmap(imatge)

app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
