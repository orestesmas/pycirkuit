# -*- coding: utf-8 -*-

# Standard library imports
import os, shutil, tarfile
import urllib.request as Net
import urllib.error as NetError

# Third-party imports
from PyQt5 import QtCore

class CircuitMacrosManager(QtCore.QObject):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """


    def download_latest(self):
        origin = "http://www.ece.uwaterloo.ca/~aplevich/Circuit_macros/Circuit_macros.tar.gz"
        destination = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)
        if destination == "":
            raise RuntimeError("Cannot determine the standard writable location for PyCirkuit")
        if not os.path.exists(destination):
            os.makedirs(destination)
        destination += "/Circuit_macros.tar.gz"
        try:
            with Net.urlopen(origin) as source,  open(destination, 'wb') as dest:
                shutil.copyfileobj(source, dest)
        except NetError.URLError as e:
            #FIXME: Better handler
            print("Network error: ", e)



    def unpack_circuit_macros(self):
        try:
            sourcePath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)
            with tarfile.open(sourcePath + '/Circuit_macros.tar.gz', 'r:gz') as tarFile:
                tarFile.extractall(path=sourcePath)
                # Millor:
                # for fitxer in tarFile.getMembers():
                #   nom = fitxer.name
                #   <Eliminar/canviar (regexp) el primer element del nom>
                #   fitxer.name = nouNom
                # Fet això, ja podem fer un extractall al directori actual
            settings = QtCore.QSettings()
            settings.setValue("General/cmPath", sourcePath)
        except tarfile.TarError as e:
            print("Error uncompressing the Circuit Macros: ", e)
            shutil.rmtree(sourcePath+"/.")
