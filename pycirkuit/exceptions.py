# -*- coding: utf-8 -*-
"""
Module implementing the PyCirkuit exceptions
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

# Third-party imports
from PyQt5.QtCore import QCoreApplication

# Translation function
_translate = QCoreApplication.translate

class PyCirkuitError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.title=_translate("PyCirkuitError", "PyCirkuit Error",  "Exception title")
#        self.msg=message

class PyCktToolExecutionError(PyCirkuitError):
    def __init__(self, message):
        super().__init__(message)
        self.title=_translate("ExternalTool", "Tool Execution Error", "Exception title")

class PyCktToolNotFoundError(PyCirkuitError):
    def __init__(self, execName, longName):
        errMsg = _translate("MessageBox", "Cannot find the {toolLongName}!\n\n", "Leave untranslated the variable name inside curly braces (included)")
        errMsg += _translate("MessageBox", "Please ensure that you have this application properly installed and the executable \"{toolExecName}\" is in the PATH.\n\n", "Leave untranslated the variable name inside curly braces (included)")
        errMsg += _translate("MessageBox", "Cannot generate the preview.")
        errMsg = errMsg.format(toolLongName=longName,  toolExecName=execName)
        super().__init__(errMsg)
        self.title=_translate("ExternalTool", "Tool Not Found Error", "Exception title")
