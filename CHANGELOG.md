# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3 series
#### Added
- Log output tab ([4251c0f](https://github.comhttps://github.com/orestesmas/pycirkuit/commit/b5aa03b/orestesmas/pycirkuit/commit/4251c0f))
#### Changed
- Better searching for Dpic and Circuit Macros manuals
- Code refactoring, cleaning and polishing

## 0.2 series
<a name="0.2.1"></a>
### 0.2.1 [unreleased]
#### Bug Fixes 
- Fix potential bugs on windows due to path separator ([9192eae](https://github.com/orestesmas/pycirkuit/commit/9192eae)), ([b5aa03b](https://github.com/orestesmas/pycirkuit/commit/b5aa03b))
- Don't be silent when trying to export into a write-protected location ([6f0f891](https://github.com/orestesmas/pycirkuit/commit/6f0f891)). Closes [#26](https://github.com/orestesmas/pycirkuit/issues/26)
- Fix erroneous polarity in one example circuit ([0b2db1fa](https://github.com/orestesmas/pycirkuit/commit/0b2db1fa))

<a name="0.2.0"></a>
### [0.2.0](https://github.com/orestesmas/pycirkuit/compare/v0.1..v0.2.0) : (2019-02-24)
#### Added
- Changes in the editor widget:
    - Zoomable text
    - Syntax highlighting
- Progress bar for potentially lenghty operations
- Added example source files
- Make main window appear centered on screen at startup
- Added menu option for fast access to Circuit Macros/dpic documentation
- Windows and MacOS support
- CHANGELOG file
- Contributing guide
- Added contributors list into the "about" dialog
- Full internationalization (i18n)
- Catalan translation
- Code published on [GitHub](https://github.com/orestesmas/pycirkuit)
- Package added to [PyPI](https://pypi.org/project/pycirkuit/)
- GitHub issue template

#### Changed
- Better and simplified installation procedure
- Better "About" dialog, with automatically updated version and copyright information.
- Improved README
- Improved configuration file/parameters. Added version number into configuration.
- Code refactoring, cleaning and polishing

#### Bug Fixes
- Some bugs detected by early adopters. See GitHub for details.

## 0.1 series
<a name="0.1.0"></a>
### 0.1.0 : (2018-11-29) [YANKED]
Initial release with very basic functionality. Intended primarily for personal use.
