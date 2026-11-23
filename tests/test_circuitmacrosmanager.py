# -*- coding: utf-8 -*-
"""
Tests for the verified Circuit Macros download (GitHub issue #52).
They never touch the network: the signed TeX Live index checksum in
tests/data/ was captured from a real mirror.
"""
import hashlib
import io
import os
import shutil
import tarfile

import pytest

from pycirkuit.exceptions import PyCktCMFetchError
from pycirkuit.tools import circuitmacrosmanager as cmm
from pycirkuit.tools.circuitmacrosmanager import CircuitMacrosManager

DATA = os.path.join(os.path.dirname(__file__), "data")
needs_gpgv = pytest.mark.skipif(
    not (shutil.which("gpgv") or shutil.which("gpgv2")), reason="gpgv not installed"
)


def _read(name):
    with open(os.path.join(DATA, name), "rb") as f:
        return f.read()


@needs_gpgv
def test_genuine_texlive_signature_is_accepted():
    CircuitMacrosManager()._verify_signature(
        _read("texlive.tlpdb.sha512"), _read("texlive.tlpdb.sha512.asc")
    )


@needs_gpgv
def test_tampered_index_checksum_is_rejected():
    data = bytearray(_read("texlive.tlpdb.sha512"))
    data[0] = ord("0") if data[0] != ord("0") else ord("1")
    with pytest.raises(PyCktCMFetchError):
        CircuitMacrosManager()._verify_signature(
            bytes(data), _read("texlive.tlpdb.sha512.asc")
        )


@needs_gpgv
def test_signature_from_unexpected_key_is_rejected(monkeypatch):
    monkeypatch.setattr(cmm, "TEXLIVE_KEY_FINGERPRINT", "0" * 40)
    with pytest.raises(PyCktCMFetchError):
        CircuitMacrosManager()._verify_signature(
            _read("texlive.tlpdb.sha512"), _read("texlive.tlpdb.sha512.asc")
        )


def test_checksum_mismatch_is_rejected():
    data = b"circuit macros"
    CircuitMacrosManager._check_sha512(data, hashlib.sha512(data).hexdigest(), "x")
    with pytest.raises(PyCktCMFetchError):
        CircuitMacrosManager._check_sha512(data + b"!", hashlib.sha512(data).hexdigest(), "x")


def test_tlpdb_entry_is_parsed_only_for_the_requested_package():
    tlpdb = (
        "name circuit-macros-evil\ndoccontainerchecksum bad\n\n"
        "name circuit-macros\ncategory Package\ndoccontainerchecksum good\n\n"
        "name other\ndoccontainerchecksum other\n"
    )
    entry = CircuitMacrosManager._tlpdb_entry(tlpdb, "circuit-macros")
    assert entry["doccontainerchecksum"] == "good"


def test_non_https_download_is_refused():
    with pytest.raises(PyCktCMFetchError):
        CircuitMacrosManager._fetch("http://example.org/x", 10)


def _make_archive(path, entries):
    with tarfile.open(path, "w:xz") as tar:
        for name, content, kind in entries:
            info = tarfile.TarInfo(name)
            if kind == "symlink":
                info.type = tarfile.SYMTYPE
                info.linkname = "/etc/passwd"
                tar.addfile(info)
            else:
                info.size = len(content)
                tar.addfile(info, io.BytesIO(content))


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    # tmp_path itself also holds the isolated QSettings file
    data = tmp_path / "appdata"
    data.mkdir()
    monkeypatch.setattr(CircuitMacrosManager, "_data_path", lambda self: str(data))
    monkeypatch.setattr(
        CircuitMacrosManager,
        "default_CMPath",
        lambda self: str(data / "circuit-macros"),
    )
    return data


def test_unpack_installs_only_the_circuit_macros_folder(data_dir):
    _make_archive(
        data_dir / CircuitMacrosManager.CIRCUIT_MACROS_FILE,
        [
            (cmm.TEXLIVE_CM_DIR + "/libcct.m4", b"divert(-1)", "file"),
            (cmm.TEXLIVE_CM_DIR + "/doc/Circuit_macros.pdf", b"%PDF", "file"),
            ("tlpkg/tlpobj/circuit-macros.doc.tlpobj", b"x", "file"),
        ],
    )
    CircuitMacrosManager().unpack_circuit_macros()
    assert sorted(os.listdir(data_dir)) == ["circuit-macros"]
    assert (data_dir / "circuit-macros" / "libcct.m4").exists()
    assert (data_dir / "circuit-macros" / "doc" / "Circuit_macros.pdf").exists()


@pytest.mark.parametrize(
    "name, kind",
    [
        (cmm.TEXLIVE_CM_DIR + "/../../../escaped.m4", "file"),
        (cmm.TEXLIVE_CM_DIR + "/link", "symlink"),
    ],
)
def test_unpack_rejects_unsafe_entries(data_dir, name, kind):
    _make_archive(
        data_dir / CircuitMacrosManager.CIRCUIT_MACROS_FILE,
        [(cmm.TEXLIVE_CM_DIR + "/libcct.m4", b"x", "file"), (name, b"x", kind)],
    )
    with pytest.raises(PyCktCMFetchError):
        CircuitMacrosManager().unpack_circuit_macros()
    assert os.listdir(data_dir) == []
