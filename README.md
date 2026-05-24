# Pulsar Subhalo Calibration Gate

Calibration and release-gate workflow for a pulsar subhalo inference pipeline.

This repository evaluates whether normalized residuals and uncertainty estimates satisfy explicit reliability thresholds before a model run is accepted as a release candidate.

## What the gate checks

The gate evaluates four target axes:

```text
z_log10M, z_x, z_y, z_z
```

For each axis, the workflow can check:

- sample count
- PIT mean
- Kolmogorov-Smirnov distance against a uniform PIT target
- worst absolute normalized residual
- coverage inside 2-sigma and 3-sigma intervals

## Included example

The included example file contains a compact release summary with 4,000 samples per axis and a post-hoc z-axis transform:

```text
tau = 0.660
intercept = -0.030
```

Run the gate:

```bash
python scripts/run_gate.py examples/release_20251112_metrics.json
```

Expected result:

```text
PASS
```

## Run tests

```bash
python -m pytest
```

## Repository structure

```text
src/pulsar_subhalo_calibration/
  gate.py       # threshold checks and decision logic
  metrics.py    # PIT, KS distance, and coverage helpers

scripts/
  run_gate.py   # command-line gate runner

examples/
  release_20251112_metrics.json

docs/
  methodology.md
  release_gate.md

results/
  gate_decision_20251112.json
```

## Technical purpose

The calibration gate converts uncertainty diagnostics into a reproducible decision. A model run passes only when its residual distributions, coverage, and worst-case normalized errors satisfy the configured thresholds.
