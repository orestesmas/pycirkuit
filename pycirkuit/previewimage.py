# -*- coding: utf-8 -*-
"""
Module implementing pycktPreviewImage
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

# Third-party imports
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QTransform

# Translation function
_translate = QCoreApplication.translate

class pycktPreviewImage(QGraphicsView):
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
        self.scene = QGraphicsScene(self)
        # Then the pixmap (initially empty)...
        self.image = self.scene.addPixmap(QPixmap())
        # Then the graphics view (ourselves)
        self.setScene(self.scene)
        
        # Class properties initialization
        self.__presentZoomFactor = 1
    
    def _clear_items(self):
        for item in self.scene.items():
            self.scene.removeItem(item)

    def _adjust_view(self):
        r = self.scene.itemsBoundingRect()
        print("Scene rect: {}".format(r))
        s = self.Image.pixmap().rect()
        print("Pixmap rect: {}".format(s))
        self.resize(s.width(), s.height())
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.resetTransform()

    def setPixmap(self, newPixmap):
        self._clear_items()
        self.Image = self.scene.addPixmap(newPixmap)
        self._adjust_view()

    def setText(self, newText):
        self._clear_items()
        self.scene.addText(newText)
        self._adjust_view()

    def wheelEvent(self,event):
        if (event.modifiers()==Qt.ControlModifier):
            event.accept()
            numSteps = event.angleDelta() / 120
            self.__presentZoomFactor += (numSteps.y() / 10)
            scaling = QTransform()
            scaling.scale(self.__presentZoomFactor, self.__presentZoomFactor)
            self.setTransform(scaling)
        else:
            super().wheelEvent(event)
