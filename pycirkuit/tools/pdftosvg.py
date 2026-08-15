# -*- coding: utf-8 -*-
"""
Module implementing a class to handle the pdf2svg external tool
"""
# Copyright (C) 2018-2026 Orestes Mas
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
from PySide6.QtCore import QCoreApplication

# Local application imports
from pycirkuit.tools.tool_base import ExternalTool

# Translation function
_translate = QCoreApplication.translate


class ToolPdfToSvg(ExternalTool):
    # Class variable
    ID = "PDFTOSVG"

    def __init__(self):
        super().__init__(
            "pdf2svg",
            _translate("ExternalTool", "PDF to SVG image converter", "Tool Long Name"),
        )

    def execute(self, baseName):
        # Calculate src and dst names
        src = baseName + ".pdf"
        dst = baseName + ".svg"
        # pdf2svg writes its output directly to the given destination file,
        # unlike pdftoppm/dpic, so there's no stdout to capture here.
        command = [
            self.executableName,
            "{source}".format(source=src),
            "{destination}".format(destination=dst),
        ]
        errMsg = _translate(
            "ExternalTool", "PDF2SVG: Error converting PDF -> SVG", "Error message"
        )
        super().execute(command, errMsg)
