# -*- coding: utf-8 -*-
"""
Module implementing a personalized AboutDialog.
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
from PyQt5.QtWidgets import QDialog

# Local application imports
from pycirkuit import __version__, __copyright__
from .Ui_aboutdialog import Ui_AboutDialog


class AboutDialog(QDialog, Ui_AboutDialog):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        # Now change the placeholders in dialog
        # Cannot use str.format() here because the HTML string does contain other items between curly brackets
        # Try to change the variable in the text for the version number
        s = self.textVersion.toHtml()
        self.textVersion.setHtml(s.replace("{versionNumber}", __version__, 1))

        # Try to change the variable in the text for the copyright
        s = self.textLicense.toHtml()
        self.textLicense.setHtml(s.replace("{copyrightInfo}", __copyright__, 1))

        # Start with first Tab visible
        self.tabWidget.setCurrentIndex(0)
