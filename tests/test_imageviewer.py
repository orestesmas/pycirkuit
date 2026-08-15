# -*- coding: utf-8 -*-
"""
Regression test for pycktImageViewer's Ctrl+wheel zoom: PySide6/Qt6 removed
QWheelEvent.pos()/globalPos() in favor of position()/globalPosition(),
which broke this at runtime (no static analysis catches it - it's only
exercised by an actual QWheelEvent).
"""
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QPoint, QPointF, QRectF, Qt
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QApplication

import pycirkuit
from pycirkuit.imageviewer import pycktImageViewer


@pytest.fixture
def viewer(tmp_path, monkeypatch):
    QApplication.instance() or QApplication([])

    class FakeTmpDir:
        def path(self):
            return str(tmp_path)

    pycirkuit.__tmpDir__ = FakeTmpDir()
    monkeypatch.setattr("pycirkuit.imageviewer.ToolPdfToPng", MagicMock())

    v = pycktImageViewer()
    v.resize(400, 300)
    v._pycktImageViewer__file_base_name = "fake"
    v.setImage = MagicMock()
    yield v


def _ctrl_wheel_event(x=200, y=150, delta=120):
    pos = QPointF(x, y)
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


def test_ctrl_wheel_zoom_does_not_raise_when_scene_fits_viewport(viewer):
    # currentViewportRect.contains(currentSceneRect) branch
    viewer._pycktImageViewer__scene.addRect(QRectF(0, 0, 10, 10))
    viewer.wheelEvent(_ctrl_wheel_event())
    viewer.setImage.assert_called_once()


def test_ctrl_wheel_zoom_does_not_raise_when_scene_exceeds_viewport(viewer):
    # else branch: uses event.position() to keep the point under the cursor
    viewer._pycktImageViewer__scene.addRect(QRectF(0, 0, 2000, 2000))
    viewer.wheelEvent(_ctrl_wheel_event())
    viewer.setImage.assert_called_once()


def test_wheel_event_ignored_without_a_loaded_image(viewer):
    viewer._pycktImageViewer__file_base_name = None
    viewer.wheelEvent(_ctrl_wheel_event())
    viewer.setImage.assert_not_called()
