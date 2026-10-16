# Description #

PyCirkuit is a GUI/CLI front-end for [Circuit Macros] and [Dpic] by Dwight Aplevich, which make up a software chain for drawing high-quality line diagrams to include in LaTeX, web, LibreOffice or similar documents. PyCirkuit GUI builds a live preview of the source code and can export the resulting images in TikZ code, PDF, SVG, PNG and JPEG formats. PyCirkuit CLI mode is useful for batch-processing multiple files.

PyCirkuit is written in Python 3 using the PySide6 (Qt6) libraries, but is largely inspired (in both ideas and code snippets) on [Cirkuit], a C++ application written by Matteo Agostinelli using KDE4 libraries, which is nowadays very difficult to build on current systems. Its port to newer KDE platforms [was started] but never reached a usable state.

[Circuit Macros]: <https://ece.uwaterloo.ca/~aplevich/Circuit_macros/>
(M4 Macros for diagram and circuit drawing)

[Dpic]: <https://gitlab.com/aplevich/dpic>
(An implementation of the pic "little language," with support for LaTeX, PDF, SVG, Postscript, and xfig 3.2 output)

[Cirkuit]: <https://wwwu.uni-klu.ac.at/magostin/cirkuit.html>
(Cirkuit)

[was started]: <https://invent.kde.org/graphics/cirkuit>


# Source code #

