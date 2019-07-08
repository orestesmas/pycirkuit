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
import glob
from os.path import abspath, isfile

# Third-party imports
from PyQt5.QtCore import QObject, QCoreApplication, QCommandLineParser, QCommandLineOption

# Local imports
from pycirkuit import outputFormat

# Translation function
_translate = QCoreApplication.translate

# Some strings
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

class PyCirkuitParser(QObject):
    def __init__(self, args):
        super().__init__()
        self.args = args

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
        print("DEBUG: Processing command-line arguments: {}".format(sys.argv))
        print("DEBUG: Processing command-line arguments: {}".format(self.args))
        parser.process(self.args)

        ##### 3) FETCH OPTIONS AND ARGUMENTS
        validOutputFormatNames = {format.value for format in outputFormat}
        requestedOutputFormats = set()
        requestedValues = dict()
        requestedRecursive = False
        for option in options:
            if parser.isSet(option):
                optionName = option.names()[0]
                if optionName == 'r':
                    requestedRecursive = True
                elif optionName in validOutputFormatNames:
                    print("DEBUG: Detectada opció {}".format(optionName))
                    requestedOutputFormats.add(outputFormat(optionName))
                elif optionName == 'dpi':
                    try:
                        requestedValues['dpi'] = int(parser.value(option))
                    except:
                        print(_translate("CommandLine", "Error: The --dpi parameter must be an integer.", "Error message"))
                        sys.exit(-1)
                elif optionName == 'quality':
                    try:
                        requestedValues['quality'] = int(parser.value(option))
                        if requestedValues['quality'] not in range(0, 100):
                            raise Exception()
                    except:
                        print(_translate("CommandLine", "Error: The --quality parameter must be an integer between 0 and 100.", "Error message"))
                        sys.exit(-1)
                else:
                    print("DEBUG: No hauríem d'haver anat a parar aquí...")
        NumFormats = len(requestedOutputFormats)
                
        # Finished test for options. Now test for some path passed as parameters, or none
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
        
        ##### 4) MAKE DECISIONS
        # If called without options nor arguments nor options, launch GUI with a new empty drawing
        if (NumFiles == 0) and (not pathPresent) and (NumFormats == 0):
            return None
        # If No file match the specified arguments, throw error
        elif (NumFiles == 0) and (pathPresent):
            print("DEBUG: ERROR: No files match the argument")
            sys.exit(-1)
        # If called with a single file argument, and no options, launch GUI and open that file
        elif (NumFiles == 1) and (len(requestedOutputFormats) == 0):
            return abspath(filesToProcess[0])
        # Is an error to call pycirkuit with a batch option and no filenames
        elif (NumFormats > 0) and (NumFiles==0):
            print(_translate("CommandLine", "ERROR: Batch processing requested with no files.", "Commandline error message"))
            parser.showHelp(exitCode=-1)
        # If there's more than one file to process, this is an error if no option is given
        elif (NumFiles > 1) and (NumFormats == 0):
            # Display help and exit.
            print(_translate("CommandLine", "ERROR: More than one file to process with no batch option given.", "Commandline error message"))
            parser.showHelp(exitCode=-1)
        # So, we have a bunch of files to process sequentially. 
        # For each file, the operations can be always: CKT -> PIC -> TIKZ -> PDF -> PNG and pick the
        # intermediate formats requested by the user.
        # But of course we can optimize by stopping the chain as soon as the rightmost requested format is obtained
        for file in filesToProcess:
            #FIXME: Implement real functionality
            print("Processing file: {}".format(file))
        print("Finished: {} files processed".format(NumFiles))
        sys.exit(0)
