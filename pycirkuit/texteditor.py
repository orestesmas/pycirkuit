# -*- coding: utf-8 -*-
"""
Module implementing a customized TextEditor
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
from PySide6.QtCore import QCoreApplication, QRect, QSize, Qt
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget
from PySide6.QtGui import (
    QColor,
    QFont,
    QKeySequence,
    QPainter,
    QTextCursor,
    QTextFormat,
)

# Translation function
_translate = QCoreApplication.translate

# Matching brackets, and the reverse mapping used when scanning backwards
# from a closing bracket.
_BRACKET_PAIRS = {"(": ")", "{": "}", "[": "]"}
_REVERSE_BRACKET_PAIRS = {close: open_ for open_, close in _BRACKET_PAIRS.items()}

# Circuit Macros/PIC comments start with '#' and run to the end of the line.
_COMMENT_PREFIX = "# "


class _LineNumberArea(QWidget):
    """
    The narrow gutter widget to the left of the editor that shows line
    numbers. All actual painting is delegated back to the editor, which
    has the font metrics and block geometry needed to lay it out.
    """

    def __init__(self, editor):
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self):
        return QSize(self._editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self._editor.lineNumberAreaPaintEvent(event)


class pycktTextEditor(QPlainTextEdit):
    """
    Editor widget for Circuit Macros/PIC/M4 source: line numbers, current
    line and matching-bracket highlighting, comment/uncomment toggling
    (Ctrl+/), and Ctrl+wheel/Ctrl+=/Ctrl+- font zoom.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)

        self._lineNumberArea = _LineNumberArea(self)
        self.blockCountChanged.connect(self._update_line_number_area_width)
        self.updateRequest.connect(self._update_line_number_area)
        self.cursorPositionChanged.connect(self._update_extra_selections)

        self._update_line_number_area_width(0)
        self._update_extra_selections()

    # --- Line number gutter -------------------------------------------------
    # Ported from Qt's "Code Editor Example", which pairs line numbers with
    # current-line highlighting as a single recipe.

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        return 3 + self.fontMetrics().horizontalAdvance("9") * digits

    def _update_line_number_area_width(self, _newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def _update_line_number_area(self, rect, dy):
        if dy:
            self._lineNumberArea.scroll(0, dy)
        else:
            self._lineNumberArea.update(
                0, rect.y(), self._lineNumberArea.width(), rect.height()
            )
        if rect.contains(self.viewport().rect()):
            self._update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self._lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = round(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(Qt.black)
                painter.drawText(
                    0,
                    top,
                    self._lineNumberArea.width() - 2,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    str(blockNumber + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            blockNumber += 1

    # --- Current line + matching bracket highlighting -----------------------

    def _update_extra_selections(self):
        self.setExtraSelections(
            [self._current_line_selection()] + self._bracket_match_selections()
        )

    def _current_line_selection(self):
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(Qt.yellow).lighter(160))
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        return selection

    def _bracket_match_selections(self):
        doc = self.document()
        pos = self.textCursor().position()

        match = self._find_bracket_match(doc, pos)
        if match is None:
            match = self._find_bracket_match(doc, pos - 1)
        if match is None:
            return []

        selections = []
        for charPos in match:
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("lightgreen"))
            selection.format.setFontWeight(QFont.Bold)
            cursor = QTextCursor(doc)
            cursor.setPosition(charPos)
            cursor.setPosition(charPos + 1, QTextCursor.KeepAnchor)
            selection.cursor = cursor
            selections.append(selection)
        return selections

    def _find_bracket_match(self, doc, pos):
        if pos < 0 or pos >= doc.characterCount() - 1:
            return None
        char = doc.characterAt(pos)
        if char in _BRACKET_PAIRS:
            endPos = self._scan_for_match(doc, pos + 1, 1, char, _BRACKET_PAIRS[char])
            return (pos, endPos) if endPos is not None else None
        if char in _REVERSE_BRACKET_PAIRS:
            startPos = self._scan_for_match(
                doc, pos - 1, -1, char, _REVERSE_BRACKET_PAIRS[char]
            )
            return (startPos, pos) if startPos is not None else None
        return None

    def _scan_for_match(self, doc, startPos, direction, searchChar, matchChar):
        depth = 1
        pos = startPos
        limit = doc.characterCount() - 1
        while 0 <= pos < limit:
            char = doc.characterAt(pos)
            if char == searchChar:
                depth += 1
            elif char == matchChar:
                depth -= 1
                if depth == 0:
                    return pos
            pos += direction
        return None

    # --- Comment/uncomment toggle -------------------------------------------

    def _toggle_comment(self):
        cursor = self.textCursor()
        doc = self.document()
        startBlockNum = doc.findBlock(cursor.selectionStart()).blockNumber()
        endCursor = QTextCursor(doc)
        endCursor.setPosition(cursor.selectionEnd())
        endBlockNum = endCursor.blockNumber()
        if endCursor.atBlockStart() and endBlockNum > startBlockNum:
            endBlockNum -= 1

        blocks = []
        block = doc.findBlockByNumber(startBlockNum)
        for _ in range(startBlockNum, endBlockNum + 1):
            blocks.append(block)
            block = block.next()

        nonBlank = [b for b in blocks if b.text().strip()]
        allCommented = bool(nonBlank) and all(
            b.text().lstrip().startswith("#") for b in nonBlank
        )

        editCursor = QTextCursor(doc)
        editCursor.beginEditBlock()
        for b in blocks:
            text = b.text()
            if allCommented:
                stripped = text.lstrip()
                if not stripped.startswith("#"):
                    continue
                prefixLen = 2 if stripped.startswith(_COMMENT_PREFIX) else 1
                offset = len(text) - len(stripped)
                editCursor.setPosition(b.position() + offset)
                editCursor.setPosition(
                    b.position() + offset + prefixLen, QTextCursor.KeepAnchor
                )
                editCursor.removeSelectedText()
            elif text.strip():
                editCursor.setPosition(b.position())
                editCursor.insertText(_COMMENT_PREFIX)
        editCursor.endEditBlock()

    # --- Input handling (comment toggle + inherited font zoom) --------------

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.ZoomIn):
            self._change_font_size(1)
        elif event.matches(QKeySequence.ZoomOut):
            self._change_font_size(-1)
        elif event.key() == Qt.Key_Slash and event.modifiers() & Qt.ControlModifier:
            # Checking only the Ctrl bit (not exact-matching the whole
            # modifier set) is deliberate: on ES/CAT keyboards '/' is
            # typed as Shift+7, so Ctrl+/ arrives as Ctrl+Shift+Slash -
            # Shift is incidental to reaching the character, not a
            # distinct shortcut.
            self._toggle_comment()
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            event.accept()
            numSteps = event.angleDelta() / 120
            self._change_font_size(numSteps.y())
        else:
            super().wheelEvent(event)

    def _change_font_size(self, steps):
        editorFont = self.font()
        fontSize = editorFont.pointSize()
        newFontSize = fontSize + steps
        editorFont.setPointSize(newFontSize)
        self.setFont(editorFont)
