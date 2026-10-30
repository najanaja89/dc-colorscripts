"""Original character-specific artwork for the expanded hero collection.

Shared anatomy establishes proportions; hair, costumes, props and insignia are
hand-directed per character. No downloaded artwork or runtime dependencies.
"""


def body(Canvas, suit, light, boots="o", gloves=None):
    c = Canvas()
    c.poly([(12, 22), (27, 22), (29, 34), (25, 43), (14, 43), (10, 34)], suit)
    c.rect(13, 25, 16, 34, light)
    c.rect(17, 35, 24, 37, light)
    c.poly([(11, 23), (7, 26), (5, 39), (9, 43), (13, 32)], suit)
    c.poly([(28, 23), (32, 26), (34, 39), (30, 43), (26, 32)], suit)
    c.rect(7, 28, 8, 35, light)
    c.rect(5, 39, 9, 44, gloves or suit)
    c.rect(30, 39, 34, 44, gloves or suit)
    c.rect(13, 42, 18, 58, suit)
    c.rect(22, 42, 27, 58, suit)
    c.rect(14, 47, 15, 54, light)
    c.rect(23, 47, 24, 54, light)
    c.rect(12, 55, 18, 61, boots)
    c.rect(22, 55, 28, 61, boots)
    c.rect(10, 60, 18, 62, boots)
    c.rect(22, 60, 30, 62, boots)
    return c


def face(c, skin="s", shadow="t", hair="o"):
    c.rect(17, 18, 23, 23, shadow)
    c.poly([(12, 7), (16, 3), (24, 3), (28, 7), (26, 18), (23, 21), (17, 21), (13, 17)], skin)
    if hair:
        c.poly(
            [
                (12, 12),
                (11, 6),
                (15, 2),
                (24, 2),
                (28, 6),
                (27, 12),
                (24, 8),
                (21, 6),
                (16, 7),
                (14, 12),
            ],
            hair,
        )
    c.rect(15, 12, 17, 12, "o")
    c.rect(23, 12, 25, 12, "o")
    c.rect(20, 13, 20, 16, shadow)
    c.rect(18, 18, 22, 18, shadow)


def wonder_woman(Canvas):
    c = body(Canvas, "s", "w", "r", "s")
    # Long blue-black hair behind bare shoulders.
    c.poly(
        [
            (12, 6),
            (17, 1),
            (25, 2),
            (29, 8),
            (31, 32),
            (25, 29),
            (24, 18),
            (15, 18),
            (13, 31),
            (8, 32),
        ],
        "o",
    )
    c.rect(10, 13, 12, 27, "b")
    c.rect(27, 12, 28, 28, "n")
    face(c, hair="o")
    # Red armored bodice and stacked gold W, blue star-spangled briefs.
    c.poly([(12, 25), (18, 27), (20, 25), (23, 27), (27, 25), (26, 39), (14, 39)], "r")
    c.poly(
        [
            (12, 25),
            (17, 29),
            (20, 27),
            (23, 29),
            (28, 25),
            (26, 30),
            (23, 33),
            (20, 30),
            (17, 33),
            (13, 30),
        ],
        "y",
    )
    c.rect(15, 33, 17, 37, "R")
    c.poly([(13, 39), (20, 41), (27, 39), (26, 46), (20, 49), (13, 46)], "u")
    c.poly([(13, 38), (20, 40), (27, 38), (27, 40), (20, 43), (13, 40)], "y")
    for x, y in [(15, 43), (23, 43), (19, 46)]:
        c.rect(x, y, x + 1, y + 1, "w")
    c.rect(5, 35, 10, 39, "h")
    c.rect(29, 35, 34, 39, "h")
    c.rect(6, 35, 7, 39, "w")
    # Gold tiara and centered red star.
    c.poly(
        [
            (13, 8),
            (18, 8),
            (20, 6),
            (22, 8),
            (26, 8),
            (26, 10),
            (21, 10),
            (20, 12),
            (18, 10),
            (13, 10),
        ],
        "y",
    )
    c.rect(19, 8, 20, 9, "r")
    c.rect(18, 18, 22, 18, "r")
    # White boot stripes and a hanging golden lasso on the right hip.
    c.rect(15, 55, 16, 61, "w")
    c.rect(24, 55, 25, 61, "w")
    c.poly(
        [
            (29, 40),
            (33, 42),
            (35, 47),
            (34, 53),
            (30, 55),
            (28, 52),
            (28, 46),
            (30, 43),
            (32, 44),
            (30, 47),
            (30, 51),
            (32, 52),
            (33, 48),
            (32, 45),
            (29, 42),
        ],
        "y",
    )
    return c


