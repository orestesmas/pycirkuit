# -*- coding: utf-8 -*-
"""
Module implementing pycktImageViewer
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
import os

# Third-party imports
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QFont

# Local application imports
import pycirkuit
from pycirkuit.tools.pdftopng import ToolPdfToPng

# Translation function
_translate = QCoreApplication.translate

class pycktImageViewer(QGraphicsView):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        
        # Initialize the graphics Scene-View pair with an empty pixmap
        # First the scene...
        self.__scene = QGraphicsScene(self)
        # Initial image does not correspond to any file
        self.__fileBaseName = None
        # Then the pixmap (initially empty)...
        self.__image = self.__scene.addPixmap(QPixmap())
        # Then the graphics view (ourselves)
        self.setScene(self.__scene)
        
        # Class properties initialization
        self.__wheelSteps = 0
    
    def _adjust_view(self):
        self.__scene.setSceneRect(self.__scene.itemsBoundingRect())
        self.resetTransform()

    def _clear_items(self):
        for item in self.__scene.items():
            self.__scene.removeItem(item)

    def _qBound(self, minVal, current, maxVal):
        """PyQt5 does not wrap the qBound function from Qt's global namespace
           This is equivalent."""
        return max(min(current, maxVal), minVal)

    def setImage(self, fileBaseName):
        self._clear_items()
        try:
            newPixmap = QPixmap("{baseName}.png".format(baseName=fileBaseName))
        except Exception as err:
            print(err)
        else:
            self.__fileBaseName = fileBaseName
            self.__image = self.__scene.addPixmap(newPixmap)
            self._adjust_view()

    def setText(self, newText):
        self._clear_items()
        font = QFont()
        font.setPointSize(22)
        self.__scene.addText(newText, font)
        self._adjust_view()

    def wheelEvent(self,event):
        if (self.__fileBaseName != None) and (event.modifiers()==Qt.ControlModifier):
            event.accept()
            # Set working dir
            saveWD = os.getcwd()
            os.chdir(pycirkuit.__tmpDir__.path())
            # Accumulated mouse wheel steps
            self.__wheelSteps = self._qBound(-10, self.__wheelSteps + event.angleDelta().y() / 120,  10)
            zoomFactor = 1 + round(self.__wheelSteps/10, 1)
            res = int(round(150 * zoomFactor, 0))
            try:
                converter = ToolPdfToPng()
                converter.execute(self.__fileBaseName, resolution=res)
                self.setImage(self.__fileBaseName)
            except:
                pass
#            scaling = QTransform()
#            scaling.scale(zoomFactor, zoomFactor)
#            self.setTransform(scaling)
            finally:
                os.chdir(saveWD)
        else:
            event.ignore()
