"""Build a compressed executable with all runtime assets; requires only Python."""

import argparse
import hashlib
import shutil
import tempfile
import zipapp
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(output):
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dc-colorscripts-build-") as temporary:
        staging = Path(temporary)
        shutil.copytree(
            ROOT / "src/dc_colorscripts",
            staging / "dc_colorscripts",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        shutil.copy2(ROOT / "LICENSE", staging / "LICENSE")
        (staging / "__main__.py").write_text(
            "import sys\n"
            "if sys.version_info < (3, 11):\n"
            '    sys.exit("dc-colorscripts requires Python 3.11 or newer")\n'
            "from dc_colorscripts.cli import main\n"
            "sys.exit(main())\n",
            encoding="utf-8",
        )
        zipapp.create_archive(
            staging, output, interpreter="/usr/bin/env python3", compressed=True
        )
    output.chmod(0o755)
    checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_name(output.name + ".sha256").write_text(
        f"{checksum}  {output.name}\n", encoding="ascii"
    )
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/dc-colorscripts")
    args = parser.parse_args()
    output = build(args.output)
    print(f"Built {output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