def flash(Canvas):
    c = body(Canvas, "r", "R", "y", "r")
    face(c, hair=None)
    c.poly(
        [
            (12, 7),
            (16, 2),
            (24, 2),
            (28, 7),
            (27, 17),
            (24, 16),
            (24, 11),
            (16, 11),
            (15, 17),
            (12, 16),
        ],
        "r",
    )
    c.rect(14, 7, 16, 10, "R")
    c.rect(15, 12, 17, 13, "w")
    c.rect(23, 12, 25, 13, "w")
    # Ear lightning wings, not generic round ears.
    c.poly([(12, 10), (7, 8), (9, 12), (6, 12), (11, 17), (10, 13), (12, 14)], "y")
    c.poly([(27, 10), (32, 8), (30, 12), (33, 12), (28, 17), (29, 13), (27, 14)], "y")
    c.poly(
        [(16, 25), (23, 25), (26, 28), (26, 32), (23, 35), (16, 35), (13, 32), (13, 28)], "w"
    )
    c.poly([(21, 25), (17, 30), (20, 30), (17, 35), (24, 28), (21, 28), (24, 25)], "y")
    c.poly(
        [
            (13, 39),
            (18, 40),
            (20, 38),
            (22, 40),
            (27, 39),
            (26, 42),
            (21, 43),
            (19, 41),
            (14, 43),
        ],
        "y",
    )
    c.rect(5, 36, 10, 37, "y")
    c.rect(29, 36, 34, 37, "y")
    c.rect(12, 56, 14, 59, "a")
    c.rect(22, 56, 24, 59, "a")
    return c


def green_lantern(Canvas):
    c = body(Canvas, "o", "n", "v", "w")
    c.poly([(11, 22), (28, 22), (28, 34), (24, 39), (15, 39), (11, 34)], "v")
    c.rect(13, 25, 16, 34, "V")
    c.rect(7, 26, 10, 31, "v")
    c.rect(29, 26, 32, 31, "v")
    face(c, hair="k")
    c.rect(15, 4, 23, 5, "a")
    c.poly(
        [
            (13, 11),
            (18, 11),
            (20, 13),
            (22, 11),
            (27, 11),
            (26, 15),
            (22, 15),
            (20, 14),
            (17, 15),
            (13, 15),
        ],
        "v",
    )
    c.rect(15, 12, 17, 12, "w")
    c.rect(23, 12, 25, 12, "w")
    # White disc containing the green lantern symbol.
    c.poly(
        [(17, 25), (23, 25), (26, 28), (26, 32), (23, 35), (17, 35), (14, 32), (14, 28)], "w"
    )
    c.rect(17, 26, 23, 27, "v")
    c.rect(17, 32, 23, 33, "v")
    c.rect(17, 28, 18, 31, "v")
    c.rect(22, 28, 23, 31, "v")
    # Ring glows against a small green construct, separate from the costume.
    c.poly([(33, 34), (35, 31), (38, 34), (38, 40), (35, 43), (33, 40)], "v")
    c.rect(33, 35, 36, 38, "V")
    c.rect(31, 40, 32, 41, "V")
    return c


