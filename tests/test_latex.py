# -*- coding: utf-8 -*-
"""
Tests for the LaTeX engine registry (tools/latex.py), introduced in
MODERNIZATION.md step 5 to replace the old pdflatex.py/lualatex.py
duplication.
"""
from pycirkuit.tools.latex import (
    DEFAULT_LATEX_ENGINE,
    ToolLaTeX,
    create_latex_engine,
    default_template_filename,
    latex_engine_choices,
)


def test_default_engine_is_lualatex():
    assert DEFAULT_LATEX_ENGINE == "lualatex"


def test_latex_engine_choices_lists_both_engines():
    ids = [engineId for engineId, _ in latex_engine_choices()]
    assert ids == ["pdflatex", "lualatex"]


def test_create_latex_engine_pdflatex(fake_tools_on_path):
    tool = create_latex_engine("pdflatex")

    assert isinstance(tool, ToolLaTeX)
    assert tool.executableName.endswith("pdflatex")
    assert tool.shortName == "pdfLaTeX"


def test_create_latex_engine_lualatex(fake_tools_on_path):
    tool = create_latex_engine("lualatex")

    assert tool.executableName.endswith("lualatex")
    assert tool.shortName == "LuaLaTeX"


def test_create_latex_engine_unknown_id_falls_back_to_default(fake_tools_on_path):
    tool = create_latex_engine("some-future-engine-nobody-added-yet")

    assert tool.executableName.endswith(DEFAULT_LATEX_ENGINE)


def test_default_template_filename_matches_shipped_files():
    # These exact filenames must exist under pycirkuit/templates/.
    assert default_template_filename("pdflatex") == "cm_tikz_pdflatex.tpl"
    assert default_template_filename("lualatex") == "cm_tikz_lualatex.tpl"
