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

PyCirkuit source code is now hosted on github.com. The project homepage is [https://github.com/orestesmas/pycirkuit.git](https://github.com/orestesmas/pycirkuit.git).


# Requirements #

As PyCirkuit is written in python 3 and uses multiplatform GUI libraries, it loads without problems on Windows (macOS not tested). However, its execution relies on using some helper applications whose availability on non-GNU systems is irregular. Version 0.1 has been reported to work on MacOS using external tools provided by [MacPorts](https://www.macports.org/). Windows support is coming and planned for version 0.2.

To run this application you need to have the following applications/libraries installed:

  * Qt5 libraries
  * Python 3, with virtual environment support
  * PyQt5 python bindings to Qt libraries (*see note below*)
  * (pdf)latex
  * m4
  * dpic
  * pdftoppm (from poppler project)
  * Circuit Macros


# Installation #
## Installing on GNU/Linux systems ##


(**Note:** I prefer to install PyQt5 in a sandbox Virtual Environment only for PyCirkuit. See the **Installation** section.)


To install PyCirkuit in you computer, please follow this steps:

  1. Install the auxiliary apps: On Debian-based systems<sup>1</sup> (e.g. Ubuntu/Kubuntu)
  type the following command to install the required apps and dependencies (tested on Ubuntu
  18.04 LTS): 

        sudo apt-get install texlive-latex-base texlive-latex-recommended \
        texlive-base-bin texlive-extra-utils texlive-pictures preview-latex-style \
        m4 dpic poppler-utils python3-venv qtcreator

    <sup>1</sup> Apparently, Debian does not have ```dpic``` packaged, but Ubuntu has (in
    the *universe* repository). If you are trying PyCirkuit in a Debian system, you'll
    have to compile and install it yourself. Luckily, this is very easy because it's a
    little program with few/no dependencies. Download ```dpic``` from
    [https://ece.uwaterloo.ca/~aplevich/dpic/](https://ece.uwaterloo.ca/~aplevich/dpic/)
    and follow the instructions in the README file.

    There's no Debian package for the Circuit Macros, but if PyCirkuit doesn't find them at
    startup, it will offer the user to download and install them automatically. They don't
    require building.

  2. Choose or create a directory somewhere and __change into it__. Create a Python Virtual
  Environment inside and activate it:

        python3 -m venv PyCirkuit
        source PyCirkuit/bin/activate

  3. Install PyCirkuit using PIP. It will download and install alongside the required
  dependencies (PyQt5). After installation, PyCirkuit code and files will be under
  ```PyCirkuit/lib/python3.X/site-packages/pycirkuit```

        pip install git+https://github.com/orestesmas/pycirkuit.git#egg=pycirkuit

    (NOTE: If you prefer to have an installation __in source form__ -also known as 'editable
    mode'-, __add the '-e' option after 'install'__. In this case PyCirkuit files will be
    installed by default at ```PyCirkuit/src/pycirkuit```)

  4. If all went well, you can execute PyCirkuit by means of an executable script
  created under ```PyCirkuit/bin```:

        pycirkuit

## Installing on MacOS ##

## Installing on MS Windows ##

# Usage #

To execute PyCirkuit open a terminal window, navigate into the directory where PyCirkuit is installed and activate the virtual environment:

```shell
   cd <path-to-Virtual-Environment>
   source PyCirkuit/bin/activate
```

Then execute the program as above:

```shell
   pycirkuit
```

Upon finished executing PyCirkuit, you should deactivate the virtual environment:

```shell
   deactivate
```

Have fun!
