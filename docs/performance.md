# Startup measurement

Measured on 2026-10-30 in this development environment:

- Nobara Linux, kernel `7.3.0-202.nobara.fc44.x86_64`, x86_64, glibc 2.43.
- Conda `default` Python 3.14.10, with an isolated `.venv-conda` derived from it.
- Installed editable entry point; Batman, quote enabled, forced true color.
- 100 launches after five warmups, warm filesystem caches, stdout to `/dev/null`.
- Median **21.89 ms**, p95 **23.06 ms**, minimum **20.71 ms**.

The under-100-ms target was met in this environment. These measurements include
process startup and output generation, not terminal painting. They are not a
promise for every workstation or Python installation.

Reproduce:

```sh
python tools/benchmark.py --command .venv-conda/bin/dc-colorscripts --runs 100
```

The ordinary development environment defaults to `.venv/bin/dc-colorscripts`.
No subprocess is launched by the application; only this benchmark launches
processes. Normal-width colored sprites use precompiled ANSI; narrower terminals
perform palette rendering, and monochrome uses palette rendering as well.

## Single-file archive (2026-10-30)

After archive-compatible resource loading was added, the same 100-launch method
with five warmups measured:

| Installation | Median | p95 | Minimum |
| --- | ---: | ---: | ---: |
| Compressed executable zipapp | 30.34 ms | 32.93 ms | 28.95 ms |
| Editable package | 26.41 ms | 27.43 ms | 25.21 ms |

The archive was 17,540 bytes at measurement time. Its `/usr/bin/env python3`
shebang resolved to system Python 3.14.8; the editable package used Conda Python
3.14.10. The benchmark driver used Conda Python 3.14.10 for both runs. These are
different interpreter installations, so the difference is not a controlled
measurement of ZIP overhead. Both remained below the 100 ms target here.

```sh
python tools/benchmark.py --command dist/dc-colorscripts
```

## Expanded hero collection (2026-10-30)

After adding the eight remaining heroes/antiheroes with compact variants and
localized phrases, the compressed executable contains 11 released characters and
is 46,539 bytes. Using the same environment and 100-launch method:

- Median: **28.89 ms**; p95: **33.44 ms**; minimum: **28.35 ms**.
- System Python 3.14.8 runs the executable; Conda Python 3.14.10 drives the benchmark.
- Batman, forced true color, quote enabled; five discarded warmups; stdout to
  `/dev/null` (terminal paint time excluded).

The collection remains under the 100 ms startup target in this environment.
