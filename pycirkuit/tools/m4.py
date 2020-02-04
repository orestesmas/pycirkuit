# -*- coding: utf-8 -*-
"""
Module implementing a class to handle the M4 external tool
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


# Third-party imports
from PyQt5.QtCore import QCoreApplication, QSettings

# Local application imports
from pycirkuit.tools.tool_base import ExternalTool

# Translation function
_translate = QCoreApplication.translate

class ToolM4(ExternalTool):
    # Class variable
    ID = 'M4'
    def __init__(self):
        super().__init__("m4", _translate("ExternalTool", "'M4' Macro Processor", "Tool Long Name"))
        
    def execute(self, baseName):
        # Calculate src and dst names
        src = baseName + '.ckt'
        dst = baseName + '.pic'
        # Instantiate a settings object to load config values. At this point the config have valid entries, so don't test much
        settings = QSettings()
        cmPath = settings.value("General/cmPath") 
        srcPath = settings.value("General/lastSrcDir")
        command = [self.executableName , "-I", "{cmPath}".format(cmPath=cmPath),  "-I", "{srcPath}".format(srcPath=srcPath), "pgf.m4",  "{source}".format(source=src)]
        errMsg = _translate("ExternalTool", "M4: Error converting CKT -> PIC",  "Error message")
        super().execute(command, errMsg, destination=dst)
