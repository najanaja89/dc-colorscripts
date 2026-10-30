"""Palette sprites to ANSI half blocks, independent of CLI and character data."""

import json
import math
from pathlib import Path

RESET = "\x1b[0m"


def load_sprite(path):
    resource = Path(path) if isinstance(path, str) else path
    sprite = json.loads(resource.read_text(encoding="utf-8"))
    rows, palette = sprite["pixels"], sprite["palette"]
    for variant in (rows, sprite.get("compact_pixels", rows)):
        if not variant or not variant[0] or len({len(row) for row in variant}) != 1:
            raise ValueError("Sprite rows must have equal, nonzero width")
        if any(pixel != "." and pixel not in palette for row in variant for pixel in row):
            raise ValueError("Sprite contains an undefined palette symbol")
    for color in palette.values():
        if len(color) != 3 or any(type(v) is not int or not 0 <= v <= 255 for v in color):
            raise ValueError("Palette entries must be RGB byte triples")
    return sprite


def color_mode(environ, is_tty):
    if not is_tty or "NO_COLOR" in environ or environ.get("TERM") == "dumb":
        return "none"
    if environ.get("COLORTERM", "").lower() in ("truecolor", "24bit"):
        return "truecolor"
    return "256" if "256color" in environ.get("TERM", "") else "16"


ANSI16 = (
    (0, 0, 0),
    (128, 0, 0),
    (0, 128, 0),
    (128, 128, 0),
    (0, 0, 128),
    (128, 0, 128),
    (0, 128, 128),
    (192, 192, 192),
    (128, 128, 128),
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
)


def escape(rgb, background, mode):
    prefix = 48 if background else 38
    if mode == "truecolor":
        return f"\x1b[{prefix};2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    if mode == "256":
        levels = (0, 95, 135, 175, 215, 255)
        r, g, b = [min(range(6), key=lambda i: abs(levels[i] - v)) for v in rgb]
        index = 16 + 36 * r + 6 * g + b
        gray = min(range(24), key=lambda i: abs(8 + 10 * i - sum(rgb) / 3))
        if sum((v - (8 + 10 * gray)) ** 2 for v in rgb) < sum(
            (v - levels[i]) ** 2 for v, i in zip(rgb, (r, g, b), strict=True)
        ):
            index = 232 + gray
        return f"\x1b[{prefix};5;{index}m"
    index = min(
        range(16), key=lambda i: sum((a - b) ** 2 for a, b in zip(rgb, ANSI16[i], strict=True))
    )
    code = (40 if background else 30) + index % 8 + (60 if index >= 8 else 0)
    return f"\x1b[{code}m"


def render(sprite, width, mode="truecolor", scale=1.0):
    """Scale with nearest-neighbor sampling, preserving proportions within width."""
    if mode not in ("truecolor", "256", "16", "none"):
        raise ValueError(f"Unknown color mode: {mode}")
    if not math.isfinite(scale) or not 0 < scale <= 4:
        raise ValueError("Scale must be greater than 0 and at most 4")
    rows, palette = sprite["pixels"], sprite["palette"]
    source_width, source_height = len(rows[0]), len(rows)
    target_width = min(max(1, width), max(1, round(source_width * scale)))
    target_height = max(1, round(source_height * target_width / source_width))
    compact = sprite.get("compact_pixels")
    if compact and target_width <= len(compact[0]):
        rows = compact
        source_width, source_height = len(rows[0]), len(rows)
    if (target_width, target_height) != (source_width, source_height):
        # Sample pixel centers; use the same ratio on both axes.
        rows = [
            "".join(
                rows[min(source_height - 1, int((y + 0.5) * source_height / target_height))][
                    min(source_width - 1, int((x + 0.5) * source_width / target_width))
                ]
                for x in range(target_width)
            )
            for y in range(target_height)
        ]
    if len(rows) % 2:
        rows.append("." * len(rows[0]))
    lines = []
    for y in range(0, len(rows), 2):
        cells = []
        for top, bottom in zip(rows[y], rows[y + 1], strict=True):
            if top == bottom == ".":
                cells.append(" ")
                continue
            glyph = "▄" if top == "." else "▀"
            if mode == "none":
                cells.append("█" if top == bottom else glyph)
                continue
            if top == ".":
                cell = escape(palette[bottom], False, mode) + glyph
            elif bottom == ".":
                cell = escape(palette[top], False, mode) + glyph
            else:
                cell = escape(palette[top], False, mode)
                cell += escape(palette[bottom], True, mode) + glyph
            cells.append(cell + RESET)
        lines.append("".join(cells).rstrip())
    return "\n".join(lines) + "\n"
