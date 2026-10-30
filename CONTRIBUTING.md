# Contributing

Use Python 3.11+ and the virtual environment commands in README.md. Use Ruff,
four-space Python indentation, and a 96-column target. Keep runtime dependencies
at zero. Run pytest and both Ruff checks before opening a pull request. Explain
the change, link relevant issues, and include previews for artwork. Use focused,
imperative commit subjects.

## Add a character sprite

1. Edit `src/dc_colorscripts/assets/characters.json`. Use a lowercase hyphenated
   identifier and category `heroes` or `villains`. Keep `available: false` until
   the artwork and both phrase translations are ready.
2. Draw original art, extending `tools/build_assets.py` or creating palette JSON
   at `assets/sprites/<id>.json`. `pixels` is an equal-width array of strings;
   `.` is transparent. `palette` maps other single-character symbols to RGB byte
   triples. Prefer 40×64 pixels and review the art on a dark terminal background.
3. Include recognizable costume details, a clear silhouette, and multiple shades.
   Never mark generic placeholders as finished sprites.
4. Compile `truecolor`, `256`, and `16` variants with `renderer.render`, naming
   them `<id>.<mode>.ansi`. `python tools/build_assets.py` regenerates the bundled
   sprites, caches, and `docs/preview.svg`. Extend it for new procedural artwork.
5. Set `sprite` to `sprites/<id>.json`, `palette` to
   `sprites/<id>.json#palette`, and `available` to true. Add localized phrases and
   asset/cache tests. Core selection and CLI logic need no changes.

Include source and provenance. No runtime downloads. Preview images should show
actual sprite pixels rather than promotional mockups.

## Phrases and translations

Edit UTF-8 `assets/quotes/en.json` and `ru.json`. Each character ID maps to a
nonempty array of original inspired phrases. Missing translations fall back to
English; missing English entries omit the phrase. Another language requires its
JSON file, CLI language choice, and tests. Do not invent canonical dialogue.
Canonical quotes need attribution and separate copyright review.

## Validation

Cover selection, invalid inputs, transparency, terminal widths, language fallback,
and installed package assets. There is no numeric coverage threshold. Keep caches
in sync with JSON sources. Run `python tools/benchmark.py` after startup changes
and report measured results and the environment.

## Compact artwork

Bundled sprites include optional `compact_pixels` arrays, sharing the main palette.
These are 20×32 pixel variants retouched for small output. The renderer chooses
this artwork for target widths of 20 columns or fewer. Keep both eyes, costume
insignia, and facial expressions readable rather than trusting automatic reduction.
Add retouches in `compact_pixels()` in `tools/build_assets.py` or
`retouch_compact()` in `tools/hero_art.py`; regenerate the
assets and `docs/compact-preview.svg`. Sprites without a compact variant still
render through nearest-neighbor scaling.
