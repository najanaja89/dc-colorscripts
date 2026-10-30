"""Create original, hand-directed pixel sprites and terminal caches (stdlib only)."""

import json
import sys
from pathlib import Path

from hero_art import HEROES, retouch_compact

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dc_colorscripts.renderer import render  # noqa: E402

ASSETS = ROOT / "src/dc_colorscripts/assets"
PALETTE = {
    "k": [101, 65, 48],
    "d": [172, 129, 83],
    "e": [217, 181, 128],
    "o": [18, 20, 36],
    "n": [31, 40, 63],
    "b": [48, 65, 96],
    "g": [101, 121, 144],
    "h": [161, 182, 197],
    "w": [245, 241, 217],
    "s": [239, 181, 137],
    "t": [181, 112, 88],
    "y": [255, 209, 62],
    "a": [183, 124, 33],
    "r": [191, 33, 57],
    "R": [250, 68, 71],
    "u": [28, 82, 175],
    "U": [53, 142, 230],
    "c": [110, 199, 242],
    "p": [92, 39, 137],
    "P": [158, 71, 182],
    "v": [43, 128, 65],
    "V": [106, 211, 79],
    "f": [176, 197, 169],
}


class Canvas:
    def __init__(self):
        self.pixels = [["."] * 40 for _ in range(64)]

    def rect(self, x1, y1, x2, y2, color):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.pixels[y][x] = color

    def poly(self, points, color):
        for y in range(64):
            for x in range(40):
                inside = False
                j = len(points) - 1
                for i, (xi, yi) in enumerate(points):
                    xj, yj = points[j]
                    if (yi > y + 0.5) != (yj > y + 0.5):
                        if x + 0.5 < (xj - xi) * (y + 0.5 - yi) / (yj - yi) + xi:
                            inside = not inside
                    j = i
                if inside:
                    self.pixels[y][x] = color

    def rows(self):
        return ["".join(row) for row in self.pixels]


def batman():
    c = Canvas()
    # Scalloped cape, pointed cowl, heavy gauntlets, gray suit and yellow oval crest.
    c.poly(
        [
            (12, 19),
            (27, 19),
            (33, 26),
            (39, 57),
            (32, 54),
            (29, 59),
            (24, 55),
            (20, 60),
            (15, 55),
            (10, 59),
            (7, 54),
            (0, 57),
            (6, 27),
        ],
        "o",
    )
    c.poly([(9, 25), (13, 23), (9, 49), (5, 53)], "n")
    c.poly([(28, 24), (31, 28), (35, 53), (29, 50)], "b")
    c.poly([(12, 22), (27, 22), (29, 35), (25, 42), (14, 42), (10, 34)], "g")
    c.rect(13, 25, 16, 33, "h")
    c.rect(24, 26, 26, 35, "b")
    c.poly([(11, 23), (7, 26), (5, 39), (9, 43), (13, 32)], "g")
    c.poly([(28, 23), (32, 26), (34, 39), (30, 43), (26, 32)], "g")
    c.rect(5, 36, 10, 44, "n")
    c.rect(29, 36, 34, 44, "n")
    for y in (35, 38, 41):
        c.poly([(5, y), (2, y - 2), (4, y + 3)], "b")
        c.poly([(34, y), (37, y - 2), (35, y + 3)], "b")
    c.rect(13, 40, 26, 43, "y")
    for x in (14, 18, 23):
        c.rect(x, 40, x + 1, 43, "a")
    c.rect(19, 40, 21, 42, "w")
    c.poly([(14, 44), (25, 44), (26, 50), (22, 53), (19, 47), (17, 54), (12, 51)], "n")
    c.rect(13, 48, 17, 56, "g")
    c.rect(22, 48, 26, 56, "g")
    c.rect(12, 54, 17, 61, "n")
    c.rect(22, 54, 27, 61, "n")
    c.rect(9, 60, 17, 62, "o")
    c.rect(22, 60, 30, 62, "o")
    c.poly(
        [(13, 9), (12, 1), (17, 7), (23, 7), (28, 1), (27, 18), (24, 22), (16, 22), (12, 17)],
        "n",
    )
    c.rect(14, 9, 16, 14, "b")
    c.poly([(14, 13), (19, 14), (18, 16), (14, 15)], "w")
    c.poly([(21, 14), (26, 13), (26, 15), (22, 16)], "w")
    c.rect(16, 17, 23, 20, "s")
    c.rect(18, 20, 22, 20, "t")
    c.rect(18, 18, 22, 18, "o")
    c.poly([(14, 27), (17, 25), (23, 25), (26, 27), (25, 30), (15, 30)], "y")
    c.poly(
        [
            (15, 27),
            (18, 28),
            (18, 26),
            (20, 27),
            (22, 26),
            (22, 28),
            (25, 27),
            (23, 29),
            (21, 29),
            (20, 31),
            (18, 29),
            (16, 29),
        ],
        "o",
    )
    return c


