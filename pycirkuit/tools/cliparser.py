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
from os.path import abspath, realpath, isfile, isdir
from subprocess import run
from enum import Enum

# Third-party imports
from PyQt5.QtCore import QObject, QCoreApplication, QCommandLineParser, QCommandLineOption, QSettings

# Local imports
import pycirkuit
from pycirkuit.exceptions import *
from pycirkuit import Option, __productname__
from pycirkuit.tools.processor import PyCirkuitProcessor, Overwrite

# Translation function
_translate = QCoreApplication.translate

# A Enumeration class
class Decision(Enum):
    ABORT = 1
    SKIP = 2
    OPEN = 3

# The command line parser (Qt-based)
class PyCirkuitParser(QObject):
    def _initStrings(self):
        self._appDescriptionStr = _translate("CommandLine",
            "\n"
            "{productName} is a front-end for Circuit Macros by Dwight Aplevich,\n"
            "which are a set of macros for drawing high-quality line diagrams\n"
            "to be included in TeX, LaTeX, web or similar documents.",
            "Commandline application description. Don't translate '{productName}'.")
        self._batchOptionStr = _translate("CommandLine",
            "Activates batch (unattended) mode, and convert files specified by <path> to {formatID} format. Several output formats can be used together.", 
            "Commandline option description. Don't translate the '{formatID}' variable.")
        self._dpiOptionStr = _translate("CommandLine",
            "Sets the resolution of output raster images (png, jpg), in dots per inch. Value <N> is mandatory. If option is not set, default is {defaultDPI}dpi (defined in 'settings' dialog).", 
            "Commandline argument description. Don't translate the '{defaultDPI}' variable.")
        self._qualityOptionStr = _translate("CommandLine",
            "Sets the quality of output raster lossy images (jpg), in percent. Value <Q> is mandatory. If option is not set, default is {defaultQuality}% (defined in 'settings' dialog).", 
            "Commandline option description. Don't translate the '{defaultQuality}' variable.")
        self._overwriteOptionStr = _translate("CommandLine", 
            "Overwrite by default the converted files if they are present. If not set, user will be asked at runtime.", 
            "Commandline option description.")
        self._followLinksOptionStr = _translate("CommandLine", 
            "Follow symbolic links.\n"
            "- If not set, destination file will be saved into the same directory where the source file is, whether it's a real file or a symbolic link.\n"
            "- If set, destination file will be saved into the directory where the real source file is located.", 
            "Commandline option description.")
        self._destDirOptionStr = _translate("CommandLine", 
            "Save all converted files into the same destination directory <D> (value is mandatory).", 
            "Commandline option description. Don't translate '<D>'.")
        self._recurseOptionStr = _translate("CommandLine",
            "Using this option the pattern '**' will match any files and zero or more subdirs, so '**/*.ckt' will match all files with 'ckt' extension in the current directory and all its subdirectories.", 
            "Commandline option description.")
        self._pathDescriptionStr = _translate("CommandLine", 
            "Path to source drawing file(s) to process. Wildcards accepted.\n"
            "- If no <path> is given, the GUI is opened.\n"
            "- If <path> points to only one file and no batch conversion options are present, this file is opened into the GUI for editing.\n"
            "- If <path>s point to more than one valid file and a combination of output formats options are present, these source files are processed sequentially in batch (unattended) mode and converted into the requested formats.\n"
            "- Specifying more than one file to process with no output format options present is not allowed.",
            "Commandline argument description. If you translate <path>, translate the name and path syntax accordingly.")
        self._seeHelpStr = _translate("CommandLine",
            'Try "{appName} --help" to get more information.',
            "Command-line error message. Don't translate '{appName}'.")

    def __init__(self, args):
        super().__init__()
        self.args = args
        settings = QSettings()
        self.imageParam = {
            Option.DPI: settings.value("Export/exportDPI", 150, type=int),  
            Option.QUAL: settings.value("Export/exportQuality", 80, type=int), 
        }
        self.cli_mode = False
        self.requestedRecursive = False
        self.overwrite = Overwrite.UNSET
        self.dstDir = ""
        self._initStrings()
        self.parser = QCommandLineParser()
        #self.parser.setSingleDashWordOptionMode(QCommandLineself.parser.ParseAsLongOptions)
        self.parser.setApplicationDescription(self._appDescriptionStr.format(productName=__productname__))
        # Adding the '-h, --help' option
        self.parser.addHelpOption()
        # Adding the '-v --version' option
        self.parser.addVersionOption()
        # Allowing positional arguments (the file/files to open or process)
        self.parser.addPositionalArgument(
            _translate("CommandLine", "path", "Commandline argument name. If you translate this name, translate it accordingly into the path description and path syntax."), 
            self._pathDescriptionStr, 
            _translate("CommandLine",  "[<path> [ <path2>...]]",  "Commandline argument syntax. If you translate <path>, translate the name and path description accordingly.")
        )
        # Adding command line options
        self.options = {
            Option.TIKZ: QCommandLineOption(
                    ["t", "tikz"],
                    self._batchOptionStr.format(formatID='TIkZ'), 
                ),
            Option.PDF:  QCommandLineOption(
                    ["f", "pdf"],
                    self._batchOptionStr.format(formatID='PDF'),
                ),
            Option.PNG:  QCommandLineOption(
                    ["p", "png"],
                    self._batchOptionStr.format(formatID='PNG'),
                ),
            Option.JPEG: QCommandLineOption(
                    ["j", "jpeg"],
                    self._batchOptionStr.format(formatID='JPEG'),
                ),
            Option.DPI:  QCommandLineOption(
                    ["dpi"], 
                    self._dpiOptionStr.format(defaultDPI=self.imageParam[Option.DPI]),
                    "N", 
                ), 
            Option.QUAL: QCommandLineOption(
                    ["quality"], 
                    self._qualityOptionStr.format(defaultQuality=self.imageParam[Option.QUAL]), 
                    "Q", 
                ), 
            Option.DEST: QCommandLineOption(
                    ["destination"], 
                    self._destDirOptionStr, 
                    "D", 
                ), 
            Option.LINK: QCommandLineOption(
                    ["links"], 
                    self._followLinksOptionStr, 
                ), 
            Option.OVER: QCommandLineOption(
                    ["overwrite"], 
                    self._overwriteOptionStr, 
                ), 
            Option.REC:  QCommandLineOption(
                    ["r"],
                    self._recurseOptionStr, 
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
                if isfile(realpath(f)):
                    f = realpath(f) if self.followSymlinks else abspath(f)
                    self.requestedFilesToProcess.append(f)
        NumFiles = len(self.requestedFilesToProcess)
        if (NumFiles == 0) and pathPresent:
            print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "The given path does not match any existing file.", "Commandline error message"))
            print(self._seeHelpStr.format(appName=QCoreApplication.applicationName()))
            sys.exit(-1)
        return NumFiles

    def _checkFileOptions(self):
        self.followSymlinks = self.parser.isSet(self.options[Option.LINK])
        self.overwrite = Overwrite.ALL if self.parser.isSet(self.options[Option.OVER]) else Overwrite.UNSET
        if self.parser.isSet(self.options[Option.DEST]):
            self.dstDir = abspath(self.parser.value((self.options[Option.DEST])))
            if not isdir(self.dstDir):
                print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "The given path does not match any existing file.", "Commandline error message"))
                print(self._seeHelpStr.format(appName=QCoreApplication.applicationName()))
                sys.exit(-1)
        else:
            self.dstDir = ""
    
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
        self.requestedRecursive = self.parser.isSet(self.options[Option.REC])
    
    def _checkRasterOptions(self):
        # Set the "dpi" and "quality" parameters to the values provided by user, if any
        # process the "dpi" option
        if self.parser.isSet(self.options[Option.DPI]):
            try:
                self.imageParam[Option.DPI] = int(self.parser.value(self.options[Option.DPI]))
                if self.imageParam[Option.DPI] not in range(25, 3001):
                    raise Exception()
            except:
                print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "The --dpi parameter must be an integer between 25 and 3000.", "Error message"))
                print(self._seeHelpStr.format(appName=QCoreApplication.applicationName()))
                sys.exit(-1)
        # Process the "quality" option
        if self.parser.isSet(self.options[Option.QUAL]):
            try:
                self.imageParam[Option.QUAL] = int(self.parser.value(self.options[Option.QUAL]))
                if self.imageParam[Option.QUAL] not in range(0, 101):
                    raise Exception()
            except:
                print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "The --quality parameter must be an integer between 0 and 100.", "Error message"))
                print(self._seeHelpStr.format(appName=QCoreApplication.applicationName()))
                sys.exit(-1)

    def parseCmdLine(self):
        self.parser.process(self.args)
        ##### FETCH OPTIONS AND ARGUMENTS
        # Test if "recursive" flag is set
        self._checkRecursive()
        # Check if user set some image raster parameters
        self._checkRasterOptions()
        # Test how many output formats were requested.
        self._checkFormats()
        # Test for various file options
        self._checkFileOptions()
        # Find files to process
        NumFiles = self._checkFiles()
        
        ##### Process CLI mode
        if self.cli_mode:
            # Is an error to call pycirkuit with a batch option and no filenames
            if (NumFiles == 0):
                print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "Batch processing requested with no files.", "Commandline error message"))
                print(self._seeHelpStr.format(appName=QCoreApplication.applicationName()))
                sys.exit(-1)
            # Instantiate a processor object for this CLI session
            try:
                processor = PyCirkuitProcessor()
                for fileName in self.requestedFilesToProcess:
                    processed = False
                    print(_translate("CommandLine",  "Processing file:", "Command line message. Will be followed by an absolute pile path"), fileName)
                    while not processed:
                        processor.beginProcessing(fileName)
                        for format in self.requestedOutputFormats:
                            try:
                                processor.requestResult(format, dstDir=self.dstDir, overwrite=self.overwrite, dpi=self.imageParam[Option.DPI], quality=self.imageParam[Option.QUAL])
                                processed = True
                            except PyCktToolExecutionError as err:
                                answer = self._askOnError(err)
                                if answer == Decision.ABORT:
                                    # Terminate program
                                    sys.exit(-1)
                                elif answer == Decision.SKIP:
                                    # Consider file processed and jump to the next one
                                    processed = True
                                    continue
                                elif answer == Decision.OPEN:
                                    # Open a IGU
                                    try:
                                        run(["pycirkuit", fileName], shell=False, check=False)
                                    except:
                                        processed = True
                    print("")
            except PyCirkuitError as err:
                print("\npycirkuit:", err)
                sys.exit(-1)
            print(_translate("CommandLine", "Files processed: {N}.", "Command line message. {N} will be an integer, don't translate it.").format(N=NumFiles))
            sys.exit(0)

        ##### Process GUI mode. Perform some final checks and exit.
        if NumFiles == 0:
            return None
        elif NumFiles == 1:
            return abspath(self.requestedFilesToProcess[0])
        else:
            print(QCoreApplication.applicationName() + ": " + _translate("CommandLine", "More than one file to process with no batch option given.", "Commandline error message"))
            print(self._seeHelpStr.format(appName=QCoreApplication.applicationName()))
            sys.exit(-1)

    def _askOnError(self, err):
        # Test if we have GUI or not, and ask accordingly
        print("\npycirkuit:", err)
        if pycirkuit.__haveGUI__:
            pass
        question = _translate("CommandLine-UserInput2", 
            "Please choose what to do: [a]bort processing, [s]kip file, [o]pen in GUI for editing: ", 
            "WARNING!! Critical translation. You should translate this message to your language, enclosing into brackets one single DIFFERENT character for each option, and translate accordingly the characters in the next message.")
        answerAbort = _translate("CommandLine-UserInput2",
            "a", 
            "WARNING!! Critical translation. This char must match one of those of the message 'Please choose what to do:'")
        answerSkip = _translate("CommandLine-UserInput2",
            "s", 
            "WARNING!! Critical translation. This char must match one of those of the message 'Please choose what to do:'")
        answerOpen = _translate("CommandLine-UserInput2",
            "o", 
            "WARNING!! Critical translation. This char must match one of those of the message 'Please choose what to do:'")
        if pycirkuit.__haveGUI__:
            question = _translate("CommandLine-UserInput2", 
                "Please choose what to do: [a]bort processing, [s]kip file, [o]pen in GUI for editing: ", 
                "WARNING!! Critical translation. You should translate this message to your language, enclosing into brackets one single DIFFERENT character for each option, and translate accordingly the characters in the next message.")
            answers = {
                answerAbort: Decision.ABORT, 
                answerSkip: Decision.SKIP, 
                answerOpen: Decision.OPEN
            }
        else:
            question = _translate("CommandLine-UserInput2", 
                "Please choose what to do: [a]bort processing, [s]kip file: ", 
                "WARNING!! Critical translation. You should translate this message to your language, enclosing into brackets one single DIFFERENT character for each option, and translate accordingly the characters in the next message.")
            answers = {
                answerAbort: Decision.ABORT, 
                answerSkip: Decision.SKIP, 
            }
        # Ask for user decision, loop until answered
        while True:
            answer = input(question)
            if answer.lower() in answers:
                return answers[answer]
