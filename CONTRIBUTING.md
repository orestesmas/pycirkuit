# Contributing to PyCirkuit

You are here to help on PyCirkuit? Awesome! PyCirkuit is still at its infancy and needs a lot of love and work. If tou find this application useful, there are some areas where you can help, depending on your interests and level of expertise:

  - Writing documentation
  - Translating the app to your native language
  - Finding bugs and fixing issues
  - Contributing code


## Contributing guidelines

At present, PyCirkuit is a small project with little infrastructure around. Contributions are welcome and they don't have to adhere to any particular convention, but will be accepted or rejected at developer's discretion.

You can send contributions as a pull request on the [GitHub repository](https://github.com/orestesmas/pycirkuit), or ask questions and send contributions directly to me at [mailto:orestes.mas@upc.edu](mailto:orestes.mas@upc.edu).

**Thanks!**


## Contributing translations

The application is fully internationalized, so you can translate it to your language. If you want to do so, please follow these steps:

  1. Install the [Qt developping tools](https://www.qt.io/download), specially "Linguist". Unfortunately, Qt company does not offer you to download Linguist separately of the other developping tools. If you need/want install only QtLinguist, you can check [this project](https://github.com/lelegard/qtlinguist-installers).
  2. Locate the file [pycirkuit/L10n/pycirkuit_empty.ts](https://github.com/orestesmas/pycirkuit/blob/master/pycirkuit/L10n/pycirkuit_empty.ts) and copy it into a new file named "pycirkuit.LOCALE.ts" where LOCALE is the code/country of your language. For instance for french it can be "fr", "fr_CA", "fr_FR", etc. See [this Wikipedia entry](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for a complete list.
  3. Open the new file under Linguist and translate all the strings in it. The [Qt Linguist manual](http://doc.qt.io/qt-5/qtlinguist-index.html) can be helpful.
  4. Send the translated .TS file to the PyCirkuit developers or, if you know how to do it, create a pull/merge request.


## Maintaining translations (developers)

If you add or change a translatable string (a `_translate(...)` call, or a `.ui` file), the full chain to make it actually show up in the running app is: source -> `.ts` -> translated `.ts` -> `.qm` -> embedded resource. Each step has its own tool, and skipping one leaves you looking at stale text with no error to explain why.

  1. **Extract strings into the `.ts` files.** From the repository root, for
     every locale file the project ships (currently `pycirkuit.ca.ts`) plus `pycirkuit_empty.ts`:
     ```
     PY_FILES=($(find pycirkuit -name '*.py' -not -name 'resources_rc.py'))
     pyside6-lupdate -tr-function-alias translate+=_translate \
       "${PY_FILES[@]}" -ts pycirkuit/L10n/pycirkuit.ca.ts pycirkuit/L10n/pycirkuit_empty.ts
     ```
     `PY_FILES` must be a shell array (`(...)` + `"${PY_FILES[@]}"`), not a
     plain string variable expanded unquoted (`$PY_FILES`) - in `zsh`
     (unlike `bash`) an unquoted variable does not split on whitespace by
     default, so the whole multi-line `find` output collapses into a single
     giant "filename" and `lupdate` fails with `File '...' does not exist`.
     The array form works the same way in both shells.

     The `-tr-function-alias` flag is required: by default `pyside6-lupdate`
     does not recognize this project's `_translate = QCoreApplication.translate`
     alias at all, and silently extracts zero strings from files using it.
     Telling it that `_translate` is an alternate spelling of `translate`
     (not of `tr` - see below) fixes that.

     **Three things this command relies on, all confirmed, worth knowing
     if the recipe is ever "simplified":**

     - **`pycirkuit/resources/resources_rc.py` must always be excluded.**
       This is the actual, single root cause behind what first looked like
       two separate problems: `pyside6-lupdate` reliably segfaults the
       moment it tries to parse this file's huge embedded-binary content -
       confirmed in isolation (`pyside6-lupdate .../resources_rc.py` alone
       crashes) and confirmed *not* to be about directory scanning in
       general (`pyside6-lupdate -extensions py pycirkuit/ui` and
       `pycirkuit/tools` both work fine; only pointing it at
       `pycirkuit/resources`, the one directory containing this file,
       crashes). It has zero translatable strings anyway, so excluding it
       loses nothing.
     - **Still list files explicitly rather than pointing at a bare
       directory** (`pyside6-lupdate pycirkuit/`, no `-extensions`) -
       that mode only honors a fixed default extension list that doesn't
       include `.py`, so it silently extracts straight from the `.ui`
       files and skips every hand-written `.py` file, with no warning
       that anything was skipped.
     - **Don't "simplify" by renaming `_translate` calls to `_tr`/`tr`
       to dodge the alias flag.** `tr(text, comment=None, n=-1)` and
       `translate(context, text, comment=None, n=-1)` are different Qt
       function shapes, not two spellings of the same thing.
  2. **Fill in the translation** for any new `<translation
     type="unfinished"></translation>` entries in each locale's `.ts` file
     (Qt Linguist, or edit the XML directly) — for whichever language(s)
     you're maintaining.
  3. **Compile each `.ts` to `.qm`:** `lrelease pycirkuit.<LOCALE>.ts` (and
     `pycirkuit_empty.ts`, for consistency, though it stays empty).
  4. **Regenerate the embedded resource bundle.** The app does not load a
     locale's `.qm` from disk — it loads it from
     `:/translations/pycirkuit.<LOCALE>.qm`, embedded in
     `pycirkuit/resources/resources_rc.py`, which is compiled from
     `resources.qrc` and bundles every `.qm` listed there. Updating a `.qm`
     alone has no visible effect until this is redone:
     ```
     cd pycirkuit/resources && pyside6-rcc resources.qrc -o resources_rc.py
     ```
     If a `.ui` file changed instead, the equivalent step is regenerating
     its `Ui_*.py`: `dev-scripts/regen-ui.sh [file.ui ...]` (no arguments
     regenerates every `.ui` file). It wraps `pyside6-uic`, fixes the
     generated `import resources_rc` line to
     `from pycirkuit.resources import resources_rc` (no `pyside6-uic` flag
     produces the correctly-qualified import directly - unlike PyQt5's
     `pyuic5 --import-from`, which PySide6 has no equivalent of), and runs
     `black` on the result.

  Note: `pyside6-uic`/`pyside6-rcc` output can differ noticeably between
  PySide6 versions (byte-level re-encoding of embedded resources, line
  wrapping). A large, hard-to-review diff in `resources_rc.py` or a
  `Ui_*.py` file after regenerating isn't necessarily a sign anything is wrong — the compiled `.qm`/`.ui` content is what actually matters, not the generated source's shape.


## Running the tests

```
pip install -e ".[test]"
pytest
```

Tests mock every external tool (m4, dpic, lualatex, pdf2svg...), so none of
them need to be installed to run the suite.