def nightwing(Canvas):
    c = body(Canvas, "o", "n", "o", "o")
    face(c)
    # Swept black hair, domino mask and blue bird spreading onto shoulders.
    c.poly([(11, 8), (13, 3), (23, 1), (29, 4), (25, 7), (18, 6), (14, 10)], "o")
    c.poly(
        [
            (13, 11),
            (18, 11),
            (20, 13),
            (22, 11),
            (27, 11),
            (26, 15),
            (22, 15),
            (20, 14),
            (17, 15),
            (13, 15),
        ],
        "o",
    )
    c.rect(15, 12, 17, 12, "w")
    c.rect(23, 12, 25, 12, "w")
    c.poly(
        [
            (7, 25),
            (12, 24),
            (18, 28),
            (20, 26),
            (22, 28),
            (28, 24),
            (33, 25),
            (32, 29),
            (27, 28),
            (22, 32),
            (20, 35),
            (18, 32),
            (12, 28),
            (8, 29),
        ],
        "U",
    )
    c.rect(7, 30, 8, 35, "u")
    c.rect(31, 30, 32, 35, "u")
    # Twin blue escrima sticks held beside the legs.
    c.rect(3, 41, 4, 57, "u")
    c.rect(3, 42, 3, 55, "c")
    c.rect(35, 41, 36, 57, "u")
    c.rect(35, 42, 35, 55, "c")
    c.rect(6, 40, 8, 42, "b")
    c.rect(31, 40, 33, 42, "b")
    return c


def red_hood(Canvas):
    c = body(Canvas, "n", "b", "o", "o")
    # Brown cropped biker jacket framing a red bat insignia.
    c.poly([(12, 22), (16, 23), (15, 40), (11, 43), (9, 31), (6, 38), (5, 29), (8, 24)], "k")
    c.poly(
        [(24, 23), (28, 22), (32, 24), (35, 29), (34, 38), (30, 31), (29, 43), (25, 40)], "k"
    )
    c.rect(8, 27, 9, 35, "d")
    c.rect(29, 25, 30, 34, "d")
    c.poly([(13, 23), (16, 24), (15, 30), (12, 27)], "d")
    c.poly([(26, 23), (23, 24), (25, 30), (28, 27)], "d")
    c.poly(
        [
            (16, 29),
            (19, 31),
            (20, 28),
            (21, 31),
            (24, 29),
            (23, 33),
            (21, 34),
            (20, 36),
            (18, 33),
            (16, 33),
        ],
        "r",
    )
    c.rect(13, 41, 26, 43, "k")
    c.rect(18, 41, 21, 42, "h")
    # Full red armored helmet, white lenses and a dark central face seam.
    c.rect(17, 18, 23, 23, "o")
    c.poly([(12, 8), (15, 3), (24, 3), (28, 8), (27, 17), (24, 21), (16, 21), (12, 17)], "r")
    c.rect(14, 6, 16, 11, "R")
    c.rect(20, 5, 20, 18, "t")
    c.poly([(14, 12), (19, 14), (18, 16), (14, 14)], "w")
    c.poly([(21, 14), (26, 12), (26, 14), (22, 16)], "w")
    c.rect(17, 18, 23, 18, "o")
    c.rect(12, 47, 14, 51, "k")
    c.rect(26, 47, 28, 51, "k")
    return c


