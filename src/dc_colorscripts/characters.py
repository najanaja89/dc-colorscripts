"""Data-driven character collection; only released sprites are selectable."""

import json
import random
from importlib.resources import files

ASSETS = files("dc_colorscripts") / "assets"


def load_characters():
    return json.loads((ASSETS / "characters.json").read_text(encoding="utf-8"))


def select_character(characters, name=None, category=None):
    available = [c for c in characters if c["available"]]
    if name:
        matches = [c for c in characters if c["id"] == name.lower()]
        if not matches:
            raise ValueError(f"Unknown character: {name}. Use --list to see identifiers.")
        if not matches[0]["available"]:
            raise ValueError(f"{matches[0]['name']}: sprite not released yet.")
        if category and matches[0]["category"] != category:
            raise ValueError(f"{name} does not belong to {category}.")
        return matches[0]
    if category:
        available = [c for c in available if c["category"] == category]
    if not available:
        raise ValueError("No released characters match this selection.")
    return random.choice(available)
