# -*- coding: utf-8 -*-
"""
Module implementing a CircuitMacros Manager class.
"""
# Copyright (C) 2018-2026 Orestes Mas
# Copyright (C) 2019 Aniol Marti
# This file is part of PyCirkuit.
#
# PyCirkuit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCirkuit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyCirkuit.  If not, see <https://www.gnu.org/licenses/>.
#

# Standard library imports
import base64
import hashlib
import lzma
import os
from os.path import normpath, join, exists, dirname, abspath
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request as Net
import urllib.error as NetError

# Third-party imports
from PySide6 import QtCore
from PySide6.QtCore import QStandardPaths

# Local application imports
from pycirkuit.exceptions import *

# Translation function
_translate = QtCore.QCoreApplication.translate

# Circuit Macros are fetched from TeX Live (see CircuitMacrosManager.download_latest)
TEXLIVE_MIRROR_REDIRECTOR = "https://mirrors.ctan.org/systems/texlive/tlnet"
TLPDB_FILE = "tlpkg/texlive.tlpdb"
TLPDB_SHA512 = TLPDB_FILE + ".sha512"
TEXLIVE_CM_PACKAGE = "circuit-macros"
TEXLIVE_CM_DIR = "doc/latex/circuit-macros"
# Public key of "TeX Live Distribution <tex-live@tug.org>", from
# https://tug.org/texlive/files/texlive.asc, shipped in pycirkuit/keys/
TEXLIVE_KEY_FILE = "texlive.asc"
TEXLIVE_KEY_FINGERPRINT = "C78B82D8C79512F79CC0D7C80D5E5D9106BAB6BC"
NETWORK_TIMEOUT = 60  # seconds
MAX_ARCHIVE_SIZE = 64 * 1024 * 1024
MAX_UNPACKED_SIZE = 256 * 1024 * 1024


