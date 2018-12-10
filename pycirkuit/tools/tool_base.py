# -*- coding: utf-8 -*-
"""
Module implementing an abstract class to handle external tools
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
import abc
import os
import subprocess

# Third-party imports
from PyQt5.QtCore import QCoreApplication

# Local application imports
from pycirkuit.exceptions import PyCirkuitError

# Translation function
_translate = QCoreApplication.translate

# Own exceptions
class PyCktToolExecutionError(PyCirkuitError):
    def __init__(self, message):
        super().__init__(message)
        self.title=_translate("ExternalTool", "Tool Execution Error", "Exception title")


class PyCktToolNotFoundError(PyCirkuitError):
    def __init__(self, executableName, longName):
        errMsg = _translate("ExternalTool", "Cannot find the {toolLongName}!\n\n", "Leave untranslated the variable name inside curly braces (included)")
        errMsg += _translate("ExternalTool", "Please ensure that you have this application properly installed and the executable \"{toolExecutableName}\" is in the PATH.\n\n", "Leave untranslated the variable name inside curly braces (included)")
        errMsg += _translate("ExternalTool", "Cannot generate the preview.")
        errMsg = errMsg.format(toolLongName=longName,  toolExecutableName=executableName)
        super().__init__(errMsg)
        self.title=_translate("ExternalTool", "Tool Not Found Error", "Exception title")


# Base class for external tools
class ExternalTool(abc.ABC):
    def __init__(self, executableName, longName):
        self.executableName = executableName
        self.longName = longName
        self.check_tool()
   
    def check_tool(self):
        execPath = os.get_exec_path()
        for testPath in execPath:
            if os.path.exists(testPath + "/{executableName}".format(executableName=self.executableName)):
                print("Found: {executableName}\n".format(executableName=self.executableName))
                break
        else:
            raise PyCktToolNotFoundError(self.executableName, self.longName)

    @abc.abstractmethod
    def execute(self, cmd, errMsg):
        # La crida subprocess.run() és molt interessant
        # el 'check=False' fa que no salti una excepció si l'ordre falla, atès que ja la llanço jo després
        # amb un missatge més personalitzat
        result = subprocess.run(cmd, shell=True, check=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        if result.returncode != 0:
            errMsg += result.stdout.decode()
            raise PyCktToolExecutionError(errMsg)
