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

To install PyCirkuit in you computer, please follow this steps:

  1. Install the auxiliary apps: On Debian-based systems<sup>1</sup> (e.g. Ubuntu/Kubuntu)
  type the following command to install the required apps and dependencies (tested on Ubuntu
  18.04 LTS): 

         sudo apt-get install texlive-latex-base texlive-latex-recommended \
         texlive-base-bin texlive-extra-utils texlive-latex-extra texlive-pictures preview-latex-style \
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

  2. In order to isolate PyCirkuit and its dependencies from other python packages on your system, it's advisable to install it into a Python's Virtual Environment. To do so, choose or create a directory somewhere and __change into it__. Do the following to create the Virtual Environment inside and activate it:

         python3 -m venv PyCirkuit
         source PyCirkuit/bin/activate

  3. Install PyCirkuit. You have several ways to do so. Choose one of the following:
  
     3.1 PyCirkuit is available at the [Python Package Index (PyPI)](https://pypi.org/), so you can install it using PIP. It will download and install alongside the required dependencies (PyQt5). After installation, PyCirkuit code and files will be under
  ```PyCirkuit/lib/python3.X/site-packages/pycirkuit```

         pip install pycirkuit

     3.2 The former will install the lastest stable version on PyPI. If you prefer to install the latest development version, [download it grom GitHub as a .ZIP file](https://github.com/orestesmas/pycirkuit/archive/master.zip) and install from it:
     
         pip install <path_to_the_downloaded_ZIP_file>

  4. If all went well, you can execute PyCirkuit by means of an executable script created under ```PyCirkuit/bin```. Test it with:

         pycirkuit

## Installing on MacOS ##
(These explanations were provided by some user. I cannot test them personally)
  1. Prerequisites and dependencies:
  
     1.1 You need to have installed Xcode and Xcode command tools. Of course, you will need also Python 3. To install it you can follow [https://www.python.org/downloads/release/python-372/](https://www.python.org/downloads/release/python-372/) or [https://docs.python-guide.org/starting/install3/osx/](https://docs.python-guide.org/starting/install3/osx/).
     
     1.2 Then you have to install LaTeX using MacPorts: [https://docs.typo3.org/typo3cms/extensions/sphinx/AdministratorManual/RenderingPdf/InstallingLaTeXLinux.html](https://docs.typo3.org/typo3cms/extensions/sphinx/AdministratorManual/RenderingPdf/InstallingLaTeXLinux.html).
     
     1.3 The M4 and DPIC are UNIX apps, so they run without much trouble on macOS. Similar with poppler. Some useful links are [https://ece.uwaterloo.ca/~aplevich/Circuit_macros/](https://ece.uwaterloo.ca/~aplevich/Circuit_macros/) and [https://www.google.es/amp/macappstore.org/poppler/amp/](https://www.google.es/amp/macappstore.org/poppler/amp/).
     
  2. Finally, proceed as explained on the steps #2 and #3 of the previous section to create a Python virtual environment and to install PyCirkuit from PyPI there.

## Installing on MS Windows ##
  1. Install the dependencies and auxiliary programs:

     1.1 Choose a LaTeX distribution for windows. I tested PyCirkuit with MikTeX. Download it from https://miktex.org/ and follow the instructions to install it.

     1.2 Download and install a python 3 interpreter for windows from https://www.python.org/downloads/windows/.

     1.3 Download and install the M4 macro processor and the DPIC executables for windows from https://ece.uwaterloo.ca/~aplevich/dpic/Windows/index.html

     1.4 Finally, obtain and install a copy of the "pdftoppm" utility. It usually comes bundled along with other utilities from the "Poppler" library, although it can be found alone on some webs. For instance from http://blog.alivate.com.au/poppler-windows/.

     You have to put this utilities somewhere on your PATH, but alternatively you can put them inside PyCirkuit code. See #4 below.

  2. Prepare a location where to install PyCircuit. It's advisable to install it inside a so-called python environment to isolate it from other python installations and libraries you may have on your system. To do so, choose a directory where to install PyCirkuit. Open a command line (I assume you have how to do it) and navigate to the chosen location. Then create the Python virtual environment and activate it using the commands below:

         python -m venv PyCirkuit
         PyCirkuit\Scripts\activate

        The console "prompt" should change and show "(PyCirkuit)" at the beginning indicating the environment is active.

  3. To install PyCirkuit, proceed like Step 3 in the "Linux Installation" section
     
  4. For convenience you can put the m4.exe, dpic.exe and pdftoppm.exe executables downloaded before inside the pycirkuit package you've just installed. Copy them to "PyCirkuit\Lib\site-packages\pycirkuit\lib\". PyCirkuit will add this directory to the executable's PATH when running.

  5. Test the executable:

         PyCirkuit

     You will find some examples inside "PyCirkuit\Lib\site-packages\pycirkuit\examples\"

  6. When you're done you can deactivate the virtual environment:

         deactivate

     or simply close the command line console.




# Usage #

To execute PyCirkuit open a console/terminal window, navigate into the directory where PyCirkuit is installed and activate the virtual environment as in 2:

```shell
   cd <path-to-Virtual-Environment>
   source PyCirkuit/bin/activate         (for GNU/Linux systems)
   PyCirkuit\Scripts\activate            (for Windows systems)
```

Then execute the program as above:

```shell
   pycirkuit
```

Upon finished executing PyCirkuit, you should deactivate the virtual environment (and/or close the terminal window):

```shell
   deactivate
```

Have fun!