class CircuitMacrosManager(QtCore.QObject):
    """
    Class documentation goes here.
    """

    CIRCUIT_MACROS_FILE = "circuit-macros.doc.tar.xz"

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        pass

    def check_installed(self):
        # TODO: Should:
        #  1) Test several places, starting with the one set up in config, but then test also standard locations
        #  2) Two possibilities can arise:
        #     a) There's only one place where CM are
        #     b) They are found in two or more places
        dirList = QStandardPaths.standardLocations(QStandardPaths.GenericDataLocation)
        # Append specific app subdir to each possible location
        dirList = [normpath(join(dir, "circuit-macros")) for dir in dirList]
        settings = QtCore.QSettings()
        extraPath = normpath(settings.value("General/cmPath", ""))
        if extraPath != "":
            dirList.insert(0, extraPath)
        for testPath in dirList:
            if exists(join(testPath, "libcct.m4")):
                #  3) We pick up the first found. Perhaps we might consider other possibilities
                #  4) Finally, as a SIDE EFFECT we can update config automatically or not.
                settings.setValue("General/cmPath", testPath)
                return True
        else:
            return False

    def default_CMPath(self):
        return normpath(
            join(
                QtCore.QStandardPaths.writableLocation(
                    QtCore.QStandardPaths.AppDataLocation
                ),
                "circuit-macros",
            )
        )

    # ------------------------------------------------------------------
    # Verified download of the Circuit Macros (see GitHub issue #52)
    #
    # CTAN does not sign individual packages, but TeX Live does sign its
    # package index: "texlive.tlpdb.sha512" is GPG-signed by the TeX Live
    # distribution key, it holds the SHA-512 of "texlive.tlpdb", and the
    # latter holds the SHA-512 of every package container. Following that
    # chain from a public key shipped with PyCirkuit lets us check that the
    # files we get from an (untrusted) mirror are authentic.
    #
    # All files MUST come from the same mirror: mirrors.ctan.org redirects
    # each request independently, and mixing mirrors that are out of sync
    # makes the signature check fail.
    # ------------------------------------------------------------------

    def _data_path(self):
        dataPath = QtCore.QStandardPaths.writableLocation(
            QtCore.QStandardPaths.AppDataLocation
        )
        if dataPath == "":
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "Cannot determine the standard writable location for PyCirkuit",
                    "Error message",
                )
            )
        os.makedirs(dataPath, exist_ok=True)
        return dataPath

    @staticmethod
    def _fetch(url, maxSize, percent=None):
        """Download url into memory, refusing anything larger than maxSize bytes."""
        if not url.startswith("https://"):
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "Refusing to download from a non-HTTPS location: {url}",
                    "Error message. DO NOT translate '{url}' variable.",
                ).format(url=url)
            )
        try:
            with Net.urlopen(url, timeout=NETWORK_TIMEOUT) as source:
                finalUrl = source.geturl()
                if not finalUrl.startswith("https://"):
                    raise PyCktCMFetchError(
                        _translate(
                            "ExternalTool",
                            "Refusing to download from a non-HTTPS location: {url}",
                            "Error message. DO NOT translate '{url}' variable.",
                        ).format(url=finalUrl)
                    )
                length = source.getheader("content-length")
                length = int(length) if length and length.isdigit() else 0
                if percent is not None:
                    percent.setRange(0, length if 0 < length <= maxSize else 0)
                    percent.setValue(0)
                chunks = []
                size = 0
                while True:
                    buf = source.read(65536)
                    if not buf:
                        break
                    size += len(buf)
                    if size > maxSize:
                        raise PyCktCMFetchError(
                            _translate(
                                "ExternalTool",
                                "The downloaded file is larger than expected: {url}",
                                "Error message. DO NOT translate '{url}' variable.",
                            ).format(url=finalUrl)
                        )
                    chunks.append(buf)
                    if percent is not None and length:
                        percent.setValue(min(size, length))
                return finalUrl, b"".join(chunks)
        except (NetError.URLError, OSError, ValueError) as e:
            raise PyCktCMFetchError(
                _translate("ExternalTool", "Network error: ", "Error message")
                + str(e)
            )

    @staticmethod
    def _dearmor(armored):
        """Convert an ASCII-armored OpenPGP key into its binary form."""
        lines = armored.splitlines()
        try:
            start = lines.index("-----BEGIN PGP PUBLIC KEY BLOCK-----") + 1
        except ValueError:
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "The TeX Live public key shipped with PyCirkuit is damaged.",
                    "Error message",
                )
            )
        # Skip armor headers, which end with an empty line
        while start < len(lines) and lines[start].strip() != "":
            start += 1
        body = []
        for line in lines[start + 1 :]:
            line = line.strip()
            if line.startswith("=") or line.startswith("-----END"):
                break
            body.append(line)
        return base64.b64decode("".join(body))

    @staticmethod
    def _find_gpgv():
        for candidate in ("gpgv", "gpgv2"):
            path = shutil.which(candidate)
            if path:
                return path
        raise PyCktCMFetchError(
            _translate(
                "ExternalTool",
                "Cannot verify the authenticity of the Circuit Macros because the program 'gpgv' (part of GnuPG) is not installed.\n\nPlease install GnuPG, or install the Circuit Macros manually and set their path in the settings dialog.",
                "Error message. DO NOT translate 'gpgv'.",
            )
        )

    def _verify_signature(self, signedData, signature):
        """Check signature with gpgv, trusting only the TeX Live key shipped with PyCirkuit."""
        gpgv = self._find_gpgv()
        keyFile = join(dirname(dirname(abspath(__file__))), "keys", TEXLIVE_KEY_FILE)
        try:
            with open(keyFile, "r", encoding="ascii") as f:
                keyring = self._dearmor(f.read())
        except OSError as e:
            raise PyCktCMFetchError(str(e))
        with tempfile.TemporaryDirectory() as tmp:
            keyringPath = join(tmp, "texlive.gpg")
            dataPath = join(tmp, "texlive.tlpdb.sha512")
            sigPath = dataPath + ".asc"
            for path, content in (
                (keyringPath, keyring),
                (dataPath, signedData),
                (sigPath, signature),
            ):
                with open(path, "wb") as f:
                    f.write(content)
            try:
                result = subprocess.run(
                    [
                        gpgv,
                        "--homedir",
                        tmp,
                        "--keyring",
                        keyringPath,
                        "--status-fd",
                        "1",
                        sigPath,
                        dataPath,
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=NETWORK_TIMEOUT,
                )
            except (OSError, subprocess.SubprocessError) as e:
                raise PyCktCMFetchError(str(e))
        # VALIDSIG <subkey fpr> <date> <timestamp> <expire> <ver> <rsvd> <pkalgo> <hashalgo> <class> <primary fpr>
        validPrimaryKeys = set()
        for line in result.stdout.decode("utf-8", "replace").splitlines():
            fields = line.split()
            if len(fields) >= 3 and fields[:2] == ["[GNUPG:]", "VALIDSIG"]:
                validPrimaryKeys.add(fields[-1].upper())
        if result.returncode != 0 or TEXLIVE_KEY_FINGERPRINT not in validPrimaryKeys:
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "The digital signature of the TeX Live package index is NOT valid. The download has been aborted for security reasons.",
                    "Error message",
                )
            )

    @staticmethod
    def _check_sha512(data, expected, what):
        if hashlib.sha512(data).hexdigest() != expected.lower():
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "Checksum mismatch for {file}. The download has been aborted for security reasons.",
                    "Error message. DO NOT translate '{file}' variable.",
                ).format(file=what)
            )

    @staticmethod
    def _tlpdb_entry(tlpdb, packageName):
        """Return the "key value" pairs of a package entry in texlive.tlpdb."""
        entry = {}
        inside = False
        for line in tlpdb.splitlines():
            if not inside:
                inside = line == "name " + packageName
                continue
            if line == "":
                break
            key, _, value = line.partition(" ")
            entry.setdefault(key, value)
        return entry

    def download_latest(self, percent):
        """
        Download the Circuit Macros from TeX Live and verify their authenticity.

        Raises PyCktCMFetchError if anything cannot be downloaded or verified.
        """
        # 1) Pick one mirror and get the signed checksum of the package index
        indexUrl, indexChecksum = self._fetch(
            TEXLIVE_MIRROR_REDIRECTOR + "/" + TLPDB_SHA512, 4096
        )
        if not indexUrl.endswith("/" + TLPDB_SHA512):
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "Unexpected redirection to {url}",
                    "Error message. DO NOT translate '{url}' variable.",
                ).format(url=indexUrl)
            )
        mirror = indexUrl[: -len("/" + TLPDB_SHA512)]
        _, indexSignature = self._fetch(mirror + "/" + TLPDB_SHA512 + ".asc", 65536)
        # 2) Verify that the checksum was signed by TeX Live
        self._verify_signature(indexChecksum, indexSignature)
        expectedIndexHash = indexChecksum.split()[0].decode("ascii", "replace")
        # 3) Get the package index and check it against the signed checksum
        _, compressedIndex = self._fetch(
            mirror + "/" + TLPDB_FILE + ".xz", 64 * 1024 * 1024, percent
        )
        try:
            tlpdb = lzma.decompress(compressedIndex)
        except lzma.LZMAError as e:
            raise PyCktCMFetchError(str(e))
        self._check_sha512(tlpdb, expectedIndexHash, TLPDB_FILE)
        # 4) Get the Circuit Macros and check them against the (now trusted) index
        entry = self._tlpdb_entry(
            tlpdb.decode("utf-8", "replace"), TEXLIVE_CM_PACKAGE
        )
        expectedHash = entry.get("doccontainerchecksum", "")
        if len(expectedHash) != 128:
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "Cannot find the Circuit Macros in the TeX Live package index.",
                    "Error message",
                )
            )
        _, archive = self._fetch(
            mirror + "/archive/" + CircuitMacrosManager.CIRCUIT_MACROS_FILE,
            MAX_ARCHIVE_SIZE,
            percent,
        )
        self._check_sha512(archive, expectedHash, CircuitMacrosManager.CIRCUIT_MACROS_FILE)
        # 5) Only verified data reaches the disk
        destination = join(self._data_path(), CircuitMacrosManager.CIRCUIT_MACROS_FILE)
        with open(destination, "wb") as dest:
            dest.write(archive)

    def getManUrl(self):
        import glob

        try:
            import magic
        except ImportError:
            raise PyCirkuitError(
                _translate(
                    "ExternalTool",
                    "Module 'python-magic' not found. Please check that all PyCirkuit dependencies are correctly installed.",
                    "Error message",
                )
            )
        mime = magic.Magic(
            mime=True
        )  # Prepare to detect a file's mimetype based on its contents
        # Get standard locations for documentation in a platform-independent way
        dirList = QStandardPaths.standardLocations(QStandardPaths.GenericDataLocation)
        # Append specific app subdir to each possible location
        dirList = [normpath(join(dir, "doc", "circuit-macros")) for dir in dirList]
        # Add the config-stored Circuit Macros Location to this list
        settings = QtCore.QSettings()
        extraPath = normpath(settings.value("General/cmPath", ""))
        extraPath = join(extraPath, "doc")
        dirList.insert(0, extraPath)
        # Add the default Circuit Macros location to this list (can be the same as above)
        dirList.append(join(self.default_CMPath(), "doc"))
        # Explore the generated list searching for pdf or compressed pdf
        for testPath in dirList:
            # Perhaps we should search for *.pdf* or, at least, for *.pdf AND *.pdf.gz
            candidates = glob.glob(join(testPath, "Circuit_macros.pdf"))
            candidates.extend(glob.glob(join(testPath, "Circuit_macros.pdf.gz")))
            for candidate in candidates:
                mimeType = mime.from_file(candidate)
                if (mimeType == "application/pdf") or (mimeType == "application/gzip"):
                    return candidate
        else:
            raise PyCktCMManNotFoundError(
                normpath(settings.value("General/cmPath", ""))
            )

    def unpack_circuit_macros(self):
        """
        Unpack the archive fetched by download_latest() into default_CMPath().

        Only regular files and directories inside the Circuit Macros folder of
        the archive are extracted, and they are first unpacked into a staging
        directory so that a failure never leaves a half-installed copy behind.
        """
        dataPath = self._data_path()
        archiveName = join(dataPath, CircuitMacrosManager.CIRCUIT_MACROS_FILE)
        target = self.default_CMPath()
        if exists(target):
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "Cannot install the Circuit Macros because the folder {path} already exists. Please remove it or set the correct Circuit Macros path in the settings dialog.",
                    "Error message. DO NOT translate '{path}' variable.",
                ).format(path=target)
            )
        staging = tempfile.mkdtemp(prefix="circuit-macros-", dir=dataPath)
        try:
            with tarfile.open(archiveName, "r:xz") as tar:
                members = []
                total = 0
                for member in tar.getmembers():
                    name = member.name
                    if not name.startswith(TEXLIVE_CM_DIR + "/"):
                        continue
                    parts = name.split("/")
                    if (
                        name.startswith("/")
                        or "\\" in name
                        or ".." in parts
                        or not (member.isreg() or member.isdir())
                    ):
                        raise PyCktCMFetchError(
                            _translate(
                                "ExternalTool",
                                "The Circuit Macros archive contains an unsafe entry: {name}",
                                "Error message. DO NOT translate '{name}' variable.",
                            ).format(name=name)
                        )
                    total += member.size
                    if total > MAX_UNPACKED_SIZE:
                        raise PyCktCMFetchError(
                            _translate(
                                "ExternalTool",
                                "The Circuit Macros archive is larger than expected.",
                                "Error message",
                            )
                        )
                    members.append(member)
                if hasattr(tarfile, "data_filter"):
                    tar.extractall(staging, members=members, filter="data")
                else:
                    tar.extractall(staging, members=members)
            unpacked = join(staging, *TEXLIVE_CM_DIR.split("/"))
            if not exists(join(unpacked, "libcct.m4")):
                raise PyCktCMFetchError(
                    _translate(
                        "ExternalTool",
                        "The downloaded archive does not contain the Circuit Macros.",
                        "Error message",
                    )
                )
            os.rename(unpacked, target)
        except (OSError, tarfile.TarError, lzma.LZMAError) as e:
            raise PyCktCMFetchError(
                _translate(
                    "ExternalTool",
                    "Error uncompressing the Circuit Macros: ",
                    "Error message",
                )
                + str(e)
            )
        finally:
            shutil.rmtree(staging, ignore_errors=True)
            try:
                os.remove(archiveName)
            except OSError:
                pass
        settings = QtCore.QSettings()
        settings.setValue("General/cmPath", target)
        settings.sync()
