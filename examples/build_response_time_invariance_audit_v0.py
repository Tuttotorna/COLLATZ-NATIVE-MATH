#!/usr/bin/env python3
"""
Response-Time Invariance Audit V0.

This bounded audit tests whether release response timing remains stable
when debt-to-release-mass correlation becomes weak.

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
            "has_post_peak_release": False,
            "has_immediate_response": False,
            "post_peak_release_mass_h": 0.0,
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

    has_immediate_response = response_delay == 1

    horizon_end = peak_index + post_peak_horizon
    post_peak_window = [
        s for s in steps
        if s["index"] > peak_index and s["index"] <= horizon_end
    ]

    post_peak_releases = [s for s in post_peak_window if s["is_release"]]

    return {
        "seed": seed,
        "odd_steps": len(steps),
        "terminated": n == 1,
        "debt_peak": debt_peak,
        "peak_index": peak_index,
        "response_delay": response_delay,
        "has_post_peak_release": has_post_peak_release,
        "has_immediate_response": has_immediate_response,
        "post_peak_release_mass_h": sum(abs(s["delta"]) for s in post_peak_releases),
    }


def summarize_records(records: list[dict]) -> dict:
    response_records = [r for r in records if r["response_delay"] is not None]
    delays = [float(r["response_delay"]) for r in response_records]

    debt_peaks = [float(r["debt_peak"]) for r in records]
    has_response = [1.0 if r["response_delay"] is not None else 0.0 for r in records]
    has_immediate = [1.0 if r["has_immediate_response"] else 0.0 for r in records]
    delay_for_corr = [
        float(r["response_delay"]) if r["response_delay"] is not None else float(ODD_STEPS + 1)
        for r in records
    ]
    masses = [float(r["post_peak_release_mass_h"]) for r in records]

    n = len(records)

    if n == 0:
        raise ValueError("No records to summarize")

    p_delay_1 = sum(1 for d in delays if d == 1.0) / n
    p_delay_le_2 = sum(1 for d in delays if d <= 2.0) / n
    p_delay_le_3 = sum(1 for d in delays if d <= 3.0) / n
    no_response_rate = sum(1 for r in records if r["response_delay"] is None) / n

    return {
        "record_count": n,
        "response_count": len(response_records),
        "no_response_count": n - len(response_records),
        "no_response_rate": no_response_rate,
        "median_response_delay": safe_median(delays),
        "mean_response_delay": safe_mean(delays),
        "min_response_delay": min(delays) if delays else None,
        "max_response_delay": max(delays) if delays else None,
        "p_delay_1": p_delay_1,
        "p_delay_le_2": p_delay_le_2,
        "p_delay_le_3": p_delay_le_3,
        "debt_peak_vs_response_delay_pearson": pearson(debt_peaks, delay_for_corr),
        "debt_peak_vs_has_immediate_response_pearson": pearson(debt_peaks, has_immediate),
        "debt_peak_vs_has_response_pearson": pearson(debt_peaks, has_response),
        "debt_peak_vs_post_peak_release_mass_h_pearson": pearson(debt_peaks, masses),
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

    median_delays = [r["aggregate"]["median_response_delay"] for r in block_results]
    mean_delays = [r["aggregate"]["mean_response_delay"] for r in block_results]
    p_delay_1_values = [r["aggregate"]["p_delay_1"] for r in block_results]
    p_delay_le_2_values = [r["aggregate"]["p_delay_le_2"] for r in block_results]
    p_delay_le_3_values = [r["aggregate"]["p_delay_le_3"] for r in block_results]
    no_response_rates = [r["aggregate"]["no_response_rate"] for r in block_results]
    max_delays = [r["aggregate"]["max_response_delay"] for r in block_results]
    mass_correlations = [
        r["aggregate"]["debt_peak_vs_post_peak_release_mass_h_pearson"]
        for r in block_results
    ]

    valid_median_delays = [x for x in median_delays if x is not None]
    valid_mean_delays = [x for x in mean_delays if x is not None]
    valid_max_delays = [x for x in max_delays if x is not None]
    valid_mass_corrs = [x for x in mass_correlations if x is not None]

    median_delay_all_1 = all(x == 1 for x in valid_median_delays) if valid_median_delays else False
    median_delay_all_at_most_1 = all(x <= 1 for x in valid_median_delays) if valid_median_delays else False

    p_delay_1_floor = min(p_delay_1_values) if p_delay_1_values else None
    p_delay_le_2_floor = min(p_delay_le_2_values) if p_delay_le_2_values else None
    p_delay_le_3_floor = min(p_delay_le_3_values) if p_delay_le_3_values else None
    no_response_rate_max = max(no_response_rates) if no_response_rates else None

    last_10_p_delay_1 = p_delay_1_values[-10:] if len(p_delay_1_values) >= 10 else p_delay_1_values
    last_10_no_response = no_response_rates[-10:] if len(no_response_rates) >= 10 else no_response_rates

    p_delay_1_slope = linear_slope(log_xs, p_delay_1_values)
    p_delay_1_corr = pearson(log_xs, p_delay_1_values)

    no_response_slope = linear_slope(log_xs, no_response_rates)
    no_response_corr = pearson(log_xs, no_response_rates)

    mass_corr_slope = linear_slope(log_xs[:len(valid_mass_corrs)], valid_mass_corrs) if len(valid_mass_corrs) == len(log_xs) else None
    mass_corr_corr = pearson(log_xs[:len(valid_mass_corrs)], valid_mass_corrs) if len(valid_mass_corrs) == len(log_xs) else None

    if (
        median_delay_all_1
        and p_delay_1_floor is not None
        and p_delay_1_floor >= 0.50
        and p_delay_le_2_floor is not None
        and p_delay_le_2_floor >= 0.75
    ):
        timing_status = "strong_response_time_invariance"
    elif (
        median_delay_all_at_most_1
        and p_delay_le_2_floor is not None
        and p_delay_le_2_floor >= 0.60
    ):
        timing_status = "weak_response_time_invariance"
    else:
        timing_status = "response_time_variation_detected"

    return {
        "block_count": len(block_results),
        "x_values": xs,
        "log10_x_values": log_xs,
        "median_response_delay_values": median_delays,
        "mean_response_delay_values": mean_delays,
        "max_response_delay_values": max_delays,
        "p_delay_1_values": p_delay_1_values,
        "p_delay_le_2_values": p_delay_le_2_values,
        "p_delay_le_3_values": p_delay_le_3_values,
        "no_response_rate_values": no_response_rates,
        "mass_correlation_values": mass_correlations,
        "median_delay_all_1": median_delay_all_1,
        "median_delay_all_at_most_1": median_delay_all_at_most_1,
        "p_delay_1_floor": p_delay_1_floor,
        "p_delay_le_2_floor": p_delay_le_2_floor,
        "p_delay_le_3_floor": p_delay_le_3_floor,
        "no_response_rate_max": no_response_rate_max,
        "last_10_p_delay_1_mean": safe_mean(last_10_p_delay_1),
        "last_10_p_delay_1_min": min(last_10_p_delay_1) if last_10_p_delay_1 else None,
        "last_10_no_response_rate_mean": safe_mean(last_10_no_response),
        "last_10_no_response_rate_max": max(last_10_no_response) if last_10_no_response else None,
        "p_delay_1_slope_per_log10_x": p_delay_1_slope,
        "p_delay_1_correlation_log10_x": p_delay_1_corr,
        "no_response_slope_per_log10_x": no_response_slope,
        "no_response_correlation_log10_x": no_response_corr,
        "mass_correlation_slope_per_log10_x": mass_corr_slope,
        "mass_correlation_correlation_log10_x": mass_corr_corr,
        "mean_of_mean_response_delay": safe_mean(valid_mean_delays),
        "max_of_max_response_delay": max(valid_max_delays) if valid_max_delays else None,
        "mean_mass_correlation": safe_mean(valid_mass_corrs),
        "min_mass_correlation": min(valid_mass_corrs) if valid_mass_corrs else None,
        "timing_status": timing_status,
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

    timing_summary = summarize_blocks(block_results)

    if timing_summary["timing_status"] == "strong_response_time_invariance":
        bounded_assessment = "strong_response_time_invariance_candidate"
    elif timing_summary["timing_status"] == "weak_response_time_invariance":
        bounded_assessment = "weak_response_time_invariance_candidate"
    else:
        bounded_assessment = "response_time_variation_detected"

    return {
        "version": "v5.6",
        "machine": "Response-Time Invariance Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_steps": ODD_STEPS,
            "post_peak_horizon": POST_PEAK_HORIZON,
            "block_size": BLOCK_SIZE,
            "max_end": MAX_END,
        },
        "block_ranges": BLOCK_RANGES,
        "block_results": block_results,
        "timing_summary": timing_summary,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit tests whether release response timing remains stable even when release-mass correlation weakens.",
            "primary_timing_signal": "response_delay_after_debt_peak",
            "native_hypothesis": "Debt peaks continue to trigger rapid release responses across seed blocks.",
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

    lines.append("# Response-Time Invariance Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded response-time invariance audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
    lines.append("")
    lines.append("## Timing summary")
    lines.append("")

    for key, value in summary["timing_summary"].items():
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
            f"- {item['label']}: median_response_delay=`{fmt(agg['median_response_delay'])}`, "
            f"p_delay_1=`{fmt(agg['p_delay_1'])}`, "
            f"p_delay_le_2=`{fmt(agg['p_delay_le_2'])}`, "
            f"no_response_rate=`{fmt(agg['no_response_rate'])}`"
        )

    lines.append("")
    lines.append("## Native interpretation")
    lines.append("")
    lines.append("The audit tests whether timing is more robust than release mass.")
    lines.append("")
    lines.append("If median delay remains 1 while mass correlation decays, the stable structure is rapid response rather than proportional mass.")
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

    json_path = RESULTS / "response_time_invariance_audit_v0.json"
    md_path = RESULTS / "response_time_invariance_audit_v0.md"
    cert_path = RESULTS / "response_time_invariance_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.6",
        "artifact": "Response-Time Invariance Audit V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "timing_status": summary["timing_summary"]["timing_status"],
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
    print("TIMING STATUS:")
    print(f"  {summary['timing_summary']['timing_status']}")
    print("")
    print("KEY TIMING:")
    print(f"  block_count: {summary['timing_summary']['block_count']}")
    print(f"  median_delay_all_1: {summary['timing_summary']['median_delay_all_1']}")
    print(f"  p_delay_1_floor: {summary['timing_summary']['p_delay_1_floor']}")
    print(f"  p_delay_le_2_floor: {summary['timing_summary']['p_delay_le_2_floor']}")
    print(f"  p_delay_le_3_floor: {summary['timing_summary']['p_delay_le_3_floor']}")
    print(f"  no_response_rate_max: {summary['timing_summary']['no_response_rate_max']}")
    print(f"  last_10_p_delay_1_mean: {summary['timing_summary']['last_10_p_delay_1_mean']}")
    print(f"  last_10_p_delay_1_min: {summary['timing_summary']['last_10_p_delay_1_min']}")
    print(f"  last_10_no_response_rate_mean: {summary['timing_summary']['last_10_no_response_rate_mean']}")
    print(f"  max_of_max_response_delay: {summary['timing_summary']['max_of_max_response_delay']}")
    print("")
    print("MASS CORRELATION COMPARISON:")
    print(f"  min_mass_correlation: {summary['timing_summary']['min_mass_correlation']}")
    print(f"  mean_mass_correlation: {summary['timing_summary']['mean_mass_correlation']}")
    print(f"  mass_correlation_slope_per_log10_x: {summary['timing_summary']['mass_correlation_slope_per_log10_x']}")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