def constantine(Canvas):
    c = body(Canvas, "n", "b", "o", "s")
    # Open tan trench coat, white shirt, loosened red tie, blond stubble.
    c.poly(
        [
            (11, 22),
            (28, 22),
            (30, 32),
            (33, 55),
            (25, 56),
            (23, 43),
            (16, 43),
            (14, 56),
            (6, 55),
            (9, 32),
        ],
        "d",
    )
    c.rect(16, 24, 23, 40, "w")
    c.rect(19, 27, 21, 30, "r")
    c.poly([(20, 30), (22, 33), (21, 41), (18, 39)], "r")
    c.poly([(12, 23), (17, 25), (15, 34), (12, 30), (14, 28)], "a")
    c.poly([(27, 23), (22, 25), (24, 34), (28, 29), (25, 28)], "a")
    c.poly([(10, 24), (6, 27), (4, 40), (9, 42), (13, 30)], "d")
    c.poly([(28, 24), (32, 27), (35, 39), (30, 42), (26, 30)], "d")
    c.rect(7, 29, 8, 37, "e")
    c.rect(5, 41, 9, 44, "s")
    c.rect(30, 40, 34, 43, "s")
    c.rect(10, 43, 13, 44, "k")
    c.rect(26, 43, 29, 44, "k")
    face(c, hair="a")
    c.poly(
        [
            (12, 7),
            (13, 3),
            (16, 4),
            (18, 1),
            (21, 4),
            (25, 2),
            (28, 6),
            (25, 9),
            (22, 6),
            (19, 9),
            (16, 6),
            (13, 10),
        ],
        "y",
    )
    c.rect(16, 19, 23, 20, "t")
    # Cigarette and a curling blue-gray smoke trail.
    c.rect(24, 17, 29, 17, "w")
    c.rect(29, 17, 30, 17, "R")
    c.rect(31, 13, 31, 15, "g")
    c.rect(32, 10, 32, 12, "h")
    c.rect(31, 8, 31, 9, "g")
    return c


def rorschach(Canvas):
    c = body(Canvas, "k", "d", "o", "k")
    c.poly(
        [
            (12, 22),
            (27, 22),
            (30, 33),
            (33, 54),
            (23, 56),
            (20, 47),
            (16, 56),
            (6, 54),
            (9, 32),
        ],
        "d",
    )
    c.poly([(11, 24), (7, 26), (4, 39), (9, 42), (13, 31)], "d")
    c.poly([(28, 24), (32, 26), (35, 39), (30, 42), (26, 31)], "k")
    c.rect(5, 40, 9, 44, "k")
    c.rect(30, 40, 34, 44, "k")
    c.poly([(12, 23), (19, 28), (17, 35), (12, 29)], "k")
    c.poly([(27, 23), (20, 28), (23, 35), (28, 29)], "k")
    c.rect(18, 29, 21, 47, "a")
    c.rect(11, 40, 29, 42, "k")
    c.rect(18, 40, 22, 42, "h")
    c.rect(19, 41, 21, 41, "o")
    for y in (33, 37, 46, 50):
        c.rect(22, y, 23, y, "k")
    # Featureless ivory mask with deliberately bilateral inkblots.
    c.rect(17, 19, 23, 25, "p")
    c.poly([(13, 8), (26, 8), (27, 16), (24, 22), (16, 22), (12, 16)], "w")
    for x in (15, 23):
        c.rect(x, 11, x + 1, 15, "o")
    c.rect(16, 14, 18, 16, "o")
    c.rect(22, 14, 24, 16, "o")
    c.rect(18, 16, 22, 18, "o")
    c.rect(17, 19, 18, 20, "o")
    c.rect(22, 19, 23, 20, "o")
    # Broad fedora brim and pinched crown.
    c.poly([(12, 9), (14, 2), (18, 3), (21, 2), (25, 3), (28, 9)], "k")
    c.rect(14, 6, 25, 7, "o")
    c.rect(8, 8, 31, 10, "k")
    c.rect(9, 8, 30, 8, "a")
    return c


