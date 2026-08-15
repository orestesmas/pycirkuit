# -*- coding: utf-8 -*-
"""
Characterization tests for PyCirkuitProcessor: lock down the pipeline's
call order and memoization behaviour before it's refactored further.
External tools are stand-in MagicMocks (see conftest.py's `processor`
fixture) - these tests never call m4/dpic/lualatex/pdftoppm/pdf2svg for
real.
"""
import os

from PySide6.QtCore import QSettings

import pycirkuit
from pycirkuit.tools.m4 import ToolM4
from pycirkuit.tools.dpic import ToolDpic
from pycirkuit.tools.latex import ToolLaTeX
from pycirkuit.tools.pdftopng import ToolPdfToPng
from pycirkuit.tools.pdftojpg import ToolPdfToJpeg
from pycirkuit.tools.pdftosvg import ToolPdfToSvg
from pycirkuit.tools.processor import PyCirkuitProcessor


def test_toPic_calls_m4_exactly_once(processor):
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toPic()
    processor.toPic()  # repeated call must be memoized, not re-run

    assert processor.extTools[ToolM4].execute.call_count == 1
    assert processor.picExists is True


def test_toTikz_cascades_through_toPic(processor):
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toTikz()

    assert processor.extTools[ToolM4].execute.call_count == 1
    assert processor.extTools[ToolDpic].execute.call_count == 1
    assert processor.picExists is True
    assert processor.tikzExists is True


def test_toPdf_cascades_through_tikz_and_pic(processor):
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toPdf()

    assert processor.extTools[ToolM4].execute.call_count == 1
    assert processor.extTools[ToolDpic].execute.call_count == 1
    assert processor.extTools[ToolLaTeX].execute.call_count == 1
    assert processor.pdfExists is True


def test_toSvg_goes_through_pdf_not_pic_directly(processor):
    """Regression guard for the dpic -> pdf2svg switch (step 4): SVG must
    depend on the rendered PDF, not go straight from .pic like it used to."""
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toSvg()

    # The whole PDF cascade ran on the way to the SVG...
    assert processor.extTools[ToolM4].execute.call_count == 1
    assert processor.extTools[ToolDpic].execute.call_count == 1
    assert processor.extTools[ToolLaTeX].execute.call_count == 1
    assert processor.pdfExists is True
    # ...and the SVG itself was produced from the PDF via pdf2svg.
    assert processor.extTools[ToolPdfToSvg].execute.call_count == 1
    assert processor.svgExists is True


def test_toPng_reuses_already_generated_pdf(processor):
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toPdf()
    processor.toPng(dpi=150)

    # toPdf() was already satisfied above; toPng() must not redo it.
    assert processor.extTools[ToolLaTeX].execute.call_count == 1
    processor.extTools[ToolPdfToPng].execute.assert_called_once_with(
        processor.TMP_FILE_BASENAME, resolution=150
    )


def test_toJpeg_passes_dpi_and_quality(processor):
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toJpeg(dpi=200, q=90)

    processor.extTools[ToolPdfToJpeg].execute.assert_called_once_with(
        processor.TMP_FILE_BASENAME, resolution=200, quality=90
    )
    assert processor.jpegExists is True


def test_beginProcessingSource_resets_memoized_state(processor):
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toPdf()
    assert processor.pdfExists is True

    # Starting a new processing round must forget everything generated so
    # far, or a second "Process" click in the GUI would silently reuse a
    # stale PDF instead of regenerating it from the (possibly edited) source.
    processor.beginProcessingSource(".PS\n.PE\n")
    assert processor.picExists is False
    assert processor.tikzExists is False
    assert processor.pdfExists is False
    assert processor.pngExists is False
    assert processor.jpegExists is False
    assert processor.svgExists is False


def test_beginProcessingSource_writes_the_given_text(processor):
    processor.beginProcessingSource("hello circuit")
    with open(processor.TMP_FILE_BASENAME + ".ckt") as f:
        assert f.read() == "hello circuit"


def test_beginProcessing_copies_source_file(processor, tmp_path):
    srcFile = tmp_path / "example.ckt"
    srcFile.write_text("some circuit macros source")

    processor.beginProcessing(str(srcFile))

    with open(processor.TMP_FILE_BASENAME + ".ckt") as f:
        assert f.read() == "some circuit macros source"


def test_printProgress_true_writes_to_stdout(processor, capsys):
    processor.printProgress = True
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toPic()

    assert "PIC" in capsys.readouterr().out


def test_printProgress_false_is_silent(processor, capsys):
    processor.printProgress = False
    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toPic()

    assert capsys.readouterr().out == ""


def test_check_programs_uses_configured_engine(fake_tools_on_path):
    QSettings().setValue("General/latexEngine", "pdflatex")
    proc = PyCirkuitProcessor()
    try:
        proc.check_programs()
        assert proc.extTools[ToolLaTeX].shortName == "pdfLaTeX"
    finally:
        os.chdir(proc.savedWD)
        pycirkuit.__tmpDir__.remove()


def test_check_programs_defaults_to_lualatex_when_unset(fake_tools_on_path):
    proc = PyCirkuitProcessor()
    try:
        proc.check_programs()
        assert proc.extTools[ToolLaTeX].shortName == "LuaLaTeX"
    finally:
        os.chdir(proc.savedWD)
        pycirkuit.__tmpDir__.remove()


# --- pipeline step signals -------------------------------------------------


def test_signals_fire_in_order_for_the_whole_cascade(processor):
    events = []
    processor.stepStarted.connect(lambda name: events.append(("started", name)))
    processor.stepFinished.connect(lambda name: events.append(("finished", name)))

    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toPdf()

    assert events == [
        ("started", "PIC"),
        ("finished", "PIC"),
        ("started", "TIKZ"),
        ("finished", "TIKZ"),
        ("started", "PDF"),
        ("finished", "PDF"),
    ]


def test_memoized_step_does_not_re_emit_signals(processor):
    events = []
    processor.stepStarted.connect(lambda name: events.append(name))

    processor.beginProcessingSource(".PS\n.PE\n")
    processor.toPic()
    processor.toPic()

    assert events == ["PIC"]


def test_step_failure_emits_stepFailed_and_still_raises(processor):
    from pycirkuit.exceptions import PyCktToolExecutionError

    processor.extTools[ToolM4].execute.side_effect = PyCktToolExecutionError(
        "boom", tool=ToolM4
    )
    events = []
    processor.stepFailed.connect(lambda name: events.append(name))

    processor.beginProcessingSource(".PS\n.PE\n")
    try:
        processor.toPic()
        assert False, "expected PyCktToolExecutionError to propagate"
    except PyCktToolExecutionError:
        pass

    assert events == ["PIC"]
    # A failed step must not be marked as done - a later retry should still
    # try to actually run it again, not silently skip it as "memoized".
    assert processor.picExists is False
