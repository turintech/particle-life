# Particle Life (Discovery-ready lab)

Particle Life is a deterministic C++17 simulation with five interacting species in a toroidal world.

This branch is a **teaching seed**: compile and correctness tests are present, but there is **no Discovery-ready benchmark harness**. Your job is to add one before importing the repository into Artemis.

The seed implementation intentionally checks every particle pair even though forces have a fixed interaction radius. This creates a clear optimization opportunity while the correctness test protects deterministic simulation behavior.

## What is missing

Artemis Discovery needs a root-level, headless benchmark that writes numeric metrics to `artemis_results.json` (or `.csv`). This branch does not provide that file or a wrapper that creates it.

`./build/particle_life benchmark` still times the simulation and prints `fps=` to stdout. That is a useful timed path, not an Artemis results channel.

## Requirements

- CMake 3.16 or newer
- A C++17 compiler
- Python 3 (once you add a harness script)

## Local build and test

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --parallel
ctest --test-dir build --output-on-failure
```

Optional timed path (stdout only — not Discovery-ready):

```bash
./build/particle_life benchmark 2200 30
```

## Success criteria for the lab

1. Add a headless harness (typically under `tools/`) that measures `simulation_fps`.
2. Write numeric `{"simulation_fps": ...}` to `artemis_results.json` at the repository root.
3. Verify compile → test → benchmark from the repository root.
4. Push the harness to your fork, import that fork into Artemis, and run a short Discovery.

Follow the Artemis documentation example **Making Particle Life Discovery-ready** for the full fork → harness → import → Discovery workflow.
