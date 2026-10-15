# -*- coding: utf-8 -*-
"""
Module implementing palette-aware helpers for widget styling.
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

# Third-party imports
from PySide6.QtGui import QColor, QPalette

# How much red gets mixed into the widget's own background colour to flag
# invalid input. Low enough to stay a hint, high enough to be noticed.
_RED_TINT = 0.15


def invalid_input_style(widget):
    """
    Return a stylesheet marking `widget` as holding invalid input.

    The colours are derived from the widget's current palette instead of
    being hardcoded, so the hint stays readable under both light and dark
    themes: a hardcoded light background left a dark theme's own (light)
    text colour unreadable on top of it.
    """
    palette = widget.palette()
    base = palette.color(QPalette.Base)
    text = palette.color(QPalette.Text)
    keep = 1.0 - _RED_TINT
    tinted = QColor(
        round(base.red() * keep + 255 * _RED_TINT),
        round(base.green() * keep),
        round(base.blue() * keep),
    )
    return "background-color: {}; color: {};".format(tinted.name(), text.name())

