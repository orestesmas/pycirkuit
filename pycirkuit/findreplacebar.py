# -*- coding: utf-8 -*-
"""
Module implementing a non-modal find/replace bar for pycktTextEditor.
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
from PySide6.QtCore import QCoreApplication, QEvent, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

# Translation function
_translate = QCoreApplication.translate

_NO_MATCH_STYLE = "background-color: rgb(255, 230, 230);"


class FindReplaceBar(QWidget):
    """
    Non-modal find/replace bar meant to sit above a pycktTextEditor (Kate/VS
    Code style): hidden by default, shown on demand, closed with Esc. The
    actual searching/replacing lives in the pycktTextEditor it drives
    (find()/replace_all() in texteditor.py) - this widget only handles input
    and feedback.
    """

    def __init__(self, editor, parent=None):
        """
        Constructor

        @param editor the pycktTextEditor instance this bar searches/replaces in
        @type pycktTextEditor
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self._editor = editor
        self._searchAnchor = None

        self.closeButton = QToolButton(self)
        self.closeButton.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.WindowClose))
        self.closeButton.setAutoRaise(True)
        self.closeButton.setToolTip(_translate("FindReplaceBar", "Close", ""))
        self.closeButton.clicked.connect(self.hide_bar)

        self.findField = QLineEdit(self)
        self.findField.setPlaceholderText(_translate("FindReplaceBar", "Find...", ""))
        self.findField.textChanged.connect(self._on_search_text_changed)
        self.findField.returnPressed.connect(self.find_next)
        self.findField.installEventFilter(self)

        self.prevButton = QToolButton(self)
        self.prevButton.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.prevButton.setAutoRaise(True)
        self.prevButton.setToolTip(_translate("FindReplaceBar", "Find previous", ""))
        self.prevButton.clicked.connect(self.find_previous)

        self.nextButton = QToolButton(self)
        self.nextButton.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        self.nextButton.setAutoRaise(True)
        self.nextButton.setToolTip(_translate("FindReplaceBar", "Find next", ""))
        self.nextButton.clicked.connect(self.find_next)

        self.caseSensitive = QCheckBox(
            _translate("FindReplaceBar", "Aa", "Case sensitive, abbreviated"), self
        )
        self.caseSensitive.setToolTip(
            _translate("FindReplaceBar", "Case sensitive", "")
        )
        self.caseSensitive.toggled.connect(self._on_search_options_changed)

        self.wholeWord = QCheckBox(
            _translate("FindReplaceBar", "Ab", "Whole word, abbreviated"), self
        )
        self.wholeWord.setToolTip(_translate("FindReplaceBar", "Whole word", ""))
        self.wholeWord.toggled.connect(self._on_search_options_changed)

        findRow = QHBoxLayout()
        findRow.addWidget(self.findField)
        findRow.addWidget(self.prevButton)
        findRow.addWidget(self.nextButton)
        findRow.addWidget(self.caseSensitive)
        findRow.addWidget(self.wholeWord)
        findRow.addWidget(self.closeButton)

        self.replaceField = QLineEdit(self)
        self.replaceField.setPlaceholderText(
            _translate("FindReplaceBar", "Replace...", "")
        )
        self.replaceField.returnPressed.connect(self.replace_current)
        self.replaceField.installEventFilter(self)

        self.replaceButton = QPushButton(
            _translate("FindReplaceBar", "Replace", ""), self
        )
        self.replaceButton.clicked.connect(self.replace_current)

        self.replaceAllButton = QPushButton(
            _translate("FindReplaceBar", "Replace All", ""), self
        )
        self.replaceAllButton.clicked.connect(self.replace_all)

        self.replaceRow = QWidget(self)
        replaceRowLayout = QHBoxLayout(self.replaceRow)
        replaceRowLayout.setContentsMargins(0, 0, 0, 0)
        replaceRowLayout.addWidget(self.replaceField)
        replaceRowLayout.addWidget(self.replaceButton)
        replaceRowLayout.addWidget(self.replaceAllButton)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(4, 2, 4, 2)
        mainLayout.addLayout(findRow)
        mainLayout.addWidget(self.replaceRow)

    # --- Showing/hiding -------------------------------------------------------

    def show_find(self):
        """Show the bar in find-only mode, focused and ready to type."""
        self.replaceRow.setVisible(False)
        self._open()

    def show_replace(self):
        """Show the bar with the replace row visible too."""
        self.replaceRow.setVisible(True)
        self._open()

    def _open(self):
        cursor = self._editor.textCursor()
        if cursor.hasSelection():
            self.findField.setText(cursor.selectedText())
        self._remember_anchor()
        self.show()
        self.findField.setFocus()
        self.findField.selectAll()

    def hide_bar(self):
        """Hide the bar, drop the match highlighting and return focus to the editor."""
        self.hide()
        self._editor.clear_search_highlight()
        self._editor.setFocus()

    def _remember_anchor(self):
        cursor = self._editor.textCursor()
        cursor.setPosition(min(cursor.position(), cursor.anchor()))
        self._searchAnchor = cursor

    # --- Searching --------------------------------------------------------

    def _on_search_text_changed(self, _text):
        # Every keystroke restarts the search from where the bar was opened,
        # instead of compounding from wherever the previous partial match
        # landed - otherwise typing "ci" would search for "c", then "ci"
        # from just after that "c".
        if self._searchAnchor is not None:
            self._editor.setTextCursor(self._searchAnchor)
        self._run_find(backward=False)

    def _on_search_options_changed(self, _checked):
        self._run_find(backward=False)

    def find_next(self):
        """Jump to the next match, wrapping around the document if needed."""
        self._run_find(backward=False)

    def find_previous(self):
        """Jump to the previous match, wrapping around the document if needed."""
        self._run_find(backward=True)

    def _run_find(self, *, backward):
        term = self.findField.text()
        found = self._editor.find(
            term,
            case_sensitive=self.caseSensitive.isChecked(),
            whole_word=self.wholeWord.isChecked(),
            backward=backward,
        )
        self.findField.setStyleSheet("" if found or not term else _NO_MATCH_STYLE)

    # --- Replacing --------------------------------------------------------

    def replace_current(self):
        """Replace the current match (if any is selected) and advance to the next one."""
        cursor = self._editor.textCursor()
        term = self.findField.text()
        matches = self.caseSensitive.isChecked() and cursor.selectedText() == term
        matches = matches or (
            not self.caseSensitive.isChecked()
            and cursor.selectedText().casefold() == term.casefold()
        )
        if cursor.hasSelection() and matches:
            cursor.insertText(self.replaceField.text())
        self.find_next()

    def replace_all(self):
        """Replace every match in the document, as a single undo step."""
        self._editor.replace_all(
            self.findField.text(),
            self.replaceField.text(),
            case_sensitive=self.caseSensitive.isChecked(),
            whole_word=self.wholeWord.isChecked(),
        )

    # --- Escape closes the bar ----------------------------------------------

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key_Escape:
            self.hide_bar()
            return True
        return super().eventFilter(watched, event)
