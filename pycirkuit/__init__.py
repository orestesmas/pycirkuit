# -*- coding: utf-8 -*-
"""
Module storing the application version number and other metadata in a single place
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
from enum import Enum

__all__ = ["mainwindow"]

__productname__   = "PyCirkuit"
# Expecting trailing "-rcN" or "" for stable releases.
__version__       = "0.4.0"
__description__   = "A front-end for Circuit Macros"
__author__        = "Orestes Mas"
__author_email__  = "orestes@tsc.upc.edu"
__license_short__ = "GPLv3+"
__license_long__  = "Licensed under the GNU GPL v3 or any later version"
__copyright__     = "Copyright 2018-2019 {__author__}".format(**locals())
__bigcopyright__  = """{__productname__} {__version__}
{__license_long__}""".format(**locals())
__homepage__      = "https://github.com/orestesmas/pycirkuit"

# The temporary working dir should be globally addressed through the entire application
__tmpDir__ = None

# Global variable that indicates if we are being executed on a desktop environment or not
__haveGUI__ = None

# CLI options
class Option(Enum):
    TIKZ = 'tikzOption'
    PDF = 'pdfOption'
    PNG = 'pngOption'
    JPEG = 'jpgOption'
    SVG = 'svgOption'
    DPI = 'dpiOption'
    QUAL = 'qualityOption'
    REC = 'recurseOption'
    LINK = 'followLinksOption'
    DEST = 'destDirOption'
    OVER = 'overwriteOption'

