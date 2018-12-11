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

# Exceptions in pycirkuit are used mainly to display info to the user via MessageBoxes
# Thus, an exception must convey 3 infos:
# 1) The MessageBox Title, different for each kind of error
# 2) The main message, perhaps as short as possible
# 3) Additional info
class PyCirkuitError(Exception):
    def __init__(self, message, title=_translate("PyCirkuitError", "PyCirkuit Error",  "Exception title"), moreInfo=""):
        super().__init__(message)
        self.title=title
        self.moreInfo=moreInfo
