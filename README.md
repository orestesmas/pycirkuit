WARNING!!  Pre-release code
* * *


# Description #

PyCirkuit is a GUI front-end for [Circuit Macros] by Dwight Aplevich, which is a set of macros for drawing high-quality line diagrams to include in TeX, LaTeX, web or similar documents. PyCirkuit builds a live preview of the source code and can export the resulting images in TikZ code (other formats will be added in the future) to be included directly in any LaTeX document. Other export formats are also planned.

PyCirkuit is written in Python 3 using the PyQt5 libraries, but is largely inspired (in both ideas and code snippets) on [Cirkuit], a C++ application written by Matteo Agostinelli using KDE4 libraries, which is nowadays increasingly difficult to compile due to the switching, started in 2013, of KDE project from KDE4 platform to the Qt5-based KDE frameworks 5. A port of Cirkuit to KDE frameworks 5 [has begun], but's still not functional and its development appears to be stalled.

[Circuit Macros]: <https://ece.uwaterloo.ca/~aplevich/Circuit_macros/>
(M4 Macros for diagram and circuit drawing)

[Cirkuit]: <https://wwwu.uni-klu.ac.at/magostin/cirkuit.html>
(Cirkuit)

[has begun]: <https://cgit.kde.org/cirkuit.git/>


# Source code #

PyCirkuit source code is now hosted on gitlab.upc.edu. The project homepage is [https://gitlab.upc.edu/CSL/Programari/pycirkuit.git](https://gitlab.upc.edu/CSL/Programari/pycirkuit.git).


# <a name="requirements"></a>Requirements #

As PyCirkuit is written in python 3 and uses multiplatform GUI libraries, it loads without problems on Windows (macOS not tested). However, at present does not work correctly 
To run this application you need to have the following applications installed:

  * (pdf)latex
  * m4
  * dpic
  * pdftoppm
  * Circuit Macros

On Debian-based systems (e.g. Ubuntu/Kubuntu) type the following command to install the required apps:

    sudo apt-get install texlive-latex-base texlive-latex-recommended \
    texlive-base-bin texlive-extra-utils texlive-pictures preview-latex-style \
    m4 dpic poppler-utils

There's no Debian package for the Circuit Macros, but if PyCirkuit doesn't find them at startup, it will offer the user to download and install them automatically.


# Installation #

To be written. This is still a pre-release.

To install PyCirkuit in you computer, please follow this steps:

  1. Install the auxiliary apps as explained in the [Requirements] (#requirements)

