# -*- coding: utf-8 -*-

"""
Application core functionality
"""
# Copyright (C) 2018-2019 Orestes Mas
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
import sys
from os.path import abspath, isfile
import glob

# Third-party imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, QCommandLineParser, QCommandLineOption

# Local imports
from .tools.commandlineoptions import CommandLineOptions
from pycirkuit import outputFormat

# Translation function
_translate = QCoreApplication.translate

_appDescription = """
PyCirkuit is a GUI front-end for Circuit Macros by Dwight Aplevich,
which are a set of macros for drawing high-quality line diagrams
to be included in TeX, LaTeX, web or similar documents."""
_batchOption = "Convert files specified by <path> to {} format in batch mode. Several output formats can be used together."
_dpiOption = "Sets the resolution of output bitmap images (png, jpg), in dots per inch. Value <N> is mandatory."
_qualityOption = "Sets the quality of output bitmap lossy images (jpg), in percent. Value <Q> is mandatory."
_recurseOption = "Using this option the pattern '**' will match any files and zero or more subdirs, so '**/*.ckt' will match all files with 'ckt' extension in the current directory and all its subdirectories"
_pathDescription = """Path(s) to source drawing file(s) to process. Wildcards accepted.
- If no <path> is given, the GUI is opened.
- If <path> points to only one file and no batch conversion options are present, this file is opened into the GUI for editing.
- If <path>s point to more than one valid file and a combination of output formats options are present, these source files are processed sequentially in batch (unattended) mode and converted into the requested formats.
- Specifying more than one file to process with no output format options present is not allowed."""

class PyCirkuitApp(QApplication):
    def __init__(self, args):
        super().__init__(args)

    # The command line parser (Qt-based)
    def parseCmdLine(self):
        ##### 1) PARSER SET-UP
        parser = QCommandLineParser()
        #parser.setSingleDashWordOptionMode(QCommandLineParser.ParseAsLongOptions)
        parser.setApplicationDescription(_translate("CommandLine", _appDescription, "Commandline application description"))
        # Adding the '-h, --help' option
        parser.addHelpOption()
        # Adding the '-v --version' option
        parser.addVersionOption()
        # Allowing one positional argument (the file to open)
        parser.addPositionalArgument(
            _translate("CommandLine", "path", "Commandline argument name"), 
            _translate("CommandLine", _pathDescription, "Commandline argument description"), 
            _translate("CommandLine",  "[<path> [ <path2>...]]",  "Commandline argument syntax")
        )
        # Adding command line options
        options = [
            QCommandLineOption(
                [outputFormat.TIKZ.value, "tikz"],
                _translate("CommandLine", _batchOption.format('TIkZ'), "Commandline option description"),
            ),
            QCommandLineOption(
                [outputFormat.PDF.value, "pdf"],
                _translate("CommandLine", _batchOption.format('PDF'), "Commandline option description"),
            ),
            QCommandLineOption(
                [outputFormat.PNG.value, "png"],
                _translate("CommandLine", _batchOption.format('PNG'), "Commandline option description"),
            ),
            QCommandLineOption(
                [outputFormat.JPEG.value, "jpg"],
                _translate("CommandLine", _batchOption.format('JPG'), "Commandline option description"),
            ),
            QCommandLineOption(
                ["dpi"], 
                _translate("CommandLine", _dpiOption, "Commandline option description"), 
                "N", 
                "150", 
            ), 
            QCommandLineOption(
                ["quality"], 
                _translate("CommandLine", _qualityOption, "Commandline option description"), 
                "Q", 
                "80", 
            ), 
            QCommandLineOption(
                ["r"],
                _translate("CommandLine", _recurseOption, "Commandline option description"), 
            ),
        ]
        # Adding the options in the list
        for option in options:
            parser.addOption(option)

        ##### 2) COMMAND-LINE PARSING
        parser.process(self)

        ##### 3) FETCH OPTIONS AND ARGUMENTS
        cli_mode = False
        requestedRecursive = False
        if parser.isSet("r"):
            requestedRecursive = True

        # Test for some path passed as parameters, or none
        paths = parser.positionalArguments()
        # User gave no files to process?
        pathPresent = (not len(paths)==0)
        # User may have entered more than one path, and these can contain wildcards
        # We have to expand them into files prior to process
        filesToProcess = list()
        for pathSpec in paths:
            for f in glob.iglob(pathSpec, recursive=requestedRecursive):
                if isfile(f):
                    filesToProcess.append(f)
        NumFiles = len(filesToProcess)

        # Test all the output options.
        for option in options:
            if parser.isSet(option):
                optionName = option.names()[0]
                cli_mode = True
                cli = CommandLineOptions(parser, option, paths)
                if optionName == outputFormat.PNG.value:
                    cli.png(parser.value("dpi"))
                elif optionName == outputFormat.JPEG.value:
                    cli.jpg(parser.value("dpi"), parser.value("quality"))
                # More options have to be added.

        # Perform some final checks and exit.
        if cli_mode:
            sys.exit(0)
        elif NumFiles == 0 and not pathPresent:
            return None
        elif NumFiles == 0:
            print(_translate("CommandLine", "ERROR: The given file does not exist.", "Commandline error message"))
            parser.showHelp(exitCode=-1)
        elif NumFiles == 1:
            return abspath(filesToProcess[0])
        else:
            print(_translate("CommandLine", "ERROR: More than one file to process with no batch option given.", "Commandline error message"))
            parser.showHelp(exitCode=-1)

        sys.exit(0)
