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

# Translation function
_translate = QCoreApplication.translate

_appDescription = """
PyCirkuit is a GUI front-end for Circuit Macros by Dwight Aplevich,
which are a set of macros for drawing high-quality line diagrams
to be included in TeX, LaTeX, web or similar documents."""

_batchOption = "Convert files specified by <path> to {} format in batch mode. Options -t, -p and -d can be used together."

_pathDescription = """Path(s) to source drawing file(s) to process. Wildcards accepted.
- If no <path> is given, the GUI is opened.
- If <path> points to only one file and no '-t', '-p' or '-d' options are present, this file is opened into the GUI for editing.
- If <path>s point to more than one valid file and a combination of '-t', '-p' or '-d' options are present, these source files are processed sequentially in batch (unattended) mode and converted into the requested formats.
- Specifying more than one file to process with no '-t', '-b' or '-d' options present is not allowed."""

class PyCirkuitApp(QApplication):
    def __init__(self, args):
        super().__init__(args)

    # The command line parser
    def parseCmdLine(self):

        ##### 1) PARSER SET-UP
        parser = QCommandLineParser()
        parser.setApplicationDescription(_translate("CommandLine", _appDescription, "Commandline help text"))
        # Adding command line options
        options = [
            QCommandLineOption(
                ["t", "tikz"],
                _translate("CommandLine", _batchOption.format('TIkZ'), "Commandline help text"),
            ),
            QCommandLineOption(
                ["p", "png"],
                _translate("CommandLine", _batchOption.format('PNG'), "Commandline help text"),
                "dpi", 
                "150"
            ),
#            QCommandLineOption(
#                ["j", "jpg"],
#                _translate("CommandLine", _batchOption.format('JPG'), "Commandline help text"),
#            ),pdf
            QCommandLineOption(
                ["d", "pdf"],
                _translate("CommandLine", _batchOption.format('PDF'), "Commandline help text"),
            ),
            QCommandLineOption(
                ["r", "recurse"],
                _translate("CommandLine", "Using this option the pattern '**' will match any files and zero or more subdirs, so '**/*.ckt' will match all files with 'ckt' extension in the current directory and all its subdirectories", "Commandline help text"),
            ),
        ]
        # Adding the '-h, --help' option
        parser.addHelpOption()
        # Adding the '-v --version' option
        parser.addVersionOption()
        # Adding the options in the list
        for option in options:
            parser.addOption(option)
        # Allowing one positional argument -- the file to open
        parser.addPositionalArgument(
            _translate("CommandLine", "[<path> [ <path2>...]]", "Commandline help text"), 
            _translate("CommandLine", _pathDescription, "Commandline help text")
        )

        ##### 2) COMMAND-LINE PARSING
        parser.process(self)

        ##### 3) FETCH OPTIONS AND ARGUMENTS
        requestedOutputFormats = set()
        recursive=False
        for option in options:
            if parser.isSet(option):
                optionName = option.names()[0]
                if optionName == 'r':
                    recursive=True
                else:
                    requestedOutputFormats.add(option.names()[1])
        NumOpts = len(requestedOutputFormats)
                
        # Finished test for options. Now test for some path passed as parameters, or none
        paths = parser.positionalArguments()
        # User may have entered more than one path, and these can contain wildcards
        # We have to expand them into files prior to process
        filesToProcess = list()
        for pathSpec in paths:
            for f in glob.iglob(pathSpec, recursive=recursive):
                if isfile(f):
                    filesToProcess.append(f)
        NumArgs = len(filesToProcess)
        
        ##### 4) MAKE DECISIONS
        # If called without options nor arguments, launch GUI
        if (NumArgs == 0):
            return None
        # If called with a single file argument, and no options, launch GUI and open that file
        elif (NumArgs == 1) and (len(requestedOutputFormats) == 0):
            return abspath(filesToProcess[0])
        # If there's more than one file to process, this is an error if no option is given
        elif (NumArgs > 1) and (NumOpts == 0):
            # Display help and exit.
            print(_translate("CommandLine", "ERROR: ", "Commandline help text"))
            parser.showHelp(exitCode=-1)
        # So, we have a bunch of files to process sequentially. 
        # For each file, the operations can be always: CKT -> PIC -> TIKZ -> PDF -> PNG and pick the
        # intermediate formats requested by the user.
        # But of course we can optimize by stopping the chain as soon as the rightmost requested format is obtained
        for file in filesToProcess:
            #FIXME: Implement real functionality
            print("Processing file: {}".format(file))
        print("Finished: {} files processed".format(NumArgs))
        sys.exit(0)
