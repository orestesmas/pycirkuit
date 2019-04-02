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
from math import log10

# Third-party imports
from PyQt5.QtCore import QCoreApplication, Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QFont

# Local application imports
import pycirkuit
from pycirkuit.exceptions import *
from pycirkuit.tools.pdftopng import ToolPdfToPng

# Translation function
_translate = QCoreApplication.translate

class pycktImageViewer(QGraphicsView):
    """
    Class documentation goes here.
    """
    # A signal to inform of errors
    conversion_failed = pyqtSignal(PyCirkuitError)
    image_changed = pyqtSignal(QRect)

    def __init__(self, parent = None, maxZoom = 5):
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

        # Set operation mode
        self.setAlignment(Qt.AlignCenter)   # Image appears centered if fits in view
        # self.setTransformationAnchor(self.AnchorUnderMouse)
        
        # Zoom parameters initialization
        self.__ppi_base = 150      # Base image resolution (pixels per inch)
        self.__max_zoom = maxZoom  # Maximum magnification factor (default = 5)
        self.__max_steps = 10      # No. of wheel steps required to achieve max. zoom
        self.__wheel_steps = 0     # Initial value for wheel position
    
    def _adjust_view(self):
        # Center image in view (if image fits inside)
        center = self.mapToScene(self.viewport().rect().center())
        self.centerOn(center)
        self.__scene.setSceneRect(self.__scene.itemsBoundingRect())

    def _calc_ppi(self, wheelSteps):
        """
        This function calculates the image resolution required to achieve the desired zoom level,
        indicated by number of steps the mouse wheel has turned.
        
        @param wheelSteps Number of steps the user has turned the mouse wheel (must be bounded)
        @type integer
        """
        # 'ratio' could be precalculated in __init__. Doing so here is a waste of cpu cycles
        # but allows for more (future) flexibility, as we can, for instance, use variable ratios.
        ratio = 10 ** (log10(self.__max_zoom)/self.__max_steps)
        newPPI = round(self.__ppi_base * (ratio ** wheelSteps))
        return newPPI

    def _clear_items(self):
        for item in self.__scene.items():
            self.__scene.removeItem(item)

    def _qBound(self, minVal, current, maxVal):
        """
        PyQt5 does not wrap the qBound function from Qt's global namespace.
        This is equivalent. Returns "current" if it's between "minVal" and "maxVal",
        otherwise saturates to one of these two limits.
        """
        return max(min(current, maxVal), minVal)

    def setImage(self, fileBaseName, adjustIGU=False):
        """
        Tries to load a PNG image from disk and display it
        
        Args:
            fileBaseName (str): the file name of the image to load (without extension) relative to current dir.
            adjustIGU (bool): Whether we want to adjust the size of IGU viewport to fit the image or not (default=False).
        """
        self._clear_items()
        try:
            newPixmap = QPixmap("{baseName}.png".format(baseName=fileBaseName))
            if newPixmap.isNull():
                raise PyCirkuitError(
                    _translate("PyCirkuitError", "The converted image could not be loaded.", "Exception message"), 
                    _translate("PyCirkuitError", "PyCirkuit Internal Error", "Exception title"), 
                    moreInfo = _translate("PyCirkuitError", "This error should not happen in a normal operation. Please contact the developers.", "Exception additional info")
                )
        except PyCirkuitError as err:
            self.setText( _translate("PyCirkuitError", "Internal error: cannot load image", "Displayed error message"))
            self.conversion_failed.emit(err)
        else:
            self.__fileBaseName = fileBaseName
            self.__image = self.__scene.addPixmap(newPixmap)
            if adjustIGU:
                self.image_changed.emit(newPixmap.rect())
            self._adjust_view()

    def setText(self, newText):
        """
        Displays a text string (in bigger font and in red color) into the viewport
        
        Args:
            newText (str): the string to display.
        """       
        self._clear_items()
        font = QFont()
        font.setPointSize(22)
        self.__scene.addText(newText, font).setDefaultTextColor(Qt.red)
        self._adjust_view()

    def wheelEvent(self,event):
        if (self.__fileBaseName != None) and (event.modifiers()==Qt.ControlModifier):
            event.accept()
            # Set working dir
            saveWD = os.getcwd()
            os.chdir(pycirkuit.__tmpDir__.path())
            # Accumulated mouse wheel steps
            self.__wheel_steps = self._qBound(
                -self.__max_steps,
                 self.__wheel_steps + event.angleDelta().y() / 120,
                 self.__max_steps)
            newPPI = self._calc_ppi(self.__wheel_steps)
            try:
                converter = ToolPdfToPng()
                converter.execute(self.__fileBaseName, resolution = newPPI)
                self.setImage(self.__fileBaseName)
            except PyCirkuitError as err:
                self.setText(_translate("PyCirkuitError", "Error creating zoomed image.", "Displayed error message"))
                self.conversion_failed.emit(err)
            finally:
                os.chdir(saveWD)
        else:
            event.ignore()
