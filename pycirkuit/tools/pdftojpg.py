# -*- coding: utf-8 -*-
"""
Module implementing a class to handle the pdftoppm external tool
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

# System library imports
from os import extsep

# Third-party imports
from PyQt5.QtCore import QCoreApplication

# Local application imports
from pycirkuit.tools.tool_base import ExternalTool

# Translation function
_translate = QCoreApplication.translate

class ToolPdfToJpeg(ExternalTool):
    # Class variable
    ID = 'PDFTOJPG'
    def __init__(self):
        super().__init__("pdftoppm", _translate("ExternalTool", "PDF to JPEG image converter", "Tool Long Name"))
        
    def execute(self, baseName, resolution=150, quality=100):
        # Calculate src and dst names
        src = baseName + extsep + "pdf"
        dst = baseName + extsep + "jpeg"
        # Instantiate a settings object to load config values. At this point the config have valid entries, so don't test much
        command = [self.executableName, "-jpeg", "-jpegopt", "quality={q}".format(q=quality), "-r", "{ppp}".format(ppp=resolution), "{source}".format(source=src)]
        errMsg = _translate("ExternalTool", "PDFTOPPM: Error converting PDF -> JPEG", "Error message")
        super().execute(command, errMsg, destination=dst)
