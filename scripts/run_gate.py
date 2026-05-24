from __future__ import annotations

import json
import sys
from pathlib import Path

from pulsar_subhalo_calibration import evaluate_release


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/run_gate.py examples/release_20251112_metrics.json")
        return 2

    in_path = Path(sys.argv[1])
    payload = json.loads(in_path.read_text(encoding="utf-8"))
    decision = evaluate_release(payload)

    Path("results").mkdir(exist_ok=True)
    out_path = Path("results") / f"gate_decision_{payload.get('release_id', 'release')}.json"
    out_path.write_text(json.dumps(decision.to_dict(), indent=2), encoding="utf-8")

    print(decision.status)
    print(out_path.as_posix())
    if decision.reasons:
        for reason in decision.reasons:
            print(reason)

    return 0 if decision.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
