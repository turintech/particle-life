#!/usr/bin/env python3
"""Run the headless Particle Life benchmark and publish Artemis metrics."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile


FPS_PATTERN = re.compile(r"\bfps=([0-9]+(?:\.[0-9]+)?)\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--particles", type=int, default=2200)
    parser.add_argument("--frames", type=int, default=30)
    parser.add_argument(
        "--no-visualize",
        action="store_true",
        help="Accepted explicitly because Artemis benchmarks must stay headless.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    binary = root / "build" / "particle_life"
    result = root / "artemis_results.json"
    csv_result = root / "artemis_results.csv"

    if not (root / "CMakeLists.txt").is_file():
        raise SystemExit("run this benchmark from the repository root")
    if not binary.is_file():
        raise SystemExit("build/particle_life is missing; run the compile command first")
    if args.particles <= 0 or args.frames <= 0:
        raise SystemExit("particles and frames must be positive")

    result.unlink(missing_ok=True)
    csv_result.unlink(missing_ok=True)

    completed = subprocess.run(
        [str(binary), "benchmark", str(args.particles), str(args.frames)],
        check=True,
        capture_output=True,
        text=True,
    )
    print(completed.stdout, end="")

    match = FPS_PATTERN.search(completed.stdout)
    if match is None:
        raise SystemExit("benchmark output did not contain a numeric fps value")
    simulation_fps = float(match.group(1))
    if not math.isfinite(simulation_fps) or simulation_fps <= 0:
        raise SystemExit("benchmark produced an invalid simulation_fps")

    payload = {"simulation_fps": simulation_fps}
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=root,
        prefix=".artemis_results.",
        suffix=".tmp",
        delete=False,
    ) as output:
        json.dump(payload, output)
        output.write("\n")
        temporary = Path(output.name)

    os.replace(temporary, result)
    print(f"published {result}: {json.dumps(payload)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
