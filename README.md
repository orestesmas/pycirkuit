# Description

PyCirkuit is a GUI for Circuit Macros [1] by Dwight Aplevich, which is a set of macros for drawing high-quality line diagrams to include in TeX, LaTeX, or similar documents. PyCirkuit builds a live preview of the source code and can export the resulting images in TikZ code to be included directly in any LaTeX document. Other export formats are also planned.

PyCirkuit is written in Python 3 using the PyQt5 libraries, but is largely inspired (in both ideas and code snippets) on "Cirkuit" [2], a C++ application written by Matteo Agostinelli using KDE4 libraries, which is nowadays increasingly difficult to compile due to the switching, started in 2013, of KDE project from KDE4 platform to the Qt5-based KDE frameworks 5.

[1] [https://ece.uwaterloo.ca/~aplevich/Circuit_macros/](https://ece.uwaterloo.ca/~aplevich/Circuit_macros/)

[2] [https://wwwu.uni-klu.ac.at/magostin/cirkuit.html](https://wwwu.uni-klu.ac.at/magostin/cirkuit.html)


# Source code

PyCirkuit source code is now hosted on gitlab.upc.edu. The project homepage is [https://gitlab.upc.edu/CSL/Programari/pycirkuit.git](https://gitlab.upc.edu/CSL/Programari/pycirkuit.git).


# Requirements

As PyCirkuit is written in python 3 and uses multiplatform GUI libraries, it loads without problems on Windows (macOS not tested). However, at present does not work correctly 
To run this application you need to have the following applications installed:

  * (pdf)latex
  * m4
  * dpic
  * pdftoppm
  * Circuit Macros

On Debian-based systems (e.g. Ubuntu/Kubuntu) type the following command to install the required apps:

    sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-base-bin texlive-extra-utils texlive-pictures preview-latex-style m4 dpic poppler-utils

There's no Debian package for the Circuit Macros, but if PyCirkuit doesn't find them at startup, it will offer the user to download and install them automatically.


# Installation

To be written. For now tested only in a virtual environment.

