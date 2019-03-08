"""
Copyright (c) 2018 Orestes Mas

This file is part of PyCirkuit.

PyCirkuit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyCirkuit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyCirkuit.  If not, see <https://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages
import pycirkuit
import platform

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name = 'pycirkuit',
    version = pycirkuit.__version__,
    description = pycirkuit.__description__, 
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = pycirkuit.__homepage__,
    author = pycirkuit.__author__,
    author_email = pycirkuit.__author_email__,
    license = pycirkuit.__license_short__,
    packages = find_packages(),
    package_data = {
        'pycirkuit': ['lib/*', 'templates/*', 'examples/*'],
    },
    entry_points = {
        'gui_scripts': [
            'pycirkuit = pycirkuit.main:main',
        ],
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Editors",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
    ],
    install_requires = [
        # Debian package is python3-pyqt5
        'PyQt5',
        # Debian package is python3-magic
        'python-magic-bin' if platform.system() == 'Windows' else 'python-magic'
    ],
    zip_safe = True)
