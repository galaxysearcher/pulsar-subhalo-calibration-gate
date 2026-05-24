"""
Statistical helpers for uncertainty calibration checks.
"""
from __future__ import annotations

from math import erf, sqrt
from typing import Iterable, Sequence


def pit_from_abs_z(abs_z: float) -> float:
    """Map an absolute normalized residual to a two-sided PIT-like value."""
    return erf(abs(float(abs_z)) / sqrt(2.0))


def ks_distance_uniform(values: Sequence[float]) -> float:
    """Compute one-sample Kolmogorov-Smirnov distance against U(0, 1)."""
    if not values:
        return float("nan")

    ordered = sorted(float(v) for v in values)
    n = len(ordered)
    d_plus = max((i + 1) / n - ordered[i] for i in range(n))
    d_minus = max(ordered[i] - i / n for i in range(n))
    return max(d_plus, d_minus)


def coverage_at(abs_z_values: Iterable[float], sigma: float) -> float:
    """Return the share of absolute normalized residuals inside a sigma band."""
    vals = [abs(float(v)) for v in abs_z_values]
    if not vals:
        return float("nan")
    return sum(v <= sigma for v in vals) / len(vals)
