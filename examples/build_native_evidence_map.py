from __future__ import annotations

import json
from pathlib import Path

VERSION = "v1.9"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

FRONTIER_CERTIFICATE = RESULTS / "frontier_stability_certificate.json"
COMPENSATION_CERTIFICATE = RESULTS / "compensation_law_candidate_certificate.json"
ADVERSARIAL_CERTIFICATE = RESULTS / "adversarial_compensation_certificate.json"
HARDNESS_REPORT = RESULTS / "hardness_metric_report.json"

OUTPUT_JSON = RESULTS / "native_evidence_map.json"
OUTPUT_MD = RESULTS / "native_evidence_map.md"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {
            "missing": True,
            "path": str(path.relative_to(ROOT)),
        }
    return json.loads(path.read_text(encoding="utf-8"))


def as_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return bool(value)


def get_nested(data, *keys, default=None):
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    return default if current is None else current


def build_frontier_mapping(data: dict) -> dict:
    current_n0 = data.get("current_hardest_n0")
    if current_n0 is None:
        current_n0 = get_nested(data, "current_hardest", "n0")

    distance = data.get("current_hardest_distance")
    if distance is None:
        distance = get_nested(data, "current_hardest", "max_post_chain_recovery_distance")

    surplus = data.get("current_hardest_min_surplus")
    if surplus is None:
        surplus = get_nested(data, "current_hardest", "min_post_chain_recovery_surplus")

    frontier_stable = as_bool(data.get("frontier_stable"), False)

    return {
        "evidence_id": "frontier_stability_certificate",
        "source": "results/frontier_stability_certificate.json",
        "native_role": "frontier_anchor",
        "native_objects": {
            "debt": "detected_as_hard_frontier_recovery_structure",
            "shadow": "represented_by_post_chain_recovery_distance",
            "compensation": "detected_by_recovery_after_chain",
            "regeneration": "not_primary_in_this_artifact",
            "closure": "frontier_remained_stable_under_selected_scan" if frontier_stable else "frontier_not_stable_under_selected_scan",
            "obstruction": "not_detected",
        },
        "key_case": {
            "n0": current_n0,
            "post_chain_recovery_distance": distance,
            "minimum_surplus": surplus,
        },
        "closure_status": "EVIDENCE_FOR_LOCAL_CLOSURE_NOT_FULL_NATIVE_CLOSURE",
        "obstruction_status": "NO_OBSTRUCTION_DETECTED_IN_SELECTED_FRONTIER",
        "proof_status": "finite_evidence_not_proof",
        "limits": "This artifact stabilizes a selected frontier case. It does not establish global native closure.",
    }


def build_compensation_mapping(data: dict) -> dict:
    hardest = data.get("hardest_case") or {}
    all_recovered = as_bool(data.get("all_bad_windows_recovered"), False)
    unrecovered = data.get("total_unrecovered_bad_windows")

    return {
        "evidence_id": "compensation_law_candidate_certificate",
        "source": "results/compensation_law_candidate_certificate.json",
        "native_role": "compensation_recovery_evidence",
        "native_objects": {
            "debt": "bad_windows_detected",
            "shadow": "implicit_in_recovery_after_bad_windows",
            "compensation": "all_detected_bad_windows_recovered" if all_recovered else "some_bad_windows_unrecovered",
            "regeneration": "not_exhaustively_tested_by_this_artifact",
            "closure": "local_recovery_evidence_only",
            "obstruction": "not_detected" if all_recovered else "candidate_unrecovered_bad_window_detected",
        },
        "key_case": {
            "n0": hardest.get("n0"),
            "max_hardness_score": hardest.get("max_hardness_score"),
            "min_combined_surplus": hardest.get("min_combined_surplus"),
            "max_post_recovery_blocks": hardest.get("max_post_recovery_blocks"),
        },
        "closure_status": "LOCALLY_RECOVERED_NOT_FULLY_CLOSED",
        "obstruction_status": "NO_UNRECOVERED_BAD_WINDOW" if all_recovered else "UNRECOVERED_BAD_WINDOW_PRESENT",
        "unrecovered_bad_windows": unrecovered,
        "proof_status": "finite_evidence_not_proof",
        "limits": "This artifact supports compensation behavior over selected candidates, but does not prove forced compensation for all admissible debt structures.",
    }


def build_adversarial_mapping(data: dict) -> dict:
    all_recovered = as_bool(data.get("all_bad_windows_recovered"), False)
    counterexamples = int(data.get("counterexample_candidate_count") or 0)

    hardest_n0 = data.get("hardest_case_n0")
    hardest_score = data.get("hardest_case_score")
    tightest_n0 = data.get("tightest_surplus_n0")
    tightest_surplus = data.get("tightest_surplus")

    return {
        "evidence_id": "adversarial_compensation_certificate",
        "source": "results/adversarial_compensation_certificate.json",
        "native_role": "adversarial_obstruction_search",
        "native_objects": {
            "debt": "adversarial_bad_windows_detected",
            "shadow": "tested_through_extended_recovery_windows",
            "compensation": "all_adversarial_bad_windows_recovered" if all_recovered else "unrecovered_adversarial_windows_present",
            "regeneration": "stress_tested_by_adversarial_candidate_generation",
            "closure": "evidence_against_selected_obstruction_candidates",
            "obstruction": "not_detected" if counterexamples == 0 else "counterexample_candidates_detected",
        },
        "key_case": {
            "hardest_n0": hardest_n0,
            "hardest_score": hardest_score,
            "tightest_surplus_n0": tightest_n0,
            "tightest_surplus": tightest_surplus,
        },
        "closure_status": "REGENERATED_BUT_COMPENSATED",
        "obstruction_status": "NO_COUNTEREXAMPLE_CANDIDATE_DETECTED" if counterexamples == 0 else "COUNTEREXAMPLE_CANDIDATE_DETECTED",
        "counterexample_candidate_count": counterexamples,
        "proof_status": "finite_evidence_not_proof",
        "limits": "This artifact is the strongest current finite adversarial evidence, but remains bounded and computational.",
    }


