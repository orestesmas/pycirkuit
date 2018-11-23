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
            dataPath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)
            with tarfile.open(dataPath + '/Circuit_macros.tar.gz', 'r:gz') as tarFile:
                # Circuit Macros is distributed in a tree structure. 
                # We want the top dir of this structure to be 'circuit_macros', whichever it is now
                # The following algorithm assumes that all circuit macros's files are in a subdir.
                entry = tarFile.next()
                storedDir, foo, bar = entry.name.partition('/')  # Got stored top dir name in 'storedDir'
                # Now iterate and replace top directory name in all entries
                for entry in tarFile.getmembers():
                    filename = entry.name
                    entry.name = filename.replace(storedDir, 'circuit_macros', 1)
                tarFile.extractall(path=dataPath)
            os.remove(dataPath +'/Circuit_macros.tar.gz')
            settings = QtCore.QSettings()
            settings.setValue("General/cmPath", dataPath + '/circuit_macros')
            settings.sync()
        except tarfile.TarError as e:
            print("Error uncompressing the Circuit Macros: ", e)
            shutil.rmtree(dataPath+"/.")
