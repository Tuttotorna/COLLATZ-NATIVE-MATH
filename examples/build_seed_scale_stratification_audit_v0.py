#!/usr/bin/env python3
"""
Seed-Scale Stratification Audit V0.

This bounded audit separates cumulative seed-scale decay from local block-level signal.

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

CUMULATIVE_RANGES = [
    {"label": "1..999", "start": 1, "end": 999},
    {"label": "1..1999", "start": 1, "end": 1999},
    {"label": "1..2999", "start": 1, "end": 2999},
    {"label": "1..3999", "start": 1, "end": 3999},
    {"label": "1..4999", "start": 1, "end": 4999},
    {"label": "1..5999", "start": 1, "end": 5999},
]

BLOCK_RANGES = [
    {"label": "1..999", "start": 1, "end": 999},
    {"label": "1001..1999", "start": 1001, "end": 1999},
    {"label": "2001..2999", "start": 2001, "end": 2999},
    {"label": "3001..3999", "start": 3001, "end": 3999},
    {"label": "4001..4999", "start": 4001, "end": 4999},
    {"label": "5001..5999", "start": 5001, "end": 5999},
]


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
            "has_post_peak_release": False,
            "post_peak_release_count_h": 0,
            "post_peak_strong_release_count_h": 0,
            "post_peak_release_mass_h": 0.0,
            "total_release_count": 0,
        }

    debt_peak = max(prefixes)
    peak_index = prefixes.index(debt_peak)

    later_steps = [s for s in steps if s["index"] > peak_index]
    later_releases = [s for s in later_steps if s["is_release"]]

    if later_releases:
        response_delay = later_releases[0]["index"] - peak_index
        has_post_peak_release = True
    else:
        response_delay = None
        has_post_peak_release = False

    horizon_end = peak_index + post_peak_horizon
    post_peak_window = [
        s for s in steps
        if s["index"] > peak_index and s["index"] <= horizon_end
    ]

    post_peak_releases = [s for s in post_peak_window if s["is_release"]]
    post_peak_strong_releases = [s for s in post_peak_window if s["is_strong_release"]]
    total_releases = [s for s in steps if s["is_release"]]

    return {
        "seed": seed,
        "odd_steps": len(steps),
        "terminated": n == 1,
        "debt_peak": debt_peak,
        "peak_index": peak_index,
        "response_delay": response_delay,
        "has_post_peak_release": has_post_peak_release,
        "post_peak_release_count_h": len(post_peak_releases),
        "post_peak_strong_release_count_h": len(post_peak_strong_releases),
        "post_peak_release_mass_h": sum(abs(s["delta"]) for s in post_peak_releases),
        "total_release_count": len(total_releases),
    }


def run_range(label: str, start: int, end: int, odd_steps: int, post_peak_horizon: int) -> dict:
    seeds = odd_seeds(start, end)
    records = [measure_seed(seed, odd_steps, post_peak_horizon) for seed in seeds]

    debt_peaks = [r["debt_peak"] for r in records]
    post_peak_masses = [float(r["post_peak_release_mass_h"]) for r in records]
    post_peak_counts = [float(r["post_peak_release_count_h"]) for r in records]
    post_peak_strong_counts = [float(r["post_peak_strong_release_count_h"]) for r in records]
    total_release_counts = [float(r["total_release_count"]) for r in records]

    response_delays = [
        float(r["response_delay"])
        for r in records
        if r["response_delay"] is not None
    ]

    primary = pearson(debt_peaks, post_peak_masses)

    return {
        "label": label,
        "start": start,
        "end": end,
        "midpoint": (start + end) / 2.0,
        "odd_seed_count": len(seeds),
        "aggregate": {
            "primary_signal": primary,
            "debt_peak_vs_post_peak_release_mass_h_pearson": primary,
            "debt_peak_vs_post_peak_release_count_h_pearson": pearson(debt_peaks, post_peak_counts),
            "debt_peak_vs_post_peak_strong_release_count_h_pearson": pearson(debt_peaks, post_peak_strong_counts),
            "debt_peak_vs_total_release_count_pearson": pearson(debt_peaks, total_release_counts),
            "median_response_delay": safe_median(response_delays),
            "mean_response_delay": safe_mean(response_delays),
            "mean_debt_peak": safe_mean(debt_peaks),
            "mean_post_peak_release_mass_h": safe_mean(post_peak_masses),
            "terminated_within_bound": sum(1 for r in records if r["terminated"]),
        },
    }


def summarize_family(name: str, results: list[dict], x_key: str) -> dict:
    xs = [float(r[x_key]) for r in results if r["aggregate"]["primary_signal"] is not None]
    log_xs = [math.log10(x) for x in xs]
    ys = [
        r["aggregate"]["primary_signal"]
        for r in results
        if r["aggregate"]["primary_signal"] is not None
    ]

    if ys:
        first_signal = ys[0]
        last_signal = ys[-1]
        total_drop = first_signal - last_signal
        relative_drop = total_drop / first_signal if first_signal != 0 else None
        min_signal = min(ys)
        max_signal = max(ys)
        mean_signal = mean(ys)
        all_positive = all(y > 0 for y in ys)
        zero_crossing_observed = any(y <= 0 for y in ys)
    else:
        first_signal = None
        last_signal = None
        total_drop = None
        relative_drop = None
        min_signal = None
        max_signal = None
        mean_signal = None
        all_positive = False
        zero_crossing_observed = False

    corr_log = pearson(log_xs, ys)
    slope_log = linear_slope(log_xs, ys)

    if corr_log is not None and corr_log < -0.5:
        direction = "decay"
    elif corr_log is not None and corr_log > 0.5:
        direction = "growth"
    else:
        direction = "flat_or_mixed"

    if all_positive and min_signal is not None and min_signal > 0.45:
        floor_status = "positive_floor_preserved"
    elif all_positive:
        floor_status = "positive_but_weak_floor"
    elif zero_crossing_observed:
        floor_status = "zero_crossing_observed"
    else:
        floor_status = "inconclusive"

    median_response_delays = [
        r["aggregate"]["median_response_delay"]
        for r in results
        if r["aggregate"]["median_response_delay"] is not None
    ]

    return {
        "family_name": name,
        "x_values": xs,
        "log10_x_values": log_xs,
        "primary_signal_values": ys,
        "first_signal": first_signal,
        "last_signal": last_signal,
        "total_drop": total_drop,
        "relative_drop": relative_drop,
        "min_signal": min_signal,
        "max_signal": max_signal,
        "mean_signal": mean_signal,
        "slope_per_log10_x": slope_log,
        "x_vs_signal_correlation_log10": corr_log,
        "direction": direction,
        "floor_status": floor_status,
        "all_positive": all_positive,
        "zero_crossing_observed": zero_crossing_observed,
        "median_response_delay_values": median_response_delays,
        "median_response_delay_all_at_most_1": all(x <= 1 for x in median_response_delays) if median_response_delays else False,
    }


def compare_cumulative_vs_block(cumulative_summary: dict, block_summary: dict) -> dict:
    cumulative_direction = cumulative_summary["direction"]
    block_direction = block_summary["direction"]

    cumulative_min = cumulative_summary["min_signal"]
    block_min = block_summary["min_signal"]

    if cumulative_direction == "decay" and block_direction != "decay":
        attribution = "cumulative_mixing_decay"
    elif cumulative_direction == "decay" and block_direction == "decay":
        attribution = "local_block_decay"
    elif cumulative_direction != "decay" and block_direction == "decay":
        attribution = "block_decay_masked_by_cumulative_pooling"
    else:
        attribution = "no_clear_local_decay"

    if (
        cumulative_min is not None
        and block_min is not None
        and cumulative_min > 0
        and block_min > 0
    ):
        positivity_status = "both_positive"
    elif cumulative_min is not None and cumulative_min > 0:
        positivity_status = "cumulative_positive_only"
    elif block_min is not None and block_min > 0:
        positivity_status = "block_positive_only"
    else:
        positivity_status = "zero_or_negative_detected"

    return {
        "cumulative_direction": cumulative_direction,
        "block_direction": block_direction,
        "cumulative_min_signal": cumulative_min,
        "block_min_signal": block_min,
        "attribution": attribution,
        "positivity_status": positivity_status,
    }


def build() -> dict:
    cumulative_results = [
        run_range(
            label=r["label"],
            start=r["start"],
            end=r["end"],
            odd_steps=ODD_STEPS,
            post_peak_horizon=POST_PEAK_HORIZON,
        )
        for r in CUMULATIVE_RANGES
    ]

    block_results = [
        run_range(
            label=r["label"],
            start=r["start"],
            end=r["end"],
            odd_steps=ODD_STEPS,
            post_peak_horizon=POST_PEAK_HORIZON,
        )
        for r in BLOCK_RANGES
    ]

    cumulative_summary = summarize_family("cumulative_ranges", cumulative_results, "end")
    block_summary = summarize_family("local_blocks", block_results, "midpoint")

    comparison = compare_cumulative_vs_block(cumulative_summary, block_summary)

    if comparison["attribution"] == "cumulative_mixing_decay":
        bounded_assessment = "cumulative_decay_but_local_blocks_preserve_signal"
    elif comparison["attribution"] == "local_block_decay":
        bounded_assessment = "local_seed_block_decay_detected"
    elif comparison["attribution"] == "block_decay_masked_by_cumulative_pooling":
        bounded_assessment = "local_decay_masked_by_cumulative_pooling"
    else:
        bounded_assessment = "no_clear_local_seed_decay"

    return {
        "version": "v5.3",
        "machine": "Seed-Scale Stratification Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_steps": ODD_STEPS,
            "post_peak_horizon": POST_PEAK_HORIZON,
        },
        "cumulative_results": cumulative_results,
        "block_results": block_results,
        "cumulative_summary": cumulative_summary,
        "block_summary": block_summary,
        "comparison": comparison,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit separates cumulative seed-scale decay from local block-level signal.",
            "primary_signal": "debt_peak_vs_post_peak_release_mass_h_pearson",
            "native_hypothesis": "Seed-scale weakening may be caused by cumulative mixing rather than uniform local collapse.",
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

    lines.append("# Seed-Scale Stratification Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded seed-scale stratification audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Comparison")
    lines.append("")

    for key, value in summary["comparison"].items():
        lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Cumulative summary")
    lines.append("")

    for key, value in summary["cumulative_summary"].items():
        if isinstance(value, list):
            formatted = ", ".join(fmt(v) for v in value)
            lines.append(f"- {key}: `{formatted}`")
        else:
            lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Block summary")
    lines.append("")

    for key, value in summary["block_summary"].items():
        if isinstance(value, list):
            formatted = ", ".join(fmt(v) for v in value)
            lines.append(f"- {key}: `{formatted}`")
        else:
            lines.append(f"- {key}: `{fmt(value)}`")

    lines.append("")
    lines.append("## Cumulative range results")
    lines.append("")

    for item in summary["cumulative_results"]:
        agg = item["aggregate"]
        lines.append(
            f"- {item['label']}: primary_signal=`{fmt(agg['primary_signal'])}`, "
            f"median_response_delay=`{fmt(agg['median_response_delay'])}`"
        )

    lines.append("")
    lines.append("## Local block results")
    lines.append("")

    for item in summary["block_results"]:
        agg = item["aggregate"]
        lines.append(
            f"- {item['label']}: primary_signal=`{fmt(agg['primary_signal'])}`, "
            f"median_response_delay=`{fmt(agg['median_response_delay'])}`"
        )

    lines.append("")
    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit tests whether seed-scale decay is local or produced by cumulative mixing.")
    lines.append("")
    lines.append("A local block signal that remains positive while cumulative signal decays suggests dilution rather than collapse.")
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

    json_path = RESULTS / "seed_scale_stratification_audit_v0.json"
    md_path = RESULTS / "seed_scale_stratification_audit_v0.md"
    cert_path = RESULTS / "seed_scale_stratification_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.3",
        "artifact": "Seed-Scale Stratification Audit V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "comparison": summary["comparison"],
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
    print("COMPARISON:")
    for key, value in summary["comparison"].items():
        print(f"  {key}: {value}")
    print("")
    print("CUMULATIVE SIGNAL VALUES:")
    print(f"  {summary['cumulative_summary']['primary_signal_values']}")
    print("")
    print("BLOCK SIGNAL VALUES:")
    print(f"  {summary['block_summary']['primary_signal_values']}")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
