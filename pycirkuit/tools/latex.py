# -*- coding: utf-8 -*-
"""
Module implementing a class to handle a LaTeX engine external tool
(pdflatex, lualatex...), and a small registry of the engines PyCirkuit
supports.
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

# Standard library imports
import re

# Third-party imports
from PySide6.QtCore import QCoreApplication, QSettings

# Local application imports
from pycirkuit.tools.tool_base import ExternalTool, PyCktToolExecutionError

# Translation function
_translate = QCoreApplication.translate


class ToolLaTeX(ExternalTool):
    """A LaTeX engine (pdflatex, lualatex...) able to compile a TikZ source,
    wrapped in the configured template, into a PDF."""

    def __init__(self, executableName, longName, shortName):
        super().__init__(executableName, longName)
        # Used for terser messages (e.g. "LuaLaTeX: Error converting...")
        # where the full longName ("LuaLaTeX program") would read awkwardly.
        self.shortName = shortName

    def execute(self, baseName):
        # Calculate src and dst names
        tikz = baseName + ".tikz"
        tex = baseName + ".tex"
        # Instantiate a settings object to load config values. At this point the config have valid entries, so don't test much
        settings = QSettings()
        latexTemplateFile = settings.value("General/templatePath")
        # Now we read a LaTeX template and wrap the tikz code inside
        templateCode = ""
        with open(
            "{templateFile}".format(templateFile=latexTemplateFile), "r"
        ) as template:
            templateCode = template.read()
        with (
            open("{source}".format(source=tikz), "r") as f,
            open("{destination}".format(destination=tex), "w") as g,
        ):
            source = f.read()
            dest = templateCode.replace("%%SOURCE%%", source, 1)
            g.write(dest)
            g.write("\n")
        # Execution of the LaTeX engine creates a PDF file
        command = [
            self.executableName,
            "-interaction=batchmode",
            "-halt-on-error",
            "{texFile}".format(texFile=tex),
        ]
        # NOTE: keep context/source/comment on one folded line - pylupdate5's
        # scanner misses _translate() calls that Black wraps one-arg-per-line.
        errMsgTemplate = _translate(
            "ExternalTool", "{engine}: Error converting TIKZ -> PDF", "Error message"
        )
        errMsg = errMsgTemplate.format(engine=self.shortName)
        try:
            super().execute(command, errMsg)
        except PyCktToolExecutionError as err:
            # If a LaTeX error has been triggered, try to obtain a meaningful error message
            # Very useful: https://regex101.com/#python
            info = ""
            with open("{basename}.log".format(basename=baseName), "r") as log:
                expr = r"! (\S.*$)|l\.([0-9]+) (.*$)"
                prog = re.compile(expr)
                for line in log:
                    # 'match' searches from line beginning
                    match = prog.match(line)
                    if match:
                        if match.group(0)[0] == "l":
                            # TODO: Perhaps we can return some info (error string?) to allow spotting the error at the source file
                            info = (
                                _translate(
                                    "ExternalTool",
                                    "Error at TeX file line number {N}".format(
                                        N=match.group(2)
                                    ),
                                    "Error message. Don't translate '{N}'",
                                )
                                + "\n"
                            )
                            info += match.group(3) + "\n"
                        else:
                            info += match.group(1) + "\n"
            err.moreInfo = info
            raise err


# Registry of the LaTeX engines PyCirkuit knows how to drive. Each entry maps
# an engine id (stored in settings, used as a template filename suffix) to
# its executable name and display names.
#
# NOTE: keep every _translate() call's context/source/comment folded onto one
# line - pylupdate5's scanner misses calls that Black wraps one-arg-per-line,
# which a dict-of-dicts layout here would force. Shallow local variables
# avoid that.
def _engine_specs():
    pdflatex_long = _translate("ExternalTool", "pdfLaTeX program", "Tool Long Name")
    pdflatex_short = _translate("ExternalTool", "pdfLaTeX", "LaTeX engine name")
    lualatex_long = _translate("ExternalTool", "LuaLaTeX program", "Tool Long Name")
    lualatex_short = _translate("ExternalTool", "LuaLaTeX", "LaTeX engine name")
    return {
        "pdflatex": {
            "executable": "pdflatex",
            "longName": pdflatex_long,
            "shortName": pdflatex_short,
        },
        "lualatex": {
            "executable": "lualatex",
            "longName": lualatex_long,
            "shortName": lualatex_short,
        },
    }


# lualatex handles UTF-8/fonts natively, avoiding the wrong-character
# rendering that pdflatex-era template packages (inputenc, fontenc,
# lmodern) caused.
DEFAULT_LATEX_ENGINE = "lualatex"


def latex_engine_choices():
    """Return an ordered list of (engineId, shortDisplayName) for UI population."""
    return [(engineId, spec["shortName"]) for engineId, spec in _engine_specs().items()]


def create_latex_engine(engineId):
    """Instantiate the ToolLaTeX for the given engine id.

    Falls back to DEFAULT_LATEX_ENGINE for an unrecognized id (e.g. a stale
    settings value from a downgrade). Raises PyCktToolNotFoundError, like any
    other ExternalTool, if the chosen engine's executable isn't installed.
    """
    specs = _engine_specs()
    spec = specs.get(engineId, specs[DEFAULT_LATEX_ENGINE])
    return ToolLaTeX(spec["executable"], spec["longName"], spec["shortName"])


def default_template_filename(engineId):
    """The bundled default template filename for a given engine id."""
    return "cm_tikz_{engineId}.tpl".format(engineId=engineId)