def superman():
    c = Canvas()
    c.poly(
        [(10, 21), (29, 21), (33, 32), (38, 57), (28, 60), (19, 56), (8, 59), (2, 55), (6, 30)],
        "r",
    )
    c.poly([(8, 27), (11, 24), (8, 51), (4, 55)], "R")
    c.poly([(29, 26), (31, 34), (34, 55), (29, 57)], "t")
    c.poly([(11, 22), (28, 22), (29, 36), (25, 43), (14, 43), (10, 34)], "u")
    c.rect(13, 24, 16, 36, "U")
    c.rect(17, 35, 24, 38, "U")
    c.poly([(11, 23), (7, 25), (5, 39), (8, 44), (12, 34)], "u")
    c.poly([(28, 23), (32, 25), (34, 39), (31, 44), (27, 34)], "u")
    c.rect(7, 27, 9, 35, "U")
    c.rect(5, 40, 9, 45, "s")
    c.rect(30, 40, 34, 45, "s")
    c.rect(13, 40, 26, 42, "y")
    c.rect(18, 40, 21, 42, "a")
    c.poly([(13, 43), (26, 43), (24, 48), (20, 50), (15, 47)], "r")
    c.rect(13, 47, 17, 57, "u")
    c.rect(22, 47, 26, 57, "u")
    c.rect(14, 49, 15, 54, "U")
    c.rect(23, 49, 24, 54, "U")
    c.rect(12, 55, 17, 61, "r")
    c.rect(22, 55, 27, 61, "r")
    c.rect(9, 60, 17, 62, "R")
    c.rect(22, 60, 30, 62, "R")
    c.rect(17, 18, 23, 23, "t")
    c.poly([(12, 7), (16, 4), (25, 4), (28, 8), (26, 17), (23, 21), (17, 21), (13, 17)], "s")
    c.rect(13, 11, 14, 16, "t")
    c.poly(
        [
            (12, 12),
            (11, 6),
            (15, 2),
            (24, 2),
            (28, 5),
            (28, 12),
            (25, 8),
            (22, 6),
            (16, 7),
            (14, 12),
        ],
        "o",
    )
    c.rect(15, 4, 22, 4, "b")
    c.poly([(21, 6), (23, 8), (21, 11), (20, 10), (22, 8)], "o")
    c.rect(15, 12, 18, 12, "o")
    c.rect(23, 12, 25, 12, "o")
    c.rect(20, 13, 20, 16, "t")
    c.rect(18, 18, 23, 18, "w")
    c.poly([(13, 26), (16, 24), (24, 24), (27, 26), (20, 34)], "y")
    # A hand-pixelled red S inside the gold diamond.
    for x1, y, x2 in [
        (17, 25, 23),
        (16, 26, 17),
        (17, 27, 21),
        (20, 28, 23),
        (22, 29, 23),
        (18, 30, 22),
        (19, 31, 20),
    ]:
        c.rect(x1, y, x2, y, "r")
    return c


def joker():
    c = Canvas()
    # Exaggerated green pompadour, angular ivory face, red grin, purple tailcoat.
    c.poly(
        [
            (12, 24),
            (27, 24),
            (31, 36),
            (33, 55),
            (26, 52),
            (23, 45),
            (16, 46),
            (12, 55),
            (6, 53),
            (9, 35),
        ],
        "p",
    )
    c.poly([(12, 25), (8, 27), (5, 40), (8, 44), (13, 33)], "p")
    c.poly([(28, 25), (32, 28), (34, 39), (31, 43), (27, 33)], "P")
    c.rect(5, 40, 9, 45, "w")
    c.rect(30, 40, 34, 45, "w")
    c.rect(16, 26, 24, 42, "v")
    c.rect(18, 27, 22, 39, "V")
    c.poly([(12, 23), (18, 27), (17, 34), (13, 30), (15, 29)], "P")
    c.poly([(26, 23), (22, 27), (23, 35), (28, 29), (25, 29)], "P")
    c.rect(18, 25, 22, 29, "a")
    c.rect(18, 26, 19, 28, "y")
    for y in (32, 36, 40):
        c.rect(21, y, 21, y, "y")
    c.rect(13, 44, 18, 59, "p")
    c.rect(23, 44, 28, 59, "p")
    c.rect(14, 47, 15, 57, "P")
    c.rect(24, 47, 25, 57, "P")
    c.rect(10, 59, 18, 62, "o")
    c.rect(23, 59, 31, 62, "o")
    c.rect(17, 19, 23, 25, "f")
    c.poly([(12, 9), (17, 5), (25, 7), (28, 12), (26, 19), (22, 23), (17, 22), (12, 17)], "w")
    c.poly([(12, 12), (12, 17), (17, 22), (18, 19), (15, 15)], "f")
    c.poly(
        [
            (11, 14),
            (8, 8),
            (12, 9),
            (10, 4),
            (15, 6),
            (17, 1),
            (20, 4),
            (25, 2),
            (30, 7),
            (28, 14),
            (25, 9),
            (21, 8),
            (17, 10),
            (14, 9),
        ],
        "v",
    )
    c.poly(
        [(12, 6), (16, 7), (18, 3), (21, 6), (25, 4), (28, 7), (22, 7), (18, 9), (14, 8)], "V"
    )
    c.rect(14, 12, 17, 12, "p")
    c.rect(22, 11, 25, 11, "p")
    c.rect(15, 13, 17, 13, "o")
    c.rect(22, 12, 24, 12, "o")
    c.rect(20, 13, 20, 16, "f")
    c.poly([(13, 15), (16, 17), (22, 17), (26, 14), (25, 19), (21, 21), (16, 20)], "r")
    c.rect(16, 17, 23, 18, "w")
    c.rect(18, 19, 22, 19, "o")
    c.rect(25, 30, 27, 30, "R")
    return c


