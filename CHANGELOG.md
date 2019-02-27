# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.2 series
### 0.2.1 [unreleased]
#### Fixed 
- Fix potential bugs on windows due to path separator ([9192eae](https://github.com/orestesmas/pycirkuit/commit/9192eae))
- Don't be silent when trying to export into a write-protected location ([6f0f891](https://github.com/orestesmas/pycirkuit/commit/6f0f891))

### 0.2.0 - 2019-02-24
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

#### Fixed
- Some bugs detected by early adopters. See GitHub for details.

## 0.1 series
### 0.1.0 - 2018-11-29 [YANKED]
Initial release with very basic functionality. Intended primarily for personal use.
