"""Original character-inspired writing, never attributed as canonical dialogue."""

import json
import random
import textwrap

from .characters import ASSETS


def choose_quote(character_id, language="en"):
    path = ASSETS / "quotes" / f"{language}.json"
    entries = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    choices = entries.get(character_id)
    if not choices:
        choices = json.loads((ASSETS / "quotes/en.json").read_text(encoding="utf-8")).get(
            character_id, []
        )
    return random.choice(choices) if choices else None


def format_quote(quote, name, width):
    return "\n".join(
        textwrap.fill(line, width=max(1, width))
        for line in (f"“{quote}”", f"— {name} · original inspired phrase")
    )
