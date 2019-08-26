# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3 series
### [0.3.3] [Unreleased]
#### Bug Fixes
- Reprocess erroneus source file that has been manually corrected in the middle of a batch operation ([de1c9c31bf](https://github.com/orestesmas/pycirkuit/commit/de1c9c31bf)). Closes [#50](https://github.com/orestesmas/pycirkuit/issues/50).
### [0.3.2](https://github.com/orestesmas/pycirkuit/compare/v0.3.2..v0.3.0) : (2019-08-02) [Bugfix release]
#### Bug fixes
- Fix the GUI for Mac.
### [0.3.1](https://github.com/orestesmas/pycirkuit/compare/v0.3.1..v0.3.0) : (2019-07-26) [Bugfix release]
#### Added
- Added 2 more examples
#### Changed
- Changed some GUI names and shortcuts ([0ec9b859](https://github.com/orestesmas/pycirkuit/commit/0ec9b859)).
- Changed export icon in settings dialog.
- Updated catalan translation.
#### Bug fixes
- Implemented a missed feature: when an error is encountered while processing a file in batch (CLI) mode, allow to open the GUI to solve the issue manually ([670c51e0](https://github.com/orestesmas/pycirkuit/commit/670c51e0)).
- Make behave correctly when executing from a non-graphical session (several commits).
- Fix regression introduced by commit [e4eab569](https://github.com/orestesmas/pycirkuit/commit/e4eab569) related to image zooming.
- Make some MessageBox titles homogeneous ([eb4ddb0c](https://github.com/orestesmas/pycirkuit/commit/eb4ddb0c)).
<a name="0.3.0"></a>
### [0.3.0](https://github.com/orestesmas/pycirkuit/compare/v0.2.0..v0.3.0) : (2019-07-22)
#### Added
- Command line interface to process files in batch mode with rich functionality: selectable raster resolution, selectable output quality, intermediate vector formats, recursivity, selectable destination dir, overwriting switch, etc.
- Parametrized export functionality in settings.
- Added new export formats, either vector (PDF) and raster (BMP, JPEG).
- Zoomable graphics with no quality loss.
- Log output tab ([4251c0f](https://github.com/orestesmas/pycirkuit/commit/4251c0f)).
#### Changed
- Updated catalan translation.
- Updated credits.
- Code refactoring, cleaning and polishing.
#### Bug Fixes
- Clear image when 'New' menu option is clicked ([a98a4125](https://github.com/orestesmas/pycirkuit/commit/a98a4125)).
- Fixed inconsistency between dash (-) and underscore(_) in Circuit Macros path ([27fc7680](https://github.com/orestesmas/pycirkuit/commit/27fc7680)). Closes [#33](https://github.com/orestesmas/pycirkuit/issues/33).

## 0.2 series
### [0.2.3](https://github.com/orestesmas/pycirkuit/compare/v0.2.2..v0.2.3) : (2019-07-10) [Bugfix release]
#### Bug fixes
- Fixed broken link to Circuit Macros ([2cb630f5](https://github.com/orestesmas/pycirkuit/commit/2cb630f5))
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