def build_hardness_mapping(data: dict) -> dict:
    metrics = data.get("metrics") or []
    unique_values = data.get("unique_hardest_n0_values") or []

    return {
        "evidence_id": "hardness_metric_report",
        "source": "results/hardness_metric_report.json",
        "native_role": "hardness_is_stress_not_obstruction",
        "native_objects": {
            "debt": "stress_measured_across_multiple_metrics",
            "shadow": "metric_dependent",
            "compensation": "metric_dependent",
            "regeneration": "metric_dependent",
            "closure": "not_decided_by_hardness_alone",
            "obstruction": "not_equivalent_to_hardness",
        },
        "key_cases": unique_values,
        "metric_count": len(metrics),
        "closure_status": "UNDECIDED_BY_HARDNESS_ALONE",
        "obstruction_status": "HARDNESS_DOES_NOT_IMPLY_OBSTRUCTION",
        "proof_status": "classification_not_proof",
        "limits": "This artifact prevents the incorrect inference that the hardest case under one metric is automatically a native obstruction.",
    }


def build_map() -> dict:
    frontier = load_json(FRONTIER_CERTIFICATE)
    compensation = load_json(COMPENSATION_CERTIFICATE)
    adversarial = load_json(ADVERSARIAL_CERTIFICATE)
    hardness = load_json(HARDNESS_REPORT)

    evidence_maps = [
        build_frontier_mapping(frontier),
        build_compensation_mapping(compensation),
        build_adversarial_mapping(adversarial),
        build_hardness_mapping(hardness),
    ]

    obstruction_detected = any(
        item["obstruction_status"] in {
            "UNRECOVERED_BAD_WINDOW_PRESENT",
            "COUNTEREXAMPLE_CANDIDATE_DETECTED",
        }
        for item in evidence_maps
    )

    map_data = {
        "version": VERSION,
        "layer": "native_evidence_mapping",
        "status": "existing_evidence_mapped_into_native_objects",
        "primary_claim": "Existing computational artifacts are evidence layers that can be mapped to native objects, but they are not proof.",
        "standard_translation_status": "deferred",
        "proof_status": "not_a_proof",
        "native_objects": [
            "debt",
            "shadow",
            "compensation",
            "regeneration",
            "closure",
            "obstruction",
        ],
        "closure_result_types_used": [
            "EVIDENCE_FOR_LOCAL_CLOSURE_NOT_FULL_NATIVE_CLOSURE",
            "LOCALLY_RECOVERED_NOT_FULLY_CLOSED",
            "REGENERATED_BUT_COMPENSATED",
            "UNDECIDED_BY_HARDNESS_ALONE",
        ],
        "obstruction_detected": obstruction_detected,
        "evidence_count": len(evidence_maps),
        "evidence_maps": evidence_maps,
        "next_recommended_version": "v2.0 Native-to-Standard Translation Boundary",
    }

    return map_data


def write_markdown(data: dict) -> str:
    lines = []
    lines.append("# Native Evidence Map")
    lines.append("")
    lines.append("Version: v1.9")
    lines.append("")
    lines.append("This report maps existing computational artifacts into native objects.")
    lines.append("")
    lines.append("It does not add a bigger scan.")
    lines.append("")
    lines.append("It does not prove the Collatz conjecture.")
    lines.append("")
    lines.append("It prevents the previous mistake: returning to standard mathematics before the native structure is complete.")
    lines.append("")
    lines.append("## Native objects")
    lines.append("")
    for obj in data["native_objects"]:
        lines.append(f"- {obj}")
    lines.append("")
    lines.append("## Evidence mappings")
    lines.append("")

    for item in data["evidence_maps"]:
        lines.append(f"### {item['evidence_id']}")
        lines.append("")
        lines.append(f"Source: {item['source']}")
        lines.append("")
        lines.append(f"Native role: {item['native_role']}")
        lines.append("")
        lines.append(f"Closure status: {item['closure_status']}")
        lines.append("")
        lines.append(f"Obstruction status: {item['obstruction_status']}")
        lines.append("")
        lines.append("Native object mapping:")
        lines.append("")
        for key, value in item["native_objects"].items():
            lines.append(f"- {key}: {value}")
        lines.append("")
        lines.append(f"Proof status: {item['proof_status']}")
        lines.append("")
        lines.append(f"Limits: {item['limits']}")
        lines.append("")

    lines.append("## Conclusion")
    lines.append("")
    lines.append("The existing artifacts support the native research path, but only as finite evidence.")
    lines.append("")
    lines.append("The next correct step is not another larger scan by default.")
    lines.append("")
    lines.append("The next correct step is the native-to-standard translation boundary, after the native objects have been mapped.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v1.9")
    print("=" * 80)
    print("Native evidence mapping")
    print("=" * 80)

    data = build_map()

    OUTPUT_JSON.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(write_markdown(data), encoding="utf-8")

    print(f"evidence count: {data['evidence_count']}")
    print(f"obstruction detected: {str(data['obstruction_detected']).lower()}")
    print(f"proof status: {data['proof_status']}")
    print(f"next: {data['next_recommended_version']}")

    for item in data["evidence_maps"]:
        print(
            f"{item['evidence_id']}: "
            f"closure={item['closure_status']} "
            f"obstruction={item['obstruction_status']}"
        )

    print(f"Wrote JSON map to: {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Wrote Markdown map to: {OUTPUT_MD.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
