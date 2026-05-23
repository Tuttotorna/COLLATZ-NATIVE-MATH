#!/usr/bin/env python3
"""
Mature Rebound Guard V0.

This bounded audit corrects raw fuzzy rebound classification by separating
weak-prefix rebound from mature-debt rebound.

It does not prove Collatz.
It does not claim Collatz is solved.
It is measurement only.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

INPUT_PATH = RESULTS / "fuzzy_rebound_anatomy_v0.json"
MATURE_PRIOR_PEAK_THRESHOLD = 4.0
SECOND_NEAR_BREACH_THRESHOLD = 0.95


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def classify_guarded_rebound(instance: dict) -> str:
    prior_peak = instance.get("prior_debt_peak")
    ratio = instance.get("post_max_to_prior_peak_ratio")
    raw_class = instance.get("rebound_class")

    if prior_peak is None or ratio is None:
        return "unclassified"

    if prior_peak < MATURE_PRIOR_PEAK_THRESHOLD:
        if raw_class == "breach_after_fuzzy_pattern":
            return "weak_prefix_false_breach"
        return "weak_prefix_rebound"

    if ratio > 1.0:
        return "mature_breach_after_fuzzy_pattern"

    if ratio >= SECOND_NEAR_BREACH_THRESHOLD:
        return "mature_second_near_breach_candidate"

    return "mature_harmless_rebound"


def enrich_instance(instance: dict) -> dict:
    enriched = dict(instance)

    prior_peak = enriched.get("prior_debt_peak")
    ratio = enriched.get("post_max_to_prior_peak_ratio")
    post_max = enriched.get("post_horizon_max_prefix")
    post_gain = enriched.get("post_pattern_debt_gain")

    mature_prior_peak = (
        prior_peak is not None
        and prior_peak >= MATURE_PRIOR_PEAK_THRESHOLD
    )

    guarded_class = classify_guarded_rebound(enriched)

    enriched["mature_prior_peak_threshold"] = MATURE_PRIOR_PEAK_THRESHOLD
    enriched["mature_prior_peak"] = mature_prior_peak
    enriched["guarded_rebound_class"] = guarded_class
    enriched["raw_rebound_class"] = enriched.get("rebound_class")
    enriched["raw_breach_after_fuzzy_pattern"] = enriched.get("breach_after_fuzzy_pattern")
    enriched["guarded_breach_after_fuzzy_pattern"] = guarded_class == "mature_breach_after_fuzzy_pattern"
    enriched["guarded_second_near_breach_candidate"] = guarded_class == "mature_second_near_breach_candidate"
    enriched["weak_prefix_artifact"] = guarded_class in {
        "weak_prefix_false_breach",
        "weak_prefix_rebound",
    }

    if prior_peak is not None:
        enriched["prior_peak_deficit_to_maturity"] = max(
            0.0,
            MATURE_PRIOR_PEAK_THRESHOLD - prior_peak,
        )
    else:
        enriched["prior_peak_deficit_to_maturity"] = None

    if post_max is not None:
        enriched["post_max_minus_maturity_threshold"] = post_max - MATURE_PRIOR_PEAK_THRESHOLD
    else:
        enriched["post_max_minus_maturity_threshold"] = None

    if post_gain is not None and prior_peak is not None:
        enriched["gain_relative_to_maturity_gap"] = (
            post_gain / max(MATURE_PRIOR_PEAK_THRESHOLD - prior_peak, 1e-12)
            if prior_peak < MATURE_PRIOR_PEAK_THRESHOLD
            else None
        )
    else:
        enriched["gain_relative_to_maturity_gap"] = None

    return enriched


def count_by(items: list[dict], key: str) -> dict:
    counts = {}

    for item in items:
        value = str(item.get(key))
        counts[value] = counts.get(value, 0) + 1

    return dict(sorted(counts.items(), key=lambda kv: kv[0]))


def build() -> dict:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input artifact: {INPUT_PATH}. "
            "Run examples/build_fuzzy_rebound_anatomy_v0.py first."
        )

    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))

    rebound_instances = source.get("rebound_instances", [])
    enriched_instances = [enrich_instance(x) for x in rebound_instances]

    weak_prefix_instances = [
        x for x in enriched_instances
        if x["guarded_rebound_class"] in {
            "weak_prefix_false_breach",
            "weak_prefix_rebound",
        }
    ]

    weak_prefix_false_breaches = [
        x for x in enriched_instances
        if x["guarded_rebound_class"] == "weak_prefix_false_breach"
    ]

    mature_instances = [
        x for x in enriched_instances
        if x["mature_prior_peak"]
    ]

    mature_breach_instances = [
        x for x in enriched_instances
        if x["guarded_rebound_class"] == "mature_breach_after_fuzzy_pattern"
    ]

    mature_second_near_breach_instances = [
        x for x in enriched_instances
        if x["guarded_rebound_class"] == "mature_second_near_breach_candidate"
    ]

    mature_harmless_instances = [
        x for x in enriched_instances
        if x["guarded_rebound_class"] == "mature_harmless_rebound"
    ]

    raw_breach_instances = [
        x for x in enriched_instances
        if x.get("raw_rebound_class") == "breach_after_fuzzy_pattern"
    ]

    ratios = [
        x["post_max_to_prior_peak_ratio"]
        for x in enriched_instances
        if x.get("post_max_to_prior_peak_ratio") is not None
    ]

    mature_ratios = [
        x["post_max_to_prior_peak_ratio"]
        for x in mature_instances
        if x.get("post_max_to_prior_peak_ratio") is not None
    ]

    prior_peaks = [
        x["prior_debt_peak"]
        for x in enriched_instances
        if x.get("prior_debt_peak") is not None
    ]

    weak_prior_peaks = [
        x["prior_debt_peak"]
        for x in weak_prefix_instances
        if x.get("prior_debt_peak") is not None
    ]

    post_gains = [
        x["post_pattern_debt_gain"]
        for x in enriched_instances
        if x.get("post_pattern_debt_gain") is not None
    ]

    summary = {
        "source_version": source.get("version"),
        "source_machine": source.get("machine"),
        "rebound_instance_count": len(enriched_instances),
        "raw_breach_after_fuzzy_pattern_count": len(raw_breach_instances),
        "weak_prefix_rebound_count": len(weak_prefix_instances),
        "weak_prefix_false_breach_count": len(weak_prefix_false_breaches),
        "mature_rebound_count": len(mature_instances),
        "mature_breach_count": len(mature_breach_instances),
        "mature_second_near_breach_count": len(mature_second_near_breach_instances),
        "mature_harmless_rebound_count": len(mature_harmless_instances),
        "guarded_class_counts": count_by(enriched_instances, "guarded_rebound_class"),
        "raw_class_counts": count_by(enriched_instances, "raw_rebound_class"),
        "mature_prior_peak_threshold": MATURE_PRIOR_PEAK_THRESHOLD,
        "second_near_breach_threshold": SECOND_NEAR_BREACH_THRESHOLD,
        "max_raw_ratio": max(ratios) if ratios else None,
        "max_mature_ratio": max(mature_ratios) if mature_ratios else None,
        "mean_prior_peak": safe_mean(prior_peaks),
        "min_prior_peak": min(prior_peaks) if prior_peaks else None,
        "max_prior_peak": max(prior_peaks) if prior_peaks else None,
        "mean_weak_prior_peak": safe_mean(weak_prior_peaks),
        "max_weak_prior_peak": max(weak_prior_peaks) if weak_prior_peaks else None,
        "mean_post_pattern_debt_gain": safe_mean(post_gains),
        "max_post_pattern_debt_gain": max(post_gains) if post_gains else None,
        "raw_breach_reclassified_as_weak_prefix_false_breach": len(weak_prefix_false_breaches),
    }

    if mature_breach_instances:
        bounded_assessment = "mature_breach_after_fuzzy_pattern_detected"
    elif mature_second_near_breach_instances:
        bounded_assessment = "mature_second_near_breach_rebound_detected"
    elif weak_prefix_false_breaches and not mature_instances:
        bounded_assessment = "raw_breaches_reclassified_as_weak_prefix_artifacts"
    elif weak_prefix_false_breaches:
        bounded_assessment = "raw_breaches_guarded_no_mature_breach_detected"
    elif mature_harmless_instances:
        bounded_assessment = "mature_rebounds_harmless_under_guard"
    else:
        bounded_assessment = "no_guarded_mature_rebound_detected"

    return {
        "version": "v6.4",
        "machine": "Mature Rebound Guard V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "input_path": (
                str(INPUT_PATH.relative_to(ROOT))
                if INPUT_PATH.is_relative_to(ROOT)
                else str(INPUT_PATH)
            ),
            "mature_prior_peak_threshold": MATURE_PRIOR_PEAK_THRESHOLD,
            "second_near_breach_threshold": SECOND_NEAR_BREACH_THRESHOLD,
        },
        "summary": summary,
        "guarded_rebound_instances": enriched_instances,
        "weak_prefix_false_breach_instances": weak_prefix_false_breaches,
        "mature_rebound_instances": mature_instances,
        "mature_breach_instances": mature_breach_instances,
        "mature_second_near_breach_instances": mature_second_near_breach_instances,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "Raw fuzzy rebound breaches are guarded by requiring a mature prior debt peak.",
            "primary_guard": "prior_debt_peak >= mature_prior_peak_threshold",
            "native_result": "A rebound over a weak prefix is not equivalent to a mature near-breach rebound.",
        },
        "boundary": {
            "proof_status": "not_a_proof",
            "collatz_status": "not_claimed_solved",
            "theorem_status": "no_theorem_claimed",
            "global_closure_status": "not_claimed",
            "global_invariant_status": "not_claimed",
            "bounded_evidence_status": "measurement_only",
        },
    }


def fmt(x):
    if x is None:
        return "None"
    if isinstance(x, float):
        return f"{x:.12f}"
    return str(x)


def write_markdown(result: dict) -> str:
    lines = []

    lines.append("# Mature Rebound Guard V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded guard over fuzzy rebound anatomy.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{result['bounded_assessment']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")

    for key, value in result["summary"].items():
        lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Weak-prefix false breaches")
    lines.append("")

    if result["weak_prefix_false_breach_instances"]:
        for item in result["weak_prefix_false_breach_instances"]:
            lines.append(f"### seed `{item['seed']}` pattern `{item['pattern']}` position `{item['position']}`")
            lines.append("")
            lines.append(f"- raw_rebound_class: `{item['raw_rebound_class']}`")
            lines.append(f"- guarded_rebound_class: `{item['guarded_rebound_class']}`")
            lines.append(f"- prior_debt_peak: `{fmt(item['prior_debt_peak'])}`")
            lines.append(f"- mature_prior_peak_threshold: `{fmt(item['mature_prior_peak_threshold'])}`")
            lines.append(f"- prior_peak_deficit_to_maturity: `{fmt(item['prior_peak_deficit_to_maturity'])}`")
            lines.append(f"- post_horizon_max_prefix: `{fmt(item['post_horizon_max_prefix'])}`")
            lines.append(f"- post_max_to_prior_peak_ratio: `{fmt(item['post_max_to_prior_peak_ratio'])}`")
            lines.append(f"- post_pattern_debt_gain: `{fmt(item['post_pattern_debt_gain'])}`")
            lines.append("")
    else:
        lines.append("None.")
        lines.append("")

    lines.append("## Mature breach instances")
    lines.append("")

    if result["mature_breach_instances"]:
        for item in result["mature_breach_instances"]:
            lines.append(f"- seed `{item['seed']}` pattern `{item['pattern']}` ratio `{fmt(item['post_max_to_prior_peak_ratio'])}`")
    else:
        lines.append("None.")

    lines.append("")
    lines.append("## Mature second near-breach instances")
    lines.append("")

    if result["mature_second_near_breach_instances"]:
        for item in result["mature_second_near_breach_instances"]:
            lines.append(f"- seed `{item['seed']}` pattern `{item['pattern']}` ratio `{fmt(item['post_max_to_prior_peak_ratio'])}`")
    else:
        lines.append("None.")

    lines.append("")
    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The guard separates raw rebound over a weak prefix from rebound over mature accumulated debt.")
    lines.append("")
    lines.append("A raw breach caused by a low prior peak is reclassified as a weak-prefix artifact.")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")

    for key, value in result["boundary"].items():
        lines.append(f"- {key}: `{value}`")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    result = build()

    json_path = RESULTS / "mature_rebound_guard_v0.json"
    md_path = RESULTS / "mature_rebound_guard_v0.md"
    cert_path = RESULTS / "mature_rebound_guard_v0_certificate.json"

    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(result), encoding="utf-8")

    certificate = {
        "version": "v6.4",
        "artifact": "Mature Rebound Guard V0",
        "generated_at_utc": result["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": result["bounded_assessment"],
        "summary": result["summary"],
        "boundary": result["boundary"],
    }

    cert_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"WROTE: {json_path}")
    print(f"WROTE: {md_path}")
    print(f"WROTE: {cert_path}")
    print("")
    print("BOUNDED ASSESSMENT:")
    print(f"  {result['bounded_assessment']}")
    print("")
    print("SUMMARY:")
    for key, value in result["summary"].items():
        print(f"  {key}: {value}")
    print("")
    print("WEAK-PREFIX FALSE BREACHES:")
    if result["weak_prefix_false_breach_instances"]:
        for item in result["weak_prefix_false_breach_instances"]:
            print(
                "  "
                f"seed={item['seed']} | "
                f"pattern={item['pattern']} | "
                f"raw={item['raw_rebound_class']} | "
                f"guarded={item['guarded_rebound_class']} | "
                f"prior_peak={item['prior_debt_peak']} | "
                f"ratio={item['post_max_to_prior_peak_ratio']} | "
                f"post_gain={item['post_pattern_debt_gain']}"
            )
    else:
        print("  none")
    print("")
    print("MATURE BREACH INSTANCES:")
    if result["mature_breach_instances"]:
        for item in result["mature_breach_instances"]:
            print(
                "  "
                f"seed={item['seed']} | "
                f"pattern={item['pattern']} | "
                f"prior_peak={item['prior_debt_peak']} | "
                f"ratio={item['post_max_to_prior_peak_ratio']}"
            )
    else:
        print("  none")
    print("")
    print("MATURE SECOND NEAR-BREACH INSTANCES:")
    if result["mature_second_near_breach_instances"]:
        for item in result["mature_second_near_breach_instances"]:
            print(
                "  "
                f"seed={item['seed']} | "
                f"pattern={item['pattern']} | "
                f"prior_peak={item['prior_debt_peak']} | "
                f"ratio={item['post_max_to_prior_peak_ratio']}"
            )
    else:
        print("  none")
    print("")
    print("BOUNDARY:")
    for key, value in result["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
