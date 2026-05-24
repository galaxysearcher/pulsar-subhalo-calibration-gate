# Methodology

## Objective

This workflow evaluates calibration quality for a pulsar subhalo inference run. The central question is whether estimated uncertainty is consistent with observed normalized residuals across the target axes.

## Target axes

```text
z_log10M, z_x, z_y, z_z
```

The axes correspond to normalized residuals for the inferred compact mass scale and 3D position components.

## Calibration statistics

### PIT mean

The PIT-style statistic maps absolute normalized residuals into the unit interval. A calibrated Gaussian residual distribution should produce values centered near 0.5.

### KS distance

The Kolmogorov-Smirnov distance measures the largest deviation between the empirical PIT distribution and a uniform target. Lower distance indicates closer agreement with the calibration target.

### Coverage

Coverage checks whether residuals fall inside expected sigma bands. The current gate uses 2-sigma and 3-sigma thresholds for the z-axis because that dimension drove the release decision in this iteration.

### Worst normalized residual

The gate also bounds the largest absolute residual. This prevents a run from passing solely because aggregate statistics look acceptable.

## Release decision

A release passes when each configured metric satisfies its threshold. The gate returns a structured JSON decision with status, thresholds, metrics, and reasons for any failed check.
