# -*- coding: utf-8 -*-
"""
Tests for pycktTextEditor (line numbers, current-line/bracket-match
highlighting, comment toggling, zoom) and PyCirkuitHighlighter.
"""

from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QKeyEvent, QTextCursor, QWheelEvent
from PySide6.QtWidgets import QApplication

from pycirkuit.highlighter import PyCirkuitHighlighter
from pycirkuit.texteditor import pycktTextEditor


def _editor():
    QApplication.instance() or QApplication([])
    e = pycktTextEditor()
    e.resize(400, 300)
    return e


def _select(editor, start, end):
    cursor = editor.textCursor()
    cursor.setPosition(start)
    cursor.setPosition(end, QTextCursor.KeepAnchor)
    editor.setTextCursor(cursor)


def _place_cursor(editor, pos):
    cursor = editor.textCursor()
    cursor.setPosition(pos)
    editor.setTextCursor(cursor)


def _ctrl_slash_event(extra_modifiers=Qt.KeyboardModifier.NoModifier):
    return QKeyEvent(
        QKeyEvent.Type.KeyPress,
        Qt.Key_Slash,
        Qt.KeyboardModifier.ControlModifier | extra_modifiers,
        "/",
    )


def _ctrl_wheel_event(delta=120):
    pos = QPointF(10, 10)
    return QWheelEvent(
        pos,
        pos,
        QPoint(0, 0),
        QPoint(0, delta),
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.ControlModifier,
        Qt.ScrollPhase.NoScrollPhase,
        False,
    )


def test_line_number_area_width_grows_with_line_count():
    e = _editor()
    e.setPlainText("\n".join(str(i) for i in range(5)))
    narrow = e.lineNumberAreaWidth()
    e.setPlainText("\n".join(str(i) for i in range(500)))
    wide = e.lineNumberAreaWidth()
    assert wide > narrow


def test_bracket_match_finds_pair_across_lines():
    e = _editor()
    e.setPlainText("box(width,height) {\n  arrow right\n}\n")
    text = e.toPlainText()

    _place_cursor(e, text.index("(") + 1)
    matches = e._bracket_match_selections()
    assert len(matches) == 2

    _place_cursor(e, text.index("{") + 1)
    matches = e._bracket_match_selections()
    assert len(matches) == 2


def test_bracket_match_empty_when_cursor_not_on_bracket():
    e = _editor()
    e.setPlainText("box(width,height)\n")
    _place_cursor(e, 1)
    assert e._bracket_match_selections() == []


def test_toggle_comment_on_selection_then_back():
    e = _editor()
    e.setPlainText("box(w,h) {\n  arrow right\n}\n# already commented\n")
    text = e.toPlainText()
    _select(e, text.index("box"), text.index("}") + 1)

    e._toggle_comment()
    commented = e.toPlainText()
    assert "# box(w,h) {" in commented
    assert "#   arrow right" in commented
    assert "# }" in commented
    # The pre-existing comment outside the selection is untouched.
    assert "# already commented" in commented

    _select(e, commented.index("box"), commented.index("}") + 1)
    e._toggle_comment()
    assert e.toPlainText() == text


def test_toggle_comment_via_real_key_event():
    e = _editor()
    e.setPlainText("arrow right\n")
    _place_cursor(e, 0)
    e.keyPressEvent(_ctrl_slash_event())
    assert e.toPlainText().startswith("# arrow right")


def test_toggle_comment_via_key_event_with_incidental_shift():
    # On ES/CAT keyboards '/' is typed as Shift+7, so Ctrl+/ arrives as
    # Ctrl+Shift+Slash. Shift must not prevent the shortcut from firing.
    e = _editor()
    e.setPlainText("arrow right\n")
    _place_cursor(e, 0)
    e.keyPressEvent(_ctrl_slash_event(Qt.KeyboardModifier.ShiftModifier))
    assert e.toPlainText().startswith("# arrow right")


def test_ctrl_wheel_zoom_changes_font_size():
    e = _editor()
    before = e.font().pointSize()
    e.wheelEvent(_ctrl_wheel_event(delta=120))
    assert e.font().pointSize() == before + 1


def test_highlighter_formats_pic_keyword():
    e = _editor()
    PyCirkuitHighlighter(e.document())
    e.setPlainText("arrow right from Here\n")
    block = e.document().findBlockByNumber(0)
    formats = block.layout().formats()
    assert len(formats) == 4
    for fr in formats:
        assert fr.format.foreground().color().name() == "#0000ff"
        assert fr.format.fontItalic() is True
