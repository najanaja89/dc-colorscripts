import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from dc_colorscripts import __version__
from dc_colorscripts.characters import ASSETS, load_characters, select_character
from dc_colorscripts.cli import main, parser
from dc_colorscripts.quotes import choose_quote, format_quote
from dc_colorscripts.renderer import RESET, color_mode, load_sprite, render

ANSI = re.compile(r"\x1b\[[0-9;]*m")
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


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["--random"],
        ["--villains", "--lang", "ru"],
        ["--name", "batman", "--no-quote"],
        ["--heroes"],
    ],
)
def test_parsing(args):
    parser().parse_args(args)


@pytest.mark.parametrize(
    "args",
    [
        ["--heroes", "--villains"],
        ["--lang", "de"],
        ["--name", "batman", "--random"],
        ["--quote-only", "--no-quote"],
        ["--unknown"],
    ],
)
def test_invalid_arguments(args):
    with pytest.raises(SystemExit) as error:
        parser().parse_args(args)
    assert error.value.code == 2


def test_database_and_random():
    characters = load_characters()
    assert len(characters) == len({c["id"] for c in characters}) == 20
    assert {c["id"] for c in characters if c["available"]} == set(RELEASED)
    assert len([c for c in characters if c["available"] and c["category"] == "heroes"]) == 10
    for category in ("heroes", "villains"):
        for _ in range(30):
            chosen = select_character(characters, category=category)
            assert chosen["available"] and chosen["category"] == category
    assert select_character(characters, "BATMAN")["id"] == "batman"


@pytest.mark.parametrize(
    "name,category,message",
    [
        ("unknown", None, "Unknown character"),
        ("bane", None, "not released"),
        ("joker", "heroes", "does not belong"),
    ],
)
def test_selection_errors(name, category, message):
    with pytest.raises(ValueError, match=message):
        select_character(load_characters(), name, category)


def test_empty_selection():
    with pytest.raises(ValueError, match="No released"):
        select_character([])


@pytest.mark.parametrize("name", RELEASED)
@pytest.mark.parametrize("lang", ["en", "ru"])
def test_quotes(name, lang):
    data = json.loads((ASSETS / "quotes" / f"{lang}.json").read_text())
    assert len(data[name]) >= 3
    assert choose_quote(name, lang) in data[name]


def test_language_fallback():
    assert (
        choose_quote("batman", "missing")
        in json.loads((ASSETS / "quotes/en.json").read_text())["batman"]
    )
    assert choose_quote("unknown") is None


@pytest.mark.parametrize("width", [1, 8, 20, 39, 40, 80])
@pytest.mark.parametrize("mode", ["truecolor", "256", "16", "none"])
def test_render_width(width, mode):
    sprite = load_sprite(ASSETS / "sprites/batman.json")
    output = render(sprite, width, mode)
    assert max(map(len, ANSI.sub("", output).splitlines())) <= width
    assert ("\x1b[" in output) == (mode != "none")
    assert output.endswith("\n")


@pytest.mark.parametrize("name", RELEASED)
def test_assets_and_caches(name):
    sprite = load_sprite(ASSETS / f"sprites/{name}.json")
    assert len(sprite["pixels"]) == 64
    assert len(sprite["palette"]) >= 8
    for mode in ("truecolor", "256", "16"):
        assert (ASSETS / f"sprites/{name}.{mode}.ansi").read_text() == render(sprite, 80, mode)


def test_transparency():
    sprite = {"pixels": ["a.", ".a", "..", ".."], "palette": {"a": [255, 0, 0]}}
    output = render(sprite, 80)
    assert "\x1b[48;" not in output
    assert "▀" in output and "▄" in output and RESET in output


