# Release Gate

## Thresholds

| Metric | Threshold |
|---|---:|
| Minimum samples per axis | 200 |
| PIT mean lower bound | 0.45 |
| PIT mean upper bound | 0.55 |
| KS distance maximum | 0.20 |
| Worst absolute z maximum | 3.00 |
| Coverage at 2 sigma minimum | 0.90 |
| Coverage at 3 sigma minimum | 0.99 |

## Included release summary

The included release summary has 4,000 samples per axis. The z-axis branch uses:

| Parameter | Value |
|---|---:|
| tau | 0.660 |
| intercept | -0.030 |

## Gate result

The included release summary passes the configured gate.

| Axis | n | PIT mean | KS distance |
|---|---:|---:|---:|
| z_log10M | 4000 | 0.495 | 0.150 |
| z_x | 4000 | 0.505 | 0.150 |
| z_y | 4000 | 0.495 | 0.100 |
| z_z | 4000 | 0.500 | 0.194 |

Additional z-axis checks:

| Metric | Value |
|---|---:|
| Coverage at 2 sigma | 1.000 |
| Coverage at 3 sigma | 1.000 |
| Worst absolute z | 1.306 |
