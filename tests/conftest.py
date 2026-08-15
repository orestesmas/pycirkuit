# -*- coding: utf-8 -*-
"""
Shared pytest fixtures for the PyCirkuit test suite.
"""
import os
from unittest.mock import MagicMock

import pytest
from PyQt5.QtCore import QCoreApplication, QSettings

import pycirkuit
from pycirkuit.tools.processor import PyCirkuitProcessor


@pytest.fixture(autouse=True)
def isolated_settings(tmp_path):
    """Redirect QSettings to a throwaway directory for every test, so the
    suite never reads or overwrites the developer's real PyCirkuit config."""
    QCoreApplication.setOrganizationName("PyCirkuit")
    QCoreApplication.setApplicationName("pycirkuit")
    QSettings.setDefaultFormat(QSettings.IniFormat)
    QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, str(tmp_path))
    yield


@pytest.fixture
def fake_tools_on_path(monkeypatch):
    """Make ExternalTool.__init__'s PATH search succeed for any executable
    name, without needing m4/dpic/lualatex/etc. actually installed. Only
    the real filesystem lookups under the fake bin dir are faked - other
    os.path.exists() calls elsewhere behave normally."""
    fake_bin = os.sep + "fake-bin"
    real_exists = os.path.exists

    def fake_exists(path):
        if os.path.dirname(path) == fake_bin:
            return True
        return real_exists(path)

    monkeypatch.setattr(os.path, "exists", fake_exists)
    monkeypatch.setattr(os, "get_exec_path", lambda: [fake_bin])


@pytest.fixture
def processor():
    """A PyCirkuitProcessor with environment checks bypassed and a dict of
    MagicMock stand-ins for its external tools, so tests exercise only
    PyCirkuitProcessor's own orchestration logic (call order, memoization),
    never real subprocesses."""
    proc = PyCirkuitProcessor()
    proc.printProgress = False
    proc.environmentOk = True
    proc.extTools = {
        cls: MagicMock(name=cls.__name__)
        for cls in _tool_classes()
    }
    yield proc
    # PyCirkuitProcessor.__del__ does this too, but __del__ timing isn't
    # guaranteed, and leaving the test process's cwd inside a
    # since-forgotten temp dir would break every test that runs after it.
    os.chdir(proc.savedWD)
    pycirkuit.__tmpDir__.remove()


def _tool_classes():
    from pycirkuit.tools.m4 import ToolM4
    from pycirkuit.tools.dpic import ToolDpic
    from pycirkuit.tools.latex import ToolLaTeX
    from pycirkuit.tools.pdftopng import ToolPdfToPng
    from pycirkuit.tools.pdftojpg import ToolPdfToJpeg
    from pycirkuit.tools.pdftosvg import ToolPdfToSvg

    return [ToolM4, ToolDpic, ToolLaTeX, ToolPdfToPng, ToolPdfToJpeg, ToolPdfToSvg]
