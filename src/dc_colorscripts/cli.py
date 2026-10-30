"""Small argparse entry point with no terminal state changes."""

import argparse
import math
import os
import shutil
import sys

from . import __version__
from .characters import ASSETS, load_characters, select_character
from .quotes import choose_quote, format_quote
from .renderer import color_mode, load_sprite, render


def scale_factor(value):
    try:
        scale = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("scale must be a number in (0, 4]") from error
    if not math.isfinite(scale) or not 0 < scale <= 4:
        raise argparse.ArgumentTypeError("scale must be greater than 0 and at most 4")
    return scale


def parser():
    result = argparse.ArgumentParser(description="Original DC-inspired terminal pixel art")
    selection = result.add_mutually_exclusive_group()
    selection.add_argument("--random", action="store_true", help="choose a released character")
    selection.add_argument("--name", help="character identifier, e.g. batman")
    category = result.add_mutually_exclusive_group()
    category.add_argument("--heroes", action="store_true")
    category.add_argument("--villains", action="store_true")
    result.add_argument(
        "--list", action="store_true", help="list released and planned characters"
    )
    quotes = result.add_mutually_exclusive_group()
    quotes.add_argument("--quote-only", action="store_true")
    quotes.add_argument("--no-quote", action="store_true")
    result.add_argument(
        "--scale",
        type=scale_factor,
        default=1.0,
        metavar="FACTOR",
        help="sprite size multiplier: 0.5 = half size, 1 = original, 2 = double (max 4)",
    )
    result.add_argument("--lang", choices=("en", "ru"), default="en")
    result.add_argument(
        "--color", choices=("auto", "truecolor", "256", "16", "none"), default="auto"
    )
    result.add_argument("--version", action="version", version=f"dc-colorscripts {__version__}")
    return result


def main(argv=None):
    arguments = parser()
    args = arguments.parse_args(argv)
    try:
        characters = load_characters()
        category = "heroes" if args.heroes else "villains" if args.villains else None
        if args.list:
            for character in characters:
                if not category or character["category"] == category:
                    status = "available" if character["available"] else "planned"
                    print(f"{character['id']:<18} {character['name']} ({status})")
            return 0
        character = select_character(characters, args.name, category)
        width = max(1, shutil.get_terminal_size(fallback=(80, 24)).columns - 1)
        output = ""
        if not args.quote_only:
            mode = (
                color_mode(os.environ, sys.stdout.isatty())
                if args.color == "auto"
                else args.color
            )
            sprite = load_sprite(ASSETS / character["sprite"])
            cache = ASSETS / "sprites" / f"{character['id']}.{mode}.ansi"
            if (
                args.scale == 1.0
                and mode != "none"
                and width >= len(sprite["pixels"][0])
                and cache.is_file()
            ):
                output = cache.read_text(encoding="utf-8")
            else:
                output = render(sprite, width, mode, scale=args.scale)
        if not args.no_quote:
            quote = choose_quote(character["id"], args.lang)
            if quote:
                output += format_quote(quote, character["name"], width) + "\n"
        sys.stdout.write(output)
        return 0
    except BrokenPipeError:
        # Prevent a second flush failure during interpreter shutdown.
        sys.stdout = open(os.devnull, "w")
        return 0
    except (OSError, ValueError, KeyError) as error:
        arguments.exit(2, f"dc-colorscripts: {error}\n")