PyCirkuit source code is hosted on GitHub: [https://github.com/orestesmas/pycirkuit](https://github.com/orestesmas/pycirkuit). See [CHANGELOG.md](CHANGELOG.md) for the release history.


# Requirements #

PyCirkuit is written in Python 3 and uses multiplatform GUI libraries, so it should load on GNU/Linux, Windows and macOS. However, it relies on several helper applications whose availability on non-GNU systems is irregular.

**Platform support**: since version 1.0, PyCirkuit is built on PySide6 and **has only been tested on GNU/Linux**. The older PyQt5-based 0.x releases had been reported to work on macOS and Windows, but the maintainer has no such systems to test the current releases on. Consider Windows/macOS support experimental. Testers on either platform are very welcome!

To run PyCirkuit you need:

  * Python 3.9 or newer, with virtual environment support
  * PySide6 (Qt6 bindings for Python) — installed automatically by `pip`
  * `libmagic` and its Python bindings — the bindings are installed automatically by `pip`
  * A LaTeX distribution with TikZ, `siunitx` and `preview`, providing **LuaLaTeX** (the default engine) and/or **pdfLaTeX** (selectable in the configuration dialog)
  * `m4`
  * `dpic`
  * `pdftoppm` (from the Poppler project), used for the preview and for PNG/JPEG export
  * `pdf2svg`, used for SVG export (new dependency since version 1.0)
  * Circuit Macros — if PyCirkuit doesn't find them at startup, it offers to download and install them automatically


# Installation #

## Debian and derivatives (Ubuntu, etc.) ##

PyCirkuit is packaged in Debian, so you can install it together with all its dependencies with:

    sudo apt install pycirkuit

Check which version your distribution ships before doing so (`apt policy pycirkuit`). As of late 2026, Debian 13 "Trixie" (stable) still ships the old PyQt5-based 0.5.1 release, while Debian testing/unstable ship the 1.x series. If your distribution only offers 0.5.x, you can install the latest release from PyPI as explained in the next section.

## Other GNU/Linux systems, or the latest release on Debian/Ubuntu ##

  1. Install the auxiliary applications. On Debian 11 or newer, Ubuntu and their derivatives, everything is packaged:

         sudo apt install m4 dpic circuit-macros poppler-utils pdf2svg libmagic1 python3-venv \
             texlive-latex-recommended texlive-luatex texlive-pictures texlive-science preview-latex-style

     The `circuit-macros` package is optional: if it's not installed, PyCirkuit will offer to download the Circuit Macros on its first run.

     On other distributions, install the equivalent packages with your package manager. If `dpic` is not packaged, it's a small program with no dependencies which is easy to build: get it from [https://gitlab.com/aplevich/dpic](https://gitlab.com/aplevich/dpic) and follow the instructions in its README.

  2. In order to isolate PyCirkuit and its dependencies from other Python packages on your system, install it into a Python virtual environment. Choose or create a directory somewhere, __change into it__ and create and activate the virtual environment:

         python3 -m venv PyCirkuit
         source PyCirkuit/bin/activate

  3. Install PyCirkuit. Choose one of the following:

     3.1 Install the latest stable release from the [Python Package Index (PyPI)](https://pypi.org/project/pycirkuit/). PySide6 and the other Python dependencies are downloaded and installed automatically:

         pip install pycirkuit

     3.2 Install the latest development version directly from GitHub:

         pip install https://github.com/orestesmas/pycirkuit/archive/master.zip

  4. If all went well, the `pycirkuit` executable is now available under `PyCirkuit/bin`. Test it with:

         pycirkuit

  Alternatively, if you have [pipx](https://pipx.pypa.io/) installed, `pipx install pycirkuit` performs steps 2 and 3 for you and makes the `pycirkuit` command available without activating any environment.

## macOS ##
(Not tested by the maintainer. These notes are based on reports from users of the older 0.x releases.)

  1. Install Python 3.9 or newer (e.g. from [python.org](https://www.python.org/downloads/macos/)) and a LaTeX distribution such as [MacTeX](https://www.tug.org/mactex/).

  2. Install `m4`, `dpic`, `poppler` (which provides `pdftoppm`), `pdf2svg` and `libmagic` using a package manager such as [MacPorts](https://www.macports.org/) or [Homebrew](https://brew.sh/). If `dpic` is not available there, build it from [its sources](https://gitlab.com/aplevich/dpic); it's a small program with no dependencies.

  3. Proceed as explained in steps 2 to 4 of the previous section to create a Python virtual environment and install PyCirkuit from PyPI.

## MS Windows ##
(Not tested by the maintainer. These notes are based on reports from users of the older 0.x releases.)

  1. Install the dependencies and auxiliary programs:

     1.1 A LaTeX distribution, such as [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/).

     1.2 A Python 3 interpreter (3.9 or newer) from [python.org](https://www.python.org/downloads/windows/).

     1.3 The M4 macro processor and the DPIC executables for Windows from [https://ece.uwaterloo.ca/~aplevich/dpic/Windows/](https://ece.uwaterloo.ca/~aplevich/dpic/Windows/index.html).

     1.4 The `pdftoppm` utility, bundled with the Poppler utilities, e.g. from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases).

     1.5 A Windows build of `pdf2svg` (only needed for SVG export).

     These programs have to be somewhere on your PATH; alternatively, see step 4 below.

  2. Choose a directory where to install PyCirkuit, open a command prompt there and create and activate a Python virtual environment:

         python -m venv PyCirkuit
         PyCirkuit\Scripts\activate

     The prompt should change and show "(PyCirkuit)" at the beginning, indicating that the environment is active.

  3. Install PyCirkuit as in step 3 of the GNU/Linux section.

  4. For convenience, you can copy the `m4.exe`, `dpic.exe`, `pdftoppm.exe` and `pdf2svg.exe` executables (and their DLLs) into `PyCirkuit\Lib\site-packages\pycirkuit\lib\`. PyCirkuit adds this directory to the PATH when running.

  5. Test the executable:

         pycirkuit

     You will find some examples inside `PyCirkuit\Lib\site-packages\pycirkuit\examples\`.


# Usage #

If you installed PyCirkuit from your distribution's packages or with `pipx`, just run `pycirkuit` from a terminal or from your desktop's application menu.

If you installed it into a virtual environment, activate it first:

```shell
   cd <directory-containing-the-virtual-environment>
   source PyCirkuit/bin/activate         (GNU/Linux and macOS)
   PyCirkuit\Scripts\activate            (Windows)
```

Then run the program:

```shell
   pycirkuit
```

Run `pycirkuit --help` to see the options for batch-processing files from the command line.

When you're done, you can deactivate the virtual environment (or simply close the terminal window):

```shell
   deactivate
```

Have fun!
