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
from pycirkuit.exceptions import PyCktToolNotFoundError,  PyCktToolExecutionError

# Translation function
_translate = QCoreApplication.translate


class ExternalTool(abc.ABC):
    def __init__(self, execName, longName):
        self.execName = execName
        self.longName = longName
        self.check_tool()
   
    def check_tool(self):
        execPath = os.get_exec_path()
        for testPath in execPath:
            if os.path.exists(testPath + "/{execName}".format(execName=self.execName)):
                print("Found: {execName}\n".format(execName=self.ExecName))
                break
        else:
            raise PyCktToolNotFoundError(self.execName, self.longName)
#            QtWidgets.QMessageBox.critical(self, _translate("MessageBox", "Critical Error", "Message Box title"),  errMsg)

    @abc.abstractmethod
    def execute(self, cmd, errMsg):
        result = subprocess.run(cmd, shell=True, check=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        if result.returncode != 0:
            errMsg += result.stdout.decode()
            raise PyCktToolExecutionError(errMsg)
