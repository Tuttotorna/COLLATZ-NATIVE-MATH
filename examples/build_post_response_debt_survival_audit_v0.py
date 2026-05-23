#!/usr/bin/env python3
"""
Post-Response Debt Survival Audit V0.

This bounded audit tests whether the first rapid post-peak release response
actually reduces debt below the peak, and whether debt later regenerates.

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

ODD_STEPS = 160
POST_PEAK_HORIZON = 20
BLOCK_SIZE = 999
MAX_END = 99999


def make_block_ranges(block_size: int = BLOCK_SIZE, max_end: int = MAX_END) -> list[dict]:
    ranges = []
    start = 1

    while start <= max_end:
        end = min(start + block_size - 1, max_end)
        ranges.append(
            {
                "label": f"{start}..{end}",
                "start": start,
                "end": end,
                "midpoint": (start + end) / 2.0,
            }
        )
        start = end + 2

    return ranges


BLOCK_RANGES = make_block_ranges()


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


def linear_slope(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None

    mx = mean(xs)
    my = mean(ys)

    den = sum((x - mx) ** 2 for x in xs)

    if den == 0:
        return None

    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))

    return num / den


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def safe_median(values: list[float]) -> float | None:
    return median(values) if values else None


def odd_seeds(start: int, end: int) -> list[int]:
    first = start if start % 2 == 1 else start + 1
    return list(range(first, end + 1, 2))


def measure_seed(seed: int, odd_steps: int, post_peak_horizon: int) -> dict:
    if seed <= 0 or seed % 2 == 0:
        raise ValueError("seed must be a positive odd integer")

    n = seed
    steps = []
    prefix = 0.0
    prefixes = []

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
            }
        )

        prefixes.append(prefix)
        n = next_n

    if not steps:
        return {
            "seed": seed,
            "odd_steps": 0,
            "terminated": True,
            "debt_peak": 0.0,
            "peak_index": None,
            "response_delay": None,
            "response_index": None,
            "has_response": False,
            "debt_after_first_release": None,
            "debt_drop_after_first_release": None,
            "survival_ratio": None,
            "response_reduced_below_peak": False,
            "response_overdischarged_below_zero": False,
            "new_peak_after_release": False,
            "post_response_max_debt": None,
        }

    debt_peak = max(prefixes)
    peak_index = prefixes.index(debt_peak)

    later_steps = [s for s in steps if s["index"] > peak_index]
    later_releases = [s for s in later_steps if s["is_release"]]

    if later_releases:
        first_release = later_releases[0]
        response_index = first_release["index"]
        response_delay = response_index - peak_index
        has_response = True
        debt_after_first_release = first_release["prefix_debt"]
        debt_drop_after_first_release = debt_peak - debt_after_first_release

        if debt_peak > 0:
            survival_ratio = debt_after_first_release / debt_peak
        else:
            survival_ratio = None

        response_reduced_below_peak = debt_after_first_release < debt_peak
        response_overdischarged_below_zero = debt_after_first_release < 0

        post_response_prefixes = [
            s["prefix_debt"]
            for s in steps
            if s["index"] > response_index
        ]

        if post_response_prefixes:
            post_response_max_debt = max(post_response_prefixes)
            new_peak_after_release = post_response_max_debt > debt_peak
        else:
            post_response_max_debt = None
            new_peak_after_release = False

    else:
        response_index = None
        response_delay = None
        has_response = False
        debt_after_first_release = None
        debt_drop_after_first_release = None
        survival_ratio = None
        response_reduced_below_peak = False
        response_overdischarged_below_zero = False
        post_response_max_debt = None
        new_peak_after_release = False

    return {
        "seed": seed,
        "odd_steps": len(steps),
        "terminated": n == 1,
        "debt_peak": debt_peak,
        "peak_index": peak_index,
        "response_delay": response_delay,
        "response_index": response_index,
        "has_response": has_response,
        "debt_after_first_release": debt_after_first_release,
        "debt_drop_after_first_release": debt_drop_after_first_release,
        "survival_ratio": survival_ratio,
        "response_reduced_below_peak": response_reduced_below_peak,
        "response_overdischarged_below_zero": response_overdischarged_below_zero,
        "new_peak_after_release": new_peak_after_release,
        "post_response_max_debt": post_response_max_debt,
    }


def summarize_records(records: list[dict]) -> dict:
    n = len(records)

    if n == 0:
        raise ValueError("No records to summarize")

    response_records = [r for r in records if r["has_response"]]
    ratio_records = [r for r in response_records if r["survival_ratio"] is not None]

    delays = [float(r["response_delay"]) for r in response_records]
    drops = [float(r["debt_drop_after_first_release"]) for r in response_records]
    ratios = [float(r["survival_ratio"]) for r in ratio_records]
    debt_peaks = [float(r["debt_peak"]) for r in records]
    reduced_flags = [1.0 if r["response_reduced_below_peak"] else 0.0 for r in records]
    overdischarged_flags = [1.0 if r["response_overdischarged_below_zero"] else 0.0 for r in records]
    new_peak_flags = [1.0 if r["new_peak_after_release"] else 0.0 for r in records]

    response_count = len(response_records)
    no_response_count = n - response_count

    p_has_response = response_count / n
    no_response_rate = no_response_count / n

    p_reduced_below_peak = sum(1 for r in records if r["response_reduced_below_peak"]) / n
    p_overdischarged_below_zero = sum(1 for r in records if r["response_overdischarged_below_zero"]) / n
    p_new_peak_after_release = sum(1 for r in records if r["new_peak_after_release"]) / n

    p_survival_ratio_lt_1 = sum(1 for r in ratio_records if r["survival_ratio"] < 1) / len(ratio_records) if ratio_records else None
    p_survival_ratio_lt_0 = sum(1 for r in ratio_records if r["survival_ratio"] < 0) / len(ratio_records) if ratio_records else None
    p_survival_ratio_le_0_5 = sum(1 for r in ratio_records if r["survival_ratio"] <= 0.5) / len(ratio_records) if ratio_records else None

    return {
        "record_count": n,
        "response_count": response_count,
        "no_response_count": no_response_count,
        "p_has_response": p_has_response,
        "no_response_rate": no_response_rate,
        "median_response_delay": safe_median(delays),
        "mean_response_delay": safe_mean(delays),
        "mean_debt_drop_after_first_release": safe_mean(drops),
        "median_debt_drop_after_first_release": safe_median(drops),
        "mean_survival_ratio": safe_mean(ratios),
        "median_survival_ratio": safe_median(ratios),
        "min_survival_ratio": min(ratios) if ratios else None,
        "max_survival_ratio": max(ratios) if ratios else None,
        "p_reduced_below_peak": p_reduced_below_peak,
        "p_overdischarged_below_zero": p_overdischarged_below_zero,
        "p_new_peak_after_release": p_new_peak_after_release,
        "p_survival_ratio_lt_1": p_survival_ratio_lt_1,
        "p_survival_ratio_lt_0": p_survival_ratio_lt_0,
        "p_survival_ratio_le_0_5": p_survival_ratio_le_0_5,
        "debt_peak_vs_survival_ratio_pearson": pearson(
            [float(r["debt_peak"]) for r in ratio_records],
            ratios,
        ) if len(ratio_records) >= 2 else None,
        "debt_peak_vs_reduced_below_peak_pearson": pearson(debt_peaks, reduced_flags),
        "debt_peak_vs_overdischarged_below_zero_pearson": pearson(debt_peaks, overdischarged_flags),
        "debt_peak_vs_new_peak_after_release_pearson": pearson(debt_peaks, new_peak_flags),
    }


def run_block(label: str, start: int, end: int, midpoint: float, odd_steps: int, post_peak_horizon: int) -> dict:
    seeds = odd_seeds(start, end)
    records = [measure_seed(seed, odd_steps, post_peak_horizon) for seed in seeds]
    aggregate = summarize_records(records)

    return {
        "label": label,
        "start": start,
        "end": end,
        "midpoint": midpoint,
        "odd_seed_count": len(seeds),
        "aggregate": aggregate,
    }


def summarize_blocks(block_results: list[dict]) -> dict:
    xs = [float(r["midpoint"]) for r in block_results]
    log_xs = [math.log10(x) for x in xs]

    median_survival_ratios = [r["aggregate"]["median_survival_ratio"] for r in block_results]
    mean_survival_ratios = [r["aggregate"]["mean_survival_ratio"] for r in block_results]
    p_reduced_values = [r["aggregate"]["p_reduced_below_peak"] for r in block_results]
    p_overdischarged_values = [r["aggregate"]["p_overdischarged_below_zero"] for r in block_results]
    p_new_peak_values = [r["aggregate"]["p_new_peak_after_release"] for r in block_results]
    no_response_rates = [r["aggregate"]["no_response_rate"] for r in block_results]
    median_response_delays = [r["aggregate"]["median_response_delay"] for r in block_results]

    valid_median_survival = [x for x in median_survival_ratios if x is not None]
    valid_mean_survival = [x for x in mean_survival_ratios if x is not None]

    survival_slope = linear_slope(log_xs[:len(valid_median_survival)], valid_median_survival) if len(valid_median_survival) == len(log_xs) else None
    survival_corr = pearson(log_xs[:len(valid_median_survival)], valid_median_survival) if len(valid_median_survival) == len(log_xs) else None

    p_reduced_slope = linear_slope(log_xs, p_reduced_values)
    p_reduced_corr = pearson(log_xs, p_reduced_values)

    p_new_peak_slope = linear_slope(log_xs, p_new_peak_values)
    p_new_peak_corr = pearson(log_xs, p_new_peak_values)

    last_10_p_reduced = p_reduced_values[-10:] if len(p_reduced_values) >= 10 else p_reduced_values
    last_10_p_new_peak = p_new_peak_values[-10:] if len(p_new_peak_values) >= 10 else p_new_peak_values
    last_10_median_survival = valid_median_survival[-10:] if len(valid_median_survival) >= 10 else valid_median_survival

    p_reduced_floor = min(p_reduced_values) if p_reduced_values else None
    p_new_peak_ceiling = max(p_new_peak_values) if p_new_peak_values else None
    no_response_rate_max = max(no_response_rates) if no_response_rates else None

    median_delay_all_1 = all(x == 1 for x in median_response_delays if x is not None)

    if (
        p_reduced_floor is not None
        and p_reduced_floor >= 0.90
        and no_response_rate_max is not None
        and no_response_rate_max <= 0.02
    ):
        survival_status = "strong_debt_reduction_after_response"
    elif (
        p_reduced_floor is not None
        and p_reduced_floor >= 0.75
    ):
        survival_status = "weak_debt_reduction_after_response"
    else:
        survival_status = "debt_survival_remains_significant"

    return {
        "block_count": len(block_results),
        "x_values": xs,
        "log10_x_values": log_xs,
        "median_survival_ratio_values": median_survival_ratios,
        "mean_survival_ratio_values": mean_survival_ratios,
        "p_reduced_below_peak_values": p_reduced_values,
        "p_overdischarged_below_zero_values": p_overdischarged_values,
        "p_new_peak_after_release_values": p_new_peak_values,
        "no_response_rate_values": no_response_rates,
        "median_response_delay_values": median_response_delays,
        "median_delay_all_1": median_delay_all_1,
        "p_reduced_floor": p_reduced_floor,
        "p_new_peak_ceiling": p_new_peak_ceiling,
        "no_response_rate_max": no_response_rate_max,
        "mean_median_survival_ratio": safe_mean(valid_median_survival),
        "last_10_median_survival_ratio_mean": safe_mean(last_10_median_survival),
        "last_10_median_survival_ratio_max": max(last_10_median_survival) if last_10_median_survival else None,
        "last_10_p_reduced_mean": safe_mean(last_10_p_reduced),
        "last_10_p_reduced_min": min(last_10_p_reduced) if last_10_p_reduced else None,
        "last_10_p_new_peak_mean": safe_mean(last_10_p_new_peak),
        "last_10_p_new_peak_max": max(last_10_p_new_peak) if last_10_p_new_peak else None,
        "survival_ratio_slope_per_log10_x": survival_slope,
        "survival_ratio_correlation_log10_x": survival_corr,
        "p_reduced_slope_per_log10_x": p_reduced_slope,
        "p_reduced_correlation_log10_x": p_reduced_corr,
        "p_new_peak_slope_per_log10_x": p_new_peak_slope,
        "p_new_peak_correlation_log10_x": p_new_peak_corr,
        "survival_status": survival_status,
    }


def build() -> dict:
    block_results = [
        run_block(
            label=r["label"],
            start=r["start"],
            end=r["end"],
            midpoint=r["midpoint"],
            odd_steps=ODD_STEPS,
            post_peak_horizon=POST_PEAK_HORIZON,
        )
        for r in BLOCK_RANGES
    ]

    survival_summary = summarize_blocks(block_results)

    if survival_summary["survival_status"] == "strong_debt_reduction_after_response":
        bounded_assessment = "strong_post_response_debt_reduction_candidate"
    elif survival_summary["survival_status"] == "weak_debt_reduction_after_response":
        bounded_assessment = "weak_post_response_debt_reduction_candidate"
    else:
        bounded_assessment = "debt_survival_remains_significant"

    return {
        "version": "v5.7",
        "machine": "Post-Response Debt Survival Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_steps": ODD_STEPS,
            "post_peak_horizon": POST_PEAK_HORIZON,
            "block_size": BLOCK_SIZE,
            "max_end": MAX_END,
        },
        "block_ranges": BLOCK_RANGES,
        "block_results": block_results,
        "survival_summary": survival_summary,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit tests whether the first rapid release response actually reduces debt below the peak.",
            "primary_survival_signal": "survival_ratio_after_first_release",
            "native_hypothesis": "Rapid response is not only fast; it usually reduces accumulated debt below its local peak.",
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

    lines.append("# Post-Response Debt Survival Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded post-response debt survival audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Survival summary")
    lines.append("")

    for key, value in summary["survival_summary"].items():
        if isinstance(value, list):
            formatted = ", ".join(fmt(v) for v in value)
            lines.append(f"- {key}: `{formatted}`")
        else:
            lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Block results")
    lines.append("")

    for item in summary["block_results"]:
        agg = item["aggregate"]
        lines.append(
            f"- {item['label']}: p_reduced_below_peak=`{fmt(agg['p_reduced_below_peak'])}`, "
            f"median_survival_ratio=`{fmt(agg['median_survival_ratio'])}`, "
            f"p_new_peak_after_release=`{fmt(agg['p_new_peak_after_release'])}`"
        )

    lines.append("")
    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit tests whether rapid response is effective, not merely fast.")
    lines.append("")
    lines.append("If debt is usually reduced below peak after first release, then response timing has dissipative effect.")
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

    json_path = RESULTS / "post_response_debt_survival_audit_v0.json"
    md_path = RESULTS / "post_response_debt_survival_audit_v0.md"
    cert_path = RESULTS / "post_response_debt_survival_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.7",
        "artifact": "Post-Response Debt Survival Audit V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "survival_status": summary["survival_summary"]["survival_status"],
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
    print("SURVIVAL STATUS:")
    print(f"  {summary['survival_summary']['survival_status']}")
    print("")
    print("KEY SURVIVAL:")
    print(f"  block_count: {summary['survival_summary']['block_count']}")
    print(f"  median_delay_all_1: {summary['survival_summary']['median_delay_all_1']}")
    print(f"  p_reduced_floor: {summary['survival_summary']['p_reduced_floor']}")
    print(f"  p_new_peak_ceiling: {summary['survival_summary']['p_new_peak_ceiling']}")
    print(f"  no_response_rate_max: {summary['survival_summary']['no_response_rate_max']}")
    print(f"  mean_median_survival_ratio: {summary['survival_summary']['mean_median_survival_ratio']}")
    print(f"  last_10_median_survival_ratio_mean: {summary['survival_summary']['last_10_median_survival_ratio_mean']}")
    print(f"  last_10_p_reduced_mean: {summary['survival_summary']['last_10_p_reduced_mean']}")
    print(f"  last_10_p_reduced_min: {summary['survival_summary']['last_10_p_reduced_min']}")
    print(f"  last_10_p_new_peak_mean: {summary['survival_summary']['last_10_p_new_peak_mean']}")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
