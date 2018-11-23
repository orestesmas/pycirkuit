Description
-----------

PyCirkuit is a GUI for Circuit macros [1] by Dwight Aplevich, which is a set of macros for drawing high-quality line diagrams to include in TeX, LaTeX, or similar documents. PyCirkuit builds a live preview of the source code and can export the resulting images in TikZ code to be included directly in any LaTeX document. Other export formats are also planned.

PyCirkuit is largely inspired (in both ideas and code snippets) on "Cirkuit", written in C++ by Matteo Agostinelli using KDE4 libraries, which is nowadays increasingly difficult to compile due to the switching, started in 2013, of KDE project from KDE4 platform to the Qt5-based KDE frameworks 5.


PyCirkuit is written in Python 3 using the PyQt5 libraries.


Source code
-----------

PyCirkuit source code is now hosted on gitlab.upc.edu. The project homepage is https://gitlab.upc.edu/CSL/Programari/pycirkuit.git.

Requirements
------------

To run this application you need to have the following applications installed:

* latex
* m4
* dpic
* pdftoppm
* Circuit Macros

On Debian-based systems (e.g. Ubuntu/Kubuntu) type the following command to install the required apps:

sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-base-bin texlive-extra-utils texlive-pictures preview-latex-style m4 dpic poppler-utils

There's no Debian package for the Circuit Macros, but if PyCirkuit doesn't find them at startup, it offer the user to download and install them automatically.

To build Cirkuit you need CMake and the KDE4 and Qt4 dev packages. To install them on Debian-based systems, type

sudo apt-get install cmake kdelibs5-dev libqt4-dev libpoppler-qt4

Packages are also available for Arch Linux (in AUR).

To build the application from source, follow the usual KDE4/CMake procedure:


