# -*- coding: utf-8 -*-
"""
Module implementing a customized TextEditor
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
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QKeySequence

# Translation function
_translate = QCoreApplication.translate

class pycktTextEditor(QTextEdit):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QTextEdit
        """
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.ZoomIn):
            self._change_font_size(1)
        elif event.matches(QKeySequence.ZoomOut):
            self._change_font_size(-1)
        else:
            super().keyPressEvent(event)
    
    def wheelEvent(self, event):
        if (event.modifiers()==Qt.ControlModifier):
            event.accept()
            numSteps = event.angleDelta() / 120
            self._change_font_size(numSteps.y())
        else:
            super().wheelEvent(event)
        
    def _change_font_size(self, steps):
        editorFont = self.font()
        fontSize = editorFont.pointSize()
        newFontSize = fontSize + steps
        editorFont.setPointSize(newFontSize)
        self.setFont(editorFont)
