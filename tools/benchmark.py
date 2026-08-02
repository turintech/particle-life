#!/usr/bin/env python3

"""Lab harness: times the simulation but writes Artemis metrics in the wrong place.

Teaching defect: results go to tools/artemis_results.json. Artemis requires
artemis_results.json at the repository root. Fix the output path before Discovery.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def main() -> int:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Benchmark the Swarm Garden simulation")
    parser.add_argument("--particles", type=positive_int, default=2200)
    parser.add_argument("--frames", type=positive_int, default=30)
    parser.add_argument("--visualize", dest="visualize", action="store_true", default=False)
    parser.add_argument("--no-visualize", dest="visualize", action="store_false")
    args = parser.parse_args()

    binary = project / "build" / "swarm_garden"
    if not binary.is_file():
        parser.error("build/swarm_garden does not exist; run the compile command first")

    # Intentionally wrong location for the lab — must be the repository root.
    results = Path(__file__).resolve().parent / "artemis_results.json"
    root_results = project / "artemis_results.json"
    results.unlink(missing_ok=True)
    root_results.unlink(missing_ok=True)

    completed = subprocess.run(
        [str(binary), "benchmark", str(args.particles), str(args.frames)],
        cwd=project,
        check=True,
        capture_output=True,
        text=True,
    )
    sys.stdout.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)

    match = re.search(r"fps=([0-9]+(?:\.[0-9]+)?)", completed.stdout)
    if not match:
        print("error: could not parse fps= from benchmark stdout", file=sys.stderr)
        return 1

    fps = float(match.group(1))
    results.write_text(json.dumps({"simulation_fps": fps}) + "\n", encoding="utf-8")
    print(f"wrote {results}", file=sys.stderr)

    if args.visualize:
        visualize = subprocess.run(
            [
                sys.executable,
                str(project / "tools" / "window_renderer.py"),
                "--binary",
                str(binary),
                "--particles",
                "3500",
                "--duration",
                "10.0",
            ],
            cwd=project,
        )
        if visualize.returncode != 0:
            print(
                "warning: --visualize pass failed (exit "
                f"{visualize.returncode}); measured results above are unaffected "
                "(likely no graphical display available, e.g. a headless runner)",
                file=sys.stderr,
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
