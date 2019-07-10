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

# Third-party imports
from PyQt5.QtCore import QObject, QTemporaryDir

# Local imports
import pycirkuit
from pycirkuit import Option, imageParam
from pycirkuit.tools.m4 import ToolM4
from pycirkuit.tools.dpic import ToolDpic
from pycirkuit.tools.pdflatex import ToolPdfLaTeX
from pycirkuit.tools.pdftopng import ToolPdfToPng


class PyCirkuitProcessor(QObject):
    def __init__(self, imageParams=None):
        #FIXME: imageParams: Should read params from settings if invoked without them????
        self.imageParams = imageParams
        super().__init__()
        pycirkuit.__tmpDir__ = QTemporaryDir()
        # SET UP environment:
        # 1) Check if all tools are installed
        self._check_programs()
        # 2) enforce circuit macros
        # 3) check templates
        # 4) Save current WD and set a new one
        # 5) Establish a temporary file base name to store intermediate results
    
    def __del__(self):
        print("DEBUG: In «processor» destructor. Removing tmpdir.")
        pycirkuit.__tmpDir__.remove()

    def _check_templates(self):
        pass

    def _check_programs(self):
        # Dictionary using a class as index and a class instance as value
        self.extTools = {
            ToolM4: ToolM4(),
            ToolDpic: ToolDpic(), 
            ToolPdfLaTeX: ToolPdfLaTeX(), 
            ToolPdfToPng: ToolPdfToPng()
        }

    def _enforce_circuit_macros(self):
        pass

    def toPng(self):
        # Check PNG existance in temporary dir
        print("Checking existance of png into temporary dir... ", end="")
        # If not, call "toPdf" and then generate png from pdf
        if not self.pngExists:
            print("Not found!")
            self.toPdf()
            print("Converted pdf into png format at {} dpi".format(self.imageParams[Option.DPI]))
            self.pngExists = True
        else:
            print("Found!")
        return True

    def toJpg(self):
        # Check JPEG existance in temporary dir
        # If not, call "toPdf" and then generate jpeg from pdf
        print ("JPEG output format not yet implemented.")
        return False

    def toPdf(self):
        # Check PDF existance in temporary dir
        print("Checking existance of pdf into temporary dir... ", end="")
        # If not, call "toTikz" and then generate pdf from tikz
        if not self.pdfExists:
            print("Not found!")
            self.toTikz()
            print("Converted tikz into pdf format")
            self.pdfExists = True
        else:
            print("Found!")
        return True

    def toTikz(self):
        # Check existance of tikz file in temporary dir
        print("Checking existance of tikz into temporary dir... ", end="")
        if not self.tikzExists:
            print("Not found!")
            print("Converted {} to tikz format...".format(self.fileName))
            self.tikzExists = True
        else:
            print("Found!")
        return True

    def setSourceFile(self, filename):
        self.pngExists = self.pdfExists = self.tikzExists = False
        self.fileName = filename
        # Copy filename to temporary file
        print("Copying {} into temporary location".format(filename))
