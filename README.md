# Swarm Garden

Swarm Garden is a deterministic C++17 particle-life simulation with five interacting species in a toroidal world.

The seed implementation intentionally checks every particle pair even though forces have a fixed interaction radius. This creates a clear optimization opportunity while the correctness test protects deterministic simulation behavior.

## Requirements

- CMake 3.16 or newer
- A C++17 compiler
- Python 3 for the benchmark wrapper
- Python Tkinter and a graphical display only when using `--visualize`

## Artemis commands

Compile:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --parallel
```

Test:

```bash
ctest --test-dir build --output-on-failure
```

Benchmark:

```bash
python3 tools/benchmark.py
```

The benchmark measures 30 simulation frames with 2,200 particles after five warmup frames and writes `simulation_fps` to `artemis_results.json`.

## Optional visualization

Add `--visualize` to run a separate visual pass after the measured benchmark has finished:

```bash
python3 tools/benchmark.py --visualize
```

The window displays 3,500 particles for 10 seconds by default. Change the duration and visual workload without changing the measured workload:

```bash
python3 tools/benchmark.py --visualize --duration 20 --visual-particles 4000
```

The visualization is never part of the timed benchmark section and is unsuitable for a headless Artemis runner. The default benchmark command remains headless.
