# Contributing to PyCirkuit

You are here to help on PyCirkuit? Awesome! PyCirkuit is still at its infancy and needs a lot of love and work. If tou find this application useful, there are some areas where you can help, depending on your interests and level of expertise:

  - Writing documentation
  - Translating the app to your native language
  - Finding bugs and fixing issues
  - Contributing code


## Contributing guidelines

At present, PyCirkuit is a small project with little infrastructure around. Contributions are welcome and they don't have to adhere to any particular convention, but will be accepted or rejected at developer's discretion.

Meanwhile, you can ask questions or send contributions directly to me at [mailto:orestes@tsc.upc.edu](mailto:orestes@tsc.upc.edu).

**Thanks!**


## Contributing translations

The application is fully internationalized, so you can translate it to your language. If you want to do so, please follow these steps:

  1. Install the [Qt developping tools](https://www.qt.io/download), specially "Linguist". Unfortunately, Qt company does not offer you to download Linguist separately of the other developping tools. If you need/want install only QtLinguist, you can check [this project](https://github.com/lelegard/qtlinguist-installers).

  3. Locate the file [pycirkuit/L10n/pycirkuit_empty.ts](https://github.com/orestesmas/pycirkuit/blob/master/pycirkuit/L10n/pycirkuit_empty.ts) and copy it into a new file named "pycirkuit.LOCALE.ts" where LOCALE is the code/country of your language. For instance for french it can be "fr", "fr_CA", "fr_FR", etc. See [this Wikipedia entry](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for a complete list.
  4. Open the new file under Linguist and translate all the strings in it. The [Qt Linguist manual](http://doc.qt.io/qt-5/qtlinguist-index.html) can be helpful.
  5. Send the translated .TS file to the PyCirkuit developers or, if you know how to do it, create a pull/merge request.


## Maintaining translations (developers)

If you add or change a translatable string (a `_translate(...)` call, or a
`.ui` file), the full chain to make it actually show up in the running app
is: source -> `.ts` -> translated `.ts` -> `.qm` -> embedded resource. Each
step has its own tool, and skipping one leaves you looking at stale text
with no error to explain why.

  1. **Extract strings into the `.ts` files.** From `pycirkuit/L10n/`, for
     every locale file the project ships (currently `pycirkuit.ca.ts`) plus
     `pycirkuit_empty.ts`:
     ```
     pylupdate5 <changed .py files...> -ts pycirkuit.<LOCALE>.ts pycirkuit_empty.ts
     ```
     **Gotcha:** `pylupdate5`'s scanner misses `_translate(...)` calls that
     Black has reformatted one-argument-per-line; it only recognizes the
     call when `context, source, comment` are folded onto one line after
     the opening paren. This is a real, project-wide issue introduced by
     the Black migration and not yet cleaned up (see `MODERNIZATION.md`) —
     **do not run `pylupdate5` across the whole tree and blindly accept the
     merge**: check the "Found N source texts... kept M obsolete" summary
     it prints, and if M looks too high, some of those "obsolete" strings
     are probably still live and about to be silently dropped from that
     locale's compiled translation. When in doubt, add the new `<message>`
     entry to the locale `.ts` file(s) by hand instead, matching the format
     of a neighboring entry.
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
     cd pycirkuit/resources && pyrcc5 resources.qrc -o resources_rc.py
     ```
     If a `.ui` file changed instead, the equivalent step is regenerating
     its `Ui_*.py` with `pyuic5 <file>.ui -o Ui_<file>.py
     --import-from=pycirkuit.resources`, then running `black` on it to
     match the project's code style.

  Note: `pyuic5`/`pyrcc5` output differs noticeably between PyQt5 versions
  (byte-level re-encoding of embedded resources, line wrapping). A large,
  hard-to-review diff in `resources_rc.py` or a `Ui_*.py` file after
  regenerating isn't necessarily a sign anything is wrong — the compiled
  `.qm`/`.ui` content is what actually matters, not the generated source's
  shape.


## Running the tests

```
pip install -e ".[test]"
pytest
```

Tests mock every external tool (m4, dpic, lualatex, pdf2svg...), so none of
them need to be installed to run the suite.