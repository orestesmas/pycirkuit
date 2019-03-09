# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3 series [Work in progress]
#### Changed
- Code refactoring, cleaning and polishing.

## 0.2 series
### [0.2.2](https://github.com/orestesmas/pycirkuit/compare/v0.2.1..v0.2.2) : (2019-03-10) [Bugfix release]
#### Bug fixes
- Fixed nasty bug found just after the last release when testing the debian package: ask for an alternate location when exporting to a non-writable location ([3c57f8a1](https://github.com/orestesmas/pycirkuit/commit/3c57f8a1)). Closes [#32](https://github.com/orestesmas/pycirkuit/issues/32).
<a name="0.2.1"></a>
### [0.2.1](https://github.com/orestesmas/pycirkuit/compare/v0.2.0..v0.2.1) : (2019-03-09) [Bugfix release]
#### Bug Fixes 
- Fix searching for dpic and CM manuals, and for CM themselves into locations specified by Debian package (several commits). Better reporting if manual not found. Closes [#27](https://github.com/orestesmas/pycirkuit/issues/27).
- Fix potential bugs on windows due to path separator ([9192eae](https://github.com/orestesmas/pycirkuit/commit/9192eae)), ([b5aa03b](https://github.com/orestesmas/pycirkuit/commit/b5aa03b)).
- Don't be silent when trying to export into a write-protected location ([6f0f891](https://github.com/orestesmas/pycirkuit/commit/6f0f891)). Closes [#26](https://github.com/orestesmas/pycirkuit/issues/26).
- Fix erroneous polarity in one example circuit ([0b2db1fa](https://github.com/orestesmas/pycirkuit/commit/0b2db1fa)).
- Fix bug when exporting to TikZ circuits from files without extension ([efebeb4c](https://github.com/orestesmas/pycirkuit/commit/efebeb4c)).
- Start with first Tab selected in About dialog ([3115de6a](https://github.com/orestesmas/pycirkuit/commit/3115de6a)).
- Other minor fixes.

#### Changed
- Updated catalan translation.


<a name="0.2.0"></a>
### [0.2.0](https://github.com/orestesmas/pycirkuit/compare/v0.1..v0.2.0) : (2019-02-24)
#### Added
- Changes in the editor widget:
    - Zoomable text.
    - Syntax highlighting.
- Progress bar for potentially lenghty operations.
- Added example source files.
- Make main window appear centered on screen at startup.
- Added menu option for fast access to Circuit Macros/dpic documentation.
- Windows and MacOS support.
- CHANGELOG file.
- Contributing guide.
- Added contributors list into the "about" dialog.
- Full internationalization (i18n).
- Catalan translation.
- Code published on [GitHub](https://github.com/orestesmas/pycirkuit).
- Package added to [PyPI](https://pypi.org/project/pycirkuit/).
- GitHub issue template.

#### Changed
- Better and simplified installation procedure.
- Better "About" dialog, with automatically updated version and copyright information.
- Improved README.
- Improved configuration file/parameters. Added version number into configuration.
- Code refactoring, cleaning and polishing.

#### Bug Fixes
- Some bugs detected by early adopters. See GitHub for details.

## 0.1 series
<a name="0.1.0"></a>
### 0.1.0 : (2018-11-29) [YANKED]
Initial release with very basic functionality. Intended primarily for personal use.