def test_missing_and_invalid_sprite(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_sprite(tmp_path / "missing")
    path = tmp_path / "invalid.json"
    for pixels, palette in [(["..", "."], {}), (["x"], {}), (["a"], {"a": [999, 0, 0]})]:
        path.write_text(json.dumps({"pixels": pixels, "palette": palette}))
        with pytest.raises(ValueError):
            load_sprite(path)


@pytest.mark.parametrize(
    "env,tty,expected",
    [
        ({"COLORTERM": "truecolor"}, True, "truecolor"),
        ({"TERM": "xterm-256color"}, True, "256"),
        ({"TERM": "xterm"}, True, "16"),
        ({"TERM": "dumb"}, True, "none"),
        ({"NO_COLOR": ""}, True, "none"),
        ({"COLORTERM": "truecolor"}, False, "none"),
    ],
)
def test_color_detection(env, tty, expected):
    assert color_mode(env, tty) == expected


def test_quote_wrap():
    assert all(
        len(line) <= 12
        for line in format_quote("Длинная фраза " * 10, "Batman", 12).splitlines()
    )


def test_cli(capsys):
    assert main(["--name", "batman", "--quote-only", "--lang", "ru"]) == 0
    assert "Batman" in capsys.readouterr().out
    assert main(["--name", "joker", "--no-quote"]) == 0
    assert "original inspired phrase" not in capsys.readouterr().out
    assert main(["--list", "--villains"]) == 0
    output = capsys.readouterr().out
    assert "planned" in output and "Joker" in output and "Batman" not in output
    with pytest.raises(SystemExit):
        main(["--name", "missing"])
    assert "Unknown character" in capsys.readouterr().err


def test_installed_command():
    command = Path(sys.executable).parent / "dc-colorscripts"
    assert command.exists(), "Install package before testing: pip install -e ."
    result = subprocess.run(
        [str(command), "--version"], capture_output=True, text=True, check=True
    )
    assert __version__ in result.stdout
    for name in RELEASED:
        result = subprocess.run(
            [str(command), "--name", name, "--lang", "ru"],
            cwd="/tmp",
            env={**os.environ, "TERM": "dumb"},
            capture_output=True,
            text=True,
            check=True,
        )
        assert "\x1b" not in result.stdout and result.stdout.endswith("\n")
    result = subprocess.run(
        [sys.executable, "-m", "dc_colorscripts", "--list"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Batman" in result.stdout


def test_cli_missing_asset(monkeypatch, tmp_path, capsys):
    import dc_colorscripts.cli as cli

    monkeypatch.setattr(cli, "ASSETS", tmp_path)
    with pytest.raises(SystemExit) as error:
        main(["--name", "batman"])
    assert error.value.code == 2
    assert "dc-colorscripts:" in capsys.readouterr().err


def test_missing_translation_entry(monkeypatch, tmp_path):
    import dc_colorscripts.quotes as quotes

    (tmp_path / "quotes").mkdir()
    (tmp_path / "quotes/ru.json").write_text("{}")
    (tmp_path / "quotes/en.json").write_text('{"batman": ["Fallback"]}')
    monkeypatch.setattr(quotes, "ASSETS", tmp_path)
    assert quotes.choose_quote("batman", "ru") == "Fallback"


def test_real_tty_output():
    import pty

    master, slave = pty.openpty()
    command = Path(sys.executable).parent / "dc-colorscripts"
    process = subprocess.Popen(
        [str(command), "--name", "batman", "--no-quote"],
        stdout=slave,
        env={
            key: value
            for key, value in {
                **os.environ,
                "COLORTERM": "truecolor",
                "TERM": "xterm-256color",
            }.items()
            if key != "NO_COLOR"
        },
    )
    os.close(slave)
    output = bytearray()
    try:
        while True:
            try:
                chunk = os.read(master, 65536)
            except OSError:
                break
            if not chunk:
                break
            output.extend(chunk)
    finally:
        os.close(master)
    assert process.wait(timeout=5) == 0
    assert b"\x1b[38;2;" in output
    assert output.endswith(b"\x1b[0m\r\n") or output.endswith(b"\r\n")


@pytest.mark.parametrize("scale,columns,lines", [(0.5, 20, 16), (0.75, 30, 24), (2, 80, 64)])
def test_scaled_dimensions(scale, columns, lines):
    sprite = load_sprite(ASSETS / "sprites/superman.json")
    output = ANSI.sub("", render(sprite, 100, scale=scale))
    assert len(output.splitlines()) == lines
    assert max(map(len, output.splitlines())) <= columns
    assert any(pixel in output for pixel in "▀▄█")


@pytest.mark.parametrize("scale", [0, -1, 5, float("nan"), float("inf")])
def test_invalid_scale(scale):
    with pytest.raises(SystemExit) as error:
        parser().parse_args([f"--scale={scale}"])
    assert error.value.code == 2
    sprite = load_sprite(ASSETS / "sprites/batman.json")
    with pytest.raises(ValueError, match="Scale"):
        render(sprite, 80, scale=scale)


def test_scale_cli(capsys, monkeypatch):
    monkeypatch.setenv("COLUMNS", "100")
    assert (
        main(["--name", "batman", "--scale", "0.5", "--no-quote", "--color", "truecolor"]) == 0
    )
    output = ANSI.sub("", capsys.readouterr().out)
    assert len(output.splitlines()) == 16
    assert max(map(len, output.splitlines())) <= 20


def test_scale_fits_terminal():
    sprite = load_sprite(ASSETS / "sprites/batman.json")
    output = ANSI.sub("", render(sprite, 10, scale=4))
    assert max(map(len, output.splitlines())) <= 10
    assert len(output.splitlines()) == 8


@pytest.mark.parametrize("name", RELEASED)
def test_half_size_uses_compact_art(name):
    sprite = load_sprite(ASSETS / f"sprites/{name}.json")
    assert len(sprite["compact_pixels"]) == 32
    assert {len(row) for row in sprite["compact_pixels"]} == {20}
    compact_sprite = {"pixels": sprite["compact_pixels"], "palette": sprite["palette"]}
    assert render(sprite, 80, scale=0.5) == render(compact_sprite, 20)
    assert render(sprite, 20) == render(compact_sprite, 20)
    # The face/emblem corrections must survive, rather than reverting to raw sampling.
    without_compact = {"pixels": sprite["pixels"], "palette": sprite["palette"]}
    assert render(sprite, 80, scale=0.5) != render(without_compact, 80, scale=0.5)


def test_compact_asset_validation(tmp_path):
    path = tmp_path / "bad-compact.json"
    path.write_text(
        json.dumps({"pixels": ["a"], "palette": {"a": [0, 0, 0]}, "compact_pixels": ["x"]})
    )
    with pytest.raises(ValueError, match="undefined palette"):
        load_sprite(path)
