# coding: utf-8
"""
Module implementing the functions to run when a command option is called
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
import glob
import sys

# Third-party imports
from PyQt5.QtCore import QCoreApplication

# Translation function
_translate = QCoreApplication.translate

class CommandLineOptions():
    # Class constructor.
    def __init__(self, parser, option, paths):
        self.parser = parser
        self.option = option
        if len(paths) == 0:
            print(_translate("CommandLine", "ERROR: Batch processing requested with no files.", "Commandline error message"))
            parser.showHelp(exitCode=-1)
        else:
            self.paths = paths

    # Operational methods.
    def setOption(self, option):
        self.option = option

    # Check integer params.
    def check_int_param(self, param, value):
        try:
            if param == "quality":
                if int(value) not in range(0, 100):
                    raise Exception()
            return int(value)
        except:
            print(_translate("CommandLine", "Error: The --" + param + " parameter must be an integer.", "Error message"))
            sys.exit(-1)

    # Command line methods. All return a list of the files processed.
    def png(self, dpi):
        dpi = self.check_int_param("dpi", dpi)
        # Check PDF existance.
        print("Option '-p' detected. Files to process: ")
        print (self.paths)
        # Here create the PNG files.

    def jpg(self, dpi, quality):
        dpi = self.check_int_param("dpi", dpi)
        quality = self.check_int_param("quality", quality)
        # Check PDF existance.
        print("Option '-j' detected. Files to process: ")
        print (self.paths)
        # Here create the JPG files.

    def pdf(self):
        # Check TIKZ existance.
        print ("PDF")

    def tikz(self):
        print("Option '-t' not yet implemented. Exiting.")    
        sys.exit(-1)
