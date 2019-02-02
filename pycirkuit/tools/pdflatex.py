# -*- coding: utf-8 -*-
"""
Module implementing a class to handle the pdflatex external tool
"""
# Copyright (C) 2018 Orestes Mas
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
import re

# Third-party imports
from PyQt5.QtCore import QCoreApplication,  QSettings

# Local application imports
from pycirkuit.tools.tool_base import ExternalTool, PyCktToolExecutionError

# Translation function
_translate = QCoreApplication.translate

class ToolPdfLaTeX(ExternalTool):
    def __init__(self):
        super().__init__("pdflatex", _translate("ExternalTool", "pdfLaTeX program", "Tool Long Name"))
        
    def execute(self, baseName):
        # Calculate src and dst names
        tikz = baseName + '.tikz'
        tex = baseName + '.tex'
        # Instantiate a settings object to load config values. At this point the config have valid entries, so don't test much
        settings = QSettings()
        latexTemplateFile = settings.value("General/latexTemplateFile")
        # Now we read a LaTeX template and wrap the tikz code inside
        templateCode = ""
        with open("{templateFile}".format(templateFile=latexTemplateFile), 'r') as template:
            templateCode = template.read()        
        with open("{source}".format(source=tikz), 'r') as f, \
             open('{destination}'.format(destination=tex), 'w') as g:
            source = f.read()
            dest = templateCode.replace('%%SOURCE%%', source, 1)
            g.write(dest)
            g.write('\n')
        # Execution of pdfLaTeX creates a PDF file
        command = [self.executableName, "-interaction=batchmode", "-halt-on-error", "{texFile}".format(texFile=tex)]
        errMsg = _translate("ExternalTool", "PDFLaTeX: Error converting TIKZ -> PDF", "Error message")
        try:
            super().execute(command, errMsg)
        except PyCktToolExecutionError as err:
            # If a LaTeX error has been triggered, try to obtain a meaningful error message
            # Very useful: https://regex101.com/#python
            info = ""
            with open("{basename}.log".format(basename=baseName),'r') as log:
                expr = "! (\S.*$)|l\.([0-9]+) (.*$)"
                prog = re.compile(expr)
                for line in log:
                    # 'match' searches from line beginning
                    match = prog.match(line)
                    if match:
                        if match.group(0)[0] == 'l':
                            #TODO: Perhaps we can return some info (error string?) to allow spotting the error at the source file
                            info = _translate("ExternalTool", "Error at TeX file line number {N}".format(N=match.group(2)), "Error message. Don't translate '{N}'") + '\n'
                            info += match.group(3) + '\n'
                        else:
                            info += match.group(1) + '\n'
            err.moreInfo = info
            raise err
