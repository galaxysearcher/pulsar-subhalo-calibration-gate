"""
Release-gate decision logic for calibrated uncertainty outputs.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


DEFAULT_THRESHOLDS = {
    "min_samples": 200,
    "mean_u_min": 0.45,
    "mean_u_max": 0.55,
    "ks_d_max": 0.20,
    "worst_abs_z_max": 3.00,
    "coverage_2sigma_min": 0.90,
    "coverage_3sigma_min": 0.99,
}


@dataclass
class GateDecision:
    """Structured release-gate decision."""
    status: str
    release_id: str
    reasons: List[str]
    thresholds: Dict[str, float]
    metrics: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _check_axis(axis: str, block: Dict[str, Any], thresholds: Dict[str, float]) -> List[str]:
    reasons: List[str] = []

    n = int(block.get("n", 0))
    mean_u = block.get("mean_u")
    ks_d = block.get("ks_d")

    if n < thresholds["min_samples"]:
        reasons.append(f"{axis}: n={n} below {thresholds['min_samples']}")

    if mean_u is None:
        reasons.append(f"{axis}: mean_u missing")
    else:
        mean_u = float(mean_u)
        if mean_u < thresholds["mean_u_min"] or mean_u > thresholds["mean_u_max"]:
            reasons.append(
                f"{axis}: mean_u={mean_u:.3f} outside "
                f"[{thresholds['mean_u_min']:.2f}, {thresholds['mean_u_max']:.2f}]"
            )

    if ks_d is None:
        reasons.append(f"{axis}: ks_d missing")
    else:
        ks_d = float(ks_d)
        if ks_d > thresholds["ks_d_max"]:
            reasons.append(f"{axis}: ks_d={ks_d:.3f} above {thresholds['ks_d_max']:.3f}")

    return reasons


def evaluate_release(payload: Dict[str, Any], thresholds: Dict[str, float] | None = None) -> GateDecision:
    """Evaluate a release metrics payload against calibration thresholds."""
    active_thresholds = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        active_thresholds.update(thresholds)

    axes = payload.get("axes", {})
    release_id = payload.get("release_id", "unlabeled_release")
    reasons: List[str] = []

    for axis in ["z_log10M", "z_x", "z_y", "z_z"]:
        block = axes.get(axis)
        if not isinstance(block, dict):
            reasons.append(f"{axis}: metrics missing")
            continue
        reasons.extend(_check_axis(axis, block, active_thresholds))

    z_z = axes.get("z_z", {}) if isinstance(axes.get("z_z"), dict) else {}

    worst = z_z.get("worst_abs_z")
    if worst is None:
        reasons.append("z_z: worst_abs_z missing")
    elif float(worst) > active_thresholds["worst_abs_z_max"]:
        reasons.append(f"z_z: worst_abs_z={float(worst):.3f} above {active_thresholds['worst_abs_z_max']:.2f}")

    cov2 = z_z.get("coverage_2sigma")
    if cov2 is None:
        reasons.append("z_z: coverage_2sigma missing")
    elif float(cov2) < active_thresholds["coverage_2sigma_min"]:
        reasons.append(f"z_z: coverage_2sigma={float(cov2):.3f} below {active_thresholds['coverage_2sigma_min']:.2f}")

    cov3 = z_z.get("coverage_3sigma")
    if cov3 is None:
        reasons.append("z_z: coverage_3sigma missing")
    elif float(cov3) < active_thresholds["coverage_3sigma_min"]:
        reasons.append(f"z_z: coverage_3sigma={float(cov3):.3f} below {active_thresholds['coverage_3sigma_min']:.2f}")

    status = "PASS" if not reasons else "FAIL"
    return GateDecision(
        status=status,
        release_id=release_id,
        reasons=reasons,
        thresholds=active_thresholds,
        metrics=payload,
    )
