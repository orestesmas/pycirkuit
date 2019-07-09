# -*- coding: utf-8 -*-
"""
Module implementing a CircuitMacros Manager class.
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

# Standard library imports
import os
from os.path import normpath, join, exists, dirname, abspath
import zipfile
import urllib.request as Net
import urllib.error as NetError

# Third-party imports
from PyQt5 import QtCore
from PyQt5.QtCore import QStandardPaths

# Local application imports
from pycirkuit.exceptions import *

# Translation function
_translate = QtCore.QCoreApplication.translate


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
        pass

    def check_installed(self):
        #TODO: Should:
        #  1) Test several places, starting with the one set up in config, but then test also standard locations
        #  2) Two possibilities can arise:
        #     a) There's only one place where CM are
        #     b) They are found in two or more places
        dirList =  QStandardPaths.standardLocations(QStandardPaths.GenericDataLocation)
        # Append specific app subdir to each possible location
        dirList = [normpath(join(dir, "circuit-macros")) for dir in dirList]
        settings = QtCore.QSettings()
        extraPath = normpath(settings.value("General/cmPath",  ""))
        if extraPath != "":
            dirList.insert(0, extraPath)
        for testPath in dirList:
            if exists(join(testPath , "libcct.m4")):
                #  3) We pick up the first found. Perhaps we might consider other possibilities
                #  4) Finally, as a SIDE EFFECT we can update config automatically or not.
                settings.setValue("General/cmPath", testPath)
                return True
        else:
            return False

    def default_CMPath(self):
        return normpath(join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation), "circuit-macros"))
        
    def download_latest(self, percent):
        origin = "https://ctan.mirror.norbert-ruehl.de/graphics/circuit_macros.zip"
        destination = dirname(self.default_CMPath())
        if destination == "":
            raise PyCirkuitError(_translate("ExternalTool", "Cannot determine the standard writable location for PyCirkuit",  "Error message"))
        if not exists(destination):
            os.makedirs(destination)
        destination = join(destination,"circuit_macros.zip")
        try:
            with Net.urlopen(origin) as source,  open(destination, 'wb') as dest:
                length = source.getheader('content-length')
                if length:
                    length = int(length)
                    percent.setRange(0, length)
                    percent.setValue(0)
                    blocksize = max(4096, length//100)
                else:
                    blocksize = 1000000 # just made something up
                size = 0
                while True:
                    buf1 = source.read(blocksize)
                    if not buf1:
                        break
                    dest.write(buf1)
                    size += len(buf1)
                    percent.setValue(size)
        except NetError.URLError as e:
            #FIXME: Convert to MessageBox by reraising as PyCktCMFetchError
            print(_translate("ExternalTool", "Network error: ",  "Error message"), e)

    def getManUrl(self):
        import glob
        try:
            import magic
        except ImportError:
            raise PyCirkuitError(_translate("ExternalTool", "Module 'python-magic' not found. Please check that all PyCirkuit dependencies are correctly installed.",  "Error message"))
        mime = magic.Magic(mime=True)   # Prepare to detect a file's mimetype based on its contents
        # Get standard locations for documentation in a platform-independent way
        dirList = QStandardPaths.standardLocations(QStandardPaths.GenericDataLocation)
        # Append specific app subdir to each possible location
        dirList = [normpath(join(dir, "doc", "circuit-macros")) for dir in dirList]
        # Add the config-stored Circuit Macros Location to this list
        settings = QtCore.QSettings()
        extraPath = normpath(settings.value("General/cmPath",  ""))
        extraPath = join(extraPath, "doc")
        dirList.insert(0, extraPath)
        # Add the default Circuit Macros location to this list (can be the same as above)
        dirList.append(join(self.default_CMPath(), "doc"))
        # Explore the generated list searching for pdf or compressed pdf
        for testPath in dirList:
            # Perhaps we should search for *.pdf* or, at least, for *.pdf AND *.pdf.gz
            candidates = glob.glob(join(testPath, "Circuit_macros.pdf"))
            candidates.extend(glob.glob(join(testPath, "Circuit_macros.pdf.gz")))
            for candidate in candidates:
                mimeType = mime.from_file(candidate)
                if (mimeType == "application/pdf") or (mimeType == "application/gzip"):
                    return(candidate)
        else:
            raise PyCktCMManNotFoundError(normpath(settings.value("General/cmPath",  "")))

    def unpack_circuit_macros(self):
        try:
            dataPath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)
            zipName = abspath(join(dataPath,  "circuit_macros.zip"))
            zip_ref = zipfile.ZipFile(zipName, "r")
            zip_parent_dir = zip_ref.namelist()[0]
            zip_ref.extractall(dataPath)
            zip_ref.close()
            os.rename(join(dataPath, zip_parent_dir), join(dataPath, "circuit-macros"))
            os.remove(zipName)
            settings = QtCore.QSettings()
            settings.setValue("General/cmPath", join(dataPath , 'circuit-macros'))
            settings.sync()
        except Exception as e:
            #FIXME: Convert to MessageBox by reraising as PyCktCMFetchError
            print(_translate("ExternalTool", "Error uncompressing the Circuit Macros: ",  "Error message"), e)
