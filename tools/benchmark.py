#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path


def positive_int(value):
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def positive_float(value):
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def main():
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Benchmark the Swarm Garden simulation")
    parser.add_argument("--particles", type=positive_int, default=2200)
    parser.add_argument("--frames", type=positive_int, default=30)
    parser.add_argument("--visualize", action="store_true")
    parser.add_argument("--duration", type=positive_float, default=10.0)
    parser.add_argument("--visual-particles", type=positive_int, default=3500)
    args = parser.parse_args()

    binary = project / "build" / "swarm_garden"
    if not binary.is_file():
        parser.error("build/swarm_garden does not exist; run the compile command first")

    results = project / "artemis_results.json"
    results.unlink(missing_ok=True)
    subprocess.run(
        [
            str(binary),
            "benchmark",
            str(args.particles),
            str(args.frames),
            str(results),
        ],
        cwd=project,
        check=True,
    )

    if args.visualize:
        subprocess.run(
            [
                sys.executable,
                str(project / "tools" / "window_renderer.py"),
                "--binary",
                str(binary),
                "--particles",
                str(args.visual_particles),
                "--duration",
                str(args.duration),
            ],
            cwd=project,
            check=True,
        )


if __name__ == "__main__":
    main()
