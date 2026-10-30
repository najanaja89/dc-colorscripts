"""Measure warm-cache process startup including interpreter and output generation."""

import argparse
import json
import platform
import statistics
import subprocess
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", default=".venv/bin/dc-colorscripts")
    parser.add_argument("--runs", type=int, default=100)
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be positive")
    command = [str(Path(args.command).resolve()), "--name", "batman", "--color", "truecolor"]
    samples = []
    for index in range(args.runs + 5):
        start = time.perf_counter()
        subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
        elapsed = (time.perf_counter() - start) * 1000
        if index >= 5:
            samples.append(elapsed)
    print(
        json.dumps(
            {
                "benchmark_driver_python": platform.python_version(),
                "platform": platform.platform(),
                "runs": args.runs,
                "median_ms": round(statistics.median(samples), 2),
                "p95_ms": round(sorted(samples)[int(0.95 * (len(samples) - 1))], 2),
                "min_ms": round(min(samples), 2),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
