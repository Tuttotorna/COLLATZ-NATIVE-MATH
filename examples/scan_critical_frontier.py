from __future__ import annotations

import json
import runpy
from pathlib import Path

VERSION = "v1.2"

PREVIOUS_CRITICAL_N0 = 9780657630
PREVIOUS_CRITICAL_HARDNESS = 15.100955299032181
PREVIOUS_CRITICAL_DISTANCE = 114
PREVIOUS_CRITICAL_MIN_SURPLUS = 0.00275679752445801
COMPARISON_TOLERANCE = 1e-9

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "examples" / "scan_critical_frontier_v11_core.py"
RESULTS = ROOT / "results"
SCAN_PATH = RESULTS / "critical_frontier_scan.jsonl"
SUMMARY_PATH = RESULTS / "critical_frontier_summary.json"
CERTIFICATE_PATH = RESULTS / "frontier_stability_certificate.json"


def line():
    print("=" * 80)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_rows(path: Path):
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def get_hardness(row):
    if not isinstance(row, dict):
        return 0.0
    if "max_hardness_score" in row:
        return row["max_hardness_score"]
    if "hardness" in row:
        return row["hardness"]
    return 0.0


def get_distance(row):
    if not isinstance(row, dict):
        return 0
    if "max_post_chain_recovery_distance" in row:
        return row["max_post_chain_recovery_distance"]
    if "max_distance" in row:
        return row["max_distance"]
    return 0


def get_min_surplus(row):
    if not isinstance(row, dict):
        return None
    if "min_post_chain_recovery_surplus" in row:
        return row["min_post_chain_recovery_surplus"]
    if "min_surplus" in row:
        return row["min_surplus"]
    return None


def normalize_hardest(summary, rows):
    hardest = summary.get("current_hardest")

    if isinstance(hardest, dict):
        out = dict(hardest)
    else:
        nonzero = [row for row in rows if get_hardness(row) > 0]
        out = dict(max(nonzero or rows, key=get_hardness)) if rows else {}

    if "hardness" in out and "max_hardness_score" not in out:
        out["max_hardness_score"] = out["hardness"]

    if "max_distance" in out and "max_post_chain_recovery_distance" not in out:
        out["max_post_chain_recovery_distance"] = out["max_distance"]

    if "min_surplus" in out and "min_post_chain_recovery_surplus" not in out:
        out["min_post_chain_recovery_surplus"] = out["min_surplus"]

    return out


def main():
    line()
    print("COLLATZ-NATIVE-MATH v1.2")
    line()
    print("Critical frontier scan with stability certificate")
    print(f"previous critical n0: {PREVIOUS_CRITICAL_N0}")
    print(f"previous critical hardness: {PREVIOUS_CRITICAL_HARDNESS:.15f}")
    print(f"comparison tolerance: {COMPARISON_TOLERANCE}")
    line()

    if not CORE.exists():
        raise RuntimeError(f"Missing v1.1 core scanner: {CORE}")

    runpy.run_path(str(CORE), run_name="__main__")

    rows = load_rows(SCAN_PATH)
    summary = load_json(SUMMARY_PATH) if SUMMARY_PATH.exists() else {}

    hardest = normalize_hardest(summary, rows)

    current_n0 = hardest.get("n0")
    current_hardness = float(hardest.get("max_hardness_score", get_hardness(hardest)) or 0.0)
    current_distance = int(hardest.get("max_post_chain_recovery_distance", get_distance(hardest)) or 0)
    current_surplus = hardest.get("min_post_chain_recovery_surplus", get_min_surplus(hardest))

    same_case = current_n0 == PREVIOUS_CRITICAL_N0
    hardness_delta = current_hardness - PREVIOUS_CRITICAL_HARDNESS

    if same_case and abs(hardness_delta) <= COMPARISON_TOLERANCE:
        comparison_status = "SAME_AS_PREVIOUS"
    elif hardness_delta > COMPARISON_TOLERANCE:
        comparison_status = "HARDER_THAN_PREVIOUS"
    elif hardness_delta < -COMPARISON_TOLERANCE:
        comparison_status = "SOFTER_THAN_PREVIOUS"
    else:
        comparison_status = "NUMERIC_TIE_DIFFERENT_CASE"

    harder_than_previous = comparison_status == "HARDER_THAN_PREVIOUS"
    frontier_stable = same_case and comparison_status == "SAME_AS_PREVIOUS"

    summary["version"] = VERSION
    summary["previous_critical_n0"] = PREVIOUS_CRITICAL_N0
    summary["previous_critical_hardness"] = PREVIOUS_CRITICAL_HARDNESS
    summary["previous_critical_distance"] = PREVIOUS_CRITICAL_DISTANCE
    summary["previous_critical_min_surplus"] = PREVIOUS_CRITICAL_MIN_SURPLUS
    summary["comparison_tolerance"] = COMPARISON_TOLERANCE
    summary["current_hardest"] = hardest
    summary["comparison_status"] = comparison_status
    summary["same_case"] = same_case
    summary["harder_than_previous_critical"] = harder_than_previous
    summary["frontier_stable"] = frontier_stable
    summary["hardness_delta_vs_previous"] = hardness_delta

    certificate = {
        "version": VERSION,
        "certificate_type": "frontier_stability_certificate",
        "previous_critical_n0": PREVIOUS_CRITICAL_N0,
        "previous_critical_hardness": PREVIOUS_CRITICAL_HARDNESS,
        "previous_critical_distance": PREVIOUS_CRITICAL_DISTANCE,
        "previous_critical_min_surplus": PREVIOUS_CRITICAL_MIN_SURPLUS,
        "current_hardest_n0": current_n0,
        "current_hardest_hardness": current_hardness,
        "current_hardest_distance": current_distance,
        "current_hardest_min_surplus": current_surplus,
        "comparison_tolerance": COMPARISON_TOLERANCE,
        "comparison_status": comparison_status,
        "same_case": same_case,
        "harder_than_previous_critical": harder_than_previous,
        "frontier_stable": frontier_stable,
        "hardness_delta_vs_previous": hardness_delta,
        "meaning": (
            "Within this finite candidate frontier, the known critical case "
            "remains the active hardest case under exact baseline comparison."
        ),
        "limits": (
            "This is a finite computational certificate over the selected "
            "candidate frontier. It is not a proof of the Collatz conjecture."
        ),
    }

    write_json(SUMMARY_PATH, summary)
    write_json(CERTIFICATE_PATH, certificate)

    line()
    print("Frontier stability certificate")
    line()
    print(
        "current hardest: "
        f"n0={current_n0} "
        f"hardness={current_hardness:.15f} "
        f"distance={current_distance} "
        f"min_surplus={current_surplus}"
    )
    print(f"comparison status: {comparison_status}")
    print(f"same case: {str(same_case).lower()}")
    print(f"harder than previous critical: {str(harder_than_previous).lower()}")
    print(f"frontier stable: {str(frontier_stable).lower()}")
    print(f"Wrote updated summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CERTIFICATE_PATH.relative_to(ROOT)}")
    line()


if __name__ == "__main__":
    main()
