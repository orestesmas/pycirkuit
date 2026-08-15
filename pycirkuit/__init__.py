# -*- coding: utf-8 -*-
"""
Module storing the application version number and the few other bits of
metadata actually needed at runtime (see pyproject.toml for the rest).
"""
# Copyright (C) 2018-2026 Orestes Mas
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

__productname__ = "PyCirkuit"
# PEP 440 version. Pre-release identifiers (.devN, aN/bN, rcN) while master
# is mid-modernization; plain "1.0.0" once that work is ready to release.
#
# Also the single source of truth for pyproject.toml's [project] version
# (read via `attr = "pycirkuit.__version__"`), so it doesn't need to be
# updated in two places.
__version__ = "1.0.0.dev2"
# Only kept here because __copyright__ (used by the About dialog) is built
# from them. Everything else PyPI/Debian-facing (description, author email,
# license, homepage...) lives solely in pyproject.toml - nothing at runtime
# reads it back from here, so it isn't duplicated in this module.
__author__ = "Orestes Mas"
__license_long__ = "Licensed under the GNU GPL v3 or any later version"
__copyright__ = "Copyright 2018-2026 {__author__}".format(**locals())

# The temporary working dir should be globally addressed through the entire application
__tmpDir__ = None

# Global variable that indicates if we are being executed on a desktop environment or not
__haveGUI__ = None

# CLI options
class Option(Enum):
    TIKZ = "tikzOption"
    PDF = "pdfOption"
    PNG = "pngOption"
    JPEG = "jpgOption"
    SVG = "svgOption"
    DPI = "dpiOption"
    QUAL = "qualityOption"
    REC = "recurseOption"
    LINK = "followLinksOption"
    DEST = "destDirOption"
    OVER = "overwriteOption"
