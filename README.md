# Particle Life (Discovery-ready lab)

Particle Life is a deterministic C++17 simulation with five interacting species in a toroidal world.

This branch is a **teaching seed**: compile, correctness tests, and a local visualization are present, but there is **no Discovery-ready benchmark harness**. Your job is to add one before importing the repository into Artemis.

The seed implementation intentionally checks every particle pair even though forces have a fixed interaction radius. This creates a clear optimization opportunity while the correctness test protects deterministic simulation behavior.

## What is missing

Artemis Discovery needs a root-level, headless benchmark that writes numeric metrics to `artemis_results.json` (or `.csv`). This branch does not provide that file or a wrapper that creates it.

`./build/particle_life benchmark` still times the simulation and prints `fps=` to stdout. That is a useful timed path, not an Artemis results channel.

## Requirements

- CMake 3.16 or newer
- A C++17 compiler
- Python 3 (for visualization now; also for the harness you will add)
- Python Tkinter and a graphical display to run the visualization

## Local build and test

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --parallel
ctest --test-dir build --output-on-failure
```

## Visualization

After a successful build, you can watch the simulation locally:

```bash
python3 tools/window_renderer.py
```

Optional flags: `--particles`, `--duration`, `--width`, `--height`. This path is for exploration only. Do **not** include the Tk window in the Artemis timed benchmark.

## Timed path (stdout only)

This times the simulation and prints `fps=` — it does **not** write `artemis_results.json`:

```bash
./build/particle_life benchmark 2200 30
```

## Author the Artemis harness

Add a headless script (typically `tools/benchmark.py`) that:

1. Requires `build/particle_life` (fail clearly if missing).
2. Removes any stale `artemis_results.json` / `.csv` at the repository root.
3. Runs a timed workload equivalent to 2,200 particles and 30 frames after warmup — wrapping `./build/particle_life benchmark 2200 30` is fine.
4. Parses the numeric `fps=` value from that stdout line.
5. Writes `{"simulation_fps": <float>}` to `artemis_results.json` at the repository root.
6. Stays headless — do not open `tools/window_renderer.py` during the measured path.

Verify from the repository root:

```bash
rm -f artemis_results.json artemis_results.csv
python3 tools/benchmark.py --no-visualize   # or the script path you chose
test -f artemis_results.json
```

Reference solution (one file added on the after branch):  
[compare `artemis/not-ready`…`artemis/ready`](https://github.com/turintech/particle-life/compare/artemis/not-ready...artemis/ready).

Full fork → harness → import → Discovery workflow: Artemis docs **Make a repository ready** (`particle-life-harness-example`).

## Success criteria for the lab

1. Add a headless harness that measures `simulation_fps`.
2. Write numeric `{"simulation_fps": ...}` to `artemis_results.json` at the repository root.
3. Verify compile → test → benchmark from the repository root.
4. Push the harness to your fork, import that fork into Artemis, and run a short Discovery.
