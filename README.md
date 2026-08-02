# Swarm Garden (runner command-iteration lab)

Swarm Garden is a deterministic C++17 particle-life simulation with five interacting species in a toroidal world.

This branch is a **teaching seed** for verifying compile, test, and benchmark commands on an Artemis runner when local verification is not the gate. Compile and correctness tests are present. A harness exists, but it is **not** Discovery-ready yet.

## What is wrong on purpose

1. Candidate command recipes below include incomplete or incorrect strings so you practice iterating `--command` values with `changeset validate`.
2. `tools/benchmark.py` measures `simulation_fps` but writes `artemis_results.json` under `tools/` instead of the repository root. Artemis only accepts the results file in the command working directory (the repo root).

`./build/swarm_garden benchmark` still prints `fps=` to stdout. That is useful diagnostics, not the Artemis results channel.

## Requirements

- CMake 3.16 or newer
- A C++17 compiler
- Python 3

## Candidate commands to try on the runner

These are starting points for Level 1 command iteration — not verified Discovery commands.

Wrong or incomplete:

```bash
make -j$(nproc)
ctest
./build/swarm_garden benchmark 2200 30
```

Closer (compile and test should work; the harness still writes metrics in the wrong place):

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --parallel
ctest --test-dir build --output-on-failure
python3 tools/benchmark.py --no-visualize
```

## Success criteria for the lab

1. Import this branch (or your fork of it) and verify commands with `changeset validate` on your runner — do not treat local success as proof.
2. Iterate command strings until compile and test pass; use `artemis process logs` to see why the benchmark is not Discovery-ready.
3. Fix `tools/benchmark.py` so it writes numeric `{"simulation_fps": ...}` to `artemis_results.json` at the repository root.
4. Push the fix, `artemis project pull` the project to the new commit, create a **new** empty changeset, and re-validate.
5. Run a short Discovery with the verified commands.

Follow the Artemis documentation example **Verifying Particle Life commands on a runner** for the full fork → import → validate → fix → pull → Discovery workflow.
