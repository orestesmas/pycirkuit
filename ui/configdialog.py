# -*- coding: utf-8 -*-

"""
Module implementing configDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_configdialog import Ui_configDialog


class configDialog(QDialog, Ui_configDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(configDialog, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_listWidget_currentRowChanged(self, currentRow):
        """
        Slot documentation goes here.
        
        @param currentRow DESCRIPTION
        @type int
        """
        self.stackedWidget.setCurrentIndex(currentRow)
