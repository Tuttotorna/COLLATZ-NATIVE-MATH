#!/usr/bin/env python3
"""
Fuzzy Rebound Anatomy V0.

This bounded audit isolates fuzzy near-breach grammar instances that produce
post-pattern local growth and measures whether that rebound approaches
a second near-breach boundary.

It does not prove Collatz.
It does not claim Collatz is solved.
It is measurement only.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

ODD_STEPS = 960
MAX_ODD_SEED = 99999
SIMILARITY_THRESHOLD = 0.85
POST_PATTERN_HORIZON = 32
AFTER_PATTERN_TRACE_LENGTH = 48
SECOND_NEAR_BREACH_THRESHOLD = 0.95

PATTERN_A = [3, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 4, 1, 2, 1, 2, 2, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1]
PATTERN_B = [6, 1, 1, 1, 2, 1, 2, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1]


def v2(x: int) -> int:
    if x <= 0:
        raise ValueError("v2 requires a positive integer")

    count = 0

    while x % 2 == 0:
        x //= 2
        count += 1

    return count


def odd_step(n: int) -> tuple[int, int, float]:
    if n <= 0 or n % 2 == 0:
        raise ValueError("odd_step requires a positive odd integer")

    m = 3 * n + 1
    a = v2(m)
    next_n = m // (2 ** a)
    delta = math.log2(next_n / n)

    return next_n, a, delta


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def safe_median(values: list[float]) -> float | None:
    return median(values) if values else None


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None

    mx = mean(xs)
    my = mean(ys)

    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))

    if den_x == 0 or den_y == 0:
        return None

    return num / (den_x * den_y)


def trajectory(seed: int, odd_steps: int = ODD_STEPS) -> dict:
    if seed <= 0 or seed % 2 == 0:
        raise ValueError("seed must be a positive odd integer")

    n = seed
    steps = []
    prefix = 0.0

    for i in range(odd_steps):
        if n == 1:
            break

        next_n, a, delta = odd_step(n)
        prefix += delta

        steps.append(
            {
                "index": i,
                "n": n,
                "next_n": next_n,
                "a": a,
                "delta": delta,
                "prefix_debt": prefix,
                "is_release": delta < -1,
                "is_strong_release": delta < -2,
                "is_expansion": delta > 0,
            }
        )

        n = next_n

    return {
        "seed": seed,
        "terminated": n == 1,
        "final_n": n,
        "odd_steps": len(steps),
        "steps": steps,
        "a_sequence": [s["a"] for s in steps],
    }


def hamming_distance(xs: list[int], ys: list[int]) -> int:
    if len(xs) != len(ys):
        raise ValueError("hamming_distance requires equal-length lists")

    return sum(1 for x, y in zip(xs, ys) if x != y)


def similarity(xs: list[int], ys: list[int]) -> float:
    if len(xs) != len(ys):
        raise ValueError("similarity requires equal-length lists")

    if not xs:
        return 0.0

    return 1.0 - hamming_distance(xs, ys) / len(xs)


def find_fuzzy_pattern_positions(
    sequence: list[int],
    pattern: list[int],
    threshold: float = SIMILARITY_THRESHOLD,
) -> list[dict]:
    if not pattern or len(sequence) < len(pattern):
        return []

    hits = []
    width = len(pattern)

    for i in range(0, len(sequence) - width + 1):
        window = sequence[i:i + width]
        dist = hamming_distance(window, pattern)
        sim = 1.0 - dist / width

        if sim >= threshold:
            hits.append(
                {
                    "position": i,
                    "length": width,
                    "hamming_distance": dist,
                    "similarity": sim,
                    "window": window,
                }
            )

    return hits


def suppress_overlapping_hits(hits: list[dict]) -> list[dict]:
    sorted_hits = sorted(
        hits,
        key=lambda x: (-x["similarity"], x["hamming_distance"], x["position"]),
    )

    kept = []

    for candidate in sorted_hits:
        c_start = candidate["position"]
        c_end = c_start + candidate["length"] - 1

        overlaps = False

        for existing in kept:
            e_start = existing["position"]
            e_end = e_start + existing["length"] - 1

            if not (c_end < e_start or c_start > e_end):
                overlaps = True
                break

        if not overlaps:
            kept.append(candidate)

    return sorted(kept, key=lambda x: x["position"])


def classify_rebound(
    post_max_to_prior_peak_ratio: float | None,
    post_pattern_new_local_peak: bool,
) -> str:
    if post_max_to_prior_peak_ratio is None:
        return "unclassified"

    if post_max_to_prior_peak_ratio > 1.0:
        return "breach_after_fuzzy_pattern"

    if post_max_to_prior_peak_ratio >= SECOND_NEAR_BREACH_THRESHOLD:
        return "second_near_breach_candidate"

    if post_max_to_prior_peak_ratio >= 0.80:
        return "near_peak_rebound"

    if post_pattern_new_local_peak:
        return "harmless_rebound"

    return "no_rebound"


def next_release_delay(steps: list[dict], start_index: int) -> int | None:
    for s in steps:
        if s["index"] > start_index and s["is_release"]:
            return s["index"] - start_index

    return None


def extract_rebound_instance(
    seed: int,
    steps: list[dict],
    pattern_name: str,
    hit: dict,
) -> dict:
    position = hit["position"]
    length = hit["length"]
    start = position
    end = position + length - 1

    prior_steps = steps[:start + 1]
    prior_debt_peak = max((s["prefix_debt"] for s in prior_steps), default=None)
    prior_debt_peak_index = None

    if prior_debt_peak is not None:
        for s in prior_steps:
            if s["prefix_debt"] == prior_debt_peak:
                prior_debt_peak_index = s["index"]
                break

    pattern_steps = steps[start:min(end + 1, len(steps))]
    post_steps = steps[end + 1:min(end + 1 + POST_PATTERN_HORIZON, len(steps))]
    after_trace = steps[end + 1:min(end + 1 + AFTER_PATTERN_TRACE_LENGTH, len(steps))]

    pattern_start_prefix = steps[start]["prefix_debt"] if start < len(steps) else None
    pattern_end_prefix = pattern_steps[-1]["prefix_debt"] if pattern_steps else None
    pattern_sum_delta = sum(s["delta"] for s in pattern_steps)

    if post_steps:
        post_horizon_max_step = max(post_steps, key=lambda s: s["prefix_debt"])
        post_horizon_max_prefix = post_horizon_max_step["prefix_debt"]
        post_horizon_max_index = post_horizon_max_step["index"]
        post_pattern_debt_gain = (
            post_horizon_max_prefix - pattern_end_prefix
            if pattern_end_prefix is not None else None
        )
        post_pattern_new_local_peak = (
            post_pattern_debt_gain is not None
            and post_pattern_debt_gain > 0
        )
    else:
        post_horizon_max_prefix = None
        post_horizon_max_index = None
        post_pattern_debt_gain = None
        post_pattern_new_local_peak = False

    if prior_debt_peak and post_horizon_max_prefix is not None:
        post_max_to_prior_peak_ratio = post_horizon_max_prefix / prior_debt_peak
        gap_to_prior_peak = 1.0 - post_max_to_prior_peak_ratio
    else:
        post_max_to_prior_peak_ratio = None
        gap_to_prior_peak = None

    rebound_class = classify_rebound(
        post_max_to_prior_peak_ratio=post_max_to_prior_peak_ratio,
        post_pattern_new_local_peak=post_pattern_new_local_peak,
    )

    return {
        "seed": seed,
        "pattern": pattern_name,
        "position": position,
        "length": length,
        "window": hit["window"],
        "hamming_distance": hit["hamming_distance"],
        "similarity": hit["similarity"],
        "pattern_start_prefix": pattern_start_prefix,
        "pattern_end_prefix": pattern_end_prefix,
        "pattern_sum_delta": pattern_sum_delta,
        "prior_debt_peak": prior_debt_peak,
        "prior_debt_peak_index": prior_debt_peak_index,
        "post_horizon_max_prefix": post_horizon_max_prefix,
        "post_horizon_max_index": post_horizon_max_index,
        "post_pattern_debt_gain": post_pattern_debt_gain,
        "post_pattern_new_local_peak": post_pattern_new_local_peak,
        "post_max_to_prior_peak_ratio": post_max_to_prior_peak_ratio,
        "gap_to_prior_peak": gap_to_prior_peak,
        "rebound_class": rebound_class,
        "second_near_breach_candidate": rebound_class == "second_near_breach_candidate",
        "breach_after_fuzzy_pattern": rebound_class == "breach_after_fuzzy_pattern",
        "next_release_delay_after_pattern_end": next_release_delay(steps, end),
        "after_pattern_a_sequence": [s["a"] for s in after_trace],
        "after_pattern_delta_sequence": [s["delta"] for s in after_trace],
        "after_pattern_prefix_sequence": [s["prefix_debt"] for s in after_trace],
        "after_pattern_compact_trace": [
            {
                "index": s["index"],
                "n": s["n"],
                "a": s["a"],
                "delta": s["delta"],
                "prefix_debt": s["prefix_debt"],
            }
            for s in after_trace
        ],
    }


def analyze_seed(seed: int) -> dict:
    t = trajectory(seed)
    sequence = t["a_sequence"]
    steps = t["steps"]

    raw_hits_a = find_fuzzy_pattern_positions(sequence, PATTERN_A)
    raw_hits_b = find_fuzzy_pattern_positions(sequence, PATTERN_B)

    hits_a = suppress_overlapping_hits(raw_hits_a)
    hits_b = suppress_overlapping_hits(raw_hits_b)

    instances = []

    for hit in hits_a:
        instance = extract_rebound_instance(seed, steps, "A", hit)
        instances.append(instance)

    for hit in hits_b:
        instance = extract_rebound_instance(seed, steps, "B", hit)
        instances.append(instance)

    instances.sort(key=lambda x: x["position"])

    rebound_instances = [
        x for x in instances
        if x["post_pattern_new_local_peak"]
    ]

    return {
        "seed": seed,
        "terminated": t["terminated"],
        "odd_steps": t["odd_steps"],
        "fuzzy_instance_count": len(instances),
        "rebound_instance_count": len(rebound_instances),
        "instances": instances,
        "rebound_instances": rebound_instances,
    }


def build() -> dict:
    seed_results = [
        analyze_seed(seed)
        for seed in range(1, MAX_ODD_SEED + 1, 2)
    ]

    all_instances = []
    rebound_instances = []

    for result in seed_results:
        all_instances.extend(result["instances"])
        rebound_instances.extend(result["rebound_instances"])

    rebound_instances.sort(
        key=lambda x: (
            -(x["post_pattern_debt_gain"] if x["post_pattern_debt_gain"] is not None else -10**9),
            -(x["post_max_to_prior_peak_ratio"] if x["post_max_to_prior_peak_ratio"] is not None else -10**9),
            x["seed"],
            x["position"],
        )
    )

    rebound_seed_count = len(set(x["seed"] for x in rebound_instances))
    second_near_breach_instances = [
        x for x in rebound_instances
        if x["second_near_breach_candidate"]
    ]
    breach_instances = [
        x for x in rebound_instances
        if x["breach_after_fuzzy_pattern"]
    ]

    rebound_classes = {}
    for x in rebound_instances:
        rebound_classes[x["rebound_class"]] = rebound_classes.get(x["rebound_class"], 0) + 1

    gains = [
        x["post_pattern_debt_gain"]
        for x in rebound_instances
        if x["post_pattern_debt_gain"] is not None
    ]
    ratios = [
        x["post_max_to_prior_peak_ratio"]
        for x in rebound_instances
        if x["post_max_to_prior_peak_ratio"] is not None
    ]
    gaps = [
        x["gap_to_prior_peak"]
        for x in rebound_instances
        if x["gap_to_prior_peak"] is not None
    ]

    next_release_delays = [
        float(x["next_release_delay_after_pattern_end"])
        for x in rebound_instances
        if x["next_release_delay_after_pattern_end"] is not None
    ]

    summary = {
        "records_measured": len(seed_results),
        "fuzzy_instance_count": len(all_instances),
        "rebound_instance_count": len(rebound_instances),
        "rebound_seed_count": rebound_seed_count,
        "second_near_breach_instance_count": len(second_near_breach_instances),
        "breach_after_fuzzy_pattern_instance_count": len(breach_instances),
        "rebound_class_counts": rebound_classes,
        "mean_post_pattern_debt_gain": safe_mean(gains),
        "max_post_pattern_debt_gain": max(gains) if gains else None,
        "mean_post_max_to_prior_peak_ratio": safe_mean(ratios),
        "max_post_max_to_prior_peak_ratio": max(ratios) if ratios else None,
        "min_gap_to_prior_peak": min(gaps) if gaps else None,
        "mean_next_release_delay_after_pattern_end": safe_mean(next_release_delays),
        "min_next_release_delay_after_pattern_end": min(next_release_delays) if next_release_delays else None,
        "max_next_release_delay_after_pattern_end": max(next_release_delays) if next_release_delays else None,
    }

    if breach_instances:
        bounded_assessment = "breach_after_fuzzy_pattern_detected"
    elif second_near_breach_instances:
        bounded_assessment = "second_near_breach_rebound_detected"
    elif rebound_instances:
        bounded_assessment = "local_fuzzy_rebounds_detected_without_second_near_breach"
    else:
        bounded_assessment = "no_fuzzy_rebound_detected"

    return {
        "version": "v6.3",
        "machine": "Fuzzy Rebound Anatomy V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_steps": ODD_STEPS,
            "max_odd_seed": MAX_ODD_SEED,
            "similarity_threshold": SIMILARITY_THRESHOLD,
            "post_pattern_horizon": POST_PATTERN_HORIZON,
            "after_pattern_trace_length": AFTER_PATTERN_TRACE_LENGTH,
            "second_near_breach_threshold": SECOND_NEAR_BREACH_THRESHOLD,
            "pattern_A": PATTERN_A,
            "pattern_B": PATTERN_B,
            "pattern_A_length": len(PATTERN_A),
            "pattern_B_length": len(PATTERN_B),
        },
        "summary": summary,
        "rebound_instances": rebound_instances,
        "second_near_breach_instances": second_near_breach_instances,
        "breach_after_fuzzy_pattern_instances": breach_instances,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit isolates fuzzy grammar instances that produce local rebound and measures whether they approach prior debt peaks.",
            "primary_rebound_signal": "post_max_to_prior_peak_ratio",
            "native_hypothesis": "A dangerous fuzzy rebound would need to become a second near-breach or breach after the pattern.",
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


def write_markdown(summary: dict) -> str:
    lines = []

    lines.append("# Fuzzy Rebound Anatomy V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded fuzzy rebound anatomy audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")

    for key, value in summary["summary"].items():
        lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Rebound instances")
    lines.append("")

    for item in summary["rebound_instances"]:
        lines.append(f"### seed `{item['seed']}` pattern `{item['pattern']}` position `{item['position']}`")
        lines.append("")
        lines.append(f"- hamming_distance: `{item['hamming_distance']}`")
        lines.append(f"- similarity: `{fmt(item['similarity'])}`")
        lines.append(f"- post_pattern_debt_gain: `{fmt(item['post_pattern_debt_gain'])}`")
        lines.append(f"- prior_debt_peak: `{fmt(item['prior_debt_peak'])}`")
        lines.append(f"- post_horizon_max_prefix: `{fmt(item['post_horizon_max_prefix'])}`")
        lines.append(f"- post_max_to_prior_peak_ratio: `{fmt(item['post_max_to_prior_peak_ratio'])}`")
        lines.append(f"- gap_to_prior_peak: `{fmt(item['gap_to_prior_peak'])}`")
        lines.append(f"- rebound_class: `{item['rebound_class']}`")
        lines.append(f"- next_release_delay_after_pattern_end: `{fmt(item['next_release_delay_after_pattern_end'])}`")
        lines.append("")
        lines.append("after_pattern_a_sequence:")
        lines.append("")
        lines.append("`" + ", ".join(str(x) for x in item["after_pattern_a_sequence"]) + "`")
        lines.append("")

    lines.append("## Native interpretation")
    lines.append("")
    lines.append("This audit separates local rebound from second near-breach behavior.")
    lines.append("")
    lines.append("A rebound is dangerous only if it approaches or exceeds the prior debt peak.")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")

    for key, value in summary["boundary"].items():
        lines.append(f"- {key}: `{value}`")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    summary = build()

    json_path = RESULTS / "fuzzy_rebound_anatomy_v0.json"
    md_path = RESULTS / "fuzzy_rebound_anatomy_v0.md"
    cert_path = RESULTS / "fuzzy_rebound_anatomy_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v6.3",
        "artifact": "Fuzzy Rebound Anatomy V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "summary": summary["summary"],
        "boundary": summary["boundary"],
    }

    cert_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"WROTE: {json_path}")
    print(f"WROTE: {md_path}")
    print(f"WROTE: {cert_path}")
    print("")
    print("BOUNDED ASSESSMENT:")
    print(f"  {summary['bounded_assessment']}")
    print("")
    print("SUMMARY:")
    for key, value in summary["summary"].items():
        print(f"  {key}: {value}")
    print("")
    print("REBOUND INSTANCES:")
    if summary["rebound_instances"]:
        for item in summary["rebound_instances"]:
            print(
                "  "
                f"seed={item['seed']} | "
                f"pattern={item['pattern']} | "
                f"pos={item['position']} | "
                f"sim={item['similarity']} | "
                f"gain={item['post_pattern_debt_gain']} | "
                f"ratio_to_prior_peak={item['post_max_to_prior_peak_ratio']} | "
                f"gap={item['gap_to_prior_peak']} | "
                f"class={item['rebound_class']} | "
                f"next_release_delay={item['next_release_delay_after_pattern_end']}"
            )
    else:
        print("  none")
    print("")
    print("SECOND NEAR-BREACH INSTANCES:")
    if summary["second_near_breach_instances"]:
        for item in summary["second_near_breach_instances"]:
            print(
                "  "
                f"seed={item['seed']} | "
                f"pattern={item['pattern']} | "
                f"ratio={item['post_max_to_prior_peak_ratio']} | "
                f"gap={item['gap_to_prior_peak']}"
            )
    else:
        print("  none")
    print("")
    print("BREACH AFTER FUZZY PATTERN INSTANCES:")
    if summary["breach_after_fuzzy_pattern_instances"]:
        for item in summary["breach_after_fuzzy_pattern_instances"]:
            print(
                "  "
                f"seed={item['seed']} | "
                f"pattern={item['pattern']} | "
                f"ratio={item['post_max_to_prior_peak_ratio']} | "
                f"gap={item['gap_to_prior_peak']}"
            )
    else:
        print("  none")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
