#!/usr/bin/env python3
"""
Fuzzy Near-Breach Grammar Audit V0.

This bounded audit searches for approximate recurrence of the two dominant
near-breach post-response grammars found in v6.0.

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
TOP_SEEDS_TO_REPORT = 50
SIMILARITY_THRESHOLD = 0.85
POST_PATTERN_HORIZON = 32

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


def min_distance_between_positions(positions: list[int]) -> int | None:
    if len(positions) < 2:
        return None

    distances = [
        positions[i + 1] - positions[i]
        for i in range(len(positions) - 1)
    ]

    return min(distances)


def post_pattern_metrics(
    steps: list[dict],
    position: int,
    pattern_len: int,
    horizon: int = POST_PATTERN_HORIZON,
) -> dict:
    start = position
    end = position + pattern_len - 1

    if not steps or start >= len(steps):
        return {
            "pattern_start_prefix": None,
            "pattern_end_prefix": None,
            "pattern_sum_delta": None,
            "post_horizon_max_prefix": None,
            "post_pattern_debt_gain": None,
            "post_pattern_new_local_peak": False,
        }

    pattern_steps = steps[start:min(end + 1, len(steps))]
    post_steps = steps[end + 1:min(end + 1 + horizon, len(steps))]

    pattern_start_prefix = steps[start]["prefix_debt"]
    pattern_end_prefix = pattern_steps[-1]["prefix_debt"] if pattern_steps else None
    pattern_sum_delta = sum(s["delta"] for s in pattern_steps)

    if post_steps:
        post_horizon_max_prefix = max(s["prefix_debt"] for s in post_steps)
        post_pattern_debt_gain = post_horizon_max_prefix - pattern_end_prefix
        post_pattern_new_local_peak = post_horizon_max_prefix > pattern_end_prefix
    else:
        post_horizon_max_prefix = None
        post_pattern_debt_gain = None
        post_pattern_new_local_peak = False

    return {
        "pattern_start_prefix": pattern_start_prefix,
        "pattern_end_prefix": pattern_end_prefix,
        "pattern_sum_delta": pattern_sum_delta,
        "post_horizon_max_prefix": post_horizon_max_prefix,
        "post_pattern_debt_gain": post_pattern_debt_gain,
        "post_pattern_new_local_peak": post_pattern_new_local_peak,
    }


def suppress_overlapping_hits(hits: list[dict]) -> list[dict]:
    """
    Keep highest-similarity hits while suppressing overlapping hits
    of the same pattern family. This avoids counting a sliding cluster
    as many independent recurrences.
    """
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


def analyze_seed(seed: int) -> dict:
    t = trajectory(seed)
    sequence = t["a_sequence"]
    steps = t["steps"]

    raw_hits_a = find_fuzzy_pattern_positions(sequence, PATTERN_A)
    raw_hits_b = find_fuzzy_pattern_positions(sequence, PATTERN_B)

    hits_a = suppress_overlapping_hits(raw_hits_a)
    hits_b = suppress_overlapping_hits(raw_hits_b)

    combined = [
        {"pattern": "A", **hit}
        for hit in hits_a
    ] + [
        {"pattern": "B", **hit}
        for hit in hits_b
    ]

    combined.sort(key=lambda x: x["position"])

    combined_positions = [x["position"] for x in combined]
    recurrence_distances = [
        combined_positions[i + 1] - combined_positions[i]
        for i in range(len(combined_positions) - 1)
    ]

    pattern_after_pattern = len(combined) >= 2

    instance_metrics = []

    for item in combined:
        metrics = post_pattern_metrics(steps, item["position"], item["length"])
        instance_metrics.append(
            {
                "pattern": item["pattern"],
                "position": item["position"],
                "length": item["length"],
                "hamming_distance": item["hamming_distance"],
                "similarity": item["similarity"],
                "window": item["window"],
                **metrics,
            }
        )

    similarities = [x["similarity"] for x in instance_metrics]
    post_pattern_debt_gains = [
        x["post_pattern_debt_gain"]
        for x in instance_metrics
        if x["post_pattern_debt_gain"] is not None
    ]

    post_pattern_new_local_peak_count = sum(
        1 for x in instance_metrics
        if x["post_pattern_new_local_peak"]
    )

    return {
        "seed": seed,
        "terminated": t["terminated"],
        "odd_steps": t["odd_steps"],
        "fuzzy_A_count": len(hits_a),
        "fuzzy_B_count": len(hits_b),
        "fuzzy_combined_count": len(combined),
        "raw_fuzzy_A_count": len(raw_hits_a),
        "raw_fuzzy_B_count": len(raw_hits_b),
        "fuzzy_A_positions": [x["position"] for x in hits_a],
        "fuzzy_B_positions": [x["position"] for x in hits_b],
        "fuzzy_combined_positions": combined_positions,
        "fuzzy_pattern_after_pattern": pattern_after_pattern,
        "fuzzy_recurrence_distances": recurrence_distances,
        "min_fuzzy_recurrence_distance": min(recurrence_distances) if recurrence_distances else None,
        "instance_metrics": instance_metrics,
        "mean_similarity": safe_mean(similarities),
        "max_similarity": max(similarities) if similarities else None,
        "post_fuzzy_pattern_new_local_peak_count": post_pattern_new_local_peak_count,
        "mean_post_fuzzy_pattern_debt_gain": safe_mean(post_pattern_debt_gains),
        "max_post_fuzzy_pattern_debt_gain": max(post_pattern_debt_gains) if post_pattern_debt_gains else None,
        "a_sequence_prefix": sequence[:80],
    }


def build() -> dict:
    seed_results = [
        analyze_seed(seed)
        for seed in range(1, MAX_ODD_SEED + 1, 2)
    ]

    hits = [r for r in seed_results if r["fuzzy_combined_count"] > 0]
    recurrence_hits = [r for r in hits if r["fuzzy_combined_count"] > 1]
    pattern_after_pattern_hits = [r for r in hits if r["fuzzy_pattern_after_pattern"]]

    fuzzy_a_hits = [r for r in seed_results if r["fuzzy_A_count"] > 0]
    fuzzy_b_hits = [r for r in seed_results if r["fuzzy_B_count"] > 0]

    total_instances = sum(r["fuzzy_combined_count"] for r in seed_results)
    total_a_instances = sum(r["fuzzy_A_count"] for r in seed_results)
    total_b_instances = sum(r["fuzzy_B_count"] for r in seed_results)

    raw_total_a_instances = sum(r["raw_fuzzy_A_count"] for r in seed_results)
    raw_total_b_instances = sum(r["raw_fuzzy_B_count"] for r in seed_results)

    distances = []
    post_pattern_debt_gains = []
    similarities = []
    post_pattern_new_peak_counts = 0

    for r in hits:
        distances.extend(r["fuzzy_recurrence_distances"])

        for item in r["instance_metrics"]:
            similarities.append(item["similarity"])

            if item["post_pattern_debt_gain"] is not None:
                post_pattern_debt_gains.append(item["post_pattern_debt_gain"])

            if item["post_pattern_new_local_peak"]:
                post_pattern_new_peak_counts += 1

    hit_rate = len(hits) / len(seed_results) if seed_results else None
    recurrence_hit_rate = len(recurrence_hits) / len(seed_results) if seed_results else None

    hits_sorted = sorted(
        hits,
        key=lambda r: (
            -r["fuzzy_combined_count"],
            r["min_fuzzy_recurrence_distance"] if r["min_fuzzy_recurrence_distance"] is not None else 10**9,
            -(r["max_similarity"] or 0),
            r["seed"],
        ),
    )

    top_hits = hits_sorted[:TOP_SEEDS_TO_REPORT]

    dangerous_hits = [
        r for r in hits
        if r["fuzzy_pattern_after_pattern"]
        and r["post_fuzzy_pattern_new_local_peak_count"] > 0
    ]

    summary = {
        "records_measured": len(seed_results),
        "similarity_threshold": SIMILARITY_THRESHOLD,
        "fuzzy_hit_seed_count": len(hits),
        "fuzzy_hit_rate": hit_rate,
        "fuzzy_A_hit_seed_count": len(fuzzy_a_hits),
        "fuzzy_B_hit_seed_count": len(fuzzy_b_hits),
        "fuzzy_A_instance_count": total_a_instances,
        "fuzzy_B_instance_count": total_b_instances,
        "fuzzy_combined_instance_count": total_instances,
        "raw_fuzzy_A_instance_count": raw_total_a_instances,
        "raw_fuzzy_B_instance_count": raw_total_b_instances,
        "fuzzy_recurrence_seed_count": len(recurrence_hits),
        "fuzzy_recurrence_hit_rate": recurrence_hit_rate,
        "fuzzy_pattern_after_pattern_seed_count": len(pattern_after_pattern_hits),
        "dangerous_fuzzy_chain_seed_count": len(dangerous_hits),
        "mean_fuzzy_recurrence_distance": safe_mean([float(x) for x in distances]),
        "min_fuzzy_recurrence_distance": min(distances) if distances else None,
        "mean_similarity": safe_mean(similarities),
        "min_similarity": min(similarities) if similarities else None,
        "max_similarity": max(similarities) if similarities else None,
        "mean_post_fuzzy_pattern_debt_gain": safe_mean(post_pattern_debt_gains),
        "max_post_fuzzy_pattern_debt_gain": max(post_pattern_debt_gains) if post_pattern_debt_gains else None,
        "post_fuzzy_pattern_new_local_peak_count": post_pattern_new_peak_counts,
        "post_fuzzy_pattern_new_local_peak_rate_per_instance": (
            post_pattern_new_peak_counts / total_instances
            if total_instances else None
        ),
    }

    if len(dangerous_hits) > 0:
        bounded_assessment = "fuzzy_chain_with_post_pattern_growth_detected"
    elif len(recurrence_hits) > 0:
        bounded_assessment = "fuzzy_grammar_recurrence_detected_without_growth"
    elif len(hits) > 0:
        bounded_assessment = "fuzzy_grammar_isolated_occurrences_detected"
    else:
        bounded_assessment = "no_fuzzy_near_breach_grammar_detected"

    return {
        "version": "v6.2",
        "machine": "Fuzzy Near-Breach Grammar Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_steps": ODD_STEPS,
            "max_odd_seed": MAX_ODD_SEED,
            "top_seeds_to_report": TOP_SEEDS_TO_REPORT,
            "similarity_threshold": SIMILARITY_THRESHOLD,
            "post_pattern_horizon": POST_PATTERN_HORIZON,
            "pattern_A": PATTERN_A,
            "pattern_B": PATTERN_B,
            "pattern_A_length": len(PATTERN_A),
            "pattern_B_length": len(PATTERN_B),
            "matching": "exact_length_hamming_similarity_with_overlap_suppression",
        },
        "summary": summary,
        "top_fuzzy_pattern_hits": top_hits,
        "dangerous_fuzzy_chain_hits": dangerous_hits[:TOP_SEEDS_TO_REPORT],
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit tests whether approximate near-breach grammars recur or concatenate inside bounded trajectories.",
            "primary_fuzzy_signal": "fuzzy_combined_count and fuzzy_pattern_after_pattern",
            "native_hypothesis": "If fuzzy near-breach grammars recur and still generate post-pattern growth, the dangerous structure is broader than exact A/B.",
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

    lines.append("# Fuzzy Near-Breach Grammar Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded fuzzy near-breach grammar audit.")
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
    lines.append("## Pattern A")
    lines.append("")
    lines.append("`" + ", ".join(str(x) for x in summary["parameters"]["pattern_A"]) + "`")
    lines.append("")
    lines.append("## Pattern B")
    lines.append("")
    lines.append("`" + ", ".join(str(x) for x in summary["parameters"]["pattern_B"]) + "`")
    lines.append("")
    lines.append("## Top fuzzy pattern hits")
    lines.append("")

    for item in summary["top_fuzzy_pattern_hits"][:20]:
        lines.append(f"### seed `{item['seed']}`")
        lines.append("")
        lines.append(f"- fuzzy_A_count: `{item['fuzzy_A_count']}`")
        lines.append(f"- fuzzy_B_count: `{item['fuzzy_B_count']}`")
        lines.append(f"- fuzzy_combined_count: `{item['fuzzy_combined_count']}`")
        lines.append(f"- fuzzy_pattern_after_pattern: `{item['fuzzy_pattern_after_pattern']}`")
        lines.append(f"- min_fuzzy_recurrence_distance: `{fmt(item['min_fuzzy_recurrence_distance'])}`")
        lines.append(f"- max_similarity: `{fmt(item['max_similarity'])}`")
        lines.append(f"- fuzzy_A_positions: `{item['fuzzy_A_positions']}`")
        lines.append(f"- fuzzy_B_positions: `{item['fuzzy_B_positions']}`")
        lines.append(f"- post_fuzzy_pattern_new_local_peak_count: `{item['post_fuzzy_pattern_new_local_peak_count']}`")
        lines.append(f"- mean_post_fuzzy_pattern_debt_gain: `{fmt(item['mean_post_fuzzy_pattern_debt_gain'])}`")
        lines.append("")

    lines.append("## Native interpretation")
    lines.append("")
    lines.append("Fuzzy recurrence means a near-breach-like grammar appears again with high Hamming similarity.")
    lines.append("")
    lines.append("This audit distinguishes broad recurrence from dangerous recurrence that also produces post-pattern debt gain.")
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

    json_path = RESULTS / "fuzzy_near_breach_grammar_audit_v0.json"
    md_path = RESULTS / "fuzzy_near_breach_grammar_audit_v0.md"
    cert_path = RESULTS / "fuzzy_near_breach_grammar_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v6.2",
        "artifact": "Fuzzy Near-Breach Grammar Audit V0",
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
    print("TOP FUZZY PATTERN HITS:")
    for item in summary["top_fuzzy_pattern_hits"][:10]:
        print(
            "  "
            f"seed={item['seed']} | "
            f"A={item['fuzzy_A_count']} | "
            f"B={item['fuzzy_B_count']} | "
            f"combined={item['fuzzy_combined_count']} | "
            f"after_pattern={item['fuzzy_pattern_after_pattern']} | "
            f"max_sim={item['max_similarity']} | "
            f"min_dist={item['min_fuzzy_recurrence_distance']} | "
            f"new_local_peak_count={item['post_fuzzy_pattern_new_local_peak_count']} | "
            f"max_gain={item['max_post_fuzzy_pattern_debt_gain']}"
        )
    print("")
    print("DANGEROUS FUZZY CHAIN HITS:")
    if summary["dangerous_fuzzy_chain_hits"]:
        for item in summary["dangerous_fuzzy_chain_hits"][:10]:
            print(
                "  "
                f"seed={item['seed']} | "
                f"combined={item['fuzzy_combined_count']} | "
                f"new_local_peak_count={item['post_fuzzy_pattern_new_local_peak_count']} | "
                f"max_gain={item['max_post_fuzzy_pattern_debt_gain']}"
            )
    else:
        print("  none")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
