# -*- coding: utf-8 -*-
"""
Tests for FindReplaceBar (show/hide modes, driving pycktTextEditor's
find/replace, Escape closing the bar).
"""

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from pycirkuit.findreplacebar import FindReplaceBar
from pycirkuit.texteditor import pycktTextEditor


def _bar():
    QApplication.instance() or QApplication([])
    editor = pycktTextEditor()
    editor.resize(400, 300)
    editor.setPlainText("foo bar foo baz foo\n")
    bar = FindReplaceBar(editor)
    return bar, editor


def _escape_event():
    return QKeyEvent(
        QKeyEvent.Type.KeyPress, Qt.Key_Escape, Qt.KeyboardModifier.NoModifier
    )


def test_show_find_hides_replace_row_and_focuses_field():
    bar, _editor = _bar()
    bar.show_replace()
    bar.show_find()
    assert bar.replaceRow.isVisible() is False
    assert bar.isVisible() is True


def test_show_replace_shows_replace_row():
    bar, _editor = _bar()
    bar.show_replace()
    assert bar.replaceRow.isVisible() is True


def test_show_find_seeds_field_from_selection():
    bar, editor = _bar()
    cursor = editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(3, cursor.MoveMode.KeepAnchor)
    editor.setTextCursor(cursor)
    bar.show_find()
    assert bar.findField.text() == "foo"


def test_find_next_selects_next_match_in_editor():
    bar, editor = _bar()
    bar.show_find()
    bar.findField.setText("foo")
    bar.find_next()
    assert editor.textCursor().selectedText() == "foo"
    firstMatch = editor.textCursor().selectionStart()

    bar.find_next()
    assert editor.textCursor().selectionStart() > firstMatch


def test_replace_all_updates_editor_text():
    bar, editor = _bar()
    bar.show_replace()
    bar.findField.setText("foo")
    bar.replaceField.setText("X")
    bar.replace_all()
    assert editor.toPlainText() == "X bar X baz X\n"


def test_escape_in_find_field_hides_bar():
    bar, editor = _bar()
    bar.show_find()
    assert bar.isVisible() is True
    bar.eventFilter(bar.findField, _escape_event())
    assert bar.isVisible() is False


def test_hide_bar_clears_search_highlight():
    bar, editor = _bar()
    bar.show_find()
    bar.findField.setText("foo")
    bar.find_next()
    assert editor._search_match_selections() != []
    bar.hide_bar()
    assert editor._search_match_selections() == []
