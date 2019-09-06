# -*- coding: utf-8 -*-
"""
Module implementing a class to handle the dpic external tool
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

# Standard library imports
from os.path import *

# Third-party imports
from PyQt5.QtCore import QCoreApplication, QStandardPaths

# Local application imports
from pycirkuit import Option
from pycirkuit.tools.tool_base import ExternalTool, PyCktDocNotFoundError

# Translation function
_translate = QCoreApplication.translate

class ToolDpic(ExternalTool):
    # Class variable
    ID = 'DPIC'
    def __init__(self):
        super().__init__("dpic", _translate("ExternalTool", "'PIC' language compiler", "Tool Long Name"))
        
    def execute(self, baseName,  outputType = Option.TIKZ):
        # Calculate src and dst names
        src = baseName + '.pic'
        if outputType == Option.TIKZ:
            dst = baseName + '.tikz'
            flag = '-g'
        elif outputType == Option.SVG:
            dst = baseName + '.svg'
            flag = '-v'
        #NOTE: We add the '-z' flag to always execute dpic in "safe mode"
        # Instantiate a settings object to load config values. At this point the config have valid entries, so don't test much
        command = [self.executableName, flag, '-z', "{source}".format(source=src)]
        errMsg = _translate("ExternalTool", "DPIC: Error converting PIC -> TIKZ", "Error message")
        super().execute(command, errMsg, destination=dst)
        
    def getManUrl(self):
        import glob
        try:
            import magic
        except ImportError:
            raise PyCirkuitError(_translate("ExternalTool", "Module 'python-magic' not found. Please check that all PyCirkuit dependencies are correctly installed.",  "Error message"))
        mime = magic.Magic(mime=True)   # Prepare to detect a file's mimetype based on its contents
        # Get standard locations for documentation in a platform-independent way
        dirList = QStandardPaths.standardLocations(QStandardPaths.GenericDataLocation)
        # Append specific app subdir to each possible location
        dirList = [normpath(join(dir, "doc", "dpic")) for dir in dirList]
        # Explore the generated list searching for pdf or compressed pdf
        for testPath in dirList:
            # Perhaps we should search for *.pdf* or, at least, for *.pdf AND *.pdf.gz
            candidates = glob.glob(join(testPath, "dpic-doc.pdf"))
            candidates.extend(glob.glob(join(testPath, "dpic-doc.pdf.gz")))
            for candidate in candidates:
                mimeType = mime.from_file(candidate)
                if (mimeType == "application/pdf") or (mimeType == "application/gzip"):
                    return(candidate)
        else:
            err = PyCktDocNotFoundError("dpic")
            # Add the list of possible locations to 'moreinfo' message's box variable
            info = err.moreInfo + '\n'.join(dirList)
            err.moreInfo = info
            raise err

