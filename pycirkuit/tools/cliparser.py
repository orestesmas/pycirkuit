# -*- coding: utf-8 -*-
"""
Module implementing the functions to run when a command option is called
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
from pycirkuit import Option, imageParam
from pycirkuit.tools.processor import PyCirkuitProcessor

# Translation function
_translate = QCoreApplication.translate

class PyCirkuitParser(QObject):
    # Some static strings
    _appDescription = """
PyCirkuit is a GUI front-end for Circuit Macros by Dwight Aplevich,
which are a set of macros for drawing high-quality line diagrams
to be included in TeX, LaTeX, web or similar documents."""
    _batchOption = "Convert files specified by <path> to {formatID} format in batch mode. Several output formats can be used together."
    _dpiOption = "Sets the resolution of output bitmap images (png, jpg), in dots per inch. Value <N> is mandatory. If not set, default is {defaultDPI} (defined in 'settings' dialog)."
    _qualityOption = "Sets the quality of output bitmap lossy images (jpg), in percent. Value <Q> is mandatory. If not set, default is {defaultQuality}% (defined in 'settings' dialog)."
    _recurseOption = "Using this option the pattern '**' will match any files and zero or more subdirs, so '**/*.ckt' will match all files with 'ckt' extension in the current directory and all its subdirectories."
    _pathDescription = """Path(s) to source drawing file(s) to process. Wildcards accepted.
