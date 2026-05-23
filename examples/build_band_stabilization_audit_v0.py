#!/usr/bin/env python3
"""
Band Stabilization Audit V0.

This bounded audit tests whether local seed-block release-pressure signals
stabilize into a positive band after the initial seed-scale drop.

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
MAX_END = 19999


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


def rolling(values: list[float], window: int, fn) -> list[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    out = []
    for i in range(len(values)):
        if i + 1 < window:
            continue
        chunk = values[i + 1 - window : i + 1]
        out.append(fn(chunk))
    return out


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


def run_block(label: str, start: int, end: int, midpoint: float, odd_steps: int, post_peak_horizon: int) -> dict:
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
        "midpoint": midpoint,
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


def summarize_blocks(block_results: list[dict]) -> dict:
    xs = [
        float(r["midpoint"])
        for r in block_results
        if r["aggregate"]["primary_signal"] is not None
    ]

    log_xs = [math.log10(x) for x in xs]

    signals = [
        r["aggregate"]["primary_signal"]
        for r in block_results
        if r["aggregate"]["primary_signal"] is not None
    ]

    post_initial_xs = xs[1:]
    post_initial_log_xs = log_xs[1:]
    post_initial_signals = signals[1:]

    rolling_mean_3 = rolling(signals, 3, mean)
    rolling_min_3 = rolling(signals, 3, min)
    rolling_max_3 = rolling(signals, 3, max)

    if signals:
        band_floor = min(post_initial_signals) if post_initial_signals else min(signals)
        band_ceiling = max(post_initial_signals) if post_initial_signals else max(signals)
        band_width = band_ceiling - band_floor
        all_positive = all(x > 0 for x in signals)
        zero_crossing_observed = any(x <= 0 for x in signals)
    else:
        band_floor = None
        band_ceiling = None
        band_width = None
        all_positive = False
        zero_crossing_observed = False

    if post_initial_signals:
        post_initial_floor = min(post_initial_signals)
        post_initial_ceiling = max(post_initial_signals)
        post_initial_mean = mean(post_initial_signals)
        post_initial_zero_crossing = any(x <= 0 for x in post_initial_signals)
        post_initial_all_positive = all(x > 0 for x in post_initial_signals)
    else:
        post_initial_floor = None
        post_initial_ceiling = None
        post_initial_mean = None
        post_initial_zero_crossing = False
        post_initial_all_positive = False

    full_slope = linear_slope(log_xs, signals)
    full_corr = pearson(log_xs, signals)

    post_initial_slope = linear_slope(post_initial_log_xs, post_initial_signals)
    post_initial_corr = pearson(post_initial_log_xs, post_initial_signals)

    median_response_delays = [
        r["aggregate"]["median_response_delay"]
        for r in block_results
        if r["aggregate"]["median_response_delay"] is not None
    ]

    if (
        post_initial_all_positive
        and post_initial_floor is not None
        and post_initial_floor > 0.20
        and post_initial_slope is not None
        and abs(post_initial_slope) < 0.25
    ):
        band_status = "positive_band_candidate"
    elif post_initial_all_positive:
        band_status = "positive_but_unstable_band"
    elif post_initial_zero_crossing:
        band_status = "zero_crossing_in_post_initial_blocks"
    else:
        band_status = "inconclusive_band"

    return {
        "block_count": len(block_results),
        "x_values": xs,
        "log10_x_values": log_xs,
        "block_signal_values": signals,
        "post_initial_block_signal_values": post_initial_signals,
        "rolling_mean_3": rolling_mean_3,
        "rolling_min_3": rolling_min_3,
        "rolling_max_3": rolling_max_3,
        "band_floor": band_floor,
        "band_ceiling": band_ceiling,
        "band_width": band_width,
        "post_initial_floor": post_initial_floor,
        "post_initial_ceiling": post_initial_ceiling,
        "post_initial_mean": post_initial_mean,
        "full_slope_per_log10_x": full_slope,
        "full_correlation_log10_x": full_corr,
        "post_initial_slope_per_log10_x": post_initial_slope,
        "post_initial_correlation_log10_x": post_initial_corr,
        "all_positive": all_positive,
        "zero_crossing_observed": zero_crossing_observed,
        "post_initial_all_positive": post_initial_all_positive,
        "post_initial_zero_crossing_observed": post_initial_zero_crossing,
        "band_status": band_status,
        "median_response_delay_values": median_response_delays,
        "median_response_delay_all_at_most_1": all(x <= 1 for x in median_response_delays) if median_response_delays else False,
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

    block_summary = summarize_blocks(block_results)

    if block_summary["band_status"] == "positive_band_candidate":
        bounded_assessment = "post_initial_positive_band_candidate"
    elif block_summary["band_status"] == "positive_but_unstable_band":
        bounded_assessment = "positive_but_unstable_post_initial_band"
    elif block_summary["band_status"] == "zero_crossing_in_post_initial_blocks":
        bounded_assessment = "post_initial_zero_crossing_detected"
    else:
        bounded_assessment = "inconclusive_band_stabilization"

    return {
        "version": "v5.4",
        "machine": "Band Stabilization Audit V0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "odd_steps": ODD_STEPS,
            "post_peak_horizon": POST_PEAK_HORIZON,
            "block_size": BLOCK_SIZE,
            "max_end": MAX_END,
        },
        "block_ranges": BLOCK_RANGES,
        "block_results": block_results,
        "block_summary": block_summary,
        "bounded_assessment": bounded_assessment,
        "interpretation": {
            "bounded_claim": "The audit tests whether local seed-block release-pressure signals stabilize into a positive band after initial decay.",
            "primary_signal": "debt_peak_vs_post_peak_release_mass_h_pearson",
            "native_hypothesis": "After low-seed dominance is removed, local debt-to-release pressure remains visible as a weaker positive band.",
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

    lines.append("# Band Stabilization Audit V0 Results")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("This is a bounded band-stabilization audit.")
    lines.append("")
    lines.append("It is not a proof of Collatz.")
    lines.append("")
    lines.append("It is not a claim that Collatz is solved.")
    lines.append("")
    lines.append("## Bounded assessment")
    lines.append("")
    lines.append(f"`{summary['bounded_assessment']}`")
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
    lines.append("## Block results")
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
    lines.append("The audit tests whether the local block signal remains in a positive band after the first low-seed block.")
    lines.append("")
    lines.append("A positive band candidate is not a theorem.")
    lines.append("")
    lines.append("It is bounded evidence that local debt-to-release pressure remains visible after initial seed-scale decay.")
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

    json_path = RESULTS / "band_stabilization_audit_v0.json"
    md_path = RESULTS / "band_stabilization_audit_v0.md"
    cert_path = RESULTS / "band_stabilization_audit_v0_certificate.json"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(write_markdown(summary), encoding="utf-8")

    certificate = {
        "version": "v5.4",
        "artifact": "Band Stabilization Audit V0",
        "generated_at_utc": summary["generated_at_utc"],
        "outputs": [
            str(json_path.relative_to(ROOT)),
            str(md_path.relative_to(ROOT)),
            str(cert_path.relative_to(ROOT)),
        ],
        "bounded_assessment": summary["bounded_assessment"],
        "band_status": summary["block_summary"]["band_status"],
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
    print("BAND STATUS:")
    print(f"  {summary['block_summary']['band_status']}")
    print("")
    print("BLOCK SIGNAL VALUES:")
    print(f"  {summary['block_summary']['block_signal_values']}")
    print("")
    print("POST-INITIAL BLOCK SIGNAL VALUES:")
    print(f"  {summary['block_summary']['post_initial_block_signal_values']}")
    print("")
    print("BAND:")
    print(f"  post_initial_floor: {summary['block_summary']['post_initial_floor']}")
    print(f"  post_initial_ceiling: {summary['block_summary']['post_initial_ceiling']}")
    print(f"  post_initial_mean: {summary['block_summary']['post_initial_mean']}")
    print(f"  post_initial_slope_per_log10_x: {summary['block_summary']['post_initial_slope_per_log10_x']}")
    print(f"  post_initial_zero_crossing_observed: {summary['block_summary']['post_initial_zero_crossing_observed']}")
    print("")
    print("BOUNDARY:")
    for key, value in summary["boundary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