def doctor_manhattan(Canvas):
    c = body(Canvas, "U", "c", "U", "U")
    c.rect(13, 56, 14, 60, "c")
    c.rect(23, 56, 24, 60, "c")
    face(c, skin="c", shadow="U", hair=None)
    c.poly([(12, 8), (15, 3), (24, 3), (28, 8), (27, 16), (24, 20), (16, 20), (12, 16)], "U")
    c.rect(14, 7, 17, 14, "c")
    c.rect(16, 16, 24, 18, "c")
    c.rect(15, 12, 18, 13, "w")
    c.rect(22, 12, 25, 13, "w")
    # Hydrogen atom on the forehead: ring with a central nucleus.
    c.rect(18, 5, 22, 9, "u")
    c.rect(19, 6, 21, 8, "c")
    c.rect(20, 7, 20, 7, "o")
    c.rect(18, 19, 22, 19, "u")
    # Pectoral and abdominal shading, dark briefs, bare blue feet.
    c.poly(
        [
            (13, 25),
            (18, 24),
            (20, 27),
            (22, 24),
            (27, 25),
            (25, 32),
            (22, 33),
            (20, 31),
            (17, 33),
            (13, 31),
        ],
        "c",
    )
    c.rect(19, 27, 20, 38, "U")
    c.rect(16, 34, 18, 35, "c")
    c.rect(22, 34, 24, 35, "c")
    c.poly([(13, 40), (27, 40), (26, 45), (20, 49), (14, 45)], "o")
    c.rect(10, 60, 18, 61, "c")
    c.rect(22, 60, 30, 61, "c")
    return c


HEROES = {
    "wonder-woman": wonder_woman,
    "flash": flash,
    "green-lantern": green_lantern,
    "nightwing": nightwing,
    "red-hood": red_hood,
    "constantine": constantine,
    "rorschach": rorschach,
    "doctor-manhattan": doctor_manhattan,
}


def retouch_compact(name, patch):
    """Distinct low-resolution eyes, masks and chest marks for every new hero."""
    if name == "wonder-woman":
        patch(6, 4, "oyyryyo", "ossssso", "sosssos", "sststss", "ssrrsss")
        patch(6, 12, "ryryryr", "ryyryyr", "rryryrr", "rrrrrrr")
        patch(6, 21, "uwuuuuw", "uuuwuuu")
    elif name == "flash":
        patch(6, 5, "rrrrrrr", "rwwrwwr", "rssrssr", "rsstssr", "rrsssrr")
        patch(7, 13, "wwyyww", "wyywww", "wwwyyw", "wwyyww")
        patch(4, 5, "yy", ".y")
        patch(14, 5, "yy", "y.")
    elif name == "green-lantern":
        patch(6, 5, "svvvvvs", "svwvwvs", "sssvsss", "sststss", "ssstsss")
        patch(7, 13, "wvvvvw", "wvwwvw", "wvwwvw", "wvvvvw")
        patch(16, 19, "Vw")
    elif name == "nightwing":
        patch(6, 5, "sooooos", "swwowws", "ssososs", "sststss", "ssstsss")
        patch(6, 13, "UUoooUU", "oUUoUUo", "ooUUUoo", "oooUooo")
    elif name == "red-hood":
        patch(6, 5, "rRrrrrr", "rwwrwwr", "rrrtrrr", "rrooorr", "rrrrrrr")
        patch(8, 14, "rnrr", "rrrr", "nrrn")
    elif name == "constantine":
        patch(6, 2, "yyayyyy", "ayyyaya", "asssssa", "asssssa", "sosssos", "sststss", "sstttss")
        patch(9, 13, "wrw", "wrw", "wrw", "wrr")
        patch(12, 8, "wwR")
    elif name == "rorschach":
        patch(6, 5, "wwwwwww", "wowwwow", "woowoow", "wwoowww", "wowwwow", "wwwwwww")
        patch(6, 3, "kkkkkkk", "ooooooo")
    elif name == "doctor-manhattan":
        patch(
            6,
            2,
            "UUUUUUU",
            "UcuocUU",
            "UcUocUU",
            "UccccUU",
            "UwwUwwU",
            "UccUccU",
            "UcccccU",
            "UUuuuUU",
        )
        patch(7, 13, "ccUUcc", "ccUUcc", "cUUUUc")
