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

As PyCirkuit is written in python 3 and uses multiplatform GUI libraries, it loads without problems on Windows (macOS not tested). However, its execution relies on using some helper applications thar aren't readily available on non-GNU systems. For that reason, at present PyCirkuit does not work correctly (or has not been tested) on systems other than GNU/Linux.

To run this application you need to have the following applications/libraries installed:

  * Qt5 libraries
  * Python 3, with virtual environment support
  * PyQt5 python bindings to Qt libraries (*see note below*)
  * (pdf)latex
  * m4
  * dpic
  * pdftoppm
  * Circuit Macros

On Debian-based systems<sup>1</sup> (e.g. Ubuntu/Kubuntu) type the following command to install the required apps and dependencies (tested on Ubuntu 18.04 LTS):

```shell
  sudo apt-get install texlive-latex-base texlive-latex-recommended \
  texlive-base-bin texlive-extra-utils texlive-pictures preview-latex-style \
  m4 dpic poppler-utils python3-venv qtcreator
```
<sup>1</sup> Apparently, Debian does not have ```dpic``` packaged, but Ubuntu has (in the *universe* repository). So I don't really know where the latter is coming from. If you are trying PyCirkuit in a Debian system, you'll have to compile and install it yourself. Luckily, this is very easy because it's a little program with few/no dependencies. Download it from [https://ece.uwaterloo.ca/~aplevich/dpic/](https://ece.uwaterloo.ca/~aplevich/dpic/) and follow the instructions in the README file.

There's no Debian package for the Circuit Macros, but if PyCirkuit doesn't find them at startup, it will offer the user to download and install them automatically. They don't require building.

(**Note:** I prefer to install PyQt5 in a sandbox Virtual Environment only for PyCirkuit. See the **Installation** section.)


# Installation #

To install PyCirkuit in you computer, please follow this steps:

  1. Install the auxiliary apps as explained in the Requirements section.

  2. Create a directory somewhere, create a Python Virtual Environment inside and activate it:
  
```shell
   mkdir pycirkuit
   cd pycirkuit
   python3 -m venv venv
   source venv/bin/activate
```

  3. Install PyCirkuit using PIP. It will download and install alongside the required dependencies (PyQt5):\
    (NOTE: If you prefer to have en installation in source form -also known as 'editable mode'-,  add the '-e' option after 'install'. Sources will be installed by default at ./venv/src/pycirkuit)

```shell
   pip3 install git+https://github.com/orestesmas/pycirkuit.git#egg=pycirkuit
```

  4. If all went well, you can execute PyCirkuit by means of an executable script created under ./venv/bin:

```shell
   pycirkuit
```


# Usage #

To execute PyCirkuit open a terminal window, navigate into the directory where PyCirkuit is installed and activate the virtual environment:

```shell
   cd <path-to-Virtual-Environment>
   source venv/bin/activate
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
