# -*- coding: utf-8 -*-
"""
Application core functionality
"""
# Copyright (C) 2018-2019 Orestes Mas
# Copyright (C) 2019 Aniol Marti
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
import shutil

# Third-party imports
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QTemporaryDir, QSettings

# Local imports
import pycirkuit
from pycirkuit.exceptions import *
from pycirkuit import Option
from pycirkuit.tools.m4 import ToolM4
from pycirkuit.tools.dpic import ToolDpic
from pycirkuit.tools.pdflatex import ToolPdfLaTeX
from pycirkuit.tools.pdftopng import ToolPdfToPng
from pycirkuit.tools.circuitmacrosmanager import CircuitMacrosManager

# Translation function
_translate = QtCore.QCoreApplication.translate


class PyCirkuitProcessor(QObject):
    TMP_FILE_BASENAME= "cirkuit_tmp"
    def __init__(self):
        self.environmentOk = False
        super().__init__()
        # Save current work dir and change into a temporary one
        self.savedWD = os.getcwd()
        pycirkuit.__tmpDir__ = QTemporaryDir()
        os.chdir(pycirkuit.__tmpDir__.path())
  
    def __del__(self):
        # Restore working dir and remove temporary dir
        os.chdir(self.savedWD)
        pycirkuit.__tmpDir__.remove()

    def _check_latex_template(self):
        settings = QSettings()
        template = settings.value("General/templatePath",  "")
        if os.path.exists(template):
            with open(template, 'r') as t:
                templateCode = t.read()
                if "%%SOURCE%%" in templateCode:
                    return True
                else:
                    raise PyCktLatexTemplateError(_translate("CommandLine", "Found an invalid LaTeX template.", "Error message."))
        else:
            raise PyCktLatexTemplateError(_translate("CommandLine", "LaTeX template not found.", "Error message."))

    def _check_programs(self):
        # Dictionary using a class as index and a class instance as value
        self.extTools = {
            ToolM4: ToolM4(),
            ToolDpic: ToolDpic(), 
            ToolPdfLaTeX: ToolPdfLaTeX(), 
            ToolPdfToPng: ToolPdfToPng()
        }

    def _check_circuit_macros(self):
        cmMgr = CircuitMacrosManager()
        if not cmMgr.check_installed():
            raise PyCktCMNotFoundError(_translate("CommandLine", "Cannot find the Circuit Macros!",  "Command line error message."))

    def checkEnvironment(self):
        self._check_programs()
        self._check_circuit_macros()
        self._check_latex_template()
        self.environmentOk = True

    def beginProcessing(self, src):
        # 1) Check if all tools are installed
        if not self.environmentOk:
            self.checkEnvironment()
        self.tikzExists = self.pdfExists = self.pngExists = self.jpgExists = False
        # Copy source file into temporary file
        self.sourceFile = src
        dst = PyCirkuitProcessor.TMP_FILE_BASENAME + ".ckt"
        shutil.copy(src, dst)

    def copyResult(self, extension):
        # FIXME: SHOULD TEST IF dst IS PRESENT!!!!
        src = os.path.join(pycirkuit.__tmpDir__.path(), PyCirkuitProcessor.TMP_FILE_BASENAME) + os.extsep + extension
        dst = self.sourceFile.rpartition(os.extsep)[0] + os.extsep + extension
        shutil.copy(src, dst)

    def toPng(self, dpi):
        if not self.pngExists:
            self.toPdf()
            self.extTools[ToolPdfToPng].execute(PyCirkuitProcessor.TMP_FILE_BASENAME, resolution=dpi)
            print(" -> PNG ({} dpi)".format(dpi), end="")
            self.pngExists = True
        return True

    def toJpg(self):
        # Check JPEG existance in temporary dir
        # If not, call "toPdf" and then generate jpeg from pdf
        print ("JPEG output format not yet implemented.")
        return False

    def toPdf(self):
        if not self.pdfExists:
            self.toTikz()
            self.extTools[ToolPdfLaTeX].execute(PyCirkuitProcessor.TMP_FILE_BASENAME)
            print(" -> PDF", end="")
            self.pdfExists = True
        return True

    def toTikz(self):
        # Check existance of tikz file in temporary dir
        self.tikzExists = os.path.exists(os.path.join(PyCirkuitProcessor.TMP_FILE_BASENAME, "tikz"))
        if not self.tikzExists:
            self.extTools[ToolM4].execute(PyCirkuitProcessor.TMP_FILE_BASENAME)
            self.extTools[ToolDpic].execute(PyCirkuitProcessor.TMP_FILE_BASENAME)
            print("SRC -> TIKZ".format(self.sourceFile), end="")
            self.tikzExists = True
        return True
