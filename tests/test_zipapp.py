"""Exercise the distributable outside the checkout, with no installed package."""

import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RELEASED = [
    "batman",
    "superman",
    "joker",
    "wonder-woman",
    "flash",
    "green-lantern",
    "nightwing",
    "red-hood",
    "constantine",
    "rorschach",
    "doctor-manhattan",
]


@pytest.fixture(scope="module")
def executable(tmp_path_factory):
    directory = tmp_path_factory.mktemp("single-file")
    executable = directory / "dc-colorscripts"
    subprocess.run(
        [sys.executable, str(ROOT / "tools/build_zipapp.py"), "--output", str(executable)],
        check=True,
    )
    return executable


@pytest.mark.parametrize("name", RELEASED)
@pytest.mark.parametrize("color", ["truecolor", "256", "16", "none"])
def test_zipapp_sprites(executable, name, color):
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            str(executable),
            "--name",
            name,
            "--color",
            color,
            "--lang",
            "ru",
        ],
        cwd=executable.parent,
        env={**os.environ, "COLUMNS": "80"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert "original inspired phrase" in result.stdout
    assert ("\x1b[" in result.stdout) == (color != "none")


def test_zipapp_direct_execution(executable):
    result = subprocess.run(
        [str(executable), "--version"],
        cwd=executable.parent,
        env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert "dc-colorscripts 0.1.0" in result.stdout
    with zipfile.ZipFile(executable) as archive:
        assert "LICENSE" in archive.namelist()
        assert not any("__pycache__" in name for name in archive.namelist())
    assert executable.with_name(executable.name + ".sha256").is_file()


def test_zipapp_narrow_and_error(executable):
    result = subprocess.run(
        [sys.executable, "-I", str(executable), "--name", "batman", "--no-quote"],
        cwd=executable.parent,
        env={**os.environ, "COLUMNS": "12"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert max(map(len, result.stdout.splitlines())) <= 11
    result = subprocess.run(
        [sys.executable, "-I", str(executable), "--name", "unknown"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Unknown character" in result.stderr


def test_zipapp_compact_sprite(executable):
    from dc_colorscripts.characters import ASSETS
    from dc_colorscripts.renderer import load_sprite, render

    result = subprocess.run(
        [
            sys.executable,
            "-I",
            str(executable),
            "--name",
            "batman",
            "--scale",
            "0.5",
            "--no-quote",
            "--color",
            "truecolor",
        ],
        env={**os.environ, "COLUMNS": "80"},
        capture_output=True,
        text=True,
        check=True,
    )
    sprite = load_sprite(ASSETS / "sprites/batman.json")
    assert result.stdout == render(sprite, 79, scale=0.5)