def compact_pixels(name, rows):
    """Retouch half-size faces and insignia instead of discarding their key pixels."""
    pixels = [list(row[1::2]) for row in rows[1::2]]

    def patch(x, y, *lines):
        for offset, line in enumerate(lines):
            pixels[y + offset][x : x + len(line)] = line

    if name == "batman":
        # Two separate white eyes, nose bridge, jaw and mouth.
        patch(
            6,
            3,
            "nnnnnnnn",
            "nbnnnnnn",
            "nbnnnnnn",
            "nwwnnwwn",
            "nnnnnnnn",
            "nnssssnn",
            "nnsttsnn",
        )
        # A deliberately wider bat silhouette within the gold oval.
        patch(6, 12, "gggggggg", "gyyyyyyg", "gyooooyg", "gyyooyyg", "gggggggg")
        # Keep a readable row of belt pouches.
        patch(6, 20, "ayaywaya", "ayayayay")
    elif name == "superman":
        patch(6, 5, "ossssso", "sosssos", "tssstss", "tssssss", "sswwwss", "tsssstt")
        # Red S: two horizontal strokes and opposite side strokes on gold.
        patch(
            6,
            12,
            "uuyyyyuu",
            "uyrrrryu",
            "uyryyyyu",
            "uyyrrryu",
            "uuyyyryu",
            "uuurryyu",
            "uuuuyyuu",
        )
    elif name == "joker":
        patch(
            5,
            2,
            "vVvVVvvVv",
            "vVVVVVVvv",
            "vVwwwwwvv",
            "vwwwwwwwv",
            "wwopwopww",
            "fwwwfwwwf",
            "fwrwwwrwf",
            "ffrwwwrff",
            "ffwrrrwff",
            "fffwwwfff",
        )
        # Small bright lapels and a gold bow tie.
        patch(7, 12, "PyyaP", "PPVPv", "pPVPp")
    retouch_compact(name, patch)
    return ["".join(row) for row in pixels]


def write_preview(sprites, compact=False):
    columns = 4
    cell_width, cell_height, pixel_size = (180, 250, 6) if compact else (270, 470, 6)
    width = columns * cell_width
    height = ((len(sprites) + columns - 1) // columns) * cell_height
    shapes = [f'<rect width="{width}" height="{height}" fill="#151822"/>']
    for index, (name, sprite) in enumerate(sprites):
        left = (index % columns) * cell_width
        top = (index // columns) * cell_height
        rows = sprite["compact_pixels"] if compact else sprite["pixels"]
        x_offset = (cell_width - len(rows[0]) * pixel_size) // 2
        for y, row in enumerate(rows):
            for x, symbol in enumerate(row):
                if symbol == ".":
                    continue
                color = "#" + "".join(f"{v:02x}" for v in PALETTE[symbol])
                shapes.append(
                    f'<rect x="{left + x_offset + x * pixel_size}" '
                    f'y="{top + 12 + y * pixel_size}" width="{pixel_size}" '
                    f'height="{pixel_size}" fill="{color}"/>'
                )
        shapes.append(
            f'<text x="{left + cell_width // 2}" y="{top + cell_height - 20}" '
            f'fill="#eee" text-anchor="middle" font-family="monospace" '
            f'font-size="14">{name.replace("-", " ").title()}</text>'
        )
    filename = "compact-preview.svg" if compact else "preview.svg"
    (ROOT / "docs" / filename).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        + "".join(shapes)
        + "</svg>\n",
        encoding="utf-8",
    )


def main():
    sprites = []
    artists = {"batman": batman, "superman": superman, "joker": joker}
    artists.update({name: lambda draw=draw: draw(Canvas) for name, draw in HEROES.items()})
    for name, draw in artists.items():
        sprite = {"palette": PALETTE, "pixels": draw().rows()}
        sprite["compact_pixels"] = compact_pixels(name, sprite["pixels"])
        sprites.append((name, sprite))
        (ASSETS / "sprites" / f"{name}.json").write_text(json.dumps(sprite, indent=2) + "\n")
        for mode in ("truecolor", "256", "16"):
            (ASSETS / "sprites" / f"{name}.{mode}.ansi").write_text(render(sprite, 80, mode))
    write_preview(sprites)
    write_preview(sprites, compact=True)


if __name__ == "__main__":
    main()
