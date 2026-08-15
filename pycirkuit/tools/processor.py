# -*- coding: utf-8 -*-
"""
Application core functionality
"""

# Copyright (C) 2018-2026 Orestes Mas
# Copyright (C) 2019 Aniol Marti
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

# Standard library imports
import os
import shutil
from enum import Enum

# Third-party imports
from PyQt5.QtCore import QCoreApplication, QObject, QTemporaryDir, QSettings, pyqtSignal

# Local imports
import pycirkuit
from pycirkuit import Option
from pycirkuit.exceptions import *
from pycirkuit.tools.m4 import ToolM4
from pycirkuit.tools.dpic import ToolDpic
from pycirkuit.tools.latex import ToolLaTeX, create_latex_engine, DEFAULT_LATEX_ENGINE
from pycirkuit.tools.pdftopng import ToolPdfToPng
from pycirkuit.tools.pdftojpg import ToolPdfToJpeg
from pycirkuit.tools.pdftosvg import ToolPdfToSvg
from pycirkuit.tools.circuitmacrosmanager import CircuitMacrosManager

# Translation function
_translate = QCoreApplication.translate


class Overwrite(Enum):
    UNSET = 0
    YES = 1
    ALL = 2
    NO = 3
    NEVER = 4


class PyCirkuitProcessor(QObject):
    TMP_FILE_BASENAME = "cirkuit_tmp"

    # Emitted around each pipeline step (PIC/TIKZ/PDF/SVG/PNG/JPEG) that
    # actually runs (memoized steps don't re-emit). Lets callers (the GUI,
    # in particular) react to progress without the pipeline itself needing
    # to know anything about progress bars or log widgets.
    stepStarted = pyqtSignal(str)
    stepFinished = pyqtSignal(str)
    stepFailed = pyqtSignal(str)

    def __init__(self):
        self.environmentOk = False
        super().__init__()
        self.overwrite = Overwrite.UNSET
        # CLI-only terminal progress narrative ("file.ckt -> PIC -> TIKZ -> ...").
        # The GUI shares these same step methods but has its own progress
        # bar/log widget, so it turns this off (see MainWindow.__init__).
        self.printProgress = True
        # Save current work dir and change into a temporary one
        self.savedWD = os.getcwd()
        pycirkuit.__tmpDir__ = QTemporaryDir()
        os.chdir(pycirkuit.__tmpDir__.path())

    def __del__(self):
        # Restore working dir and remove temporary dir
        os.chdir(self.savedWD)
        pycirkuit.__tmpDir__.remove()

    def check_latex_template(self):
        settings = QSettings()
        template = settings.value("General/templatePath", "")
        if os.path.exists(template):
            with open(template, "r") as t:
                templateCode = t.read()
                if "%%SOURCE%%" in templateCode:
                    return True
                else:
                    raise PyCktLatexTemplateError(
                        _translate(
                            "CommandLine",
                            "Found an invalid LaTeX template.",
                            "Error message.",
                        )
                    )
        else:
            raise PyCktLatexTemplateError(
                _translate("CommandLine", "LaTeX template not found.", "Error message.")
            )

    def check_programs(self):
        # Dictionary using a class as index and a class instance as value
        settings = QSettings()
        engineId = settings.value("General/latexEngine", DEFAULT_LATEX_ENGINE)
        self.extTools = {
            ToolM4: ToolM4(),
            ToolDpic: ToolDpic(),
            ToolLaTeX: create_latex_engine(engineId),
            ToolPdfToPng: ToolPdfToPng(),
            ToolPdfToJpeg: ToolPdfToJpeg(),
            ToolPdfToSvg: ToolPdfToSvg(),
        }

    def check_circuit_macros(self):
        cmMgr = CircuitMacrosManager()
        if not cmMgr.check_installed():
            raise PyCktCMNotFoundError(
                _translate(
                    "CommandLine",
                    "Cannot find the Circuit Macros!",
                    "Command line error message.",
                )
            )

    def _askUser(self):
        print(
            _translate(
                "CommandLine-UserInput1",
                "\nThe destination file already exists.",
                "Command line message. THE STARTING NEWLINE CHARACTER (\n) IS IMPORTANT.",
            )
        )
        question = _translate(
            "CommandLine-UserInput1",
            "Would you like to overwrite it? ([y]es | [n]o | yes to [a]ll | ne[v]er): ",
            "WARNING!! Critical translation. You should translate this message to your language, enclosing into brackets one single DIFFERENT character for each option, and translate accordingly the characters in the next message.",
        )
        answerYes = _translate(
            "CommandLine-UserInput1",
            "y",
            "WARNING!! Critical translation. This char must match one of those of the message 'Would you like to overwrite it?'",
        )
        answerNo = _translate(
            "CommandLine-UserInput1",
            "n",
            "WARNING!! Critical translation. This char must match one of those of the message 'Would you like to overwrite it?'",
        )
        answerAll = _translate(
            "CommandLine-UserInput1",
            "a",
            "WARNING!! Critical translation. This char must match one of those of the message 'Would you like to overwrite it?'",
        )
        answerNever = _translate(
            "CommandLine-UserInput1",
            "v",
            "WARNING!! Critical translation. This char must match one of those of the message 'Would you like to overwrite it?'",
        )
        answers = {
            answerYes: Overwrite.YES,
            answerNo: Overwrite.NO,
            answerAll: Overwrite.ALL,
            answerNever: Overwrite.NEVER,
        }
        while True:
            answer = input(question)
            if answer.lower() not in answers:
                continue
            else:
                return answers[answer]

    def checkEnvironment(self):
        self.check_programs()
        self.check_circuit_macros()
        self.check_latex_template()
        self.environmentOk = True

    def _reset_state(self):
        # Set all formats to "ungenerated" state
        self.picExists = self.tikzExists = self.svgExists = self.pdfExists = (
            self.pngExists
        ) = self.jpegExists = False

    def beginProcessing(self, src):
        """Start processing a source file already on disk (CLI/batch entry point)."""
        # 1) Check if all tools are installed
        if not self.environmentOk:
            self.checkEnvironment()
        # 2) Reset memoized conversion state
        self._reset_state()
        # Copy source file into temporary file
        self.sourceFile = src
        dst = PyCirkuitProcessor.TMP_FILE_BASENAME + ".ckt"
        shutil.copy(src, dst)
        if self.printProgress:
            print(os.path.basename(self.sourceFile), end="")

    def beginProcessingSource(self, sourceText):
        """Start processing raw source text (GUI entry point), e.g. an editor
        buffer that may not be saved to disk yet."""
        # 1) Check if all tools are installed
        if not self.environmentOk:
            self.checkEnvironment()
        # 2) Reset memoized conversion state
        self._reset_state()
        self.sourceFile = None
        dst = PyCirkuitProcessor.TMP_FILE_BASENAME + ".ckt"
        with open(dst, "w") as f:
            f.write(sourceText)

    def requestResult(
        self, option, dstDir="", overwrite=Overwrite.UNSET, dpi=None, quality=None
    ):
        if option == Option.PNG:
            extension = "png"
            startPoint = self.toPng
            formatToCheck = self.pngExists
        elif option == Option.JPEG:
            extension = "jpeg"
            startPoint = self.toJpeg
            formatToCheck = self.jpegExists
        elif option == Option.PDF:
            extension = "pdf"
            startPoint = self.toPdf
            formatToCheck = self.pdfExists
        elif option == Option.SVG:
            extension = "svg"
            startPoint = self.toSvg
            formatToCheck = self.svgExists
        elif option == Option.TIKZ:
            extension = "tikz"
            startPoint = self.toTikz
            formatToCheck = self.tikzExists
        if (overwrite == Overwrite.ALL) or (overwrite == Overwrite.NEVER):
            self.overwrite = overwrite
        src = (
            os.path.join(
                pycirkuit.__tmpDir__.path(), PyCirkuitProcessor.TMP_FILE_BASENAME
            )
            + os.extsep
            + extension
        )
        if dstDir:
            filename = os.path.basename(self.sourceFile).rpartition(os.extsep)[0]
            dst = os.path.join(dstDir, filename) + os.extsep + extension
        else:
            dst = self.sourceFile.rpartition(os.extsep)[0] + os.extsep + extension
        if os.path.isfile(dst):
            if self.overwrite == Overwrite.UNSET:
                self.overwrite = self._askUser()
            if (self.overwrite == Overwrite.NO) or (self.overwrite == Overwrite.NEVER):
                if self.overwrite == Overwrite.NO:
                    self.overwrite = Overwrite.UNSET
                return
            if self.overwrite == Overwrite.YES:
                self.overwrite = Overwrite.UNSET
        # Let's recurse
        if not formatToCheck:
            startPoint(dpi, quality)
        # Si el font NO existeix, demanar crear-lo. Això implica
        shutil.copy(src, dst)

    def _run_step(self, name, work, label=None):
        """Run one pipeline step's own tool call, wrapped in stepStarted/
        stepFinished/stepFailed signals. Cascading to prerequisite steps
        (e.g. toPdf() calling toTikz() first) happens outside this, in each
        toXxx() method below, so prerequisites emit their own signals too.
        `label` overrides `name` for the CLI's printed narrative only, for
        steps that want to show extra detail (e.g. dpi)."""
        self.stepStarted.emit(name)
        try:
            work()
        except PyCktToolExecutionError:
            self.stepFailed.emit(name)
            raise
        self.stepFinished.emit(name)
        if self.printProgress:
            print(" -> " + (name if label is None else label), end="")

    def toPng(self, dpi, q=None):
        if not self.pngExists:
            self.toPdf()
            self._run_step(
                "PNG",
                lambda: self.extTools[ToolPdfToPng].execute(
                    PyCirkuitProcessor.TMP_FILE_BASENAME, resolution=dpi
                ),
                label="PNG ({} dpi)".format(dpi),
            )
            self.pngExists = True
        return True

    def toJpeg(self, dpi, q):
        if not self.jpegExists:
            self.toPdf()
            self._run_step(
                "JPEG",
                lambda: self.extTools[ToolPdfToJpeg].execute(
                    PyCirkuitProcessor.TMP_FILE_BASENAME, resolution=dpi, quality=q
                ),
                label="JPEG ({dpi} dpi, {q}% quality)".format(dpi=dpi, q=q),
            )
            self.jpegExists = True
        return True

    def toPdf(self, dpi=None, q=None):
        if not self.pdfExists:
            self.toTikz()
            self._run_step(
                "PDF",
                lambda: self.extTools[ToolLaTeX].execute(
                    PyCirkuitProcessor.TMP_FILE_BASENAME
                ),
            )
            self.pdfExists = True
        return True

    def toSvg(self, dpi=None, q=None):
        if not self.svgExists:
            # Go through the PDF rather than asking dpic for SVG directly:
            # dpic's own SVG output is noticeably lower quality (e.g. text
            # placement/fonts), whereas rendering via LaTeX and converting
            # the resulting PDF with pdf2svg reuses the same, better,
            # LaTeX-driven rendering as the PDF/PNG/JPEG outputs. One
            # consequence: the font set up in the LaTeX template now affects
            # the SVG output too, which it didn't before.
            self.toPdf()
            self._run_step(
                "SVG",
                lambda: self.extTools[ToolPdfToSvg].execute(
                    PyCirkuitProcessor.TMP_FILE_BASENAME
                ),
            )
            self.svgExists = True
        return True

    def toTikz(self, dpi=None, q=None):
        if not self.tikzExists:
            self.toPic()
            self._run_step(
                "TIKZ",
                lambda: self.extTools[ToolDpic].execute(
                    PyCirkuitProcessor.TMP_FILE_BASENAME, outputType=Option.TIKZ
                ),
            )
            self.tikzExists = True
        return True

    def toPic(self, dpi=None, q=None):
        if not self.picExists:
            self._run_step(
                "PIC",
                lambda: self.extTools[ToolM4].execute(
                    PyCirkuitProcessor.TMP_FILE_BASENAME
                ),
            )
            self.picExists = True
        return True
