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
from PyQt5.QtCore import QCoreApplication, Qt, QRectF, QPointF, pyqtSignal
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
    A viewer for images compiled from circuit macros source files.
    Being a subclass of QGraphicsView, this class handles zoom using
    the mouse wheel.
    """

    # A signal to inform of errors
    conversion_failed = pyqtSignal(PyCirkuitError)
    image_changed = pyqtSignal()

    def __init__(self, parent=None, maxZoom=5):
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
        self.__file_base_name = None
        # Then the pixmap (initially empty). We maintain a reference to the pixmap, for easy access
        self.__pixmap_item = self.__scene.addPixmap(QPixmap())
        # Then the graphics view (ourselves)
        self.setScene(self.__scene)

        # Set operation mode (some options set up in Designer)
        self.setAlignment(Qt.AlignCenter)  # Image appears centered if fits in view

        # Zoom parameters initialization
        self.__ppi_base = 150  # Base image resolution (pixels per inch)
        self.__max_zoom = maxZoom  # Maximum magnification factor (default = 5)
        self.__max_steps = 10  # No. of wheel steps required to achieve max. zoom
        self.__wheel_steps = 0  # Initial value for wheel position
        self.__current_ppi = self.__calc_ppi(
            self.__wheel_steps
        )  # Initial value for current resolution

    def __adjust_view(self):
        self.setSceneRect(self.__scene.itemsBoundingRect())

    def __calc_ppi(self, wheelSteps):
        """
        This function calculates the image resolution required to achieve the desired zoom level,
        indicated by number of steps the mouse wheel has turned.

        @param wheelSteps Number of steps the user has turned the mouse wheel (must be bounded)
        @type integer
        """
        # 'ratio' could be precalculated in __init__. Doing so here is a waste of cpu cycles
        # but allows for more (future) flexibility, as we can, for instance, use variable ratios.
        ratio = 10 ** (log10(self.__max_zoom) / self.__max_steps)
        newPPI = round(self.__ppi_base * (ratio ** wheelSteps))
        return newPPI

    def __clear_items(self):
        for item in self.__scene.items():
            self.__scene.removeItem(item)

    def __qBound(self, minVal, current, maxVal):
        """
        PyQt5 does not wrap the qBound function from Qt's global namespace.
        This is equivalent. Returns "current" if it's between "minVal" and "maxVal",
        otherwise saturates to one of these two limits.
        """
        return max(min(current, maxVal), minVal)

    def clearImage(self):
        self.__clear_items()
        self.__pixmap_item = self.__scene.addPixmap(QPixmap())
        self.__adjust_view()

    def getRect(self):
        return self.__pixmap_item.pixmap().rect()

    def setImage(self, fileBaseName, adjustIGU=False):
        """
        Tries to load a PNG image from disk and display it

        Args:
            fileBaseName (str): the file name of the image to load (without extension) relative to current dir.
            adjustIGU (bool): Whether we want to adjust the size of IGU viewport to fit the image or not (default=False).
        """
        self.__clear_items()
        try:
            newPixmap = QPixmap("{baseName}.png".format(baseName=fileBaseName))
            if newPixmap.isNull():
                raise PyCirkuitError(
                    _translate(
                        "PyCirkuitError",
                        "The converted image could not be loaded.",
                        "Exception message",
                    ),
                    _translate(
                        "PyCirkuitError", "PyCirkuit Internal Error", "Exception title"
                    ),
                    moreInfo=_translate(
                        "PyCirkuitError",
                        "This error should not happen in a normal operation. Please contact the developers.",
                        "Exception additional info",
                    ),
                )
        except PyCirkuitError as err:
            self.setText(
                _translate(
                    "PyCirkuitError",
                    "Internal error: cannot load image",
                    "Displayed error message",
                )
            )
            self.conversion_failed.emit(err)
        else:
            self.__file_base_name = fileBaseName
            self.__pixmap_item = self.__scene.addPixmap(newPixmap)
            if adjustIGU:
                self.image_changed.emit()
            self.__adjust_view()

    def setText(self, newText):
        """
        Displays a text string (in bigger font and in red color) into the viewport

        Args:
            newText (str): the string to display.
        """
        self.__clear_items()
        font = QFont()
        font.setPointSize(22)
        self.__scene.addText(newText, font).setDefaultTextColor(Qt.red)
        self.__adjust_view()

    def wheelEvent(self, event):
        if (self.__file_base_name != None) and (
            event.modifiers() == Qt.ControlModifier
        ):
            event.accept()
            # Accumulated mouse wheel steps, bounded to certain limits
            self.__wheel_steps = self.__qBound(
                -self.__max_steps,
                self.__wheel_steps + event.angleDelta().y() / 120,
                self.__max_steps,
            )
            newPPI = self.__calc_ppi(self.__wheel_steps)
            # Do nothing if reached one of the zoom limits
            if newPPI == self.__current_ppi:
                return

            # Get the cursor's position and translate to pixmap coordinates
            scenePos = self.mapToScene(event.pos())
            # Now find the % offset from pixmap's origin. This doesn't change with zoom
            percentX = scenePos.x() / self.__scene.itemsBoundingRect().width()
            percentY = scenePos.y() / self.__scene.itemsBoundingRect().height()

            # Now perform the zoom by converting from PDF with suitable resolution
            # Set working dir
            saveWD = os.getcwd()
            os.chdir(pycirkuit.__tmpDir__.path())
            try:
                converter = ToolPdfToPng()
                converter.execute(self.__file_base_name, resolution=newPPI)
                self.setImage(self.__file_base_name, adjustIGU=True)

                # If Scene contents area is smaller than current viewport size, center scene in view
                currentSceneRect = self.__scene.itemsBoundingRect()
                currentViewportRect = QRectF(self.rect())
                if currentViewportRect.contains(currentSceneRect):
                    self.setSceneRect(currentSceneRect)
                    self.centerOn(currentSceneRect.center())
                # Else, keep scene point under cursor at the same viewport position
                else:
                    # Calculate the scene coordinates of the position which is (%X,%Y) from origin
                    newScenePos = QPointF(
                        currentSceneRect.width() * percentX,
                        currentSceneRect.height() * percentY,
                    )
                    # Calculate pixel offset between mouse position and viewport center
                    offset = QPointF(self.width() / 2, self.height() / 2) - QPointF(
                        event.pos()
                    )
                    # Then adjust things so that this scene position appears under the mouse
                    self.centerOn(newScenePos + offset)
            except PyCirkuitError as err:
                self.setText(
                    _translate(
                        "PyCirkuitError",
                        "Error creating zoomed image.",
                        "Displayed error message",
                    )
                )
                self.conversion_failed.emit(err)
            else:
                self.__current_ppi = newPPI
            finally:
                os.chdir(saveWD)
        else:
            event.ignore()
