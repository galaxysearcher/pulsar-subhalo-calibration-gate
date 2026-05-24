import json
from pathlib import Path

from pulsar_subhalo_calibration import evaluate_release
from pulsar_subhalo_calibration.metrics import coverage_at, ks_distance_uniform, pit_from_abs_z


def test_release_example_passes():
    payload = json.loads(Path("examples/release_20251112_metrics.json").read_text(encoding="utf-8"))
    decision = evaluate_release(payload)
    assert decision.status == "PASS"
    assert decision.reasons == []


def test_gate_fails_on_ks_distance():
    payload = json.loads(Path("examples/release_20251112_metrics.json").read_text(encoding="utf-8"))
    payload["axes"]["z_z"]["ks_d"] = 0.25
    decision = evaluate_release(payload)
    assert decision.status == "FAIL"
    assert any("ks_d" in reason for reason in decision.reasons)


def test_metric_helpers():
    assert 0.0 <= pit_from_abs_z(1.0) <= 1.0
    assert ks_distance_uniform([0.1, 0.3, 0.5, 0.7, 0.9]) >= 0.0
    assert coverage_at([0.5, 1.5, 2.5], 2.0) == 2 / 3
