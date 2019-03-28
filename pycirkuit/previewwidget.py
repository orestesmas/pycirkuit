# -*- coding: utf-8 -*-
"""
Module implementing pycktPreviewWidget
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
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QDockWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform

# Translation function
_translate = QCoreApplication.translate

class pycktPreviewWidget(QDockWidget):
    """
    Class documentation goes here.
    """
    __presentZoomFactor = 1
    
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
        self.image = QPixmap()
        self.scene.addPixmap(self.image)
        # Then the graphics view. First, though, we have to lay out it
        x = self.widget()
        layout = QHBoxLayout(self.widget())
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setObjectName("horizontalLayout_2")
        self.preview = QGraphicsView(self.widget())
        self.preview.setObjectName("preview")
        self.preview.setScene(self.scene)
        layout.addWidget(self.preview)
        
    def setPixmap(self, newPixmap):
        self.scene.addPixmap(newPixmap)
        self.preview.resetTransform()
        return
        if self.image.isNull():
            self.image = QPixmap(newPixmap)
        else:
            self.image.swap(newPixmap)
        
    def setText(self, newText):
        pass

    def wheelEvent(self,event):
        if (event.modifiers()==Qt.ControlModifier):
            event.accept()
            numSteps = event.angleDelta() / 120
            self.__presentZoomFactor += (numSteps.y() / 10)
            scaling = QTransform()
            scaling.scale(self.__presentZoomFactor, self.__presentZoomFactor)
            self.preview.setTransform(scaling)
        else:
            super().wheelEvent(event)
