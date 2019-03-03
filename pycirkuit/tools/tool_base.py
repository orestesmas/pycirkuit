# -*- coding: utf-8 -*-
"""
Module implementing an abstract class to handle external tools
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
import abc
import os
import subprocess
import inspect
import platform

# Third-party imports
from PyQt5.QtCore import QCoreApplication

# Local application imports
import pycirkuit
from pycirkuit.exceptions import *

# Translation function
_translate = QCoreApplication.translate

# Base class for external tools
class ExternalTool(abc.ABC):
    # Class variable
    ID = ""
    def __init__(self, executableName, longName):
        self.longName = longName
        execPath = os.get_exec_path()

        # Windows-specific
        if platform.system() == 'Windows':
            # Append '.exe' to the executable name we're searching
            executableName = executableName + '.exe'
            # Also, we add an entry to the executable search path pointing to our "lib" dir
            libDir = os.path.dirname(inspect.getfile(pycirkuit))
            libDir = os.path.join(libDir, 'lib')
            execPath.append(libDir)
 
        for testPath in execPath:
            p = os.path.join(testPath, "{execName}".format(execName=executableName))
            if os.path.exists(p):
                self.execPath = testPath
                self.executableName = os.path.join(testPath,  executableName)
                return
        else:
            raise PyCktToolNotFoundError(executableName, self.longName)

    @abc.abstractmethod
    def execute(self, cmd, errMsg, destination=None):
        try:
            # Invoke external tool to do the job
            # For tools that give their output to STDOUT, we capture it and write contents to a file later
            result = subprocess.run(cmd, shell=False, check=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if result.returncode != 0:
                info = result.stderr.decode()
                # By calling self.ID we use polymorphism here
                raise PyCktToolExecutionError(errMsg, moreInfo=info, tool=self.__class__)
            else:
                if destination != None:
                    with open(destination, 'wb') as tmpFile:
                        tmpFile.write(result.stdout)
        except PyCktToolExecutionError as err:
            raise err
