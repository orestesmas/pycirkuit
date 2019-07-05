# coding: utf-8
"""
Module implementing the functions to run when a command option is called
"""
# Copyright (C) 2019 Orestes Mas
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
import glob
import sys

class CommandLineOptions():
    # Class constructor.
    def __init__(self, parser, option=None):
        self.parser = parser
        self.option = option

    # Operational methods.
    def setOption(self, option):
        self.option = option

    # Command line methods.
    def batch(self):
        print("Option '-b' not yet implemented. Exiting.")
        print("But the files to be processed are:")
        pathSpec =  self.parser.value(self.option)
        fileIterator = iter(glob.iglob(pathSpec))
        for file in fileIterator:
            print(file)
        sys.exit(-1)

    def tikz(self):
        '''I stop here. The code in ui/mainwindow.py shouldn't be coded there. The whole process of generating
        a tikz file needs a UI. I think that there should be independent functions doing the job.
        '''
        pass