- If no <path> is given, the GUI is opened.
- If <path> points to only one file and no batch conversion options are present, this file is opened into the GUI for editing.
- If <path>s point to more than one valid file and a combination of output formats options are present, these source files are processed sequentially in batch (unattended) mode and converted into the requested formats.
- Specifying more than one file to process with no output format options present is not allowed."""
    _seeHelp = _translate("CommandLine", 'Try "{appName} --help" to get more information.', "Command-line error message.")

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.cli_mode = False
        self.requestedRecursive = False
        self.parser = QCommandLineParser()
        #self.parser.setSingleDashWordOptionMode(QCommandLineself.parser.ParseAsLongOptions)
        self.parser.setApplicationDescription(_translate("CommandLine", PyCirkuitParser._appDescription, "Commandline application description."))
        # Adding the '-h, --help' option
        self.parser.addHelpOption()
        # Adding the '-v --version' option
        self.parser.addVersionOption()
        # Allowing positional arguments (the file/files to open or process)
        self.parser.addPositionalArgument(
            _translate("CommandLine", "path", "Commandline argument name. If you translate this name, translate it accordingly into the path description and path syntax."), 
            _translate("CommandLine", PyCirkuitParser._pathDescription, "Commandline argument description. If you translate <path>, translate the name and path syntax accordingly."), 
            _translate("CommandLine",  "[<path> [ <path2>...]]",  "Commandline argument syntax. If you translate <path>, translate the name and path description accordingly.")
        )
        # Adding command line options
        batchOptionStr = _translate("CommandLine", PyCirkuitParser._batchOption, "Commandline option description. Don't translate the '{formatID}' variable.")
        dpiOptionStr = _translate("CommandLine", PyCirkuitParser._dpiOption, "Commandline argument description. Don't translate the '{defaultDPI}' variable.")
        qualityOptionStr = _translate("CommandLine", PyCirkuitParser._qualityOption, "Commandline option description. Don't translate the '{defaultQuality}' variable.")
        recurseOptionStr = _translate("CommandLine", PyCirkuitParser._recurseOption, "Commandline option description.")
        self.options = {
            Option.TIKZ: QCommandLineOption(
                            ["t", "tikz"],
                            batchOptionStr.format(formatID='TIkZ'), 
                         ),
            Option.PDF:  QCommandLineOption(
                            ["f", "pdf"],
                            batchOptionStr.format(formatID='PDF'),
                         ),
            Option.PNG:  QCommandLineOption(
                            ["p", "png"],
                            batchOptionStr.format(formatID='PNG'),
                         ),
            Option.JPEG: QCommandLineOption(
                            ["j", "jpg"],
                            batchOptionStr.format(formatID='JPG'),
                         ),
            Option.DPI:  QCommandLineOption(
                            ["dpi"], 
                            dpiOptionStr.format(defaultDPI=imageParam[Option.DPI]),
                            "N", 
                         ), 
            Option.QUAL: QCommandLineOption(
                            ["quality"], 
                            qualityOptionStr.format(defaultQuality=imageParam[Option.QUAL]), 
                            "Q", 
                         ), 
            Option.REC:  QCommandLineOption(
                            ["r"],
                            recurseOptionStr, 
                         ),
        }
        # Adding the options in the list
        for option in self.options.values():
            self.parser.addOption(option)

    def _checkFiles(self):
        # Test for some path passed as parameters, or none
        paths = self.parser.positionalArguments()
        # User gave some filespec to process?
        pathPresent = (len(paths) > 0)
        # User may have entered more than one path, and these can contain wildcards
        # We have to expand them into files prior to process
        self.requestedFilesToProcess = list()
        for pathSpec in paths:
            for f in glob.iglob(pathSpec, recursive=self.requestedRecursive):
                if isfile(f):
                    self.requestedFilesToProcess.append(f)
        NumFiles = len(self.requestedFilesToProcess)
        if (NumFiles == 0) and pathPresent:
            print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "The given path does not match any existing file.", "Commandline error message"))
            print(PyCirkuitParser._seeHelp.format(appName=QCoreApplication.applicationName()))
            sys.exit(-1)
        return NumFiles
        
    def _checkFormats(self):
        # Test for requested output formats. If any, cli_mode is set.
        validOutputFormats = {Option.TIKZ, Option.PNG, Option.PDF, Option.JPEG}
        self.requestedOutputFormats = set()
        for outputFormat in validOutputFormats:
            if self.parser.isSet(self.options[outputFormat]):
                self.cli_mode = True
                self.requestedOutputFormats.add(outputFormat)
        NumFormats = len(self.requestedOutputFormats)
        return NumFormats

    def _checkRecursive(self):
        self.cli_mode = self.requestedRecursive = self.parser.isSet(self.options[Option.REC])
    
    def _checkRasterOptions(self):
        # "imageParam" is a variable (global for now) predefined with default values in __init__.py
        # FIXME: imageParam: In the future, its default values should be fetched from the settings
        # Set the "dpi" and "quality" parameters to the values provided by user, if any
        # process the "dpi" option
        if self.parser.isSet(self.options[Option.DPI]):
            try:
                imageParam[Option.DPI] = int(self.parser.value(self.options[Option.DPI]))
                if imageParam(Option.DPI) not in range(25, 3001):
                    raise Exception()
            except:
                print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "The --dpi parameter must be an integer between 25 and 3000.", "Error message"))
                print(PyCirkuitParser._seeHelp.format(appName=QCoreApplication.applicationName()))
                sys.exit(-1)
        # Process the "quality" option
        if self.parser.isSet(self.options[Option.QUAL]):
            try:
                imageParam[Option.QUAL] = int(self.parser.value(self.options[Option.QUAL]))
                if imageParam[Option.QUAL] not in range(0, 101):
                    raise Exception()
            except:
                print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "The --quality parameter must be an integer between 0 and 100.", "Error message"))
                print(PyCirkuitParser._seeHelp.format(appName=QCoreApplication.applicationName()))
                sys.exit(-1)

    # The command line parser (Qt-based)
    def parseCmdLine(self):
        self.parser.process(self.args)

        ##### FETCH OPTIONS AND ARGUMENTS
        # Test if "recursive" flag is set (also, if it is set, we enter cli_mode)
        self._checkRecursive()
        
        # Check if user set some image raster parameters
        self._checkRasterOptions()
        
        # Test how many output formats were requested.
        self._checkFormats()

        # Find files to process
        NumFiles = self._checkFiles()
        
        ##### Process CLI mode
        if self.cli_mode:
            # Is an error to call pycirkuit with a batch option and no filenames
            if (NumFiles==0):
                print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "Batch processing requested with no files.", "Commandline error message"))
                print(PyCirkuitParser._seeHelp.format(appName=QCoreApplication.applicationName()))
                sys.exit(-1)
            processor = PyCirkuitProcessor(imageParam)
            for fileName in self.requestedFilesToProcess:
                processor.setSourceFile(fileName)
                for format in self.requestedOutputFormats:
                    if format == Option.PNG:
                        processor.toPng()
                        # Copy the result to original dir with correct extension. Check for file existence and abort!
                        print("Copying png file into destination")
                    elif format == Option.JPEG:
                        processor.toJpg()
                    elif format == Option.PDF:
                        processor.toPdf()
                        # Copy the result to original dir with correct extension. Check for file existence and abort!
                        print("Copying pdf file into destination")
                    elif format == Option.TIKZ:
                        processor.toTikz()
                        # Copy the result to original dir with correct extension. Check for file existence and abort!
                        print("Copying tikz file into destination")
            sys.exit(0)

        ##### Process GUI mode. Perform some final checks and exit.
        if NumFiles == 0:
            return None
        elif NumFiles == 1:
            return abspath(self.requestedFilesToProcess[0])
        else:
            print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "More than one file to process with no batch option given.", "Commandline error message"))
            print(PyCirkuitParser._seeHelp.format(appName=QCoreApplication.applicationName()))
            sys.exit(-1)

